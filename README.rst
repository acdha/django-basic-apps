=================
Django Basic Apps
=================

Simple apps for Django projects.

To install any of the apps listed simply create a folder on your ``PYTHONPATH`` named 'basic' and place the apps you wish to use in that folder. Then added ``basic.<app_name>`` to your project's ``settings.py`` file. (replace <app_name> with the apps you wish to use, naturally).

Below are a list of per app dependancies:

Dependancies
============

* Basic Inlines are required to use the Blog app
* Django Comments (http://www.djangoproject.com/documentation/add_ons/#comments) are required for the blog app
* Django-Markup (http://github.com/bartTC/django-markup/tree/master) for the blog app
* Django-Sugar (http://github.com/montylounge/django-sugar/tree/master) for the blog app
* Django Tagging (http://code.google.com/p/django-tagging)
* Markdown (http://www.djangoproject.com/documentation/add_ons/#markup)
* BeautifulSoup (http://www.crummy.com/software/BeautifulSoup/) is required to use the blog and, subsequently, the inlines app.
* Django-Tinymce (http://code.google.com/p/django-tinymce/) for TinyMCE support.
* Django-Twitter (http://github.com/skevy/django-twitter/) for Twitter support.
* Django-Bitly (http://bitbucket.org/discovery/django-bitly/) for Bitly support.

Inlines
=======

Inlines is a template filter that can be used in
conjunction with inline markup to insert content objects
into other pieces of content. An example would be inserting
a photo into a blog post body.

An example of the markup is:
  <inline type="media.photo" id="1" />

The type attribute is app_name.model_name and the id is
the object id. Pretty simple.

In your template you would say:
  {% load inlines %}

  {{ post.body|render_inlines }}