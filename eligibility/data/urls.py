from django.contrib import admin
from django.urls import path, include
from eligibility import views  # ✅ Import views from your app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing_page'),  # ✅ Show landing page on root /
    path('eligibility/', include('eligibility.urls')),   # Existing routes
]
