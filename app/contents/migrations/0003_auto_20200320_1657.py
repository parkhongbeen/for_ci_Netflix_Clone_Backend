# Generated by Django 2.2.11 on 2020-03-20 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0002_auto_20200320_1605'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Actor',
        ),
        migrations.RemoveField(
            model_name='category',
            name='sub_categories',
        ),
        migrations.DeleteModel(
            name='Director',
        ),
        migrations.RemoveField(
            model_name='content',
            name='categories',
        ),
        migrations.AddField(
            model_name='content',
            name='is_movie',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='content',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='contents.Content', verbose_name='카테고리'),
        ),
        migrations.AddField(
            model_name='video',
            name='content',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video', to='contents.Content', verbose_name='컨텐츠'),
        ),
        migrations.AlterField(
            model_name='content',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='video',
            name='episode',
            field=models.CharField(max_length=150),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
