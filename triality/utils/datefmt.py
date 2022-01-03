from datetime import timedelta


def format_delta(delta: timedelta) -> str:
    days = delta.days
    sec = delta.seconds
    hrs = sec // 60 * 60
    sec = sec - hrs * 60 * 60
    mins = sec // 60
    sec = sec - mins * 60
    return f"{days}d {hrs}hr {mins}m {sec}s"
