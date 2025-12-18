from decimal import Decimal
from datetime import date, datetime, timedelta
import calendar
from models import User, Shift


def hours_for_shift(shift):
    """Return working hours for a single shift (float hours).

    Handles overnight and break times using related Time record.
    """
    t = shift.time
    if not t or not t.start_time or not t.end_time:
        return 0.0

    start_dt = datetime.combine(shift.date, t.start_time)
    end_dt = datetime.combine(shift.date, t.end_time)
    if end_dt < start_dt:
        end_dt += timedelta(days=1)

    work_duration = end_dt - start_dt

    break_duration = timedelta(0)
    if t.break_start_time and t.break_end_time:
        bstart_dt = datetime.combine(shift.date, t.break_start_time)
        bend_dt = datetime.combine(shift.date, t.break_end_time)
        if bend_dt < bstart_dt:
            bend_dt += timedelta(days=1)
        break_duration = bend_dt - bstart_dt

    net = work_duration - break_duration
    hours = max(0.0, net.total_seconds() / 3600.0)
    return hours


def monthly_summary(year: int, month: int):
    """Compute per-user monthly hours and salary for given year/month.

    Returns list of dicts: {"user": User, "hours": float, "salary": Decimal}
    """
    last_day = calendar.monthrange(year, month)[1]
    start_date = date(year, month, 1)
    end_date = date(year, month, last_day)

    results = []
    users = User.select()
    for u in users:
        shifts = Shift.select().where(
            (Shift.user == u) & (Shift.date.between(start_date, end_date))
        )
        total_hours = 0.0
        total_salary = Decimal("0")
        for s in shifts:
            h = hours_for_shift(s)
            total_hours += h
            if s.workplace and s.workplace.price is not None:
                total_salary += s.workplace.price * Decimal(str(h))
        results.append(
            {
                "user": u,
                "hours": round(total_hours, 2),
                "salary": total_salary.quantize(Decimal("0.01")),
            }
        )
    return results


def user_monthly_summary(user_id: int, year: int, month: int):
    """Compute single user's monthly hours and salary.

    Returns dict: {"user": User, "hours": float, "salary": Decimal} or None.
    """
    user = User.get_or_none(User.id == user_id)
    if not user:
        return None
    last_day = calendar.monthrange(year, month)[1]
    start_date = date(year, month, 1)
    end_date = date(year, month, last_day)
    shifts = Shift.select().where(
        (Shift.user == user) & (Shift.date.between(start_date, end_date))
    )
    total_hours = 0.0
    total_salary = Decimal("0")
    for s in shifts:
        h = hours_for_shift(s)
        total_hours += h
        if s.workplace and s.workplace.price is not None:
            total_salary += s.workplace.price * Decimal(str(h))
    return {
        "user": user,
        "hours": round(total_hours, 2),
        "salary": total_salary.quantize(Decimal("0.01")),
    }


def user_ytd_summary(user_id: int, year: int, month: int):
    """Compute single user's year-to-date (Jan ~ month) hours and salary.

    Returns dict: {"user": User, "hours": float, "salary": Decimal} or None.
    """
    user = User.get_or_none(User.id == user_id)
    if not user:
        return None
    start_date = date(year, 1, 1)
    end_date = date(year, month, calendar.monthrange(year, month)[1])
    shifts = Shift.select().where(
        (Shift.user == user) & (Shift.date.between(start_date, end_date))
    )
    total_hours = 0.0
    total_salary = Decimal("0")
    for s in shifts:
        h = hours_for_shift(s)
        total_hours += h
        if s.workplace and s.workplace.price is not None:
            total_salary += s.workplace.price * Decimal(str(h))
    return {
        "user": user,
        "hours": round(total_hours, 2),
        "salary": total_salary.quantize(Decimal("0.01")),
    }


def all_users_monthly_salary(year: int, month: int):
    """Compute all users' monthly salary for given year/month.

    Returns list of dicts: {"user_id": int, "user_name": str, "salary": float}
    """
    last_day = calendar.monthrange(year, month)[1]
    start_date = date(year, month, 1)
    end_date = date(year, month, last_day)

    results = []
    users = User.select()
    for u in users:
        shifts = Shift.select().where(
            (Shift.user == u) & (Shift.date.between(start_date, end_date))
        )
        total_salary = 0.0
        for s in shifts:
            h = hours_for_shift(s)
            if s.workplace and s.workplace.price is not None:
                total_salary += float(s.workplace.price) * h
        results.append(
            {
                "user_id": u.id,
                "user_name": u.name,
                "salary": round(total_salary, 2),
            }
        )
    return results


def all_users_ytd_salary(year: int, month: int):
    """Compute all users' year-to-date (Jan ~ month) salary.

    Returns list of dicts: {"user_id": int, "user_name": str, "salary": float}
    """
    start_date = date(year, 1, 1)
    end_date = date(year, month, calendar.monthrange(year, month)[1])

    results = []
    users = User.select()
    for u in users:
        shifts = Shift.select().where(
            (Shift.user == u) & (Shift.date.between(start_date, end_date))
        )
        total_salary = 0.0
        for s in shifts:
            h = hours_for_shift(s)
            if s.workplace and s.workplace.price is not None:
                total_salary += float(s.workplace.price) * h
        results.append(
            {
                "user_id": u.id,
                "user_name": u.name,
                "salary": round(total_salary, 2),
            }
        )
    return results
