from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/onlinecourse/")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("onlinecourse/", include("onlinecourse.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
