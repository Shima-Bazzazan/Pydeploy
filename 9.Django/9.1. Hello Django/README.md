# Django Polls Application

This project is a simple Django application that follows the official Django tutorial to create a Polls App. It covers the basics of Django, including installing Django, creating a project, defining models, and running the application.

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Setup Instructions

**Step 1: Install Django**

Install Django using pip:

```bash
pip install django
```

**Step 2: Create the Project**

Create a Django project named:

```bash
django-admin startproject mysite djangotutorial
cd djangotutorial
```

**Step 3: Create the Polls App**

```bash
python manage.py startapp polls
```

**Step 4: Migrate Database**

Run the following commands to create and apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```
**Step 5: Run the Project**

Start the Django development server:

```bash
python manage.py runserver
```

Visit the app in your browser at:

```bash
http://127.0.0.1:8000/polls
```

### 🛠️ Helpful Links

Official Django Documentation: [Django Documentation](https://docs.djangoproject.com/en/5.1/intro/tutorial01/)