"""
The primary views for our blog.
"""

from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_safe

from .models import Blog, Entry


@require_safe
def home(request):
    blogs = Blog.query().fetch()
    return render(request, 'home.html', {'blogs': blogs})


@require_safe
def summary(request, blog_title):
    blog = Blog.query(Blog.title == blog_title).get()
    if blog is None:
        raise Http404
    entries = Entry.query(Entry.blog == blog.key).order(-Entry.created).fetch()
    return render(request, 'summary.html', {
        'blog': blog,
        'entries': entries
    })


@require_safe
def entry(request, blog_title, entry_title):
    return render(request, 'entry.html')
