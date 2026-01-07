from datetime import timedelta
from django.utils import timezone
from ..models import Plan

def get_plan_duration(interval: str) -> timedelta:
    if interval == 'month':
        return timedelta(days=30)
    elif interval == 'year':
        return timedelta(days=365)
    else:
        raise ValueError(f"Invalid interval: {interval}")


def get_plan_updates(
    existing_plans: dict[str, Plan], 
    desired_plans: dict[str, dict], 
    no_delete: bool = False
) -> tuple[list[Plan], list[Plan], list[Plan]]:
    """
    Get the plans to create, update, and delete from the existing plans and the desired plans.
    """
    to_create = []
    to_update = []

    for code, payload in desired_plans.items():
        if code not in existing_plans:
            to_create.append(Plan(code=code, **payload))
        else:
            plan = existing_plans[code]
            changed = False
            for field, value in payload.items():
                if field == 'code':
                    continue
                if getattr(plan, field) != value:
                    setattr(plan, field, value)
                    changed = True
            
            if changed:
                to_update.append(plan)

    if not no_delete:
        to_delete = [plan for code, plan in existing_plans.items() if code not in desired_plans]
    else:
        to_delete = []

    return to_create, to_update, to_delete