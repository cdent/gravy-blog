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


class TagsField(forms.CharField):

    def to_python(self, value):
        """
        Turn a comma separate list into a list.
        """
        if not value:
            return []
        else:
            return [item.strip() for item in value.split(',')]

    def validate(self, value):
        return True


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
    tags = TagsField(label='Tags', required=False, max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    entry = forms.CharField(widget=forms.HiddenInput, required=False)
    blog = forms.CharField(widget=forms.HiddenInput, required=True)
