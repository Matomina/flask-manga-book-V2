from __future__ import annotations

from flask import Flask, render_template


def register_error_handlers(app: Flask) -> None:
    """Enregistrer les gestionnaires d'erreurs globaux."""

    @app.errorhandler(403)
    def forbidden(error: Exception):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error: Exception):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error: Exception):
        return render_template("errors/500.html"), 500
