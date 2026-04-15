from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, url_for

from app.core.security import login_required


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
@login_required
def create_topic():
    flash("Création de sujet à venir.", "info")
    return redirect(url_for("forum.index"))