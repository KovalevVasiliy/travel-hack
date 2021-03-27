from datetime import date, datetime, timezone


def format_datetime(dt: date) -> str:
    if isinstance(dt, datetime):
        return (
            dt.replace(tzinfo=timezone.utc)
            .isoformat(timespec='milliseconds')
            .replace('+00:00', 'Z')
        )
    return dt.isoformat()


def formatted_now() -> str:
    return format_datetime(datetime.now())
