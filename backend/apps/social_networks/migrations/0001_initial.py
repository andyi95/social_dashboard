# Generated by Django 4.2.4 on 2023-09-14 13:46

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
            name="Account",
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
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("VK", "Vk"),
                            ("TG", "Telegram"),
                            ("IG", "Instagram"),
                            ("FB", "Facebook"),
                        ],
                        default="VK",
                        max_length=32,
                    ),
                ),
                ("username", models.CharField(blank=True, default="", max_length=255)),
                ("link", models.CharField(blank=True, default="", max_length=512)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="accounts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "social network",
                "verbose_name_plural": "social networks",
            },
        ),
        migrations.CreateModel(
            name="TrackingGroup",
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
                ("group_id", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("last_updated", models.DateTimeField(default=None, null=True)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="social_networks.account",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Token",
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
                (
                    "token",
                    models.CharField(
                        max_length=255, verbose_name="social media access token"
                    ),
                ),
                (
                    "expires_at",
                    models.DateTimeField(
                        default=None, null=True, verbose_name="expires at"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("ACC", "Access"), ("REF", "Refresh")],
                        default="ACC",
                        max_length=16,
                    ),
                ),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tokens",
                        to="social_networks.account",
                    ),
                ),
            ],
            options={
                "verbose_name": "Access token",
                "verbose_name_plural": "Access tokens",
            },
        ),
    ]
