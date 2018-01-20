from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .forms import ContactUserModelForm
# Create your views here.


def index(request):
    context = {
        'form': ContactUserModelForm()
    }
    return render(request, 'app/index.html', context=context)


def ajax_submit(request):
    if request.method == 'POST':
        form = ContactUserModelForm(request.POST)
        error = {}
        success = False
        if form.is_valid():
            contact_user = form.save()

            send_mail(
                'Contact Form Submission',
                render_to_string(
                    'app/email_contact.html',
                    {'contact_user': contact_user}
                ),
                settings.EMAIL_FROM,
                [settings.EMAIL_TO],
                fail_silently=True
            )

            success = True
        else:
            error = form.errors

        return JsonResponse({'status': True, 'error': error, 'success': success})

    return JsonResponse({'status': False, 'error': 'Request Method not Allowed.'}, status=405)
