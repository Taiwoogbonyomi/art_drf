# Generated by Django 4.2 on 2025-01-21 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True, default='No content provided.')),
                ('image', models.ImageField(blank=True, default='../default_post_tx8nvq', upload_to='images/')),
                ('image_filter', models.CharField(choices=[('oil_painting', 'Oil Painting'), ('acrylic', 'Acrylic'), ('watercolor', 'Watercolor'), ('impressionist', 'Impressionist'), ('abstract_art', 'Abstract Art'), ('pencil_sketch', 'Pencil Sketch'), ('cubism', 'Cubism'), ('pop_art', 'Pop Art'), ('surrealism', 'Surrealism'), ('expressionism', 'Expressionism'), ('ink_wash', 'Ink Wash')], default='oil_painting', max_length=32)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['-created_at'],
            },
        ),
    ]