# Generated by Django 5.2 on 2025-05-09 23:00

import accounts.models
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('company_email', models.EmailField(blank=True, max_length=60, null=True, unique=True)),
                ('company_name', models.CharField(blank=True, max_length=95, null=True, unique=True)),
                ('industry', models.CharField(blank=True, max_length=100, null=True)),
                ('job_title', models.CharField(blank=True, max_length=255, null=True)),
                ('employees', models.IntegerField(blank=True, default=None, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('company_logo', models.ImageField(blank=True, default=accounts.models.get_default_image, null=True, upload_to=accounts.models.get_image_filepath)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('can_read_contact', models.BooleanField(default=False)),
                ('can_add_contact', models.BooleanField(default=False)),
                ('can_edit_contact', models.BooleanField(default=False)),
                ('can_delete_contact', models.BooleanField(default=False)),
                ('can_permanent_delete_contact', models.BooleanField(default=False)),
                ('can_add_project', models.BooleanField(default=False)),
                ('can_read_tasks', models.BooleanField(default=False)),
                ('can_add_tasks', models.BooleanField(default=False)),
                ('can_edit_tasks', models.BooleanField(default=False)),
                ('can_delete_tasks', models.BooleanField(default=False)),
                ('can_permanent_delete_tasks', models.BooleanField(default=False)),
                ('can_read_documents', models.BooleanField(default=False)),
                ('can_add_documents', models.BooleanField(default=False)),
                ('can_edit_documents', models.BooleanField(default=False)),
                ('can_delete_documents', models.BooleanField(default=False)),
                ('can_permanent_delete_documents', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.businessuser')),
            ],
            options={
                'unique_together': {('user', 'name')},
            },
        ),
        migrations.CreateModel(
            name='AccessPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_shared', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_with', to='accounts.businessuser')),
                ('shared_with', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accessible_accounts', to='accounts.businessuser')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.role')),
            ],
            options={
                'unique_together': {('owner', 'shared_with')},
            },
        ),
    ]
