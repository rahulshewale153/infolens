InfoLens
InfoLens is a Python service that connects to your Gmail account via IMAP, fetches unread emails, and processes their contents.

Prerequisites
Python 3.10+
A Gmail account and setup App Password
 https://myaccount.google.com/apppasswords

Setup
1. Install dependencies
    pip install -r requirements.txt

2. Configure Gmail App Password
    - Go to Google App Passwords. https://- myaccount.google.com/apppasswords
    - Generate a new App Password for “Mail”.
    - Copy the generated password.

3. Add credentials to .env
Create a .env file in the project root:
    GMAIL_USERNAME=your_email@gmail.com
    GMAIL_PASSWORD=your_app_password

4. Run the service
    python3 -m app.main

Expected Output
The service will:
Connect to your Gmail inbox
Fetch recent unread messages
Print or process them