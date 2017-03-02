# -*- coding:utf8 -*-

from datetime import timedelta, datetime
from dateutil import rrule
from django.utils.timezone import now
import pytz


def get_time_start(date_time):
    return datetime(date_time.year, date_time.month, date_time.day, 0, 0, 0)


def get_time_end(date_time):
    return datetime(date_time.year, date_time.month, date_time.day, 23, 59, 59)


def get_today_start():
    return get_time_start(now())


def get_today_end():
    return get_time_end(now())


def parse_date(date, format_type="%Y%m%d"):
    try:
        return datetime.strptime(date, format_type)
    except:
        return None


def parse_dt(date, format_type="%Y-%m-%d %H:%M:%S"):
    try:
        return datetime.strptime(date, format_type)
    except:
        return None


def to_date_str(date, format_type="%Y%m%d"):
    return date.strftime(format_type)


def to_datetime_str(date, format_type="%Y-%m-%d %H:%M:%S"):
    return date.strftime(format_type)


def get_ch_now():
    return datetime.now(pytz.timezone("Asia/Shanghai"))


def add_day(date, days):
    return date + timedelta(days=days)


def add_seconds(date, seconds):
    return date + timedelta(seconds=seconds)


def interval_day(start_date, end_date):
    return (end_date - start_date).days


def work_days(start, end, holidays=0, days_off=None):
    if days_off is None:
        days_off = 5, 6  # 默认：周六和周日
    workdays = [x for x in range(7) if x not in days_off]
    days = rrule.rrule(rrule.DAILY, dtstart=start, until=end, byweekday=workdays)
    return days.count() - holidays


def get_epoch(date_time):
    return int(date_time.strftime("%s")) * 1000


def get_epoch_now():
    return get_epoch(datetime.now())
