from celery import shared_task
from django.core.mail import send_mail


@shared_task
def notify_user_about_free_slot(user_email, resource_name):
    
    send_mail(
        'Free Slot Available',
        f'A slot for {resource_name} is now available.',
        'negmatovazam4@gmail.com',
        [user_email],
        fail_silently=False,
    )