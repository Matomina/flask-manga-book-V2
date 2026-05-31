from __future__ import annotations

import sqlite3
from pathlib import Path

import click
from flask import Flask, current_app, g

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / "schema.sql"
SEED_PATH = BASE_DIR / "seed.sql"
MIGRATIONS_DIR = BASE_DIR / "migrations"
MIGRATIONS_TABLE = "schema_migrations"
BASE_SCHEMA_TABLES = {"user", "articles", "orders"}


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


def _table_exists(table_name: str) -> bool:
    db = get_db()
    row = db.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table' AND name = ?
        """,
        (table_name,),
    ).fetchone()
    return row is not None


def _base_schema_exists() -> bool:
    return all(_table_exists(table_name) for table_name in BASE_SCHEMA_TABLES)


def _column_exists(table_name: str, column_name: str) -> bool:
    db = get_db()
    columns = db.execute(f"PRAGMA table_info({table_name})").fetchall()
    return any(column["name"] == column_name for column in columns)


def _ensure_migration_table() -> None:
    db = get_db()
    db.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {MIGRATIONS_TABLE} (
            name TEXT PRIMARY KEY,
            applied_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    db.commit()


def _migration_applied(name: str) -> bool:
    db = get_db()
    row = db.execute(
        f"SELECT 1 FROM {MIGRATIONS_TABLE} WHERE name = ?",
        (name,),
    ).fetchone()
    return row is not None


def _mark_migration_applied(name: str) -> None:
    db = get_db()
    db.execute(
        f"INSERT OR IGNORE INTO {MIGRATIONS_TABLE} (name) VALUES (?)",
        (name,),
    )


def _apply_payment_tracking_migration() -> bool:
    db = get_db()

    if not _table_exists("orders"):
        return False

    if not _column_exists("orders", "payment_status"):
        db.execute(
            """
            ALTER TABLE orders
            ADD COLUMN payment_status TEXT NOT NULL DEFAULT 'unpaid'
            """
        )

    if not _column_exists("orders", "payment_provider"):
        db.execute("ALTER TABLE orders ADD COLUMN payment_provider TEXT")

    if not _column_exists("orders", "payment_reference"):
        db.execute("ALTER TABLE orders ADD COLUMN payment_reference TEXT")

    db.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_orders_payment_status
        ON orders(payment_status)
        """
    )
    return True


def _apply_migration_file(migration_path: Path) -> bool:
    db = get_db()

    if migration_path.name == "002_payment_tracking.sql":
        return _apply_payment_tracking_migration()

    db.executescript(migration_path.read_text(encoding="utf-8"))
    return True


def run_migrations() -> None:
    """Exécuter les migrations SQL additionnelles dans l'ordre."""
    if not MIGRATIONS_DIR.exists() or not _base_schema_exists():
        return

    _ensure_migration_table()
    db = get_db()

    for migration_path in sorted(MIGRATIONS_DIR.glob("*.sql")):
        migration_name = migration_path.name
        if _migration_applied(migration_name):
            continue

        applied = _apply_migration_file(migration_path)
        if applied:
            _mark_migration_applied(migration_name)

    db.commit()


def init_db() -> None:
    """Créer la base via schema.sql puis appliquer les migrations."""
    db = get_db()
    db.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    db.commit()
    run_migrations()


def seed_db() -> None:
    """Insérer les données initiales via seed.sql."""
    if not SEED_PATH.exists():
        return

    db = get_db()
    db.executescript(SEED_PATH.read_text(encoding="utf-8"))
    db.commit()


def reset_db() -> None:
    """Réinitialiser complètement la base."""
    init_db()
    seed_db()


@click.command("init-db")
def init_db_command() -> None:
    init_db()
    click.echo("Base initialisée.")


@click.command("seed-db")
def seed_db_command() -> None:
    seed_db()
    click.echo("Seed injecté.")


@click.command("reset-db")
def reset_db_command() -> None:
    reset_db()
    click.echo("Base réinitialisée.")


@click.command("migrate-db")
def migrate_db_command() -> None:
    run_migrations()
    click.echo("Migrations appliquées.")


def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
    app.cli.add_command(reset_db_command)
    app.cli.add_command(migrate_db_command)
