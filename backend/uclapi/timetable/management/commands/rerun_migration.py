import time

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.loader import AmbiguityError
from django.db.migrations.recorder import MigrationRecorder


class Command(BaseCommand):
    """
    Re-run a migration by faking back to the migration prior to it,
    re-running it then faking back to the current migration state.
    Based on django/core/management/commands/migrate.py
    """
    help = 'Fakes back a migration, re-performs it then fakes back to now'
    verbosity = 3
    interactive = True

    def add_arguments(self, parser):
        parser.add_argument(
            'app_label',
            nargs='?',
            help='App label of the application which owns the migration.',
        )
        parser.add_argument(
            'migration_name',
            nargs='?',
            help='Migration to re-run.',
        )
        parser.add_argument(
            'previous_migration_name',
            nargs='?',
            help='Name of the previous mgiration to fake back to.'
        )
        parser.add_argument(
            '--database',
            action='store',
            dest='database',
            default=DEFAULT_DB_ALIAS,
            help=(
                'Nominates a database to migrate. '
                'Defaults to the "default" database.'
            ),
        )

    def migration_progress_callback(self, action, migration=None, fake=False):
        if self.verbosity >= 1:
            compute_time = self.verbosity > 1
            if action == "apply_start":
                if compute_time:
                    self.start = time.time()
                self.stdout.write("  Applying %s..." % migration, ending="")
                self.stdout.flush()
            elif action == "apply_success":
                elapsed = " (%.3fs)" % (
                    time.time() - self.start
                ) if compute_time else ""
                if fake:
                    self.stdout.write(self.style.SUCCESS(" FAKED" + elapsed))
                else:
                    self.stdout.write(self.style.SUCCESS(" OK" + elapsed))
            elif action == "unapply_start":
                if compute_time:
                    self.start = time.time()
                self.stdout.write("  Unapplying %s..." % migration, ending="")
                self.stdout.flush()
            elif action == "unapply_success":
                elapsed = " (%.3fs)" % (
                    time.time() - self.start
                ) if compute_time else ""
                if fake:
                    self.stdout.write(self.style.SUCCESS(" FAKED" + elapsed))
                else:
                    self.stdout.write(self.style.SUCCESS(" OK" + elapsed))
            elif action == "render_start":
                if compute_time:
                    self.start = time.time()
                self.stdout.write("  Rendering model states...", ending="")
                self.stdout.flush()
            elif action == "render_success":
                elapsed = " (%.3fs)" % (
                    time.time() - self.start
                ) if compute_time else ""
                self.stdout.write(self.style.SUCCESS(" DONE" + elapsed))

    def _get_migration_by_prefix(self, executor, app_label, prefix):
        try:
            migration = executor.loader.get_migration_by_prefix(
                app_label,
                prefix
            )
        except AmbiguityError:
            raise CommandError(
                "More than one migration matches '%s' in app '%s'. "
                "Please be more specific." %
                (prefix, app_label)
            )
        except KeyError:
            raise CommandError(
                "Cannot find a migration matching '%s' from app '%s'." % (
                    prefix,
                    app_label
                )
            )

        return migration

    def handle(self, *args, **options):
        if (
            not options['app_label'] or
            not options['migration_name'] or
            not options['previous_migration_name']
        ):
            print(
                "ERROR: You must provide an app label, migration name "
                "and the name of the previous migration to the one you are "
                "re-running."
            )
            return

        db = options['database']
        connection = connections[db]

        # Hook for backends needing any database preparation
        connection.prepare_database()

        # Work out which apps have migrations and which do not
        executor = MigrationExecutor(
            connection,
            self.migration_progress_callback
        )

        # Before anything else, see if there's conflicting apps and drop out
        # hard if there are any
        conflicts = executor.loader.detect_conflicts()
        if conflicts:
            name_str = "; ".join(
                "%s in %s" % (", ".join(names), app)
                for app, names in conflicts.items()
            )
            raise CommandError(
                "Conflicting migrations detected; multiple leaf nodes in the "
                "migration graph: (%s).\nTo fix them run "
                "'python manage.py makemigrations --merge'" % name_str
            )

        app_label = options['app_label']
        migration_name = options['migration_name']
        previous_migration_name = options['previous_migration_name']

        if app_label not in executor.loader.migrated_apps:
            raise CommandError(
                "App '%s' does not have migrations." % app_label
            )

        migration = self._get_migration_by_prefix(
            executor,
            app_label,
            migration_name
        )
        previous_migration = self._get_migration_by_prefix(
            executor,
            app_label,
            previous_migration_name
        )

        print("Rerunning migration: {}".format(migration.name))

        latest_migration = MigrationRecorder.Migration.objects.filter(
            app=app_label
        ).latest('id')

        print("Last applied {} migration: {}".format(
            app_label,
            latest_migration.name
        ))

        print("[Step 1/3] Faking back to {}...".format(
            previous_migration.name
        ))

        call_command(
            'migrate',
            app_label,
            previous_migration.name,
            fake=True,
            database=db
        )

        print("[Step 2/3] Re-running migration {}...".format(migration.name))

        call_command(
            'migrate',
            app_label,
            migration.name,
            fake=False,
            database=db
        )

        print("[Step 3/3] Faking back to migration {}...".format(
            latest_migration.name
        ))

        call_command(
            'migrate',
            app_label,
            latest_migration.name,
            fake=True,
            database=db
        )

        print("Done!")
