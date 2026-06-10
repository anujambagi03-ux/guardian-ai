from sqlalchemy.orm import Session

from models import Alert


def create_alert(
    db: Session,
    alert_type: str,
    severity: str,
    message: str
):
    alert = Alert(
        alert_type=alert_type,
        severity=severity,
        message=message
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


def get_all_alerts(
    db: Session
):
    return db.query(Alert).order_by(
        Alert.id.desc()
    ).all()


def get_alert_by_id(
    db: Session,
    alert_id: int
):
    return db.query(Alert).filter(
        Alert.id == alert_id
    ).first()


def delete_alert(
    db: Session,
    alert_id: int
):
    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        return None

    db.delete(alert)
    db.commit()

    return True