from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar

from flask import flash, redirect, session, url_for


F = TypeVar("F", bound=Callable[..., Any])


def login_required(view: F) -> F:
    """Protéger une vue pour les utilisateurs connectés."""

    @wraps(view)
    def wrapped_view(*args: Any, **kwargs: Any):
        if session.get("user_id") is None:
            flash("Vous devez être connecté pour accéder à cette page.", "warning")
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapped_view  # type: ignore[return-value]


def admin_required(view: F) -> F:
    """Protéger une vue pour les administrateurs connectés."""

    @wraps(view)
    def wrapped_view(*args: Any, **kwargs: Any):
        if session.get("user_id") is None:
            flash("Vous devez être connecté pour accéder à cette page.", "warning")
            return redirect(url_for("auth.login"))

        if session.get("user_role") != "admin":
            flash("Accès réservé à l'administration.", "danger")
            return redirect(url_for("public.home"))

        return view(*args, **kwargs)

    return wrapped_view  # type: ignore[return-value]