# from rest_framework import serializers
# from ..models import UserReq, LANGUAGE_CHOICES, STYLE_CHOICES
#
#
# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     # title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     # code = serializers.CharField(style={'base_template': 'textarea.html'})
#     # linenos = serializers.BooleanField(required=False)
#     # language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     # style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#
#
#     status = serializers.CharField(max_length=500)
#     action = serializers.CharField(max_length=500)
#     duration = serializers.CharField(max_length=500)
#     startTime = serializers.CharField(max_length=500)
#     stopTime = serializers.CharField(max_length=500)
