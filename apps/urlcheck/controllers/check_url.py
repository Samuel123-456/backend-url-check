from ninja_extra.controllers import api_controller, route
from apps.urlcheck.schemas import CheckURLRequest, CheckURLResponse
from injector import inject
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
        # Implement your URL checking logic here
        analysis = await self.check_url_service.check_url(url.url)
        # Retornar um objeto compatível com o schema CheckURLResponse
        return CheckURLResponse(analysis=analysis)