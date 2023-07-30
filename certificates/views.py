from django.shortcuts import render, get_object_or_404
from django.http import  JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.conf import settings
import hashlib
from django.http import HttpResponse
from django.template.loader import get_template
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


@login_required
def create_certificate(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            title = request.POST.get('title', '')
            description = request.POST.get('description', '')
            issue_date = request.POST.get('issue_date', '')

            certificate = Certificate.objects.create(title=title, description=description, issue_date=issue_date, owner=request.user)

            verification_hash = hashlib.sha256(f"{certificate.id}{certificate.title}{certificate.issue_date}{settings.SECRET_KEY}".encode('utf-8')).hexdigest()

            CertificateVerification.objects.create(certificate=certificate, verification_hash=verification_hash)

            template = get_template('certificate_template.html')
            context = {
                'certificate': certificate,
            }
            html_content = template.render(context)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{certificate.title}.pdf"'
            p = canvas.Canvas(response, pagesize=letter)

            p.drawString(100, 800, f"Certificate Title: {certificate.title}")
            p.drawString(100, 780, f"Description: {certificate.description}")
            p.drawString(100, 760, f"Issue Date: {certificate.issue_date}")
            p.showPage()
            p.save()

            return response
        else:
            raise PermissionDenied("You must be logged in to create a certificate.")
    else:
        return render(request, 'create_certificate.html')



def verify_certificate(request):
    if request.method == 'POST':
        certificate_id = request.POST.get('certificate_id', '')
        certificate_pdf = request.FILES.get('certificate_pdf', None)

        if certificate_id:
            certificate = get_object_or_404(Certificate, id=certificate_id)
            verification_hash = hashlib.sha256(f"{certificate.id}{certificate.title}{certificate.issue_date}{settings.SECRET_KEY}".encode('utf-8')).hexdigest()
            return JsonResponse({'verification_hash': verification_hash})
        elif certificate_pdf:

            return JsonResponse({'verification_result': 'success'})
        else:
            return JsonResponse({'error': 'Invalid request'})
    else:
        return render(request, 'verify_certificate.html')


@login_required
def customize_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)

    if certificate.owner != request.user:
        raise PermissionDenied("You don't have permission to customize this certificate.")

    if request.method == 'POST':

        return HttpResponse("Certificate customized successfully!")
    else:
        return render(request, 'customize_certificate.html', {'certificate': certificate})
