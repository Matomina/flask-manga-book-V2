from __future__ import annotations

import sqlite3
from pathlib import Path

import click
from flask import Flask, current_app, g


BASE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / "schema.sql"
SEED_PATH = BASE_DIR / "seed.sql"
RESET_PATH = BASE_DIR / "reset.sql"


def get_db() -> sqlite3.Connection:
    """Retourner une connexion SQLite stockée dans le contexte Flask."""
    if "db" not in g:
        database_path = current_app.config["DATABASE"]

        connection = sqlite3.connect(
            database_path,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON;")

        g.db = connection

    return g.db


def close_db(error: Exception | None = None) -> None:
    """Fermer la connexion SQLite en fin de requête."""
    db = g.pop("db", None)

    if db is not None:
        db.close()


def _execute_sql_file(path: Path) -> None:
    """Exécuter un fichier SQL."""
    if not path.exists():
        raise FileNotFoundError(f"Fichier SQL introuvable : {path}")

    db = get_db()
    sql_script = path.read_text(encoding="utf-8")
    db.executescript(sql_script)
    db.commit()


def init_db() -> None:
    """Créer la structure de la base de données."""
    _execute_sql_file(SCHEMA_PATH)


def seed_db() -> None:
    """Insérer les données initiales de la base."""
    _execute_sql_file(SEED_PATH)


def reset_db() -> None:
    """Réinitialiser complètement la base."""
    if RESET_PATH.exists():
        _execute_sql_file(RESET_PATH)
        return

    init_db()

    if SEED_PATH.exists():
        seed_db()


@click.command("init-db")
def init_db_command() -> None:
    """Commande Flask : initialiser la base."""
    init_db()
    click.echo("Base de données initialisée.")


@click.command("seed-db")
def seed_db_command() -> None:
    """Commande Flask : injecter les données initiales."""
    seed_db()
    click.echo("Données initiales insérées.")


@click.command("reset-db")
def reset_db_command() -> None:
    """Commande Flask : reset complet de la base."""
    reset_db()
    click.echo("Base de données réinitialisée.")


def init_app(app: Flask) -> None:
    """Brancher la gestion DB à l'application Flask."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
    app.cli.add_command(reset_db_command)