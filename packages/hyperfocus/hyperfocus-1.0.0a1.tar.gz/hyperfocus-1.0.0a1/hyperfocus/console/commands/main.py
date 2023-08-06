from __future__ import annotations

import sys

import click

from hyperfocus import __app_name__, __version__
from hyperfocus.console.core.decorators import hyperfocus
from hyperfocus.database.models import TaskStatus
from hyperfocus.services.session import Session
from hyperfocus.termui import formatter, printer, prompt, style
from hyperfocus.termui.components import NewDay, ProgressBar, TasksTable


@hyperfocus(invoke_without_command=True, help="Minimalist task manager")
@click.version_option(
    version=__version__, prog_name=__app_name__, help="Show the version"
)
@click.pass_context
def hyf(ctx: click.Context) -> None:
    if ctx.invoked_subcommand in ["init"] or "--help" in sys.argv[1:]:
        return

    session = Session.create()
    session.bind_context(ctx=ctx)

    if session.daily_tracker.is_a_new_day():
        printer.echo(NewDay(session.date))

    previous_day = session.daily_tracker.get_previous_day()

    unfinished_tasks = []
    if previous_day and not previous_day.is_locked():
        finished_status = [TaskStatus.DELETED, TaskStatus.DONE]
        unfinished_tasks = previous_day.get_tasks(exclude=finished_status)

    if ctx.invoked_subcommand is not None:
        if len(unfinished_tasks) > 0 and previous_day:
            printer.banner(
                f"You have {len(unfinished_tasks)} unfinished task(s) from "
                f"{formatter.date(date=previous_day.date)}, run 'hyf' "
                f"to review."
            )
        return

    if len(unfinished_tasks) > 0 and previous_day:
        if prompt.confirm(
            f"Review [{style.INFO}]{len(unfinished_tasks)}[/] unfinished task(s) "
            f"from {formatter.date(date=previous_day.date)}",
            default=True,
        ):
            for task in unfinished_tasks:
                if prompt.confirm(f'Continue "[{style.INFO}]{task.title}[/]"'):
                    session.daily_tracker.copy_task(task)

    if previous_day:
        previous_day.locked()
    tasks = session.daily_tracker.get_tasks()
    if tasks:
        printer.echo(TasksTable(tasks))
        printer.echo(ProgressBar(tasks))
    else:
        printer.echo("No tasks for today...")
