"""Base views for the file_exchange app."""

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView


class FileDownloadStatusView(TemplateView):
    """View for retrieving the status of a file download."""

    model = None
    template_name = "file_exchange/download_status.html"

    def get_context_data(self, **kwargs):
        """Return context for the view."""
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        context["download_instance"] = get_object_or_404(self.model, pk=pk)
        return context
