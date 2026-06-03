
from django.contrib import admin
from django.urls import path
from apps.urlcheck.controllers import CheckURLController
from ninja_extra import NinjaExtraAPI

app = NinjaExtraAPI()
app.register_controllers(CheckURLController)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', app.urls),
]
