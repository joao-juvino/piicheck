from app.modules.pii.pii_detector import PIIDetector


def test_detects_cpf():

    text = "Meu cpf é 123.456.789-10"

    results = PIIDetector.scan_text(text)

    assert len(results) == 1
    assert results[0]["type"] == "cpf"
    assert results[0]["value"] == "123.456.789-10"


def test_detects_email():

    text = "Email: test@email.com"

    results = PIIDetector.scan_text(text)

    assert results[0]["type"] == "email"


def test_detects_phone():

    text = "Telefone 11 91234-5678"

    results = PIIDetector.scan_text(text)

    assert results[0]["type"] == "phone"