from django.db import migrations, models
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_delete_skill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cv_file',
            field=models.FileField(blank=True, null=True, storage=profiles.models.cv_storage, upload_to='cv/'),
        ),
    ]
