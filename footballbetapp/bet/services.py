import asyncio
from django.core.mail import send_mail
from django.conf import settings



def send_contact_email(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
    )

# def send_verification_email(user, request):
#     token = 

def send_activation_email(subject, message, recipient):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient],
        fail_silently=False
    )