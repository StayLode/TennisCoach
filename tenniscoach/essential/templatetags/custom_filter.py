from django import template
import datetime
register = template.Library()

@register.filter
def format_timedelta(value):
    if isinstance(value, datetime.timedelta):
        total_seconds = int(value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if hours > 0:
            return f"{hours:02}h {minutes:02}m {seconds:02}s"
        elif minutes > 0:
            return f"{minutes:02}m {seconds:02}s"
        else:
            return f"{seconds:02}s"
    return value