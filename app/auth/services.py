from __future__ import annotations

import sqlite3
from typing import Any

from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db


class RegistrationError(ValueError):
    """Erreur contrôlée lors de l'inscription utilisateur."""


def _normalize_text(value: Any) -> str:
    """Nettoyer une valeur texte utilisateur."""
    return str(value or "").strip()


def _normalize_email(value: Any) -> str:
    """Normaliser un email utilisateur."""
    return _normalize_text(value).lower()


def _normalize_optional_text(value: Any) -> str | None:
    """Nettoyer une valeur texte optionnelle."""
    cleaned = _normalize_text(value)
    return cleaned or None


def get_user_by_email(email: str) -> sqlite3.Row | None:
    """Récupérer un utilisateur par son email."""
    db = get_db()
    normalized_email = _normalize_email(email)

    try:
        return db.execute(
            """
            SELECT id, first_name, last_name, email, password, role
            FROM user
            WHERE email = ?
            """,
            (normalized_email,),
        ).fetchone()
    except sqlite3.Error:
        return None


def get_user_by_id(user_id: int) -> sqlite3.Row | None:
    """Récupérer un utilisateur par son identifiant."""
    db = get_db()

    try:
        return db.execute(
            """
            SELECT id, first_name, last_name, email, role
            FROM user
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()
    except sqlite3.Error:
        return None


def _phone_exists(phone: str) -> bool:
    """Vérifier si un téléphone est déjà utilisé."""
    db = get_db()
    row = db.execute(
        """
        SELECT 1
        FROM user
        WHERE phone = ?
        """,
        (phone,),
    ).fetchone()
    return row is not None


def create_user(data: dict[str, Any]) -> sqlite3.Row:
    """Créer un utilisateur standard après validation métier."""
    first_name = _normalize_text(data.get("first_name"))
    last_name = _normalize_text(data.get("last_name"))
    email = _normalize_email(data.get("email"))
    password = _normalize_text(data.get("password"))
    phone = _normalize_optional_text(data.get("phone"))
    address = _normalize_optional_text(data.get("address"))
    city = _normalize_optional_text(data.get("city"))

    if not first_name:
        raise RegistrationError("Le prénom est obligatoire.")

    if not last_name:
        raise RegistrationError("Le nom est obligatoire.")

    if not email:
        raise RegistrationError("L'email est obligatoire.")

    if not password:
        raise RegistrationError("Le mot de passe est obligatoire.")

    if len(password) < 6:
        raise RegistrationError("Le mot de passe doit contenir au moins 6 caractères.")

    if get_user_by_email(email) is not None:
        raise RegistrationError("Cet email est déjà utilisé.")

    if phone is not None and _phone_exists(phone):
        raise RegistrationError("Ce numéro de téléphone est déjà utilisé.")

    db = get_db()
    db.execute(
        """
        INSERT INTO user (
            first_name,
            last_name,
            email,
            password,
            phone,
            address,
            city,
            role
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            first_name,
            last_name,
            email,
            generate_password_hash(password),
            phone,
            address,
            city,
            "user",
        ),
    )
    db.commit()

    user = get_user_by_email(email)
    if user is None:
        raise RegistrationError("Impossible de créer le compte utilisateur.")

    return user


def authenticate_user(email: str, password: str) -> sqlite3.Row | None:
    """Authentifier un utilisateur avec son email et son mot de passe."""
    user = get_user_by_email(email)

    if user is None:
        return None

    if not check_password_hash(user["password"], password):
        return None

    return user
