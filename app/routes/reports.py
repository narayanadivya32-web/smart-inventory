
from fastapi import APIRouter
from app.database import get_connection

router = APIRouter()


@router.get("/api/reports/reorder")
def reorder_report():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.id,
            p.sku,
            p.name,
            p.reorder_level,
            COALESCE(
                SUM(
                    CASE
                        WHEN sm.movement_type = 'IN'
                        THEN sm.quantity
                        ELSE -sm.quantity
                    END
                ),
                0
            ) AS current_stock
        FROM products p
        LEFT JOIN stock_movements sm
            ON p.id = sm.product_id
        GROUP BY
            p.id,
            p.sku,
            p.name,
            p.reorder_level
        HAVING
            COALESCE(
                SUM(
                    CASE
                        WHEN sm.movement_type = 'IN'
                        THEN sm.quantity
                        ELSE -sm.quantity
                    END
                ),
                0
            ) <= p.reorder_level
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "sku": row[1],
            "name": row[2],
            "reorder_level": row[3],
            "current_stock": row[4]
        }
        for row in rows
    ]