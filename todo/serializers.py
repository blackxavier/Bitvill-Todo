import rest_framework
import pytz
import django
from django.utils import timezone
from rest_framework import serializers
from todo.models import Todo
from datetime import datetime


dt = timezone.now()


class PostWriteTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            "item",
            "start_date",
            "end_date",
            "is_completed",
            "is_archived",
        ]

    def validate(self, data):

        if "start_date" in data and "end_date" in data:
            if data["start_date"] < dt:
                raise serializers.ValidationError(
                    {
                        "start_date": "start date should be equal to or greater than todays date"
                    }
                )

            if data["end_date"] < dt:
                raise serializers.ValidationError(
                    {
                        "end_date": "end_date should be equal to or greater than todays date"
                    }
                )

            if data["start_date"] > data["end_date"]:
                raise serializers.ValidationError(
                    {
                        "start_date": "start date should be equal to or lesser than end date"
                    }
                )
            if data["end_date"] < data["start_date"]:
                raise serializers.ValidationError(
                    {
                        "end_date": "end_date  should be equal to or greater than start date"
                    }
                )
        return super(PostWriteTodoSerializer, self).validate(data)


class ReadTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "item", "is_completed", "is_archived"]
        read_only_fields = fields


class ReadDetailTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            "id",
            "item",
            "start_date",
            "end_date",
            "is_completed",
            "is_archived",
        ]
        read_only_fields = fields


class TodoIscompleteSerializer(serializers.Serializer):
    is_completed = serializers.BooleanField(default=False)

    def update(self, instance, validated_data):

        instance.is_completed = validated_data.get(
            "is_completed", instance.is_completed
        )

        instance.save()
        return instance


class TodoIsarchivedSerializer(serializers.Serializer):
    is_archived = serializers.BooleanField(default=False)

    def update(self, instance, validated_data):

        instance.is_archived = validated_data.get("is_archived", instance.is_archived)

        instance.save()
        return instance
