# Generated by Django 4.2.6 on 2023-10-06 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("GreenThumb", "0004_electricitybudget_employeecount_marketsegment_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company_name", models.CharField(max_length=100)),
                ("contact_info", models.CharField(max_length=100)),
                ("postal_code", models.CharField(max_length=10)),
                (
                    "employee_count",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="companies_by_employee_count",
                        to="GreenThumb.employeecount",
                    ),
                ),
            ],
        ),
    ]
