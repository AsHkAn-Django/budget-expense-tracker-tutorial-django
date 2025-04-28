from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_alert_email(categ, user_email):
    subject = f"Spend Alert!"
    message = f"Your category '{categ}' overreached the limit! "
    send_mail(subject=subject,
              message=message,
              from_email=None,
              recipient_list=[user_email])
    