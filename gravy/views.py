"""
The primary views for our blog.
"""

import logging

# XXX: We don't want to see this in views, just models.
from google.appengine.ext import ndb

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe, require_http_methods
from django.utils.http import urlunquote


from google.appengine.api import users


from .models import Blog, Entry
from .forms import Create, Edit


SUMMARY_LIMIT = 10
LOGGER = logging.getLogger(__name__)


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
    user = users.get_current_user()

    blog_title = urlunquote(blog_title)
    blog = Blog.get_one(blog_title)
    if blog is None:
        raise Http404

    url = blog.get_absolute_url()
    logout_url = users.create_logout_url(url)
    login_url = users.create_login_url(url)

    entries = Entry.get_some(blog.key, limit=SUMMARY_LIMIT)
    return render(request, 'summary.html', {
        'user': user,
        'logout_url': logout_url,
        'login_url': login_url,
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

    user = users.get_current_user()
    url = entry.get_absolute_url()
    logout_url = users.create_logout_url(url)
    login_url = users.create_login_url(url)

    edit = user in blog.editors

    return render(request, 'entry.html', {
        'edit': edit,
        'user': user,
        'logout_url': logout_url,
        'login_url': login_url,
        'blog': blog,
        'entry': entry
    })


@require_http_methods(['POST', 'GET', 'HEAD'])
def editor(request):
    user = users.get_current_user()

    if user is None:
        raise PermissionDenied

    if request.method == 'POST':
        return edit_entry(request, user)
    else:
        # Set up the form for editing.
        entry_key = request.GET.get('entry')
        blog_key = request.GET.get('blog')
        if entry_key:
            entry = Entry.get_by_id(long(entry_key))
            if entry is None:
                raise Http404

            blog = entry.blog.get()

            data = {
                'entry': entry_key,
                'title': entry.title,
                'content': entry.content,
                'tags': ', '.join(entry.tags)
            }
        elif blog_key:
            data = {
                'blog': blog_key,
            }
            blog = Blog.get_by_id(long(blog_key))
        else:
            # No blog or entry selected
            # XXX: This could be much more friendly
            raise Http404

        if user not in blog.editors:
            raise PermissionDenied

        form = Edit(initial=data)
        logout_url = users.create_logout_url('/')
        login_url = users.create_login_url('/')
        return render(request, 'editor.html', {
            'form': form,
            'user': user,
            'logout_url': logout_url,
            'login_url': login_url,
        })


def edit_entry(request, user):
    """
    Edit or delete a single blog entry.
    """

    # If we've been asked to delete handled that.
    delete = request.POST.get('delete')
    if delete:
        entry = Entry.get_by_id(long(request.POST.get('entry')))
        blog = entry.blog.get()
        if user not in blog.editors:
            raise PermissionDenied

        entry.key.delete()
        return redirect(blog)

    # Otherwise treat this POST as an edit form 
    form = Edit(request.POST)
    if form.is_valid():
        blog = form.cleaned_data['blog']

        if user not in Blog.get_by_id(long(blog)).editors:
            raise PermissionDenied

        title = form.cleaned_data['title']
        tags = form.cleaned_data['tags']
        content = form.cleaned_data['content']
        entry_key = form.cleaned_data['entry']
        if entry_key:
            entry = Entry.get_by_id(long(entry_key))
        else:
            entry = Entry(title=form.cleaned_data['title'],
                    blog=ndb.Key('Blog', long(blog)))
        entry.title = title
        entry.tags = tags
        entry.content = content
        entry.editor = user
        entry.put()
        return redirect(entry)
    else:
        logout_url = users.create_logout_url('/')
        login_url = users.create_login_url('/')
        return render(request, 'editor.html', {
            'form': form,
            'user': user,
            'logout_url': logout_url,
            'login_url': login_url,
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

