"""
Forms used in various places.
"""

from django import forms
from django.core.exceptions import ValidationError

from .models import Blog

class BlogTitleField(forms.CharField):

    def validate(self, value):
        """
        Check that value is not already used.

        There are probably myriad ways to do this, this way seemed
        interesting.
        """
        super(BlogTitleField, self).validate(value)

        # We are only valid if the blog doesn't already exist
        blog = Blog.get_one(value)
        if blog is not None:
            raise ValidationError('Blog exists')


class Create(forms.Form):
    """
    A form for creating a blog.
    """
    title = BlogTitleField(label='Blog Title',
            required=True,
            max_length=100)


class Edit(forms.Form):
    """
    A form for creating or editing a blog entry.
    """
    title = forms.CharField(label='Entry Title', required=True, max_length=100)
    tags = forms.CharField(label='Tags', max_length=100)
    content = forms.CharField(widget=forms.Textarea)
