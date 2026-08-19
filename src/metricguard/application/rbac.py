"""Role-based access control for MetricGuard."""

from dataclasses import dataclass
from enum import StrEnum


class UserRole(StrEnum):
    VIEWER = "viewer"
    ADMIN = "admin"


class AuthorizationError(
    RuntimeError
):
    """Raised when authenticated identity cannot be authorized."""


@dataclass(
    slots=True,
    frozen=True,
)
class UserAccess:
    email: str
    role: UserRole

    @property
    def is_admin(
        self,
    ) -> bool:

        return (
            self.role
            == UserRole.ADMIN
        )

    @property
    def can_investigate(
        self,
    ) -> bool:

        return True

    @property
    def can_manage_knowledge_base(
        self,
    ) -> bool:

        return self.is_admin


def normalize_email(
    email: str,
) -> str:

    return (
        email
        .strip()
        .lower()
    )


def resolve_user_access(
    *,
    email: str,
    admin_emails: list[str]
        | tuple[str, ...]
        | set[str],
) -> UserAccess:

    normalized_email = (
        normalize_email(
            email
        )
    )

    if not normalized_email:

        raise AuthorizationError(
            "Authenticated user does not "
            "have a usable email claim."
        )

    normalized_admins = {
        normalize_email(
            value
        )
        for value
        in admin_emails
        if value.strip()
    }

    role = (
        UserRole.ADMIN
        if normalized_email
        in normalized_admins
        else UserRole.VIEWER
    )

    return UserAccess(
        email=normalized_email,
        role=role,
    )