"""API REST de pedidos simulada (substitua por um ERP/e-commerce real)."""
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/mock", tags=["mock-orders"])

ORDERS = {
    "1001": {"id": "1001", "status": "shipped", "carrier": "Correios", "eta": "2026-11-20"},
    "1002": {"id": "1002", "status": "processing", "carrier": None, "eta": "2026-11-25"},
    "1003": {"id": "1003", "status": "delayed", "carrier": "Jadlog", "eta": "2026-12-02"},
}

@router.get("/orders/{order_id}")
def get_order(order_id: str):
    order = ORDERS.get(order_id)
    if not order:
        raise HTTPException(404, "Pedido não encontrado")
    return order
