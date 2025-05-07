# Expense Analytics Dashboard 💸📊

A smart expense tracker that visualizes your spending with interactive charts, sends you alerts when you exceed your budget, and keeps your finances in check.

## 🚀 Features

- 📈 Expense analytics dashboard with charts
- 📂 Category-based budget alerts
- 📬 Email notifications on budget breaches
- 🔁 Background task processing with Celery
- 🧾 Clean UI for tracking and managing expenses

## 🔧 Tech Stack

- Python / Django
- Celery + Redis
- PostgreSQL
- Chart.js or Recharts (JS)
- Bootstrap / Tailwind for frontend styling

## 🧠 Key Concepts Covered

- Data aggregation and filtering
- Background job scheduling
- Sending emails via Django
- Real-time data visualization

## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/expense-analytics-dashboard.git
   cd expense-analytics-dashboard
   ```
2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**
   ```text
    DEBUG=True
    SECRET_KEY=your-secret-key
    EMAIL_HOST_USER=your@email.com
   ```
5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```
6. **Start Redis server and Celery worker**
   ```bash
   redis-server  # in another terminal
   celery -A your_project_name worker --loglevel=info
   ```
7. **Start the Django server**
   ```bash
   python manage.py runserver
   ```

##  Tutorial

### Checking the budget breach after each expense entery(so if it's more than limit it will send the email)

install celery
```shell
pip install celery
```

install redis
```shell
sudo apt update
sudo apt install redis
```

check if it works
```shell
redis-cli
ping
```

if you get ```PONG``` means it works so use ctrl+c to close it


then install redis in env
```shell
pip install redis
```

add ```celery.py``` in your project where settings.py is
```python
# myApp/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personalExpenseTracker.settings')
app = Celery('personalExpenseTracker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

then add this to settings.py
```python
# personalExpenseTracker/settings.py
# ...

# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/0"

# Email 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True 
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
```

add the secret information in .evn file
```text
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
SECRET_KEY=<your-secret-key>
EMAIL_HOST_USER=<your-email>
EMAIL_HOST_PASSWORD=<your-email-password>
DEFAULT_FROM_EMAIL=Expense Tracker - <your-email>
```

then same folder ```__init__.py```
```python
# proj/__init__.py

from .celery import app as celery_app

__all__ = ("celery_app",)
```

open a terminal and run your django server
```shell
python manage.py runserver
```

open another terminal and run redis server
```shell
redis-server
```

### if you get error that the server is already open do this
```shell
sudo systemctl stop redis
```
### If still didn't work and the port is busy
```shell
# find out the port is busy by what
lsof -i :6379
# then kill it
kill -9 <PID>
```

open another terminal and run celery worker
```shell
python -m celery -A personalExpenseTracker worker
```

create a ```tasks.py``` in your app folder
```python
# app/task.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_alert_email(categ, user_email):
   '''take the breached category and user_email and send an alert email to the user.'''
    subject = f"Spend Alert!"
    message = f"Your category '{categ}' overreached the limit! "
    send_mail(subject=subject,
              message=message,
              from_email=None,
              recipient_list=[user_email])
```

then use this task in views.py
```python
# myApp/views.py
from .tasks import send_alert_email


# ...
class AddExpenseView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'myApp/add_expense.html'
    success_url = reverse_lazy('home')
    
    def get_form(self):
        form = super().get_form()
        form.fields['category'].queryset = Category.objects.filter(author=self.request.user)
        return form
    
    def form_valid(self, form):
        categ = Category.objects.get(name=form.cleaned_data['category'], author=self.request.user)
        # if category has breached call the task for sending the email
        if categ.check_budget_breach():
            send_alert_email.delay(categ.name, self.request.user.email)
            messages.error(self.request, f'Your category "{categ}" has overreached the limit!')
        return super().form_valid(form)
# ...
```

every change you do on tasks you should restart the worker.
```shell
python -m celery -A proj worker -l info
```

## Periodic background task (automatic checking every X minutes)

create a new task
```python
# app/tasks.py
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
    
# we added this task so it loops through users and their categories and if the the category is breached we use the task above to send them an email alert    
@shared_task
def check_all_users_budget():
    Users = get_user_model()
    users = Users.objects.all()
    
    for user in users:
        categories = Category.objects.filter(author=user)
        for categ in categories:
            if categ.check_budget_breach():
                send_alert_email(categ, user.email)
```

install Celery Beat
```shell
pip install django-celery-beat
```

add it to INSTALLED_APPS
```python
# settings.py
INSTALLED_APPS = [
    ...
    'django_celery_beat',
]
```

run migrations
```shell
python manage.py migrate django_celery_beat
```

set the celery.py on schedule
```python
# proj/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personalExpenseTracker.settings')
app = Celery('personalExpenseTracker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'    # new
app.conf.timezone = 'UTC'    # new
app.autodiscover_tasks()
```

now go to admin panel and create a periodic task
- Go to Django Admin > Periodic Tasks > Add.
- Create a new task:
   - Name: "Check all budgets"
   - Task: ```yourapp.tasks.check_all_users_budget```
   - be sure it's enabled
   - Interval: Create a new Interval (e.g., every 10 minutes).


```FINISHED```
