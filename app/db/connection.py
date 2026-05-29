from __future__ import annotations

import sqlite3
from pathlib import Path

import click
from flask import Flask, current_app, g

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / "schema.sql"
SEED_PATH = BASE_DIR / "seed.sql"
LEGACY_ARTICLES_SEED_PATH = BASE_DIR / "legacy_articles_seed.sql"


def get_db() -> sqlite3.Connection:
    """Retourner une connexion SQLite stockée dans le contexte Flask."""
    if "db" not in g:
        connection = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON;")
        g.db = connection

    return g.db


def close_db(error: Exception | None = None) -> None:
    """Fermer la connexion SQLite."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def execute_sql_file(path: Path) -> None:
    """Exécuter un fichier SQL s'il existe."""
    if not path.exists():
        return

    db = get_db()
    db.executescript(path.read_text(encoding="utf-8"))
    db.commit()


def init_db() -> None:
    """Créer la base via schema.sql."""
    execute_sql_file(SCHEMA_PATH)


def seed_db() -> None:
    """Insérer les données initiales via seed.sql."""
    execute_sql_file(SEED_PATH)


def seed_legacy_articles_db() -> None:
    """Insérer le catalogue officiel migré depuis la V1."""
    execute_sql_file(LEGACY_ARTICLES_SEED_PATH)


def reset_db() -> None:
    """Réinitialiser complètement la base avec le catalogue officiel."""
    init_db()
    seed_db()
    seed_legacy_articles_db()


@click.command("init-db")
def init_db_command() -> None:
    init_db()
    click.echo("Base initialisée.")


@click.command("seed-db")
def seed_db_command() -> None:
    seed_db()
    click.echo("Seed injecté.")


@click.command("seed-legacy-articles")
def seed_legacy_articles_db_command() -> None:
    seed_legacy_articles_db()
    click.echo("Catalogue legacy injecté.")


@click.command("reset-db")
def reset_db_command() -> None:
    reset_db()
    click.echo("Base réinitialisée avec catalogue legacy.")


def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
    app.cli.add_command(seed_legacy_articles_db_command)
    app.cli.add_command(reset_db_command)
