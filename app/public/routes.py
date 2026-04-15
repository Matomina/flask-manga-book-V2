from __future__ import annotations

from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint(
    "public",
    __name__,
    template_folder="templates",
)


@bp.route("/")
def home():
    return render_template("public/home.html")


@bp.route("/about")
def about():
    return render_template("public/about.html")


@bp.route("/contact", methods=["POST"])
def contact():
    return redirect(url_for("auth.login"))