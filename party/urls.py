from django.urls import path
from rest_framework import routers

from . import views

app_name = 'party'


router = routers.DefaultRouter()
router.register('parties', views.PartyViewSet)
router.register('members', views.MemberReportViewSet)

urlpatterns = router.urls