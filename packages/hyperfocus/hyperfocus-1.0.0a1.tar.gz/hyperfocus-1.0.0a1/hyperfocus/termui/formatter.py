from __future__ import annotations

import datetime

from hyperfocus.database.models import Task, TaskStatus
from hyperfocus.termui import icons, style


def date(date: datetime.date) -> str:
    return date.strftime("%a, %d %B %Y")


def date_with_time(date: datetime.datetime) -> str:
    return date.strftime("%a, %d %B %Y at %H:%M:%S")


def task(task: Task, show_prefix: bool = False) -> str:
    title_style = {
        TaskStatus.DELETED: f"[{style.DELETED_TASK}]{{title}}[/]",
        TaskStatus.DONE: f"[{style.DONE_TASK}]{{title}}[/]",
    }.get(task.status, "{title}")

    title = title_style.format(title=task.title)
    prefix = f"Task: #{str(task.id)} " if show_prefix else ""

    return f"{prefix}{task_status(task.status)} {title}"


def stashed_task(old_task_id: int, task: Task) -> str:
    prefix = f"Task: #{str(old_task_id)} "
    return f"{prefix}{task_status(task.status)} {task.title}"


def task_status(status: TaskStatus) -> str:
    color = {
        TaskStatus.TODO: style.DEFAULT,
        TaskStatus.DELETED: style.ERROR,
        TaskStatus.DONE: style.SUCCESS,
        TaskStatus.STASHED: style.STASHED,
    }.get(status, style.UNKNOWN)

    return f"[{color}]{icons.TASK_STATUS}[/]"


def config(config: dict[str, str]) -> str:
    return "\n".join([f"[{style.INFO}]{k}[/] = {v}" for k, v in config.items()])
