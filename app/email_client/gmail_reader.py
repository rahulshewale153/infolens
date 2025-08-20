import imaplib
import email
from email.header import decode_header
from app.core.settings import settings
from bs4 import BeautifulSoup
import re
class GmailClient:
    def __init__(self):
        self.conn = None    
    def connect(self):
        self.conn = imaplib.IMAP4_SSL(settings.GMAIL_IMAP_URL, settings.GMAIL_IMAP_PORT)
        self.conn.login(settings.GMAIL_USERNAME, settings.GMAIL_PASSWORD)
        self.conn.select('inbox')

    def fetch_unread(self):
        if self.conn is None:
            raise Exception("Not connected. Call connect() first.")
        
        status, messages = self.conn.search(None, 'X-GM-RAW "category:primary label:unread"')
        if status != "OK":
            print("❌ Failed to fetch emails")
            return []
        

        latest_email_id = messages[0].split()[-1]
        
        _, msg_data = self.conn.fetch(latest_email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                return msg
        return None
    


    def get_decoded_header(self, header_value):
        """Decode subject / from headers with UTF-8 or fallback"""
        if not header_value:
            return ""
        decoded_parts = decode_header(header_value)
        header = ""
        for text, enc in decoded_parts:
            if isinstance(text, bytes):
                try:
                    header += text.decode(enc or "utf-8", errors="replace")
                except:
                    header += text.decode("utf-8", errors="replace")
            else:
                header += text
        return header

    def get_body(self, msg):
        """
        Extracts email body as clean UTF-8 raw text:
        - prefers text/plain
        - falls back to text/html (tags stripped)
        - decodes quoted-printable/base64 automatically
        """
        body_texts = []

        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                disp = str(part.get("Content-Disposition"))
                
                if "attachment" in disp:
                    continue  # skip attachments
                
                payload = part.get_payload(decode=True)
                if not payload:
                    continue

                charset = part.get_content_charset() or "utf-8"
                try:
                    text = payload.decode(charset, errors="replace")
                except:
                    text = payload.decode("utf-8", errors="replace")

                if ctype == "text/plain":
                    body_texts.append(text.strip())
                elif ctype == "text/html":
                    soup = BeautifulSoup(text, "html.parser")
                    # remove style, script, head, meta
                    for tag in soup(["style", "script", "head", "meta", "title"]):
                        tag.extract()
                    clean_text = soup.get_text(separator="\n")
                    body_texts.append(clean_text.strip())
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or "utf-8"
                try:
                    text = payload.decode(charset, errors="replace")
                except:
                    text = payload.decode("utf-8", errors="replace")

                if msg.get_content_type() == "text/html":
                    soup = BeautifulSoup(text, "html.parser")
                    for tag in soup(["style", "script", "head", "meta", "title"]):
                        tag.extract()
                    text = soup.get_text(separator="\n")
                body_texts.append(text.strip())

         # join all parts and normalize whitespace
        full_text = "\n\n".join(body_texts)

        # normalize spaces and collapse multiple newlines
        full_text = re.sub(r"[ \t]+", " ", full_text)          # collapse spaces/tabs
        full_text = re.sub(r"\n\s*\n\s*", "\n\n", full_text)   # collapse blank lines
        full_text = full_text.strip()

        return full_text

    

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn.logout()




            