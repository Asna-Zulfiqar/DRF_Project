from rest_framework import serializers
from posts.models import Post, Country , Comment


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    country_name = serializers.CharField(write_only=True, required=False)  # Input for country
    country = serializers.StringRelatedField(read_only=True)  # Display country name in GET

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'likes', 'country_name', 'country', 'created_at' ,'owner']
        read_only_fields = ['id', 'created_at',  'likes' , 'owner']


    def create(self, validated_data):
        country_name = validated_data.pop('country_name', None)
        if country_name:
            try:
                country = Country.objects.get(country_name=country_name)
                validated_data['country'] = country
            except Country.DoesNotExist:
                raise serializers.ValidationError({'country_name': f'Country "{country_name}" not found.'})
        else:
            print("No country_name provided")  # Debugging output

        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['owner'] = request.user

        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'body', 'created_at', 'user']
