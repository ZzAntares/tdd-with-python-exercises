from lists import views
from django.conf.urls import url
# from django.contrib import admin

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    # url(r'^admin/', admin.site.urls),
]
