import re


class PIIDetector:

    CPF_REGEX = r"\b\d{3}\.\d{3}\.\d{3}\-\d{2}\b"
    EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    PHONE_REGEX = r"\b\d{2}\s?\d{4,5}\-?\d{4}\b"

    @staticmethod
    def scan_text(text: str):

        results = []

        for match in re.finditer(PIIDetector.CPF_REGEX, text):
            results.append({
                "type": "cpf",
                "value": match.group(),
                "start": match.start(),
                "end": match.end()
            })

        for match in re.finditer(PIIDetector.EMAIL_REGEX, text):
            results.append({
                "type": "email",
                "value": match.group(),
                "start": match.start(),
                "end": match.end()
            })

        for match in re.finditer(PIIDetector.PHONE_REGEX, text):
            results.append({
                "type": "phone",
                "value": match.group(),
                "start": match.start(),
                "end": match.end()
            })

        return results