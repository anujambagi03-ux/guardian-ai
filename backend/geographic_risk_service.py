import random
from models import (
    GeographicRiskZone,
    ZoneRiskAnalytics,
    RiskHeatmap,
    IncidentPattern
)

def generate_zone(db):

    zones = [
        "CITY_CENTER",
        "HIGHWAY",
        "INDUSTRIAL_AREA",
        "AIRPORT_ROAD",
        "RESIDENTIAL_AREA"
    ]

    zone = GeographicRiskZone(
        zone_id=f"ZONE_{random.randint(1,100)}",
        zone_name=random.choice(zones),
        hotspot_count=random.randint(1,10),
        incident_count=random.randint(1,20),
        risk_score=random.randint(50,100),
        severity_level=random.choice(
            ["LOW","MEDIUM","HIGH","CRITICAL"]
        )
    )

    db.add(zone)
    db.commit()
    db.refresh(zone)

    return zone

def generate_zone_analytics(db):

    zones = db.query(
        GeographicRiskZone
    ).all()

    result = []

    for rank, zone in enumerate(
        sorted(
            zones,
            key=lambda x: x.risk_score,
            reverse=True
        ),
        start=1
    ):

        analytics = ZoneRiskAnalytics(
            analytics_id=f"AN_{rank}",
            zone_id=zone.zone_id,
            average_risk_score=zone.risk_score,
            hotspot_count=zone.hotspot_count,
            incident_count=zone.incident_count,
            risk_rank=rank
        )

        db.add(analytics)
        result.append(analytics)

    db.commit()

    return result

def generate_heatmap(db):

    zones = db.query(
        GeographicRiskZone
    ).all()

    heatmaps = []

    for zone in zones:

        item = RiskHeatmap(
            heatmap_id=f"HM_{zone.id}",
            zone_id=zone.zone_id,
            latitude=str(
                round(
                    random.uniform(
                        12.90,
                        13.10
                    ),
                    4
                )
            ),
            longitude=str(
                round(
                    random.uniform(
                        77.50,
                        77.70
                    ),
                    4
                )
            ),
            risk_score=zone.risk_score,
            severity_level=zone.severity_level
        )

        db.add(item)
        heatmaps.append(item)

    db.commit()

    return heatmaps