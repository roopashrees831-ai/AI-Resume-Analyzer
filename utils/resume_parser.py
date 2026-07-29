import re


def extract_contact_details(text):
    # Email
    email = "Not Found"
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    if email_match:
        email = email_match.group()

    # Phone Number
    phone = "Not Found"
    phone_match = re.search(r"(\+91[-\s]?)?[6-9]\d{9}", text)
    if phone_match:
        phone = phone_match.group()

    # Name (First non-empty line)
    name = "Not Found"
    lines = text.split("\n")

    for line in lines:
        line = line.strip()
        if line:
            name = line
            break

    return name, email, phone

def extract_education(text):
    education_keywords = [
        "B.E", "B.Tech", "BCA", "B.Sc", "B.Com",
        "M.E", "M.Tech", "MCA", "MBA", "M.Sc",
        "Bachelor", "Master", "Diploma", "PUC", "12th", "10th"
    ]

    found = []

    for keyword in education_keywords:
        if keyword.lower() in text.lower():
            found.append(keyword)

    return list(set(found))