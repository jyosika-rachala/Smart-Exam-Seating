## Smart Exam Seating System 

## Project Overview

The Smart Exam Seating System is a web-based application designed to automate and optimize the allocation of exam seating arrangements. It ensures fair distribution of students across rooms and reduces manual effort.

##  Features

* Automated seating allocation
* Room and block management
* Exam slot scheduling
* Student data upload
* Admin login system
* Email notification feature

## Tech Stack

* Python
* Django
* HTML, CSS
* SQLite

## How to Run the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/jyosika-rachala/Smart-Exam-Seating.git
   ```

2. Navigate to project folder:

   ```bash
   cd Smart-Exam-Seating
   ```

3. Create Virtual Environment (Important)

   ```bash
   python -m venv venv
   ```
   
   To activate it
   
   Windows
   ```bash
   venv\Scripts\activate
   ```
   
   Mac/Linux
   ```bash
   source venv/bin/activate
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
   
6. Database Setup
   
   ```bash
   python manage.py migrate
   ```

7. Create Admin User

   ```bash
   python manage.py createsuperuser
   ```
   Enter username, email, password.

8. Email Configuration (Important)

   To enable email notifications for students, configure your email settings in Django.

   Step 1: Open Settings File

   Go to:  exam_seating/settings.py
   
   Step 2: Update Email Credentials

   Find and update the following fields:
   
   ```python
   EMAIL_HOST_USER = 'your-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-app-password'
   ```
   
   * Replace 'your-email@gmail.com' with your email address
   * Replace 'your-app-password' with your Gmail App Password
     
  Step 3: Generate Gmail App Password

  To generate an App Password:

  * Go to your Google Account settings
  * Enable 2-Step Verification
  * Search for App Passwords
  * Select:
     * App: Mail
     * Device: Windows Computer
  * Click Generate
  * Copy the generated app password
  * Paste it into EMAIL_HOST_PASSWORD
   
9. Run the server:

   ```bash
   python manage.py runserver
   ```

10. Open browser and go to:

   ```
   http://127.0.0.1:8000/
   ```
After following the link add '/login' in the url(like http://127.0.0.1:8000/login) in order to redirect to Login page 

### Login using the superuser account.

## Screenshots


<img width="951" height="560" alt="image" src="https://github.com/user-attachments/assets/408b4829-865a-4a35-9cd4-bf6e9e369a2c" />
<img width="971" height="571" alt="image" src="https://github.com/user-attachments/assets/de831603-ed38-4bb6-9598-02dc3298818d" />

## Author 👩‍💻

### Jyosika R
