from datetime import timedelta

def get_plan_duration(interval: str) -> timedelta:
    if interval == 'month':
        return timedelta(days=30)
    elif interval == 'year':
        return timedelta(days=365)
    else:
        raise ValueError(f"Invalid interval: {interval}")