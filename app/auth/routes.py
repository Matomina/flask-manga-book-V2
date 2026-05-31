from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from .services import RegistrationError, authenticate_user, create_user

bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    template_folder="templates",
)


def _set_user_session(user) -> None:
    session.clear()
    session["user_id"] = user["id"]
    session["user_first_name"] = user["first_name"]
    session["user_role"] = user["role"]


def _render_auth_page(
    *,
    active_panel: str = "login",
    login_data: dict | None = None,
    register_data: dict | None = None,
    status_code: int = 200,
):
    return (
        render_template(
            "auth/login.html",
            active_panel=active_panel,
            login_data=login_data or {},
            register_data=register_data or {},
        ),
        status_code,
    )


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Connecter un utilisateur ou un administrateur."""
    if session.get("user_id") is not None:
        if session.get("user_role") == "admin":
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("public.home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        login_data = {"email": email}

        if not email or not password:
            flash("Veuillez remplir tous les champs.", "warning")
            return _render_auth_page(
                active_panel="login",
                login_data=login_data,
                status_code=400,
            )

        user = authenticate_user(email, password)

        if user is None:
            flash("Email ou mot de passe incorrect.", "danger")
            return _render_auth_page(
                active_panel="login",
                login_data=login_data,
                status_code=401,
            )

        _set_user_session(user)
        flash("Connexion réussie.", "success")

        if user["role"] == "admin":
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("public.home"))

    return _render_auth_page(active_panel="login")[0]


@bp.route("/register", methods=["GET", "POST"])
def register():
    """Afficher et traiter l'inscription utilisateur."""
    if session.get("user_id") is not None:
        return redirect(url_for("public.home"))

    if request.method == "POST":
        data = request.form.to_dict()

        try:
            user = create_user(data)
        except RegistrationError as exc:
            flash(str(exc), "danger")
            return _render_auth_page(
                active_panel="register",
                register_data=data,
                status_code=400,
            )

        _set_user_session(user)
        flash("Compte créé avec succès.", "success")
        return redirect(url_for("public.profile"))

    return _render_auth_page(active_panel="register")[0]


@bp.route("/logout", methods=["POST"])
def logout():
    """Déconnecter l'utilisateur courant."""
    session.clear()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for("public.home"))
