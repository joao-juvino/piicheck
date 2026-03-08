import io


def test_upload_txt_file(client, auth_headers, mock_celery):

    data = {
        "file": (io.BytesIO(b"cpf 123.456.789-10"), "test.txt")
    }

    response = client.post(
        "/pii/scan",
        headers=auth_headers,
        content_type="multipart/form-data",
        data=data
    )

    assert response.status_code == 202

    json_data = response.get_json()

    assert "scan_id" in json_data
    assert json_data["status"] == "queued"

def test_upload_invalid_file(client, auth_headers):

    data = {
        "file": (io.BytesIO(b"test"), "file.pdf")
    }

    response = client.post(
        "/pii/scan",
        headers=auth_headers,
        content_type="multipart/form-data",
        data=data
    )

    assert response.status_code == 400

def test_upload_without_file(client, auth_headers):

    response = client.post(
        "/pii/scan",
        headers=auth_headers,
        content_type="multipart/form-data",
        data={}
    )

    assert response.status_code == 422
