from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers

User = get_user_model()


current_datetime = timezone.now()


class CompletedManager(models.Manager):
    def get_queryset(self):
        return super(CompletedManager, self).get_queryset().filter(is_completed=True)


class ArchivedManager(models.Manager):
    def get_queryset(self):
        return super(ArchivedManager, self).get_queryset().filter(is_archived=True)


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todo")
    item = models.CharField(
        max_length=300, blank=False, help_text="Input your TODO here"
    )
    is_completed = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    end_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    created_at = models.DateTimeField(default=timezone.now)
    objects = models.Manager()
    completed = CompletedManager()
    archived = ArchivedManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.item[:10]}..."

    def clean(self):
        if self.start_date < current_datetime:
            raise serializers.ValidationError(
                "Error : start date cannot be before todays date"
            )
        if self.start_date > self.end_date:
            raise serializers.ValidationError(
                "Error : end date cannot be before the start date"
            )

        if self.end_date < self.start_date:
            raise serializers.ValidationError(
                "Error : end date cannot be before the start date"
            )
        if self.end_date < current_datetime:
            raise serializers.ValidationError(
                "Error : end date cannot be before the todays date"
            )

    def save(self, *args, **kwargs):
        if self.end_date < current_datetime:
            raise serializers.ValidationError(
                "Error : end date cannot be before the todays date"
            )
        if self.end_date < self.start_date:
            raise serializers.ValidationError(
                "Error : end date cannot be before the start date"
            )
        if self.start_date > self.end_date:
            raise serializers.ValidationError("start_date  must occur before end date")
        if self.start_date < current_datetime:
            raise serializers.ValidationError("start date cannot be before todays date")
        else:
            super(Todo, self).save(*args, **kwargs)
