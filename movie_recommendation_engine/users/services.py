from django.db import transaction

from movie_recommendation_engine.common.services import model_update
from movie_recommendation_engine.users.models import BaseUser


@transaction.atomic
def user_create(
    *,
    email: str,
    is_active: bool = True,
    is_admin: bool = False,
    password: str | None = None,
) -> BaseUser:
    user = BaseUser.objects.create_user(
        email=email,
        is_active=is_active,
        is_admin=is_admin,
        password=password,
    )

    return user


@transaction.atomic
def user_update(*, user: BaseUser, data) -> BaseUser:
    non_side_effect_fields: list[str] = [
        # "first_name",
        # "last_name"
    ]

    user, has_updated = model_update(
        instance=user,
        fields=non_side_effect_fields,
        data=data,
    )

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user
