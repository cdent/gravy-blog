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

User information comes from Google's authentication provider.

URLS include:

* /
    * list of available blogs
* /{blog_title}
    * summary of recent entries
* /{blog_title}/{entry_title}
    * full display of this
* /editor
    * On GET retrieves an editor, on POST saves an entry.

Future Possibilities
====================

Many.

* Revisions available in edit view.
* Monthly or other time-scoped views.
* Tag views.
* Search.
* Themes, wherein a blog editor can replace the template used for
  the blog with something of their own design.
