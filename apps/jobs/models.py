import uuid

from django.db import models

from apps.accounts.models import User as UserAuth
from apps.jobs.constants import values
from apps.jobs.constants.values import GENDER, HIRING_STATUS, JOB_TYPE, STATUS_CHOICES


class Company(models.Model):
    """
    Represents a company with related details.

    This class defines the attributes associated with a company, and
    belongs to the company table in the database
    """

    class Meta:
        db_table = values.DB_TABLE_COMPANY

    name = models.CharField(max_length=255, null=False)
    location = models.CharField(max_length=255, null=False)
    about = models.TextField(max_length=500, default=False, null=False)
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    is_deleted = models.BooleanField(default=False, null=True, editable=False)
    team_members = models.PositiveIntegerField(default=False, null=True)
    social_profiles = models.URLField(default=None, null=True)
    founded_year = models.PositiveIntegerField(default=False, null=False)
    creator = models.OneToOneField(UserAuth, on_delete=models.CASCADE, editable=False)


class Job(models.Model):
    """
    Represents a job posting with related details.

    This class defines the attributes associated with a job posting,
    This class has one foreign field, rest are the normal fields.
    """

    class Meta:
        db_table = values.DB_TABLE_JOBS

    job_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, 
        editable=False, null=False
    )
    job_role = models.CharField(max_length=100, null=False)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, 
        related_name="company", null=False
    )
    location = models.CharField(max_length=100, default=None)
    experience = models.IntegerField(default=0, null=False)
    employer_id = models.UUIDField(null=False, editable=True, default=None)
    job_type = models.CharField(max_length=80, choices=JOB_TYPE, null=False)
    vacancy_position = models.IntegerField(default=None, null=False)
    industry = models.CharField(max_length=50, default=None, null=False)
    category = models.CharField(max_length=20, default=None, null=True)

    # creation and updation dates
    created_at = models.DateTimeField(auto_now_add=True)  # only add the timestamp once
    updated_at = models.DateTimeField(auto_now=True)  # update timestamp on every save()

    # flags are un explained here
    is_active  = models.BooleanField(default=False, null=False, editable=False)
    is_created = models.BooleanField(default=False, null=True,  editable=False)
    is_deleted = models.BooleanField(default=False, null=True,  editable=False)

    # These fields will be displayed as a part of "description" field and the
    # body of the job
    job_responsibilities = models.TextField(
        default="No Job Responsibilities provided", max_length=1000
    )
    skills_required = models.TextField(
        default="No skills details provided", max_length=1000
    )
    education_or_certifications = models.TextField(
        default="No Education details provided", max_length=1000
    )
    about = models.TextField(default="No description provided", max_length=500)



class User(models.Model):
    """
    Represents a user profile with related details.

    This class defines the attributes associated with a user profile.
    This class has two foreign keys that point to Job and Company table
    """

    def media_upload_path(instance, filename):
        return f"user_{instance.user_id}/data/{filename}"

    class Meta:
        db_table = values.DB_TABLE_USER_PROFILE

    user_id = models.UUIDField(
        primary_key=True, default=None, 
        editable=False, null=False
    )
    name = models.CharField(max_length=30, null=False)
    address = models.TextField(max_length=100, null=True, default=None)
    about = models.TextField(max_length=100, default=None, null=True)
    resume = models.FileField(upload_to=media_upload_path, null=True, default=None)
    profile_picture = models.FileField(upload_to=media_upload_path, null=True, default=None)
    cover_letter = models.FileField(upload_to=media_upload_path, null=True)
    user_type = models.CharField(max_length=15, default=None, null=False, editable=False)
    experience = models.CharField(default=0, null=True, max_length=3)
    gender = models.CharField(choices=GENDER, max_length=6, default=None, null=True)
    age = models.PositiveIntegerField(default=None, null=True)
    education = models.JSONField(default=dict, null=False)
    professional_skills = models.JSONField(default=dict, null=False)
    hiring_status = models.CharField(
        max_length=15, choices=HIRING_STATUS, 
        default="Not Applied Yet", null=True
    )
    profession = models.TextField(max_length=100, default=None, null=True)
    work_experience = models.JSONField(default=dict, null=False)

    # These fields will be displayed as a part of "Contact" field
    email = models.CharField(max_length=30, null=False)
    phone = models.CharField(max_length=12, default=None, null=True)
    website = models.URLField(default=None, null=True)
    social_handles = models.URLField(default=None, null=True)

    # below fields are only for user_type Employer
    company_id = models.ForeignKey(Company, default=None, null=True, on_delete=models.CASCADE)


    def custom_save(self, override_uuid={}, *args, **kwargs):
        if self.resume:
            self.resume_file_path = self.resume.path
        else:
            self.resume_file_path = ""

        if override_uuid and values.USER_ID in override_uuid:
            self.user_id = override_uuid[values.USER_ID]

        super(User, self).save(*args, **kwargs)


class Applicants(models.Model):
    """Represents apply job model.
    Currently not assigning job_id as the primary key
    """

    class Meta:
        db_table = "tbl_applicants"

    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="applied")
    created_at = models.DateTimeField(auto_now_add=True)
    resume = models.FileField(upload_to="resume/", null=True, blank=True)
    cover_letter = models.FileField(upload_to="cover_letters/", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, null=True, editable=False)
    is_active = models.BooleanField(default=True, null=True)
    employer_id = models.UUIDField(null=False, editable=False, default=None)


class ContactMessage(models.Model):
    """Represents contact_us model.
    defines the attributes of the contact_us page feilds.
    """

    class Meta:
        db_table = "tbl_contact_us"

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class FavoriteProfiles(models.Model):
    """
    This model represents list of favorite profiles
    belong to specific employer
    """

    class Meta:
        db_table = "tbl_favorite_profiles"

    employer = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    favorite_profile = models.UUIDField(null=False, editable=False, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
