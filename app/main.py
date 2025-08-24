from app.core.settings import settings
from app.email_client.gmail_reader import GmailClient

def main():
    print(f"Application Name: {settings.APP_NAME}")
    print(f"Environment: {settings.ENV}")
    print(f"Database URL: {settings.DB_URL}")
    print(f"OpenAI API Key: {settings.OPEN_API_KEY}")

    gmailClient= GmailClient()
    gmailClient.connect()

    email = gmailClient.fetch_unread()
    print(f"📩 Found {len(email)} unread email")
    attachments = gmailClient.download_attachments(email)
    print("📎 Attachments saved:", attachments)
    
    if email:
            print("From:", gmailClient.get_decoded_header(email["From"]))
            print("Subject:", gmailClient.get_decoded_header(email["Subject"]))
            print("Body:\n", gmailClient.get_body(email))
    else:
            print("No unseen mails in Primary.")


if __name__ == "__main__":
    main()