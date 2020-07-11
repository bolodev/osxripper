import datetime


COCOA_EPOCH = datetime.datetime(2001, 1, 1)
UNIX_EPOCH = datetime.datetime(1970, 1, 1)
GREGORIAN_1601 = datetime.datetime(1601, 1, 1)


def get_gregorian_seconds(delta_date):
    """
    Get the date time with a second delta
    """
    if delta_date is None:
        return "[ERROR] Not a date value: None"
    else:
        try:
            return GREGORIAN_1601 + datetime.timedelta(seconds=delta_date)
        except OverflowError:
            "[ERROR] unknown date value: {0}".format(delta_date)


def get_gregorian_micros(delta_date):
    """
    Get the date time with a microsecond delta
    """
    if delta_date is None:
        return "[ERROR] Not a date value: None"
    else:
        try:
            return GREGORIAN_1601 + datetime.timedelta(microseconds=delta_date)
        except OverflowError:
            "[ERROR] unknown date value: {0}".format(delta_date)


def get_gregorian_millis(delta_date):
    """
    Get the date time with a millisecond delta
    """
    if delta_date is None:
        return "[ERROR] Not a date value: None"
    else:
        try:
            return GREGORIAN_1601 + datetime.timedelta(milliseconds=delta_date)
        except OverflowError:
            "[ERROR] unknown date value: {0}".format(delta_date)


def get_unix_seconds(delta_date):
    """
    Get the date time with a second delta
    """
    if delta_date is None:
        return "[ERROR] Not a date value: None"
    else:
        try:
            return UNIX_EPOCH + datetime.timedelta(seconds=delta_date)
        except OverflowError:
            "[ERROR] unknown date value: {0}".format(delta_date)


def get_unix_micros(delta_date):
    """
    Get the date time with a millisecond delta
    """
    if delta_date is None:
        return "[ERROR] Not a date value: None"
    else:
        try:
            return UNIX_EPOCH + datetime.timedelta(microseconds=delta_date)
        except OverflowError:
            "[ERROR] unknown date value: {0}".format(delta_date)


def get_unix_millis(delta_date):
    """
    Get the date time with a millisecond delta
    """
    if delta_date is None:
        return "[ERROR] Not a date value: None"
    else:
        try:
            return UNIX_EPOCH + datetime.timedelta(milliseconds=delta_date)
        except OverflowError:
            "[ERROR] unknown date value: {0}".format(delta_date)


def get_cocoa_millis(delta_date):
    """
    Get the date time with a millisecond delta
    """
    if delta_date is None:
        return "[ERROR] Not a date value: None"
    else:
        try:
            return COCOA_EPOCH + datetime.timedelta(milliseconds=delta_date)
        except OverflowError:
            "[ERROR] unknown date value: {0}".format(delta_date)


def get_cocoa_seconds(delta_date):
    """
    Get the date time with a millisecond delta
    """
    if delta_date is None:
        return "[ERROR] Not a date value: None"
    else:
        try:
            return COCOA_EPOCH + datetime.timedelta(seconds=delta_date)
        except OverflowError:
            "[ERROR] unknown date value: {0}".format(delta_date)
