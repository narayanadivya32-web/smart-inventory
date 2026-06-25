from fastapi import APIRouter, HTTPException
from app.database import get_connection

router = APIRouter()

@router.get("/api/movements")
def get_movements():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            sm.id,
            p.name,
            w.name,
            sm.movement_type,
            sm.quantity,
            sm.created_at
        FROM stock_movements sm
        JOIN products p
            ON sm.product_id = p.id
        JOIN warehouses w
            ON sm.warehouse_id = w.id
        ORDER BY sm.created_at DESC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "product": row[1],
            "warehouse": row[2],
            "movement_type": row[3],
            "quantity": row[4],
            "created_at": row[5]
        })

    return result

@router.post("/api/movements")
def create_movement(data: dict):

    print("========== MOVEMENT REQUEST ==========")
    print(data)
    print("======================================")

    product_id = data.get("product_id")
    warehouse_id = data.get("warehouse_id")
    movement_type = data.get("movement_type")
    quantity = data.get("quantity")

    # Validate required fields
    if product_id is None:
        raise HTTPException(
            status_code=400,
            detail="Product ID is required"
        )

    if warehouse_id is None:
        raise HTTPException(
            status_code=400,
            detail="Warehouse ID is required"
        )

    if movement_type is None:
        raise HTTPException(
            status_code=400,
            detail="Movement type is required"
        )

    if quantity is None:
        raise HTTPException(
            status_code=400,
            detail="Quantity is required"
        )

    try:
        quantity = int(quantity)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be a number"
        )

    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    if movement_type not in ["IN", "OUT"]:
        raise HTTPException(
            status_code=400,
            detail="Movement type must be IN or OUT"
        )

    conn = get_connection()
    cur = conn.cursor()

    # Check warehouse
    cur.execute(
        "SELECT id FROM warehouses WHERE id=%s",
        (warehouse_id,)
    )

    if cur.fetchone() is None:
        cur.close()
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Warehouse not found"
        )

    # Check product
    cur.execute(
        "SELECT current_stock FROM products WHERE id=%s",
        (product_id,)
    )

    product = cur.fetchone()

    if product is None:
        cur.close()
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    current_stock = int(product[0])

    # Calculate stock
    if movement_type == "IN":
        new_stock = current_stock + quantity
    else:
        if current_stock < quantity:
            cur.close()
            conn.close()
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock"
            )

        new_stock = current_stock - quantity

    # Save movement
    cur.execute("""
        INSERT INTO stock_movements
        (
            product_id,
            warehouse_id,
            movement_type,
            quantity
        )
        VALUES (%s,%s,%s,%s)
    """,
    (
        product_id,
        warehouse_id,
        movement_type,
        quantity
    ))

    # Update stock
    cur.execute("""
        UPDATE products
        SET current_stock=%s
        WHERE id=%s
    """,
    (
        new_stock,
        product_id
    ))

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "Movement created successfully",
        "current_stock": new_stock
    }