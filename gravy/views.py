"""
The primary views for our blog.
"""

from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_safe
from django.utils.http import urlunquote

from .models import Blog, Entry


SUMMARY_LIMIT = 10


@require_safe
def home(request):
    blogs = Blog.query().order(Blog.title).fetch()
    return render(request, 'home.html', {'blogs': blogs})


@require_safe
def summary(request, blog_title):
    blog_title = urlunquote(blog_title)
    blog = Blog.get_one(blog_title)
    if blog is None:
        raise Http404
    entries = Entry.get_some(blog.key, limit=SUMMARY_LIMIT)
    return render(request, 'summary.html', {
        'blog': blog,
        'entries': entries
    })


@require_safe
def entry(request, blog_title, entry_title):
    blog_title = urlunquote(blog_title)
    entry_title = urlunquote(entry_title)
    blog = Blog.get_one(blog_title)
    if blog is None:
        raise Http404

    entry = Entry.get_one(blog.key, entry_title)
    if entry is None:
        raise Http404

    return render(request, 'entry.html', {
        'blog': blog,
        'entry': entry
    })
