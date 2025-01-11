# Django Polls Application
This project is a simple Django application that follows the official Django tutorial to create a Polls App. It covers the basics of Django, including installing Django, creating a project, defining models, working with views, templates, forms, static files, and running tests.

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

**🛠️ Setup Instructions**

**Step 1: Install Django**

Install Django using pip:

```bash
pip install django
```

**Step 2: Create the Project**

Create a Django project named mysite:

```bash
django-admin startproject mysite
cd mysite
```

**Step 3: Create the Polls App**

Create a new app within the project:

```bash
python manage.py startapp polls
```

**Step 4: Configure Database**

Run the following commands to create and apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

**Step 5: Create Superuser**

Create an admin user to access the Django admin panel:

```bash
python manage.py createsuperuser
```

**Step 6: Run the Development Server**

Start the Django development server:

```bash
python manage.py runserver
```

Visit the app in your browser at:

```bash
http://127.0.0.1:8000/polls
```

## 🌟 Features

**1. Dynamic Polls:**

- Add questions and choices via the Django admin panel.
- Display a list of active polls.

**2. Vote Submission:**

- Submit votes for your selected poll choices.

**3. View Results**

- See vote counts for each choice on the results page.

**4. Dynamic Styling:**

- Use custom CSS for styling the application.

**5. Static Files Integration:**

- Serve images and CSS via Django's static files system.

**6. Comprehensive Tests:**

- Validate models, views, and app behavior with Django's testing framework.

## 🧪 Testing

Run the test suite to validate the application's functionality:

```bash
python manage.py test
```

Key tests:

- Ensure future-dated polls are not displayed.
- Exclude polls without choices.
- Verify voting functionality.

## 📖 Learn More

Explore the official Django tutorial and documentation for a deeper dive:

[Django Official Documentation](https://docs.djangoproject.com/en/5.1/intro/tutorial01/)

[Django Tutorials](https://docs.djangoproject.com/en/5.1/intro/tutorial01/)
