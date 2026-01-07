import pytest
from datetime import timedelta

from apps.identity.domain.plans import *


PLAN_A_1 = Plan(code="plan_a", name="Plan A", description="Plan A", unit_amount=100, currency="USD", interval="month")
DICT_A_1 = {"code": "plan_a", "name": "Plan A", "description": "Plan A", "unit_amount": 100, "currency": "USD", "interval": "month"}
PLAN_A_2 = Plan(code="plan_a", name="Plan A", description="Plan A", unit_amount=200, currency="USD", interval="month")
DICT_A_2 = {"code": "plan_a", "name": "Plan A", "description": "Plan A", "unit_amount": 200, "currency": "USD", "interval": "month"}
PLAN_B_1 = Plan(code="plan_b", name="Plan B", description="Plan B", unit_amount=200, currency="USD", interval="month")
DICT_B_1 = {"code": "plan_b", "name": "Plan B", "description": "Plan B", "unit_amount": 200, "currency": "USD", "interval": "month"}


def plan_attrs(plan):
    """Extract comparable attributes from a Plan object."""
    return {
        "code": plan.code,
        "name": plan.name,
        "description": plan.description,
        "unit_amount": plan.unit_amount,
        "currency": plan.currency,
        "interval": plan.interval,
    }


@pytest.mark.parametrize(
    "existing_plans, desired_plans, no_delete, expected_create, expected_update, expected_delete", 
    [
        ({"plan_a": PLAN_A_1}, {"plan_a": DICT_A_1}, False, [], [], []),
        ({"plan_a": PLAN_A_1}, {"plan_a": DICT_A_1, "plan_b": DICT_B_1}, False, [PLAN_B_1], [], []),
        ({"plan_a": PLAN_A_1}, {"plan_a": DICT_A_2}, False, [], [PLAN_A_2], []),
        ({"plan_a": PLAN_A_1}, {"plan_b": DICT_B_1}, False, [PLAN_B_1], [], [PLAN_A_1]),
        ({"plan_a": PLAN_A_1, "plan_b": PLAN_B_1}, {"plan_a": DICT_A_2}, False, [], [PLAN_A_2], [PLAN_B_1]),
        ({"plan_a": PLAN_A_1}, {"plan_b": DICT_B_1}, True, [PLAN_B_1], [], []),
        ({"plan_a": PLAN_A_1, "plan_b": PLAN_B_1}, {"plan_a": DICT_A_2}, True, [], [PLAN_A_2], []),
    ],
    ids=["no_change", "add_plan", "update_plan", "add_plan_and_delete_existing", "update_plan_and_delete_existing", "no_delete_add_plan", "no_delete_update_plan"]
)
def test_compute_plan_changes(existing_plans, desired_plans, no_delete, expected_create, expected_update, expected_delete):
    to_create, to_update, to_delete = compute_plan_changes(existing_plans, desired_plans, no_delete)

    assert [plan_attrs(p) for p in to_create] == [plan_attrs(p) for p in expected_create], "Create plans don't match"
    assert [plan_attrs(p) for p in to_update] == [plan_attrs(p) for p in expected_update], "Update plans don't match"
    assert [plan_attrs(p) for p in to_delete] == [plan_attrs(p) for p in expected_delete], "Delete plans don't match"