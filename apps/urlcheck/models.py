from django.db import models


class UrlAnalysisRecord(models.Model):
    url = models.URLField(max_length=2048, unique=True)
    analysis_json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Url Analysis Record"
        verbose_name_plural = "Url Analysis Records"
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return self.url
