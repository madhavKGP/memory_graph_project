import pandas as pd
from data.email_parser import parse_email


def load_emails(csv_path, limit=5):

    df = pd.read_csv(csv_path)

    emails = []

    for i, row in df.iterrows():

        raw_message = row["message"]

        parsed = parse_email(raw_message)

        emails.append(parsed)

        if i >= limit:
            break

    return emails