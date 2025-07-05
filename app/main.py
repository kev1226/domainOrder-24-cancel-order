from fastapi import FastAPI
from ariadne import gql, MutationType, make_executable_schema
from ariadne.asgi import GraphQL
from app.graphql.resolver import resolve_cancel_order
from dotenv import load_dotenv
import os

load_dotenv()

PORT = int(os.getenv("PORT", 3054))

type_defs = gql(open("app/graphql/schema.graphql", encoding="utf-8").read())
mutation = MutationType()
mutation.set_field("cancelOrder", resolve_cancel_order)
schema = make_executable_schema(type_defs, mutation)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "cancel-order-service running"}


app.mount("/graphql", GraphQL(schema, debug=True))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)
