"""
The primary views for our blog.
"""

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe, require_http_methods
from django.utils.http import urlunquote


from google.appengine.api import users

from .models import Blog, Entry
from .forms import Create, Edit


SUMMARY_LIMIT = 10


@require_safe
def home(request):
    user = users.get_current_user()
    logout_url = users.create_logout_url('/')
    login_url = users.create_login_url('/')
    blogs = Blog.query().order(Blog.title).fetch()
    myblogs = Blog.query(Blog.editors.IN([user])).order(Blog.title).fetch()
    return render(request, 'home.html', {
        'blogs': blogs,
        'user': user,
        'logout_url': logout_url,
        'login_url': login_url,
        'myblogs': myblogs,
    })


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

@require_http_methods(['POST', 'GET', 'HEAD'])
def creator(request):
    user = users.get_current_user()

    if user is None:
        raise PermissionDenied

    if request.method == 'POST':
        return create_blog(request, user)
    else:
        form = Create()
        logout_url = users.create_logout_url('/')
        login_url = users.create_login_url('/')
        return render(request, 'creator.html', {
            'form': form,
            'user': user,
            'logout_url': logout_url,
            'login_url': login_url,
        })

def create_blog(request, user):
    form = Create(request.POST)
    if form.is_valid():
        title = form.cleaned_data['title']
        blog = Blog(title=title, editors=[user])
        blog.put()
        return redirect(blog)
    else:
        logout_url = users.create_logout_url('/')
        login_url = users.create_login_url('/')
        return render(request, 'creator.html', {
            'form': form,
            'user': user,
            'logout_url': logout_url,
            'login_url': login_url,
        })

