EXTRACTION_PROMPT = """
You are an information extraction system.

Extract structured knowledge from this email.

Return JSON with:

entities:
- name
- type (Person, Organization, Project, Bug, Topic)

claims:
- subject
- relation
- object

Each claim MUST include evidence:
- source_id
- excerpt
- timestamp
- confidence

Rules:
- Only extract factual statements
- Do not hallucinate
- Evidence excerpt must appear in the email

Email:

Sender: {sender}
Recipients: {recipients}
Subject: {subject}

Body:
{body}
"""