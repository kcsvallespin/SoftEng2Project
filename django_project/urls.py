
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from activitylog.views import view_logs, log_detail
from accounts.custom_signup_view import CustomSignupView
from accounts.custom_login_view import CustomLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", CustomLoginView.as_view(), name="account_login"),
    path("accounts/", include("accounts.allauth_urls")),
    path('inventory/', include('inventory.urls')),
    path('sales/', include('sales.urls')),
    path('accounts/list/', include('accounts.urls')),
    path("", include("pages.urls")),
    path('menu/', include('menu.urls')),
    path('activitylog/', view_logs, name='view_logs'),
    path('activitylog/<int:log_id>/', log_detail, name='log_detail'),
]

from django.conf.urls.static import static

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        path('inventory/', include('inventory.urls')),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
