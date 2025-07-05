from fastapi import Request
from app.auth.jwt_utils import decode_token
from app.repository.cancel_order import cancel_order_logic


async def resolve_cancel_order(_, info, id):
    request: Request = info.context["request"]
    token = request.headers.get("Authorization")

    if not token or not token.startswith("Bearer "):
        raise Exception("Token de autorización faltante o mal formado")

    token = token.split(" ")[1]
    payload = decode_token(token)
    email = payload.get("email")

    return cancel_order_logic(id, email)
