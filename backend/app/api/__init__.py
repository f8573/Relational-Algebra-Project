"""API blueprint registration."""
from importlib import import_module


def register_api(app):
    """Register api sub-blueprints on the Flask app.

    This will attach each module's `bp` Blueprint under an appropriate URL
    prefix (e.g. `/api/run`, `/api/auth`, etc.).
    """
    modules = [
        (".run", "/api/run"),
        (".auth", "/api/auth"),
        (".courses", "/api/courses"),
        (".assessments", "/api/assessments"),
        (".admin", "/api/admin"),
    ]

    for mod_name, prefix in modules:
        mod = import_module(f"app.api{mod_name}")
        if hasattr(mod, "bp"):
            app.register_blueprint(mod.bp, url_prefix=prefix)
