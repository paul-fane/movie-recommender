import datetime
from django.db.models import Q
from django.utils import timezone
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




def get_recent_users(days_ago=7, ids_only=True) -> QuerySet[BaseUser]:
    delta = datetime.timedelta(days=days_ago)
    time_delta = timezone.now()  - delta
    qs = BaseUser.objects.filter(
        Q(date_joined__gte=time_delta) |
        Q(last_login__gte=time_delta) 
    )
    if ids_only:
        return qs.values_list('id', flat=True)
    return qs