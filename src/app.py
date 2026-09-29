from fastapi import FastAPI
from src.features.youtube.presentation.graphql.router import graphql_app

app = FastAPI(
    title="Neurotry YouTube Service",
    description="Servicio GraphQL para gestión de YouTube"
)

# Montar el router de GraphQL
app.include_router(graphql_app, prefix="/graphql")
