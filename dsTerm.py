'''
Author: Kazark
Purpose: Find terminal information.
For further info see dirspync-io.py
'''

__all__ = ['fill'] # TODO add

## Python
import os
import platform
from collections import namedtuple

from dsStr import fill as __fill
from dsStr import ellipsize

TermSize = namedtuple('TermSize', ('rows', 'cols'))

# TODO consolidate these classes
# TODO make use of the fact that the real reason Windows is
# TODO defaulted to 79 is because of os.linesep
# TODO Note also that this does not cover use of ConEmu etc
# TODO under Windows.
# TODO make more use of dependency injection and less OO

class LinuxTerm:
    def __init__(self, sttySize):
        self._sttySize = sttySize

    def getSize(self) -> TermSize:
        return self._getSize(self._sttySize())

    def _getSize(self, sttySize:list) -> TermSize:
        try:
            return TermSize(int(sttySize[0]), int(sttySize[1]))
        except:
            return TermSize(25, 80)

class WinTerm:
    def getSize(self) -> TermSize:
        return TermSize(25, 79)

class DefaultTerm:
    def getSize(self) -> TermSize:
        return TermSize(25, 80)

sttySize = lambda: os.popen('stty size', 'r').read().split()

def getSystemTerm():
    system = platform.system()
    if system == 'Linux':
        term = LinuxTerm(sttySize)
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


