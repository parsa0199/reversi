from .models import ArticleComment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ['body', 'email']  # فیلدهای مورد نیاز برای نمایش در فرم