import pytest

from metricguard.application.rbac import (
    AuthorizationError,
    UserRole,
    resolve_user_access,
)


def test_admin_email_receives_admin_role():

    access = resolve_user_access(
        email="admin@example.com",
        admin_emails=[
            "admin@example.com",
        ],
    )

    assert (
        access.role
        == UserRole.ADMIN
    )

    assert (
        access.can_manage_knowledge_base
        is True
    )


def test_authenticated_non_admin_is_viewer():

    access = resolve_user_access(
        email="viewer@example.com",
        admin_emails=[
            "admin@example.com",
        ],
    )

    assert (
        access.role
        == UserRole.VIEWER
    )

    assert (
        access.can_investigate
        is True
    )

    assert (
        access.can_manage_knowledge_base
        is False
    )


def test_admin_matching_is_case_insensitive():

    access = resolve_user_access(
        email="ADMIN@EXAMPLE.COM",
        admin_emails=[
            "admin@example.com",
        ],
    )

    assert (
        access.role
        == UserRole.ADMIN
    )


def test_missing_email_is_rejected():

    with pytest.raises(
        AuthorizationError
    ):

        resolve_user_access(
            email=" ",
            admin_emails=[],
        )