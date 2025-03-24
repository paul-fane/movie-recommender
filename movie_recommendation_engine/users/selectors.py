from django.db.models.query import QuerySet

from movie_recommendation_engine.common.utils import get_object
from movie_recommendation_engine.users.filters import BaseUserFilter
from movie_recommendation_engine.users.models import BaseUser


def user_get_login_data(*, user: BaseUser):
    return {
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "is_superuser": user.is_superuser,
    }


def user_list(*, filters=None) -> QuerySet[BaseUser]:
    filters = filters or {}

    qs = BaseUser.objects.all()

    return BaseUserFilter(filters, qs).qs


def user_get(user_id) -> BaseUser | None:
    user = get_object(BaseUser, id=user_id)

    return user