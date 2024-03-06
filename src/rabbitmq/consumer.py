import os

import aiormq
from aiormq.abc import DeliveredMessage
from fastapi import Depends

from src.application.tourist_packages.dtos.tourist_packages_response_dto import TouristPackagesResponseDto
from src.application.tourist_packages.services.tourist_packages_service_async import TouristPackagesServiceAsync

TOURIST_PACKAGE_QUEUE = 'tourist_packages'


class Consumer:
    def __init__(self, tourist_packages_service: TouristPackagesServiceAsync):
        self._tourist_packages_service = tourist_packages_service

    async def on_message(self, message: DeliveredMessage):
        action, package_ref_id = message.body.decode().split("::")

        if action == "CREATE":
            await self._tourist_packages_service.add_package(tourist_package=TouristPackagesResponseDto(id="", ref_id=package_ref_id))
        elif action == "DELETE":
            await self._tourist_packages_service.delete_package(ref_id=package_ref_id)

    async def consume(self):
        connection = await aiormq.connect(os.getenv("AMQP_URL", "amqp://guest:guest@localhost/"))
        channel = await connection.channel()
        declare_ok = await channel.queue_declare(TOURIST_PACKAGE_QUEUE)
        consume_ok = await channel.basic_consume(
            declare_ok.queue, self.on_message, no_ack=True
        )
