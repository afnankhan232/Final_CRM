# Generated by Django 5.2 on 2025-05-04 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_role_can_add_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='can_add_documents',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='can_add_project',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='can_add_tasks',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='can_delete_documents',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='can_delete_project',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='can_delete_tasks',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='can_edit_documents',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='can_edit_project',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='can_edit_tasks',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='can_permanent_delete_documents',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='can_permanent_delete_project',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='can_permanent_delete_tasks',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='can_read_documents',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='can_read_project',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='can_read_tasks',
            field=models.BooleanField(default=False),
        ),
    ]
