from __future__ import annotations

from flask import Blueprint, render_template

from app.core.security import admin_required


bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="templates",
)


@bp.route("/", methods=["GET"])
@admin_required
def dashboard():
    return render_template("admin/dashboard.html")