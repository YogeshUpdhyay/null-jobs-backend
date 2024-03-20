from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.jobs.models import Applicants
from apps.applicants.serializers import ApplicantModelSerializer


class AllApplicantsOfCompany(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: ApplicantModelSerializer(many=True)}
    )
    def get(self, request):
        """List all users that belong to company"""
        applicants = Applicants.objects.filter(
            employer_id=request.user.id,
        )

        return Response(
            ApplicantModelSerializer(applicants, many=True).data, 
            status=status.HTTP_200_OK
        )
    