"""Permissions and whitelist checks.

This module contains small helpers used by views to authorize actions.
"""


def can_manage_course(user, course):
    # placeholder
    if not user:
        return False
    role = getattr(user, "role", None)
    name = getattr(role, "name", "")
    return name in ("instructor", "admin")
