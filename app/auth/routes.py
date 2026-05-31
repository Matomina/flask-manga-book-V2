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

        if not email or not password:
            flash("Veuillez remplir tous les champs.", "warning")
            return render_template("auth/login.html"), 400

        user = authenticate_user(email, password)

        if user is None:
            flash("Email ou mot de passe incorrect.", "danger")
            return render_template("auth/login.html"), 401

        _set_user_session(user)
        flash("Connexion réussie.", "success")

        if user["role"] == "admin":
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("public.home"))

    return render_template("auth/login.html")


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
            return render_template("auth/register.html", data=data), 400

        _set_user_session(user)
        flash("Compte créé avec succès.", "success")
        return redirect(url_for("public.profile"))

    return render_template("auth/register.html")


@bp.route("/logout", methods=["POST"])
def logout():
    """Déconnecter l'utilisateur courant."""
    session.clear()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for("public.home"))
