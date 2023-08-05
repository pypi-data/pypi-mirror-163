# Generated by Django 4.0.4 on 2022-05-19 17:19

from django.db import migrations, models
import django.db.models.deletion
import hvad.fields


class Migration(migrations.Migration):

    dependencies = [
        ('camomilla', '0008_auto_20220309_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='_hvad_query',
            field=hvad.fields.SingleTranslationObject('camomilla.Article', 'camomilla.articletranslation'),
        ),
        migrations.AddField(
            model_name='category',
            name='_hvad_query',
            field=hvad.fields.SingleTranslationObject('camomilla.Category', 'camomilla.categorytranslation'),
        ),
        migrations.AddField(
            model_name='content',
            name='_hvad_query',
            field=hvad.fields.SingleTranslationObject('camomilla.Content', 'camomilla.contenttranslation'),
        ),
        migrations.AddField(
            model_name='media',
            name='_hvad_query',
            field=hvad.fields.SingleTranslationObject('camomilla.Media', 'camomilla.mediatranslation'),
        ),
        migrations.AddField(
            model_name='mediafolder',
            name='_hvad_query',
            field=hvad.fields.SingleTranslationObject('camomilla.MediaFolder', 'camomilla.mediafoldertranslation'),
        ),
        migrations.AddField(
            model_name='page',
            name='_hvad_query',
            field=hvad.fields.SingleTranslationObject('camomilla.Page', 'camomilla.pagetranslation'),
        ),
        migrations.AddField(
            model_name='tag',
            name='_hvad_query',
            field=hvad.fields.SingleTranslationObject('camomilla.Tag', 'camomilla.tagtranslation'),
        ),
        migrations.AlterField(
            model_name='article',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='article',
            name='og_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_related', to='camomilla.media'),
        ),
        migrations.AlterField(
            model_name='articletranslation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='articletranslation',
            name='master',
            field=hvad.fields.MasterKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='camomilla.article'),
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='categorytranslation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='categorytranslation',
            name='master',
            field=hvad.fields.MasterKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='camomilla.category'),
        ),
        migrations.AlterField(
            model_name='content',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='contenttranslation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='contenttranslation',
            name='master',
            field=hvad.fields.MasterKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='camomilla.content'),
        ),
        migrations.AlterField(
            model_name='media',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='mediafolder',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='mediafoldertranslation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='mediafoldertranslation',
            name='master',
            field=hvad.fields.MasterKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='camomilla.mediafolder'),
        ),
        migrations.AlterField(
            model_name='mediatranslation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='mediatranslation',
            name='master',
            field=hvad.fields.MasterKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='camomilla.media'),
        ),
        migrations.AlterField(
            model_name='page',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='page',
            name='og_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_related', to='camomilla.media'),
        ),
        migrations.AlterField(
            model_name='pagetranslation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='pagetranslation',
            name='master',
            field=hvad.fields.MasterKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='camomilla.page'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='tagtranslation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='tagtranslation',
            name='master',
            field=hvad.fields.MasterKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='camomilla.tag'),
        ),
    ]
