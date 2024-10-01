

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_contactmessage_options_alter_smslog_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seo',
            name='meta_title',
            field=models.TextField(help_text='حداکثر 160 کاراکتر', null=True, validators=[django.core.validators.MaxLengthValidator(160)], verbose_name='meta title (SEO)'),
        ),
    ]
