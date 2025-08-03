from rest_framework import serializers

class RecommendSerializer(serializers.Serializer):
    course_name = serializers.CharField()
    top_n = serializers.IntegerField(default=5, min_value=1, max_value =10)