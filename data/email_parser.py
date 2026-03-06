import email
from email import policy


def parse_email(raw_email: str):

    msg = email.message_from_string(raw_email, policy=policy.default)

    message_id = msg.get("Message-ID")
    date = msg.get("Date")
    sender = msg.get("From")
    to = msg.get("To")
    subject = msg.get("Subject")

    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_content()
    else:
        body = msg.get_content()

    recipients = []
    if to:
        recipients = [x.strip() for x in to.split(",")]

    return {
        "message_id": message_id,
        "timestamp": date,
        "sender": sender,
        "recipients": recipients,
        "subject": subject,
        "body": body
    }