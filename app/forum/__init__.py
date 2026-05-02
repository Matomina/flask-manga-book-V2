(
    """Package admin."""
    """
========================================================
MANGABOOK – FORUM PUBLIC BLUEPRINT
--------------------------------------------------------
Gestion du forum côté public :
- liste des sujets
- détail d’un sujet
- création de sujet
- réponses
========================================================
"""
)

from flask import Blueprint

bp = Blueprint(
    "forum",
    __name__,
    url_prefix="/forum",
    template_folder="templates",
)

from . import routes  # noqa: E402, F401
