import io
import unittest

from app import create_app


class AppTests(unittest.TestCase):
    def test_create_app_registers_email_routes(self):
        app = create_app(testing=True)

        self.assertTrue(app.testing)
        self.assertTrue(any(rule.endpoint == "email.process_email" for rule in app.url_map.iter_rules()))

    def test_process_email_returns_validation_error_for_empty_payload(self):
        app = create_app(testing=True)
        client = app.test_client()

        response = client.post("/email/process", data={})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["erro"], "Nenhum email ou arquivo válido enviado.")

    def test_process_email_rejects_invalid_file_extension(self):
        app = create_app(testing=True)
        client = app.test_client()

        response = client.post(
            "/email/process",
            data={"file": (io.BytesIO(b"conteudo"), "arquivo.exe")},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("tipo de arquivo", response.get_json()["erro"].lower())


if __name__ == "__main__":
    unittest.main()
