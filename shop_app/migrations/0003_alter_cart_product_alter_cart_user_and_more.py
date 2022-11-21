# Generated by Django 4.1.3 on 2022-11-20 06:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop_app', '0002_user_alter_cart_user_alter_customer_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='shop_app.product'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='customer',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='shop_app.customer'),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='user',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]