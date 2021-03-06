# Generated by Django 3.0.8 on 2020-07-27 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import memory_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recto', models.CharField(max_length=200, verbose_name='recto')),
                ('verso', models.CharField(max_length=200, verbose_name='verso')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.SlugField(max_length=200, verbose_name='slug')),
            ],
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('color', models.CharField(blank=True, default='#ffc728', max_length=7, null=True, verbose_name='color')),
                ('color_text', models.CharField(blank=True, default='#000000', max_length=7, null=True, verbose_name='color_text')),
                ('private', models.BooleanField(default=False, verbose_name='private')),
                ('favorite', models.BooleanField(default=False, verbose_name='favorite')),
                ('cards', models.ManyToManyField(to='memory_app.Cards')),
                ('category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='memory_app.Category')),
            ],
        ),
        migrations.CreateModel(
            name='DeckImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('image', models.ImageField(upload_to='media/')),
            ],
        ),
        migrations.CreateModel(
            name='QuickDeck',
            fields=[
                ('deck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='memory_app.Deck')),
                ('rank', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)], default=1, verbose_name='rank')),
            ],
            bases=('memory_app.deck',),
        ),
        migrations.AddField(
            model_name='deck',
            name='image',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='memory_app.DeckImage'),
        ),
        migrations.AddField(
            model_name='deck',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CardsState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('rank', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)], default=1, verbose_name='rank')),
                ('side', models.BooleanField(verbose_name='side')),
                ('new', models.BooleanField(default=True, verbose_name='new')),
                ('cards', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='memory_app.Cards')),
                ('deck', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='memory_app.Deck')),
            ],
        ),
    ]
