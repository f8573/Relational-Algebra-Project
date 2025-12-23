from flask import Flask, request
from flask_cors import CORS
from app.config import Config
from app.extensions import db
from importlib import import_module

# Ensure models are imported so SQLAlchemy metadata is registered
import_module("app.models")


def create_app(config_class=Config):
    app = Flask(__name__)
    # Allow requests to hit routes with or without a trailing slash
    # This avoids Flask redirecting OPTIONS preflight requests, which browsers block.
    app.url_map.strict_slashes = False
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    # Explicit CORS config for API endpoints to ensure dev frontend can contact backend
    # Allow credentials so Authorization headers are accepted in development.
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Register Blueprints
    from app.api import register_api

    register_api(app)

    # Auto-initialize DB in development if tables are missing to avoid
    # runtime OperationalError when starting the dev server without running
    # the CLI `flask init-db` command. Also ensure demo users exist and
    # perform lightweight schema backfills for development convenience.
    try:
        with app.app_context():
            from sqlalchemy import inspect, text

            inspector = inspect(db.engine)
            if not inspector.has_table("users"):
                app.logger.info("Database appears uninitialized; creating tables...")
                db.create_all()

            # Create or ensure demo users exist and have passwords
            from app.models.user import User as UserModel
            demo_users = [
                ("admin@university.edu", "admin-password-123", True, "Admin"),
                ("instructor@university.edu", "instructor-password-456", False, "Instructor"),
                ("student@university.edu", "student-password-789", False, "Student"),
            ]
            for email, pw, is_admin, name in demo_users:
                u = UserModel.query.filter_by(email=email).first()
                if not u:
                    u = UserModel(email=email, name=name, is_platform_admin=is_admin)
                    db.session.add(u)
                # Always ensure demo password is set on startup for development
                try:
                    u.set_password(pw)
                    db.session.add(u)
                except Exception:
                    app.logger.exception('Failed to set password for demo user: %s', email)
            db.session.commit()

            # Ensure `questions` table has `db_id` column (backfill schema for older DBs)
            if inspector.has_table('questions'):
                cols = [c['name'] for c in inspector.get_columns('questions')]
                if 'db_id' not in cols:
                    app.logger.info('Adding missing questions.db_id column to database')
                    # SQLite supports ADD COLUMN for simple cases
                    try:
                        # use session.execute (Engine.execute removed in SQLAlchemy 1.4+)
                        db.session.execute(text('ALTER TABLE questions ADD COLUMN db_id INTEGER'))
                        db.session.commit()
                        app.logger.info('Added questions.db_id column')
                    except Exception:
                        app.logger.exception('Failed to add questions.db_id column')

            # Ensure databases table exists (create missing tables as needed)
            if not inspector.has_table('databases'):
                app.logger.info('Databases table missing; creating missing tables')
                try:
                    db.create_all()
                    app.logger.info('Created missing tables')
                except Exception:
                    app.logger.exception('Failed to create missing tables')
    except Exception:
        # Don't fail app startup if DB init fails; log and continue so errors
        # surface in request handling instead.
        app.logger.exception("Auto DB initialization failed")

    # --- CLI Commands ---

    @app.cli.command("init-db")
    def init_db():
        """Creates database tables from SQLAlchemy models."""
        db.create_all()
        print("Initialized the database!")

        # Create default admin user if not exists
        from app.models.user import User

        if not User.query.filter_by(email="admin@university.edu").first():
            admin = User(
                email="admin@university.edu",
                name="System Admin",
                is_platform_admin=True,
            )
            db.session.add(admin)
            db.session.commit()
            print("Created default admin: admin@university.edu")

    @app.cli.command("init-bank")
    def init_bank():
        """Create or copy a sample `bank.db` used by the RA executor."""
        from app.cli import init_bank_db

        created = init_bank_db()
        print(f"Initialized bank DB at: {created}")

    @app.route("/health")
    def health_check():
        return {"status": "healthy", "db": str(db.engine.url)}

    # Temporary safeguard: ensure API responses include CORS headers even on errors.
    # This helps the dev frontend receive CORS headers when an endpoint raises.
    @app.after_request
    def _ensure_cors_headers(response):
        try:
            if request.path.startswith('/api/'):
                response.headers.setdefault('Access-Control-Allow-Origin', '*')
                response.headers.setdefault('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
                response.headers.setdefault('Access-Control-Allow-Headers', 'Authorization,Content-Type')
        except Exception:
            app.logger.exception('Failed to set CORS headers')
        return response

    return app
