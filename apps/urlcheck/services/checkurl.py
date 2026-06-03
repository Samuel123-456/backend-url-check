import logging

from ninja.errors import HttpError

from apps.ai.chains import CheckURLChain
from apps.ai.outputs.check_url_output import LinkAnalysisOutput

try:
    from google.genai.errors import ServerError as GoogleServerError
except Exception:
    GoogleServerError = None

logger = logging.getLogger(__name__)


class CheckURLService:

    async def check_url(self, url: str) -> LinkAnalysisOutput:
        """Run the CheckURLChain and return the structured LinkAnalysisOutput.

        Handles model/server errors by logging and raising appropriate HTTP errors
        with friendly messages for clients.
        """
        try:
            analysis_result = await CheckURLChain.run(url)
            return analysis_result

        except Exception as exc:
            # If the Google GenAI ServerError is available and matches, treat as 503
            if GoogleServerError is not None and isinstance(exc, GoogleServerError):
                logger.warning("Model service unavailable: %s", exc)
                raise HttpError(503, "Serviço de análise temporariamente indisponível. Por favor tente novamente mais tarde.")

            # Generic error handling
            logger.exception("Unexpected error while checking URL: %s", exc)
            raise HttpError(500, "Ocorreu um erro ao processar o pedido. Por favor tente novamente mais tarde.")