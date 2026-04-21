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

from flask import Blueprint

# Blueprint du forum public
bp = Blueprint(
    "forum",
    __name__,
    url_prefix="/forum",
    template_folder="templates",
)

# Import des routes (important à la fin pour éviter les imports circulaires)
from . import routes  # noqa: E402, F401