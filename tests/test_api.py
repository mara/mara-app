import pytest

from mara_app.app import MaraApp


class TestApp:
    @pytest.fixture(autouse=True)
    def set_up(self):
        app = MaraApp()
        self.app = app.test_client()

    def test_config_page_exists(self):
        response = self.app.get("/admin/configuration")
        assert response.status_code == 200



if __name__ == "__main__":
    pytest.main()
