from flask import Blueprint, request, jsonify, current_app
from app.services.execution import RAExecutor
from .auth_decorators import verify_token

from app.models import DatabaseFile
import os

bp = Blueprint("run", __name__)


@bp.route("/", methods=["POST"])
@verify_token
def run_query():
    """Execute a relational algebra query (requires authentication).

    Accepts JSON: { query: string, db_id?: integer }
    If `db_id` is provided, the uploaded database file is used as the
    execution backend. Otherwise falls back to `BANK_DB` configured path.
    """
    data = request.json or {}
    raw_query = (data.get("query") or "").strip()
    if not raw_query:
        return jsonify({"error": "Empty query"}), 400

    # Normalize db_id: treat missing/empty/'DEFAULT' as no selection
    db_id = data.get('db_id')
    db_path = None
    if db_id in (None, '', 'DEFAULT'):
        db_id = None

    if db_id is not None:
        # attempt to coerce numeric id
        try:
            db_id_int = int(db_id)
        except Exception:
            current_app.logger.debug('Invalid db_id provided to run endpoint: %r', db_id)
            return jsonify({'status': 'error', 'message': 'Invalid db_id'}), 400

        dbf = DatabaseFile.query.get(db_id_int)
        if not dbf:
            current_app.logger.debug('Requested db_id not found: %s', db_id_int)
            return jsonify({'status': 'error', 'message': 'Database not found'}), 400
        upload_dir = os.path.join(current_app.root_path, '..', 'uploads', 'databases')
        candidate = os.path.join(upload_dir, dbf.filename)
        if not os.path.exists(candidate):
            current_app.logger.error('Database file missing on disk for db_id %s: %s', db_id_int, candidate)
            return jsonify({'status': 'error', 'message': 'Database file missing on server'}), 500
        db_path = candidate
    else:
        # If no db_id provided, prefer an uploaded DatabaseFile whose filename
        # matches the configured BANK_DB basename. This makes the frontend
        # "default" selection behave like selecting the uploaded bank file
        # when present.
        bank_cfg = current_app.config.get('BANK_DB', None)
        bank_basename = os.path.basename(bank_cfg) if bank_cfg else None
        db_path = None
        if bank_basename:
            dbf = DatabaseFile.query.filter_by(filename=bank_basename).first()
            if dbf:
                upload_dir = os.path.join(current_app.root_path, '..', 'uploads', 'databases')
                candidate = os.path.join(upload_dir, dbf.filename)
                if os.path.exists(candidate):
                    db_path = candidate
        if not db_path:
            db_path = current_app.config.get('BANK_DB', 'bank.db')

    executor = RAExecutor(db_path=db_path)
    output, error = executor.execute(raw_query)

    if error:
        return jsonify({"status": "error", "error": error, "partial_output": output})

    return jsonify({"status": "success", "output": output})
