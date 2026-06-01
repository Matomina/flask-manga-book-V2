from __future__ import annotations

from app.db import get_db


def get_dashboard_stats() -> dict[str, int]:
    db = get_db()
    row = db.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM user) AS users,
            (SELECT COUNT(*) FROM articles) AS articles,
            (SELECT COUNT(*) FROM orders) AS orders,
            (SELECT COUNT(*) FROM contact) AS contacts,
            (SELECT COUNT(*) FROM contact WHERE status != 'read') AS unread_contacts,
            (SELECT COUNT(*) FROM topics) AS forum_topics,
            (SELECT COUNT(*) FROM replies) AS forum_replies,
            (SELECT COUNT(*) FROM articles WHERE stock > 0 AND stock <= 5)
                AS low_stock_articles,
            (SELECT COUNT(*) FROM articles WHERE stock <= 0) AS out_of_stock_articles
        """
    ).fetchone()
    return dict(row)
