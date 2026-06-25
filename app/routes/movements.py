
from fastapi import APIRouter, HTTPException
from app.database import get_connection

router = APIRouter()

@router.post("/api/movements")
def create_movement(data: dict):

    product_id = data.get("product_id")
    warehouse_id = data.get("warehouse_id")
    movement_type = data.get("movement_type")
    quantity = data.get("quantity")

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

    cur.execute(
        "SELECT id FROM warehouses WHERE id=%s",
        (warehouse_id,)
    )

    warehouse = cur.fetchone()

    if not warehouse:
        raise HTTPException(
            status_code=404,
            detail="Warehouse not found"
        )

    cur.execute("""
        INSERT INTO stock_movements(
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

    conn.commit()

    cur.close()
    conn.close()

    return {"message": "Movement created successfully"}