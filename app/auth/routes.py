from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, url_for

bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    template_folder="templates",
)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == "admin@test.com" and password == "test":
            return redirect(url_for("admin.dashboard"))

        return "incorrect", 200

    return render_template("auth/login.html")


@bp.route("/register", methods=["GET"])
def register():
    return render_template("auth/register.html")


@bp.route("/logout", methods=["GET"])
def logout():
    return redirect(url_for("public.home"))