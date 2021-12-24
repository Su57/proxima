import time
import calendar


class DateUtil:

    @classmethod
    def timestamp(cls):
        """
        获取当前时间戳

        :return: 时间戳，单位:秒
        """
        return calendar.timegm(time.gmtime())
