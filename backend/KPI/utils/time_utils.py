# services/utils/time_filters.py

from typing import Optional, Tuple
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy import text

def get_date_ranges(
    filter_type: str,
    custom: Optional[Tuple[datetime, datetime]]
) -> Tuple[datetime, datetime, datetime, datetime]:
    """
    Given a filter name and optional custom (start, end) datetimes,
    returns (start, end, comp_start, comp_end) datetime windows
    for current vs. comparison periods.
    """
    now   = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)

    if filter_type == 'Today':
        start      = today
        end        = now
        comp_start = start - timedelta(days=1)
        comp_end   = end   - timedelta(days=1)

    elif filter_type == 'Yesterday':
        start      = today - timedelta(days=1)
        end        = start.replace(hour=23, minute=59, second=59, microsecond=999999)
        comp_start = start - timedelta(days=1)
        comp_end   = comp_start.replace(hour=23, minute=59, second=59, microsecond=999999)

    elif filter_type == 'Daily':
        end        = today - timedelta(days=1)
        start      = end.replace(hour=0, minute=0, second=0, microsecond=0)
        comp_start = start - timedelta(days=1)
        comp_end   = end   - timedelta(days=1)

    elif filter_type == 'Weekly':
        end        = today - timedelta(days=1)
        start      = end - timedelta(days=6)
        comp_start = start - timedelta(days=7)
        comp_end   = end   - timedelta(days=7)

    elif filter_type == 'MTD':
        start = today.replace(day=1)
        end   = now
        try:
            comp_start = start - relativedelta(months=1)
            comp_end   = end   - relativedelta(months=1)
        except ValueError:
            # e.g., Mar 31 → Feb 28/29
            last_prev_month = start - timedelta(days=1)
            comp_start = last_prev_month.replace(day=1)
            comp_end   = last_prev_month.replace(
                hour=end.hour,
                minute=end.minute,
                second=end.second,
                microsecond=end.microsecond
            )

    elif filter_type == 'Monthly':
        # Full previous month, preserving time-of-day
        first_of_this = today.replace(day=1)
        end   = first_of_this - timedelta(days=1)
        start = end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        comp_start = start - relativedelta(months=1)
        comp_end   = end   - relativedelta(months=1)

    elif filter_type == 'YTD':
        start      = today.replace(month=1, day=1)
        end        = now
        comp_start = start.replace(year=start.year - 1)
        comp_end   = comp_start + (end - start)

    elif filter_type == 'custom' and custom:
        start, end = custom
        # Ensure datetimes
        if not isinstance(start, datetime):
            start = datetime.combine(start, datetime.min.time())
        if not isinstance(end, datetime):
            end = datetime.combine(end,   datetime.min.time())
        comp_start = start - timedelta(days=1)
        comp_end   = end   - timedelta(days=1)

    else:
        raise ValueError(f"Unsupported filter: {filter_type}")

    return start, end, comp_start, comp_end


def fetch_one(conn, sql: str, params: dict) -> float:
    """
    Executes a scalar SQL query and returns its single numeric result.
    Falls back to 0.0 if nothing is returned.
    """
    return float(conn.execute(text(sql), params).scalar() or 0.0)


def pct_diff(current: float, previous: float) -> float:
    """
    Returns the percentage difference between current and previous:
      (current - previous) / previous * 100,
    rounded to 2 decimals, or 0 if previous is zero.
    """
    if previous:
        return round((current - previous) / previous * 100, 2)
    return 0.0
