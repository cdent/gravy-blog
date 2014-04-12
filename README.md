What
====

Gravy Blog is a Django app for running on AppEngine. Gravy because
that's what goes on potatoes to make them tasty.

Python 2.7 as that's what Google provides

How
===

This code uses the [djappengine
code](https://github.com/potatolondon/djappengine) as a guide but
builds from scratch including things from that repo as or if required.

It appears some of the information in that repo is based on an older
version of the SDK.

Structure
=========

As the request was for something simple this tool makes no attempt
to keep revisions of blog entries. This simplifies the schema.

The entities are:

* blog
    * title
    * list of editors
* entry
    * title
    * most recent editor name
    * created date
    * modified date
    * list of tags
    * content

User information comes from Google's authentication provider.

URLS include:

* /
    * list of available blogs
* /{blog_title}
    * summary of recent entries
* /{blog_title}/{entry_title}
    * full display of this
* /editor
    * On GET retrieves an editor, on POST saves or deletes an entry.
* /creator
    * ON GET provides a form to create a new blog, on POST creates
      it.

Mistakes and Nastiness
======================

* Naming the repo `gravy-blog` conflicts with some of the package
  discovery magic that is going on. To get around it, clone the
  repo into a directory named `gravy`.
* It might have been a mistake to not use something like
  [Bootstrap](http://getbootstrap.com/) to handle CSS and ensuring
  goog typography. However I was more interested, in this case, in
  exploring the raw CSS.

Testing
=======

[py.test](http://pytest.org/latest/) is used to drive tests in the
`tests` directory. It and additional testing requirements are in
`test-requirements.txt`.

A `Makefile` is provided with a `test` target.

The tests are incomplete. There were used to establish and confirm
the initial models, the testing environment, and the basic views.
Once the templates were working properly testing slacked off a fair
bit as the style of exploration was a bit too random to be driven
by tests. In a more specified or planned exercise I prefer to be as
TDD as possible.

Running
=======

In `lib/__init__.py` is a hardcoded path to the appengine sdk, as
`SDK_PATH`. If you are not using OS X this will need to be updated
to path to the sdk.

A `serve.sh` is present. This will start up `old_devappserver.py`,
the app will then be available at `http://localhost:8080/`.

The deployed version is on appspot at
<http://gravy-blog.appspot.com/>.

In either setting, if you are logged in you can create a new blog
and then add entries to it. Existing entries can be edited or
deleted.

Todo
====

Things I have not yet done but would like to do before considering
this "done" in some way:

* Improve CSS:
    * the forms have none
    * the summary page needs to be more clearly so
    * each entry needs to present itself well, e.g. tags inlined
* Engaged `timeago`: The date information is there, just need the
  markup in the templates.
* There's currently no session handling which makes it difficult to
  do any flexible messaging between requests.
* See about the possiblity of a `showdown.js` driven preview of
  content.
* Limit length of content on summary page and/or change summary
  article count.

Future Possibilities
====================

Many.

* Explore django ModelForm to see if there is fit.
* Revisions available in edit view.
* Monthly archives or other time-scoped views.
* Tag views.
* Search.
* Blog Atom feeds.
* Themes, wherein a blog editor can replace the template used for
  the blog with something of their own design.
* Use a template context processor for handling Google user data passed to
  templates and use other ones as well.
* Take advantage of the fact that a blog can have multiple editors.
* CSS refactoring to make more DRY. SASS would probably be useful.
