# Generated by Django 3.0.5 on 2020-05-06 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='experience',
        ),
        migrations.RemoveField(
            model_name='student',
            name='internship',
        ),
        migrations.RemoveField(
            model_name='student',
            name='non_scholastic',
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('internship', models.TextField(max_length=500)),
                ('experience', models.TextField(max_length=500)),
                ('non_scholastic', models.TextField(blank=True, max_length=200)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiling.Student')),
            ],
        ),
    ]
