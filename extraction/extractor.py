import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
from extraction.prompt import EXTRACTION_PROMPT

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def clean_json(text):
    """
    Extract JSON from LLM output
    """

    # remove markdown ```json blocks
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    # find JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group(0)

    return text


def extract_from_email(email):

    prompt = EXTRACTION_PROMPT.format(
        sender=email["sender"],
        recipients=", ".join(email["recipients"]),
        subject=email["subject"],
        body=email["body"][:2000]
    )

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    text = completion.choices[0].message.content

    cleaned = clean_json(text)

    try:
        data = json.loads(cleaned)

        # attach real source info
        for claim in data["claims"]:
            claim["evidence"]["source_id"] = email["message_id"]
            claim["evidence"]["timestamp"] = email["timestamp"]

        return data

    except Exception as e:
        print("Parsing error:", e)
        print("Raw output:", text)
        return None