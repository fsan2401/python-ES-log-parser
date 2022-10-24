"""
    Parser Class
"""

from pyparsing import Word, alphas, Suppress, Combine, nums, string, Regex, Optional


class Parser(object):
    # log lines don't include the year, but if we don't provide one, datetime.strptime will assume 1900
    # ASSUMED_YEAR = '2020'

    def __init__(self):
        ints = Word(nums)

        # priority
       # priority = Suppress("<") + ints + Suppress(">")

        # timestamp
        month = Word(string.ascii_uppercase, string.ascii_lowercase, exact=3)
        day   = ints
        hour  = Combine(ints + ":" + ints + ":" + ints)

        timestamp = month + day + hour
        # a parse action will convert this timestamp to a datetime
        timestamp.setParseAction(lambda t: datetime.strptime(datetime.now().strftime("%Y") + ' ' + ' '.join(t), '%Y %b %d %H:%M:%S'))

        # hostname
        hostname = Word(alphas + nums + "_-.")

        # appname
        appname = Word(alphas + "/-_.()")("appname") + (Suppress("[") + ints("pid") + Suppress("]")) | (Word(alphas + "/-_.")("appname"))
        appname.setName("appname")

        # message
        message = Regex(".*")

        # pattern build
        # (add results names to make it easier to access parsed fields)
        self._pattern = timestamp("timestamp") + hostname("hostname") + Optional(appname) + Suppress(':') + message("message")

    def parse(self, line):
        parsed = self._pattern.parseString(line)
        # fill in keys that might not have been found in the input string
        # (this could have been done in a parse action too, then this method would
        # have just been a two-liner)
        for key in 'appname pid'.split():
            if key not in parsed:
                parsed[key] = ''
        return parsed.asDict()