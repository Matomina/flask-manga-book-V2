from __future__ import annotations

from flask import Blueprint, redirect, render_template, url_for

bp = Blueprint(
    "forum",
    __name__,
    url_prefix="/forum",
    template_folder="templates",
)


@bp.route("/", methods=["GET"])
def index():
    return render_template("forum/index.html")


@bp.route("/create", methods=["POST"])
def create_topic():
    return redirect(url_for("auth.login"))