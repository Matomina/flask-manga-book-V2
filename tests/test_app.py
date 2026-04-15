from manga import create_app


def test_create_app():
    app = create_app()
    assert app is not None
    assert app.config["SECRET_KEY"] is not None