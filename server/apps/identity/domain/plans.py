from ..models import Plan


def compute_plan_changes(
    existing_plans: dict[str, Plan], 
    desired_plans: dict[str, dict], 
    no_delete: bool = False
) -> tuple[list[Plan], list[Plan], list[Plan]]:
    """
    Get the plans to create, update, and delete from the existing plans and the desired plans.
    """
    to_create = []
    to_update = []

    print(f"DEBUG: existing_plans={existing_plans["plan_a"].unit_amount}")
    print(f"DEBUG: desired_plans={desired_plans}")

    for code, payload in desired_plans.items():
        if code not in existing_plans:
            to_create.append(Plan(**payload))
        else:
            plan = existing_plans[code]
            changed = False
            for field, value in payload.items():
                print(f"DEBUG: field={field}, value={value}")
                print(f"DEBUG: current value={plan.__dict__.get(field)}")
                if field == 'code':
                    continue
                if getattr(plan, field) != value:
                    print(f"DEBUG: Change detected for {field}, changed={changed}")
                    setattr(plan, field, value)
                    changed = True
            
            if changed:
                to_update.append(plan)

    if not no_delete:
        to_delete = [plan for code, plan in existing_plans.items() if code not in desired_plans]
    else:
        to_delete = []

    return to_create, to_update, to_delete