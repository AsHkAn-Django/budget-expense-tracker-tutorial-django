from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import Category

@shared_task
def send_alert_email(categ, user_email):
    subject = f"Spend Alert!"
    message = f"Your category '{categ}' overreached the limit! "
    send_mail(subject=subject,
              message=message,
              from_email=None,
              recipient_list=[user_email])
    
    
@shared_task
def check_all_users_budget():
    Users = get_user_model()
    users = Users.objects.all()
    
    for user in users:
        categories = Category.objects.filter(author=user)
        for categ in categories:
            if categ.check_budget_breach():
                send_alert_email(categ, user.email)