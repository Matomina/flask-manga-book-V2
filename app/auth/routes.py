from __future__ import annotations

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from .services import authenticate_user


bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    template_folder="templates",
)


@bp.route("/login", methods=["GET", "POST"])
def login():
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

        session.clear()
        session["user_id"] = user["id"]
        session["user_first_name"] = user["first_name"]
        session["user_role"] = user["role"]

        flash("Connexion réussie.", "success")

        if user["role"] == "admin":
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("public.home"))

    return render_template("auth/login.html")


@bp.route("/register", methods=["GET"])
def register():
    return render_template("auth/register.html")


@bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for("public.home"))