from rest_framework import serializers
from api.models import Repository


class RepositorySerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    collaborators = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Repository
        fields = ["owner", "repo_name", "description", "collaborators", "public"]
