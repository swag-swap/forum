# Project Forum

## Setting up project environment:
- **Install Virtual Environment**:
```shell
pip install virtualenv
```
- **Create a Virtual Environment**:
```shell
virtualenv djangoForumenv
```
- **Activate the Virtual Environment**:
```shell
source venv/bin/activate
``` 
- **Install Django**:
With the virtual environment activated, install Django:
```shell
pip install django
```
- **Create Django Project**:
Creating Django project within the virtual environment:
```shell
django-admin startproject YourProjectName
```
- **Installing Project Dependencies**:
Installing any additional dependencies project may need. We can use a requirements.txt file for this purpose.
```shell
pip install -r requirements.txt
```
- **Making migration**:
After changing in model we have to make migration of that app
```shell
python3 manage.py makemigrations app
```

- **Run Migrations**:
Run initial migrations to set up the database:
```shell
python3 manage.py migrate
```
- **Create Superuser**:
If project involves user authentication, creating an admin superuser:
```shell
python3 manage.py createsuperuser
```
- **Starting Development Server**:
```shell
python3 manage.py runserver
```
- **Accessing the Admin Interface**:
Visiting http://127.0.0.1:8000/admin/ in browser and log in with the superuser credentials to access the admin interface.
Remember to always activate your virtual environment when working on Django project. 
- To **deactivate** the virtual environment:
```shell
deactivate
```

## Django project structure
```graphql
YourProjectName/          # Project's root directory
│
├── manage.py            # Django's command-line utility for various tasks
├── YourProjectName/     # Django project's package
│   ├── __init__.py
│   ├── settings.py      # Project settings (database, static files, middleware, etc.)
│   ├── urls.py          # Top-level URL patterns
│   └── asgi.py          # ASGI configuration for channels (for WebSocket support)
│
├── yourapp/             # A Django app within the project
│   ├── migrations/     # Database migration files
│   ├── __init__.py
│   ├── admin.py        # Django admin configuration
│   ├── apps.py         # App configuration
│   ├── models.py       # Database models
│   ├── tests.py        # Unit tests
│   └── views.py        # Views handling HTTP requests
│
├── static/              # Static files (CSS, JavaScript, images)
│
├── templates/           # HTML templates
│
├── venv/                # Virtual environment (created if using virtualenv)
│
├── db.sqlite3           # SQLite database file (or other database file)
│
├── requirements.txt     # List of Python dependencies for the project
│
└── .gitignore           # Specifies files and directories to be ignored by version control

```

## Features
Some features of forum web application:
1. **User Registration and Authentication:**
   - Allow users to register with the forum and authenticate themselves to access various features.

2. **User Profile Management:**
   - Enable users to manage their profiles, update information, and view their activity history.

3. **Document Upload:**
   - Implementing a feature that allows users to upload various types of documents, such as images, text files, and more.

4. **Document Editing:**
   - Providing functionality for users to edit their uploaded documents.

5. **Tagging System:**
   - Implementing a tagging system for documents to categorize them. Users can add and remove tags from their documents.

6. **Search Functionality:**
   - Developing a search feature that allows users to search for documents based on titles and tags.

7. **User Forum:**
   - Create a discussion forum where users can post topics, reply to discussions, and engage in conversations.

8. **User Roles and Permissions:**
   - Defining user roles (e.g., regular user, moderator) with specific permissions for document management and forum moderation.

9. **User Notifications:**
   - Implementing a notification system to alert users about new forum posts, replies, and other relevant activities.

10. **User Interactions:**
    - Allows users to like, comment, and share documents and forum posts.

11. **Security Measures:**
    - Implementing security features, including secure authentication, input validation, and protection against common web vulnerabilities.

12. **Responsive Design:**
    - Ensuring that the application has a responsive design, allowing users to access and use the forum on various devices.

13. **Admin Dashboard:**
    - Creating an admin dashboard with insights into user activity, document statistics, and forum trends.

14. **Documentation:**
    - Providing comprehensive documentation for users and developers, explaining how to use the forum and its features.

## Pages
- /
- /*register*
- /*login*
- /*user/{username}*
- /*forgot-password*
- /*privacy*
- /*about*
- /*contact*
- /*admin*
- /*settings*

## Class Diagram
![Class Diagram](./media/requirements/Class%20diagram.png)

