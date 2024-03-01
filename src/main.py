from fastapi import FastAPI

from google.cloud.firestore import AsyncClient

from src.application.reserves.repositories.reserve_repository_async import ReservesRepositoryAsync
from src.application.reserves.services.reserve_service_async import ReservesServiceAsync
from src.infrastructure.firebase.config.config import initialize_firebase, get_firestore_async
from src.infrastructure.firebase.reserves.repositories.firestore_reserves_repository_async import \
    FirestoreReservesRepositoryAsync
from src.infrastructure.services.reserves.default_reserves_service_async import DefaultReservesSeviceAsync
from src.webapi.routes.reserves_routes import reserves_router

initialize_firebase("config/firebase-credentials.json")
app = FastAPI()
app.dependency_overrides = {
    ReservesServiceAsync: DefaultReservesSeviceAsync,
    ReservesRepositoryAsync: FirestoreReservesRepositoryAsync,
    AsyncClient: get_firestore_async
}
app.include_router(reserves_router)
