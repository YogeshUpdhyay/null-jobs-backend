from rest_framework import routers
from django.urls import include, path


from apps.applicants.views import AllApplicantsOfCompany

urlpatterns = [
    path("applicants/", AllApplicantsOfCompany.as_view(), name="applicants")
]
