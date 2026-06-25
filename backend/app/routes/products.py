from fastapi import APIRouter, Query
from app.database import get_connection
from fastapi import HTTPException

router = APIRouter()


# ---------------- ADD PRODUCT ----------------
@router.post("/api/products")
def add_product(data: dict):

    sku = data.get("sku")
    name = data.get("name")
    reorder_level = data.get("reorder_level")

    if not sku or not name:
        raise HTTPException(
            status_code=400,
            detail="SKU and Name are required"
        )

    conn = get_connection()
    cur = conn.cursor()

    # Check duplicate SKU
    cur.execute(
        "SELECT id FROM products WHERE sku=%s",
        (sku,)
    )

    if cur.fetchone():
        cur.close()
        conn.close()

        raise HTTPException(
            status_code=400,
            detail="SKU already exists"
        )

    cur.execute("""
        INSERT INTO products
        (
            sku,
            name,
            category_id,
            reorder_level,
            current_stock
        )
        VALUES (%s,%s,%s,%s,%s)
    """,
    (
        sku,
        name,
        1,                  # Electronics
        reorder_level,
        0
    ))

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "Product added successfully"
    }


# ---------------- UPDATE PRODUCT ----------------
@router.put("/api/products/{product_id}")
def update_product(product_id: int, data: dict):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE products
        SET
            sku=%s,
            name=%s,
            reorder_level=%s
        WHERE id=%s
    """,
    (
        data["sku"],
        data["name"],
        data["reorder_level"],
        product_id
    ))

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "Product updated successfully"
    }


# ---------------- DELETE PRODUCT ----------------
@router.delete("/api/products/{product_id}")
def delete_product(product_id: int):

    conn = get_connection()
    cur = conn.cursor()

    # Prevent deleting products with movements
    cur.execute(
        "SELECT COUNT(*) FROM stock_movements WHERE product_id=%s",
        (product_id,)
    )

    count = cur.fetchone()[0]

    if count > 0:
        cur.close()
        conn.close()

        raise HTTPException(
            status_code=400,
            detail="Cannot delete product because stock movements exist."
        )

    cur.execute(
        "DELETE FROM products WHERE id=%s",
        (product_id,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "Product deleted successfully"
    }

# ---------------- GET PRODUCTS ----------------
@router.get("/api/products")
def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str = "",
    sort: str = "id",
    order: str = "asc"
):

    allowed_sorts = [
        "id",
        "sku",
        "name",
        "reorder_level"
    ]

    if sort not in allowed_sorts:
        sort = "id"

    if order.lower() not in ["asc", "desc"]:
        order = "asc"

    offset = (page - 1) * page_size

    conn = get_connection()
    cur = conn.cursor()

    query = f"""
        SELECT
            p.id,
            p.sku,
            p.name,
            c.name AS category,
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

        LEFT JOIN categories c
            ON p.category_id = c.id

        LEFT JOIN stock_movements sm
            ON p.id = sm.product_id

        WHERE
            LOWER(p.name) LIKE LOWER(%s)
            OR LOWER(p.sku) LIKE LOWER(%s)

        GROUP BY
            p.id,
            p.sku,
            p.name,
            c.name,
            p.reorder_level

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

    products = []

    for row in rows:

        current_stock = row[5]

        if current_stock <= 0:
            status = "CRITICAL"
        elif current_stock <= row[4]:
            status = "LOW"
        else:
            status = "OK"

        products.append({
            "id": row[0],
            "sku": row[1],
            "name": row[2],
            "category": row[3],
            "reorder_level": row[4],
            "current_stock": current_stock,
            "status": status
        })

    return products


# ---------------- PRODUCT STOCK ----------------
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


# ---------------- PRODUCT MOVEMENTS ----------------
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