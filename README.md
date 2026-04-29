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
   
   To activivate it
   Windows
   ```bash
   venv\Scripts\activate
   ```
   Mac/Linux
   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
   
5. Database Setup
   
   ```bash
   python manage.py migrate
   ```

6. Create Admin User

   ```bash
   python manage.py createsuperuser
   ```
   Enter username, email, password.

7. Configure Email (VERY IMPORTANT ⚠️)
   Open:
   exam_seating/settings.py
   
   Find this section and change:
   EMAIL_HOST_USER = 'yourmail@gmail.com'
   EMAIL_HOST_PASSWORD = 'your_app_password'
   Replace these two sections with your email(from this email the mails will be sent to the students) and email app password 

   To get email app password-follow these steps
   *Turn on 2-Step Verification in Google
   *Search "App Passwords"
   *Generate for Mail → Windows Computer
   *Paste the generated app password in settings.py
   
9. Run the server:

   ```bash
   python manage.py runserver
   ```

10. Open browser and go to:

   ```
   http://127.0.0.1:8000/
   ```
After following the link add /login in the url(like http://127.0.0.1:8000/login) in order to redirect to Login page 

## Login using the superuser account.

## Screenshots


<img width="951" height="560" alt="image" src="https://github.com/user-attachments/assets/408b4829-865a-4a35-9cd4-bf6e9e369a2c" />
<img width="971" height="571" alt="image" src="https://github.com/user-attachments/assets/de831603-ed38-4bb6-9598-02dc3298818d" />

## Author 👩‍💻

Jyosika R
