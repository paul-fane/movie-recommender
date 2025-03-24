from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.shortcuts import get_object_or_404
import random
import string
from django.utils.text import slugify

def make_mock_object(**kwargs):
    return type("", (object,), kwargs)


def get_object(model_or_queryset, **kwargs):
    """
    Reuse get_object_or_404 since the implementation supports both Model && queryset.
    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None


def assert_settings(required_settings, error_message_prefix=""):
    """
    Checks if each item from `required_settings` is present in Django settings
    """
    not_present = []
    values = {}

    for required_setting in required_settings:
        if not hasattr(settings, required_setting):
            not_present.append(required_setting)
            continue

        values[required_setting] = getattr(settings, required_setting)

    if not_present:
        if not error_message_prefix:
            error_message_prefix = "Required settings not found."

        stringified_not_present = ", ".join(not_present)

        raise ImproperlyConfigured(f"{error_message_prefix} Could not find: {stringified_not_present}")

    return values


def get_random_string(size=4, chars=string.ascii_lowercase + string.digits):
    return "".join([random.choice(chars) for _ in range(size)])


def get_unique_slug(instance, new_slug=None, size=10, max_size=30):
    title = instance.title
    if new_slug is None:
        """
        Default
        """
        slug = slugify(title)
    else:
        """
        Recursive
        """
        slug = new_slug
    #slug = slug[:max_size] => not working if the slug is too long
    Klass = instance.__class__ # Playlist, Category
    parent = None
    try:
        parent = instance.parent
    except:
        pass
    if parent is not None:
        qs = Klass.objects.filter(parent=parent, slug=slug) # smaller
    else:
        qs = Klass.objects.filter(slug=slug) # larger
    if qs.exists():
        new_slug = slugify(title) + get_random_string(size=size)
        return get_unique_slug(instance, new_slug=new_slug)
    return slug