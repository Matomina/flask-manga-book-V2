from __future__ import annotations

from flask import Blueprint, redirect, render_template, url_for

bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="templates",
)


@bp.route("/", methods=["GET"])
def dashboard():
    return render_template("admin/dashboard.html")