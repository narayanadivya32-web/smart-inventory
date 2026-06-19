from fastapi import APIRouter, Query
from app.database import get_connection

router = APIRouter()


@router.get("/api/products")
def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str = "",
    sort: str = "id",
    order: str = "asc"
):

    allowed_sorts = ["id", "sku", "name", "reorder_level"]

    if sort not in allowed_sorts:
        sort = "id"

    if order.lower() not in ["asc", "desc"]:
        order = "asc"

    offset = (page - 1) * page_size

    conn = get_connection()
    cur = conn.cursor()

    query = f"""
        SELECT
            id,
            sku,
            name,
            reorder_level
        FROM products
        WHERE
            LOWER(name) LIKE LOWER(%s)
            OR LOWER(sku) LIKE LOWER(%s)
        ORDER BY {sort} {order}
        LIMIT %s
        OFFSET %s
    """

    search_term = f"%{search}%"

    cur.execute(
        query,
        (
            search_term,
            search_term,
            page_size,
            offset
        )
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "sku": row[1],
            "name": row[2],
            "reorder_level": row[3]
        }
        for row in rows
    ]


@router.get("/api/products/{product_id}/stock")
def get_stock(product_id: int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COALESCE(
                SUM(
                    CASE
                        WHEN movement_type = 'IN'
                        THEN quantity
                        ELSE -quantity
                    END
                ),
                0
            )
        FROM stock_movements
        WHERE product_id = %s
    """, (product_id,))

    stock = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "product_id": product_id,
        "current_stock": stock
    }


@router.get("/api/products/{product_id}/movements")
def get_movements(product_id: int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            warehouse_id,
            movement_type,
            quantity,
            created_at
        FROM stock_movements
        WHERE product_id = %s
        ORDER BY created_at DESC
        LIMIT 20
    """, (product_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "warehouse_id": row[1],
            "movement_type": row[2],
            "quantity": row[3],
            "created_at": row[4]
        }
        for row in rows
    ]