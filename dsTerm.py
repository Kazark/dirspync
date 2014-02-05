'''
Author: Kazark
Purpose: Find terminal information.
For further info see dirspync-io.py
'''

__all__ = ['fill'] # TODO add

## Python
import os
import platform
from abc import abstractmethod, ABCMeta
from collections import namedtuple

from dsStr import fill as __fill
from dsStr import ellipsize

#class TermSize:
#    def __init__(self, rows, cols):
#        self.__rows = rows
#        self.__cols = cols
TermSize = namedtuple('TermSize', ('rows', 'cols'))

class Term:
    __metaclass__ = ABCMeta

    @abstractmethod
    def getSize(self) -> TermSize: pass

class LinuxTerm(Term):
    ## override
    def getSize(self) -> TermSize:
        return self._getSize(self._sttySize())

    def _getSize(self, sttySize:list) -> TermSize:
        try:
            return TermSize(int(sttySize[0]), int(sttySize[1]))
        except:
            return TermSize(25, 80)

    def _sttySize(self) -> list:
        return os.popen('stty size', 'r').read().split()

class WinTerm(Term):
    ## override
    def getSize(self) -> TermSize:
        # rows, columns
        return TermSize(25, 79)

class DefaultTerm(Term):
    ## override
    def getSize(self) -> TermSize:
        return TermSize(25, 80)

def getSystemTerm() -> Term:
    system = platform.system()
    if system == 'Linux':
        term = LinuxTerm()
    elif system == 'Windows':
        term = WinTerm()
    else:
        term = DefaultTerm()
    return term


dsWidths = namedtuple('dsWidths', ('name', 'size', 'time'))

def getFieldWidths(totalwidth : int) -> dsWidths:
    return dsWidths(totalwidth-32, 9, 23)

TERMINAL_COLUMNS = getSystemTerm().getSize().cols

class Formatter:
    def __init__(self, s:str=''):
        self.format = lambda: s

    def add(self, field, width):
        return Formatter(self.format() + "{0:{1}}".format(field, width))

ellipsizeName = (lambda f, prefix, width:
    ellipsize(('' if prefix==None else prefix)+f.name, width)
)

def formatFile (f, widths:dsWidths, prefix:str=None) -> str:
    return (Formatter().add(ellipsizeName(f, prefix, widths.name-1), widths.name)
        .add(f.size(), widths.size)
        .add(f.mtime(), widths.time)
    ).format()


fill = lambda s, ch: __fill(s, ch, TERMINAL_COLUMNS)
fancy = lambda f, prefix=None: formatFile(f, getFieldWidths(TERMINAL_COLUMNS), prefix)


