from django.utils import timezone
from django.utils.text import slugify

from movie_recommendation_engine.common.models import PublishStateOptions
from movie_recommendation_engine.common.utils import get_unique_slug


def slugify_pre_save(sender, instance, *args, **kwargs):
    title = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = slugify(title)

def unique_slugify_pre_save(sender, instance, *args, **kwargs):
    title = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = get_unique_slug(instance, size=5)