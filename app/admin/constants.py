from __future__ import annotations

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
VALID_ARTICLE_GENRES = {"manga", "figurine", "textile", "vaisselle", "goodies"}
VALID_ARTICLE_UNIVERSES = {
    "naruto",
    "jujutsu_kaisen",
    "one_piece",
    "demon_slayer",
    "dragon_ball",
}
VALID_RELEASE_DAYS = {
    "Lundi",
    "Mardi",
    "Mercredi",
    "Jeudi",
    "Vendredi",
    "Samedi",
    "Dimanche",
    "Sans jour fixe",
}
VALID_ORDER_STATUSES = {"pending", "paid", "shipped", "delivered", "cancelled"}
UPLOAD_FOLDER = "uploads"
