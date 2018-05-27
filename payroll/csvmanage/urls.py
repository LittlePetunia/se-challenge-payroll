from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^upload_csv/(?P<report_id>\d+)$', views.upload_csv),
    url(r'^get_current_report/$', views.get_current_report),
]