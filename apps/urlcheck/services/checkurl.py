import logging
from typing import List, Optional

from asgiref.sync import sync_to_async
from ninja.errors import HttpError

from apps.ai.chains import CheckURLChain
from apps.ai.outputs.check_url_output import LinkAnalysisOutput
from apps.urlcheck.models import UrlAnalysisRecord

try:
    from google.genai.errors import ServerError as GoogleServerError
except Exception:
    GoogleServerError = None

logger = logging.getLogger(__name__)


class CheckURLService:

    async def check_url(self, url: str) -> LinkAnalysisOutput:
        existing_record = await self.get_record_by_url(url)
        if existing_record is not None:
            logger.info("Returning cached analysis for URL: %s", url)
            return LinkAnalysisOutput.model_validate(existing_record.analysis_json)

        try:
            analysis_result = await CheckURLChain.run(url)
            await self._save_analysis_record(url, analysis_result.model_dump())
            return analysis_result

        except Exception as exc:
            if GoogleServerError is not None and isinstance(exc, GoogleServerError):
                logger.warning("Model service unavailable: %s", exc)
                raise HttpError(503, "Serviço de análise temporariamente indisponível. Por favor tente novamente mais tarde.")

            logger.exception("Unexpected error while checking URL: %s", exc)
            raise HttpError(500, "Ocorreu um erro ao processar o pedido. Por favor tente novamente mais tarde.")

    async def list_records(self) -> List[UrlAnalysisRecord]:
        return await sync_to_async(list)(UrlAnalysisRecord.objects.all())

    async def get_record(self, record_id: int) -> Optional[UrlAnalysisRecord]:
        return await sync_to_async(lambda: UrlAnalysisRecord.objects.filter(id=record_id).first())()

    async def get_record_by_url(self, url: str) -> Optional[UrlAnalysisRecord]:
        return await sync_to_async(lambda: UrlAnalysisRecord.objects.filter(url__iexact=url).first())()

    async def delete_record(self, record_id: int) -> bool:
        record = await self.get_record(record_id)
        if record is None:
            return False
        await sync_to_async(record.delete)()
        return True

    async def update_record(
        self,
        record_id: int,
        url: Optional[str] = None,
        analysis: Optional[LinkAnalysisOutput] = None,
    ) -> Optional[UrlAnalysisRecord]:
        record = await self.get_record(record_id)
        if record is None:
            return None
        if url:
            record.url = url
        if analysis is not None:
            record.analysis_json = analysis.model_dump()
        await sync_to_async(record.save)()
        return record

    async def _save_analysis_record(self, url: str, analysis_data: dict) -> UrlAnalysisRecord:
        return await sync_to_async(UrlAnalysisRecord.objects.create)(url=url, analysis_json=analysis_data)
