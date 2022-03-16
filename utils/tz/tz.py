from django.utils import timezone
from datetime import datetime, timedelta

UTC_TZ = timezone.utc
LOCAL_TZ = timezone.get_current_timezone()


def utc_to_local(dt: datetime):
    """utc时间 to local时间"""
    if timezone.is_aware(dt):
        return dt.astimezone(LOCAL_TZ)
    return timezone.make_aware(dt, UTC_TZ).astimezone(LOCAL_TZ)


def utc_to_local_str(dt: datetime, fmt='%Y-%m-%d %H:%M:%S'):
    """UTC naive 时间转本地时间字符串 常用于mongo查询到的时间"""
    if not dt:
        return ''
    if timezone.is_aware(dt):
        return dt.astimezone(LOCAL_TZ).strftime(fmt)
    return timezone.make_aware(dt, UTC_TZ).astimezone(LOCAL_TZ).strftime(fmt)


def local_to_utc_str(dt: datetime, fmt='%Y-%m-%d %H:%M:%S'):
    """local时间 to utc时间字符串"""
    return dt.astimezone(UTC_TZ).strftime(fmt)


def to_ts(dt: datetime):
    """时间 to 时间戳"""
    return int(dt.timestamp())


def local_now():
    """获取当前local时间"""
    return timezone.localtime()


def now_ts():
    """获取当前时间戳"""
    return int(timezone.now().timestamp())


def utc_to_ts(dt):
    """utc时间 to 时间戳"""
    return int(dt.timestamp())


def ts_to_utc(ts):
    """时间戳转utc时间"""
    return datetime.utcfromtimestamp(ts)


def today_str():
    """今日日期 local"""
    return local_now().strftime('%Y-%m-%d')


def yesterday_str():
    """昨日日期 local"""
    return (local_now() - timedelta(days=1)).strftime('%Y-%m-%d')


def local_today_start_time():
    """当天零时 local时间"""
    return local_now().replace(hour=0, minute=0, second=0, microsecond=0)


def utc_today_start_time():
    """当天零时 对应的utc时间"""
    return local_to_utc(local_today_start_time())


def local_day_str_to_utc(day_str: str, fmt='%Y-%m-%d'):
    """本地时间字符串转 utc 时间 """
    if ':' in day_str:
        return local_to_utc(datetime.strptime(day_str, '%Y-%m-%d %H:%M:%S'))
    else:
        return local_to_utc(datetime.strptime(day_str, fmt))


def local_to_utc(dt: datetime):
    """local时间 to utc时间"""
    if timezone.is_aware(dt):
        return dt.astimezone(UTC_TZ)
    return timezone.make_aware(dt, LOCAL_TZ).astimezone(UTC_TZ)


def day_start_time(dt):
    """根据utc时间，得到当天0点的utc时间"""
    local = utc_to_local(dt)
    local_zero = local.replace(hour=0, minute=0, second=0, microsecond=0)
    return local_to_utc(local_zero)


def dict_str_to_time(data: dict, keys: list, time_format: str = "%Y-%m-%d %H:%M:%S") -> dict:
    """将字典中指定的多个字段值转换为时间类型"""
    for key in keys:
        if data.get(key) and isinstance(data[key], str):
            data[key] = local_to_utc(datetime.strptime(data[key], time_format))
    return data
