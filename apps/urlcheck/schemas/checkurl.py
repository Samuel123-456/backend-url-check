from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl

from apps.ai.outputs.check_url_output import LinkAnalysisOutput


class CheckURLRequest(BaseModel):
    url: HttpUrl


class CheckURLResponse(BaseModel):
    analysis: LinkAnalysisOutput


class UrlAnalysisRecordResponse(BaseModel):
    id: int
    url: HttpUrl
    analysis: LinkAnalysisOutput
    created_at: datetime
    updated_at: datetime


class UrlAnalysisRecordUpdate(BaseModel):
    url: Optional[HttpUrl] = None
    analysis: Optional[LinkAnalysisOutput] = None