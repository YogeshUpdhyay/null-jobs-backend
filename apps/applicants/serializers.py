from rest_framework import serializers

from apps.jobs.models import Applicants


class ApplicantModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicants
        fields = ['id', 'job', 'user', 'status', 'created_at', 'resume', 'cover_letter', 'updated_at', 'is_deleted', 'is_active', 'employer_id']
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_deleted', 'employer_id']  # Fields that should not be editable
