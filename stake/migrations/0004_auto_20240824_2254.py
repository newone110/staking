from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('stake', '0003_alter_stake_id'),  # Replace with your previous migration
    ]

    operations = [
        migrations.RemoveField(
            model_name='stake',
            name='id',
        ),
        migrations.AddField(
            model_name='stake',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]