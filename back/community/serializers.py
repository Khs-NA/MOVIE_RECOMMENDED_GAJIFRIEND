from rest_framework import serializers
from .models import Article, Comment
from rest_framework import serializers




class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'create_user')


class ArticleSerializer(serializers.ModelSerializer):

    class CommentSerializer(serializers.ModelSerializer):

        class Meta:
            model = Comment
            fields = '__all__'
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user','create_user')
        
        
class CommentSerializer(serializers.ModelSerializer):
    article = ArticleListSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user','create_user')
