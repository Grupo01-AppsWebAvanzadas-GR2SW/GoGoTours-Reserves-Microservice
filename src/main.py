import asyncio

from fastapi import FastAPI, Depends

from google.cloud.firestore import AsyncClient

from src.application.reserves.repositories.reserve_repository_async import ReservesRepositoryAsync
from src.application.reserves.services.reserve_service_async import ReservesServiceAsync
from src.application.tourist_packages.repositories.tourist_packages_repository_async import \
    TouristPackagesRepositoryAsync
from src.application.tourist_packages.services.tourist_packages_service_async import TouristPackagesServiceAsync
from src.infrastructure.firebase.config.config import initialize_firebase, get_firestore_async
from src.infrastructure.firebase.reserves.repositories.firestore_reserves_repository_async import \
    FirestoreReservesRepositoryAsync
from src.infrastructure.firebase.tourist_packages.repositories.firestore_tourist_packages_repository_async import \
    FirestoreTouristPackagesRepositoryAsync
from src.infrastructure.services.reserves.default_reserves_service_async import DefaultReservesSeviceAsync
from src.infrastructure.services.tourist_packages.default_tourist_packages_service_async import \
    DefaultTouristPackagesServiceAsync
from src.rabbitmq.consumer import Consumer
from src.webapi.routes.reserves_routes import reserves_router

initialize_firebase("config/firebase-credentials.json")
app = FastAPI()
app.dependency_overrides = {
    TouristPackagesRepositoryAsync: FirestoreTouristPackagesRepositoryAsync,
    TouristPackagesServiceAsync: DefaultTouristPackagesServiceAsync,
    ReservesServiceAsync: DefaultReservesSeviceAsync,
    ReservesRepositoryAsync: FirestoreReservesRepositoryAsync,
    AsyncClient: get_firestore_async
}
app.include_router(reserves_router)


@app.on_event("startup")
def startup():
    async_client = app.dependency_overrides[AsyncClient]()
    tourist_packages_repository: TouristPackagesRepositoryAsync = app.dependency_overrides[
        TouristPackagesRepositoryAsync
    ](async_client)
    tourist_packages_service: TouristPackagesServiceAsync = app.dependency_overrides[
        TouristPackagesServiceAsync
    ](tourist_packages_repository)
    consumer = Consumer(tourist_packages_service=tourist_packages_service)
    asyncio.create_task(consumer.consume())
