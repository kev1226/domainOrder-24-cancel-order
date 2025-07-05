from fastapi import HTTPException
from bson import ObjectId
from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("DB_NAME")]
orders = db["orders"]


def cancel_order_logic(order_id: str, email: str):
    order = orders.find_one({"_id": ObjectId(order_id)})

    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    if order["user"]["email"] != email:
        raise HTTPException(
            status_code=403, detail="No autorizado para cancelar esta orden"
        )

    if order["status"] != "PENDIENTE_DE_PAGO":
        raise HTTPException(
            status_code=400, detail="Solo se pueden cancelar órdenes pendientes"
        )

    orders.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": "CANCELADA"}})

    return {
        "id": str(order["_id"]),
        "status": "CANCELADA",
        "message": "Orden cancelada exitosamente",
    }
