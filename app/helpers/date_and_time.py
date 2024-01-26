from datetime import datetime


def convert_to_epoc_timestamp(datetime_obj: datetime) -> int:
    """
    this function converts the given datetime obj into epoc timestamp
    :param datetime_obj:
    :return:
    """
    return int(datetime_obj.timestamp())
