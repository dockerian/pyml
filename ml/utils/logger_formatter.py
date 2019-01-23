"""
Logging formatter factory

@author: Jason Zhu
@email: jason_zhuyx@hotmail.com
"""

import logging

DEF_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_FORMATS = '%(levelname)s: %(message)s'
USE_COLOR_STYLE = True

# customized formats. see logging.Formatter class.
FORMAT = '\n%(asctime)s [%(module)s] %(message)s'
FORMAT_CRITICAL = '\n%(asctime)s [%(name)s] %(levelname)s: %(message)s'
FORMAT_ERROR = '\n%(asctime)s [%(name)s] %(levelname)s: %(message)s'
FORMAT_INFO = '\n%(asctime)s [%(name)s]: %(message)s'
FORMAT_DEBUG = '\n%(asctime)s [%(name)s #%(lineno)d] %(levelname)s: %(message)s'
FORMAT_WARNING = '\n%(asctime)s [%(name)s] %(levelname)s: %(message)s'

# ------------------------------------------------------------------------------
# constants
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
# The first code (before semi-colon) -
# 0=Normal; 1=Bold; 2=Dim; 4=Underline; 5=Blink; 7=Inverse; 8=Hidden
# The bg color + 40, foreground + 30; lighter color + 60 more
# The sequences to set color text
SEQ_BFONT = "\033[1m"   # bold font
SEQ_COLOR = "\033[1;%dm"
SEQ_DTIME = "\033[90m"  # dim
SEQ_LINUM = "\033[93m"  # light yellow for line number
SEQ_MNAME = "\033[36m"  # cyan for module name
SEQ_GREEN = "\033[32m"  # green
SEQ_RESET = "\033[0m"

COLORS = {
    'CRITICAL': MAGENTA,
    'ERROR': RED,
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
}

FORMATS = {
    'DEFAULT': FORMAT,
    logging.DEBUG: FORMAT_DEBUG,        # levelno = 10
    logging.CRITICAL: FORMAT_CRITICAL,  # levelno = 50
    logging.ERROR: FORMAT_ERROR,        # levelno = 40
    logging.WARNING: FORMAT_WARNING,    # levelno = 30
    logging.INFO: FORMAT_INFO,          # levelno = 20
}


# ------------------------------------------------------------------------------
# factory for cumtomized logging.Formatter
def factory(fmt=DEFAULT_FORMATS, use_color=USE_COLOR_STYLE):
    """
    Logging formatter factory to get colored logging formatter
    """
    return LoggingFormatter(fmt, use_color)


class LoggingFormatter(logging.Formatter):
    """
    A customized formatter for console logging.
    """

    def __init__(self, fmt=DEFAULT_FORMATS, use_color=USE_COLOR_STYLE):
        """
        Initialize an instance of LoggerFormatter
        """
        logging.Formatter.__init__(self, fmt=fmt, datefmt=DEF_DATE_FORMAT, style='%')
        self.use_color = use_color is None or use_color is True

    def change_style(self, name_format, record):
        """
        Set color style.

        @param name_format: current format (_fmt of logging.Formatter instance).
        @param record: reference to logging.LogRecord.
        """
        if not self.use_color:
            return name_format

        time_format = SEQ_DTIME + '%(asctime)s' + SEQ_RESET
        name_format = name_format.replace('%(asctime)s', time_format)

        modu_format = SEQ_MNAME + '%(module)s' + SEQ_RESET
        name_format = name_format.replace('%(module)s', modu_format)

        dnum_format = SEQ_LINUM + '#%(lineno)d' + SEQ_RESET
        name_format = name_format.replace('#%(lineno)d', dnum_format)

        name = bold_name = record.levelname

        record.name = SEQ_GREEN + record.name + SEQ_RESET

        if record.levelno > logging.WARNING:
            bold_name = SEQ_BFONT + name

        if record.levelname in COLORS:
            colored_seq = SEQ_COLOR % (30 + COLORS[name])
            colored_name = colored_seq + bold_name + SEQ_RESET
            record.levelname = colored_name

        return name_format

    def format(self, record):
        """
        Format logging text and record level with colors

        @param record: reference to logging.LogRecord.
        """
        orig_format = self._fmt
        name_format = FORMATS.get(record.levelno, FORMATS['DEFAULT'])

        name_format = self.change_style(name_format, record)

        self._fmt = name_format  # pylint: disable=protected-access
        if hasattr(self, '_style') and hasattr(self._style, '_fmt'):
            self._style._fmt = name_format  # pylint: disable=protected-access
        # print('using format: {}', name_format)
        # print('module name: {} #{}'.format(record.name, record.lineno))
        result = logging.Formatter.format(self, record)
        self._fmt = orig_format

        return result
