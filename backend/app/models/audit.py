"""Audit logging model."""
from app.extensions import db
from datetime import datetime


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    actor_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    target_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    event_type = db.Column(db.String(100), nullable=False)
    resource_type = db.Column(db.String(50))
    resource_id = db.Column(db.Integer)
    ip_address = db.Column(db.String(100))
    user_agent = db.Column(db.String(300))
    meta = db.Column(db.JSON, default={})

    def __repr__(self):
        return f'<AuditLog {self.event_type} {self.resource_type}:{self.resource_id} by {self.actor_user_id}>'

    @classmethod
    def record(cls, actor_id=None, target_id=None, event_type=None,
               resource_type=None, resource_id=None, ip=None, ua=None, meta=None):
        entry = cls(
            actor_user_id=actor_id,
            target_user_id=target_id,
            event_type=event_type or 'unknown',
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip,
            user_agent=ua,
            meta=meta or {}
        )
        db.session.add(entry)
        db.session.commit()
        return entry
