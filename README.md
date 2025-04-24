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

...
