"""Base views for the file_exchange app."""

from typing import Any, Dict, Optional

from django.views.generic import TemplateView

from file_exchange import models


class DownloadFileView(TemplateView):
    """View for displaying file download status."""

    model = None
    template_name = "file_exchange/download_status.html"
    status_url = ""
    create_file_url = ""

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Return context for the view."""
        context = super().get_context_data(**kwargs)
        context["status_url"] = self.status_url
        context["create_file_url"] = self.create_file_url
        return context


class FileDownloadStatusView(TemplateView):
    """View for retrieving the status of a file download."""

    model: Optional[models.FileDownload] = None
    template_name = "file_exchange/download_status_display.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Return context for the view."""
        if self.model is None:
            raise ValueError("The views model attribute must be set.")
        context = super().get_context_data(**kwargs)
        try:
            context["download_instance"] = self.model.objects.latest("created_at")
        except self.model.DoesNotExist:
            context["download_instance"] = None
        return context
