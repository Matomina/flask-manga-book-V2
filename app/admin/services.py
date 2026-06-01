from __future__ import annotations

from .account_services import get_all_users_admin, get_user_by_id_admin
from .article_services import (
    VALID_ARTICLE_GENRES,
    VALID_ARTICLE_UNIVERSES,
    VALID_RELEASE_DAYS,
    create_article,
    delete_article,
    get_all_articles_admin,
    get_article_by_id_admin,
    update_article,
    validate_article_data,
)
from .contact_services import (
    delete_contact,
    get_all_contacts,
    get_contact_by_id,
    mark_contact_as_read,
)
from .dashboard_services import get_dashboard_stats
from .media_services import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, allowed_file, save_image
from .order_services import (
    VALID_ORDER_STATUSES,
    get_all_orders_admin,
    get_order_by_id_admin,
    get_order_items_by_order_id,
    update_order_status_admin,
)

__all__ = [
    "ALLOWED_EXTENSIONS",
    "UPLOAD_FOLDER",
    "VALID_ARTICLE_GENRES",
    "VALID_ARTICLE_UNIVERSES",
    "VALID_ORDER_STATUSES",
    "VALID_RELEASE_DAYS",
    "allowed_file",
    "create_article",
    "delete_article",
    "delete_contact",
    "get_all_articles_admin",
    "get_all_contacts",
    "get_all_orders_admin",
    "get_all_users_admin",
    "get_article_by_id_admin",
    "get_contact_by_id",
    "get_dashboard_stats",
    "get_order_by_id_admin",
    "get_order_items_by_order_id",
    "get_user_by_id_admin",
    "mark_contact_as_read",
    "save_image",
    "update_article",
    "update_order_status_admin",
    "validate_article_data",
]
