# Generated by Django 4.1.7 on 2023-03-08 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_branch_alter_student_user_alter_teacher_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='reg_no',
        ),
    ]
