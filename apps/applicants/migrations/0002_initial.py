# Generated by Django 4.2.2 on 2024-03-22 10:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobs', '0002_initial'),
        ('userprofile', '0002_initial'),
        ('applicants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicants',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('under-reviewed', 'Under-Reviewed'), ('shortlisted', 'Shortlisted'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('on-hold', 'On-Hold'), ('applied', 'Applied')], default='applied', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False, editable=False, null=True)),
                ('is_active', models.BooleanField(default=True, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.userprofile')),
            ],
            options={
                'db_table': 'tbl_applicants',
            },
        ),
    ]
