from django.conf.urls import url
from . import views
urlpatterns=[
    # url(r'sms_codes/(?P<mobile>1[3-9]\d{9})/^s',views.SMScodeview.as_view())
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$',views.SMScodeview.as_view())
    # url(r'sms_codes/18810349527/^s',views.SMScodeview.as_view())
]