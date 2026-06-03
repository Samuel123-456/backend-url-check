from typing import List

from ninja.errors import HttpError
from ninja_extra.controllers import api_controller, route
from injector import inject

from apps.ai.outputs.check_url_output import LinkAnalysisOutput
from apps.urlcheck.schemas import (
    CheckURLRequest,
    CheckURLResponse,
    UrlAnalysisRecordResponse,
    UrlAnalysisRecordUpdate,
)
from apps.urlcheck.services import CheckURLService


@api_controller(
    prefix_or_class="/urlcheck",
    tags=["URL Check"],
)
class CheckURLController:

    @inject
    def __init__(self, check_url_service: CheckURLService):
        self.check_url_service = check_url_service

    @route.post("/check", response=CheckURLResponse)
    async def check_url(self, request, url: CheckURLRequest):
        analysis = await self.check_url_service.check_url(url.url)
        return CheckURLResponse(analysis=analysis)

    @route.get("/records", response=List[UrlAnalysisRecordResponse])
    async def list_records(self, request):
        records = await self.check_url_service.list_records()
        return [self._record_to_response(record) for record in records]

    @route.get("/records/{record_id}", response=UrlAnalysisRecordResponse)
    async def get_record(self, request, record_id: int):
        record = await self.check_url_service.get_record(record_id)
        if record is None:
            raise HttpError(404, "Registro não encontrado")
        return self._record_to_response(record)

    @route.get("/records/by-url", response=UrlAnalysisRecordResponse)
    async def get_record_by_url(self, request, url: str):
        record = await self.check_url_service.get_record_by_url(url)
        if record is None:
            raise HttpError(404, "Registro não encontrado")
        return self._record_to_response(record)

    @route.patch("/records/{record_id}", response=UrlAnalysisRecordResponse)
    async def update_record(self, request, record_id: int, payload: UrlAnalysisRecordUpdate):
        record = await self.check_url_service.update_record(
            record_id,
            url=payload.url,
            analysis=payload.analysis,
        )
        if record is None:
            raise HttpError(404, "Registro não encontrado")
        return self._record_to_response(record)

    @route.delete("/records/{record_id}")
    async def delete_record(self, request, record_id: int):
        if not await self.check_url_service.delete_record(record_id):
            raise HttpError(404, "Registro não encontrado")
        return {"detail": "Registro apagado com sucesso."}

    def _record_to_response(self, record) -> UrlAnalysisRecordResponse:
        return UrlAnalysisRecordResponse(
            id=record.id,
            url=record.url,
            analysis=LinkAnalysisOutput.model_validate(record.analysis_json),
            created_at=record.created_at,
            updated_at=record.updated_at,
        )