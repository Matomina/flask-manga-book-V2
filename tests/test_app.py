from app import create_app


def test_config():
    app = create_app({"TESTING": True})

    assert app is not None
    assert app.config["TESTING"] is True