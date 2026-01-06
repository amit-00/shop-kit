import json
from pathlib import Path
import select

from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db import transaction
from django.conf import settings

from apps.identity.models import Plan

class Command(BaseCommand):
    help = 'Sync plans from plans.json'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--path',
            default=None,
            help='Path to plans.json'
        ),
        parser.add_argument(
            '--dry-run',
            action='store_true',
            default=False,
            help='Show what would change without writing to the DB'
        ),
        parser.add_argument(
            '--no-delete',
            action='store_true',
            default=False,
            help='Do not delete db plans that are not in the JSON file'
        )

    def handle(self, *args, **opts) -> None:
        default_path = Path(__file__).resolve().parents[2] / "plans.json"
        path_arg = opts.get('path')
        path = Path(path_arg) if path_arg else default_path

        if not path.exists():
            raise CommandError(f"File at {path} does not exist")

        with open(path, 'r') as f:
            plans = json.load(f)

        if not isinstance(plans, list):
            raise CommandError(f"File at {path} is not a valid JSON array")

        dry_run = opts.get('dry_run')
        no_delete = opts.get('no_delete')

        desired_by_code = {plan['code']: plan for plan in plans}
        
        if not no_delete:
            self.stdout.write(self.style.WARNING(
                "Running in delete mode. Plans that are not in the JSON file will be deleted."
            ))
            

        with transaction.atomic():
            existing = {plan.code: plan for plan in Plan.objects.select_for_update().all()}
            to_create = []
            to_update = []
            creates = updates = 0

            for code, payload in desired_by_code.items():
                if code not in existing:
                    to_create.append(Plan(**payload))
                else:
                    plan = existing[code]
                    changed = False
                    for field, value in payload.items():
                        if field == 'code':
                            continue
                        if getattr(plan, field) != value:
                            setattr(plan, field, value)
                            changed = True
                    
                    if changed:
                        to_update.append(plan)

            extras = []

            if not no_delete:
                extras = [plan for code, plan in existing.items() if code not in desired_by_code]

            if dry_run:
                self.stdout.write(f"[DRY RUN] Would create: {len(to_create)}")
                self.stdout.write(f"[DRY RUN] Would update: {len(to_update)}")
                self.stdout.write(f"[DRY RUN] Would delete: {len(extras)}")
                return
            
            if to_create:
                Plan.objects.bulk_create(to_create)
                creates += len(to_create)

            if to_update:
                fields = ['name', 'description', 'unit_amount', 'currency', 'interval', 'is_active']
                Plan.objects.bulk_update(to_update, fields=fields)
                updates += len(to_update)

            deletes = 0
            if extras:
                deletes = Plan.objects.filter(code__in=[plan.code for plan in extras]).delete()[0]

            self.stdout.write(self.style.SUCCESS(f"Plans synced, Created {creates}, Updated {updates}, Deleted {deletes}"))