from django.http import HttpResponseNotFound
from mezzanine.pages.middleware import PageMiddleware
from mezzanine.core.models import CONTENT_STATUS_DRAFT


class DraftShowPageMiddleware(PageMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        ret = super(DraftShowPageMiddleware, self).process_view(
            request, view_func, view_args, view_kwargs
        )
        user = request.user
        page = getattr(request, 'page', None)

        if not user.is_authenticated() or page is None or page.status != CONTENT_STATUS_DRAFT:
            return ret

        if not user.has_perm('mezzacore.view_drafts'):
            return HttpResponseNotFound()

        return ret
