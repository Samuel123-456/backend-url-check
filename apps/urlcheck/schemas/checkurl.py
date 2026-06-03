from pydantic import BaseModel, HttpUrl

from apps.ai.outputs.check_url_output import LinkAnalysisOutput


class CheckURLRequest(BaseModel):
    url: HttpUrl


class CheckURLResponse(BaseModel):
    analysis: LinkAnalysisOutput