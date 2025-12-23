import pytest
from app.models import AuditLog
from app.extensions import db


def test_audit_record_creates_entry(app):
    with app.app_context():
        # record entry
        entry = AuditLog.record(actor_id=1, target_id=2, event_type='test_event', resource_type='course', resource_id=42, ip='127.0.0.1', ua='pytest', meta={'k': 'v'})
        assert entry.id is not None
        # query back
        found = AuditLog.query.get(entry.id)
        assert found is not None
        assert found.event_type == 'test_event'
        assert found.resource_type == 'course'
        assert found.meta.get('k') == 'v'
