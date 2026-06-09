def detect_accidents(violations):

    accident_alerts = []

    total_violations = len(violations)

    if total_violations >= 20:

        accident_alerts.append(
            {
                "location": "Guardian Zone",
                "severity": "High"
            }
        )

    elif total_violations >= 10:

        accident_alerts.append(
            {
                "location": "Guardian Zone",
                "severity": "Medium"
            }
        )

    elif total_violations >= 5:

        accident_alerts.append(
            {
                "location": "Guardian Zone",
                "severity": "Low"
            }
        )

    return accident_alerts