'''
Author: Kazark
Purpose: Directory synchronization operations
For further info see dirspync.py
'''

__all__ = ['Dir', 'File', 'Time', 'fSize', 'DirCmp', 'diffNode',
           'LO', 'LN', 'SA', 'RN', 'RO', 'SZ', 'DT',
           'INCLUDE_ALL', 'INCLUDE_DIFF', 'MODES']

MODES = [LO, LN, SA, RN, RO, SZ, DT] = [2**n for n in range(7)]

INCLUDE_ALL = sum(MODES)
INCLUDE_DIFF = INCLUDE_ALL - SA - DT

#import cmd # for building an interactive shell
#import getopt # for parsing cmdline options--better builtin doc than optparse
import os
import time
import math # the logarithmic function used in file size string formatting
import hashlib

from dsStr import minusstr, ellipsize
DIRSEP = os.path.sep

class File:
    def __init__(self, name, prefix):
        self.name = name.rstrip(DIRSEP)
        self.prefix = prefix.rstrip(DIRSEP)
    
    def __format__(self, format_spec):
        return format(self.name, format_func)
        
    def path(self):
        return self.prefix + DIRSEP*(bool(self.prefix)) + self.name
        
    def mtime(self):
        return Time(os.stat(self.path()).st_mtime)
        
    def size(self):
        return fSize(os.stat(self.path()).st_size)

    # Thanks to Nathan Feger http://stackoverflow.com/a/11143944/834176
    def md5sum(self):
        md5 = hashlib.md5()
        with open(self.path(), 'rb') as f:
            for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
                md5.update(chunk)
        return md5.hexdigest()
        
class Dir(dict, File):
    def __init__(self, name, prefix):
        dict.__init__(self)
        File.__init__(self, name, prefix)
        self.subds = dict()
        
    def refresh(self, showdot=False, showtilde=False):
        try:
            names = os.listdir(self.path())
        except OSError as ex:
            print(ex)
            raise SystemExit
        self.subds = dict()
        for name in names:
            if (not showdot) and name.startswith('.'): continue
            if (not showtilde) and name.endswith('~'): continue
            if os.path.isdir(self.path()+DIRSEP+name):
                self.subds[name] = Dir(name, self.path())
            else:
                self[name] = File(name, self.path())
        
    def size(self):
        self.refresh()
        return fSize(sum([f.size() for f in self.values()]) + File.size(self) +\
                     sum([d.size() for d in self.subds.values()]))

class MetaDir:
    def __init__(self, name, subds=None):
        self.name = str(name)
        if subds==None:
            self.subds = dict()
        else:
            self.setsubds(subds)
        
    def setsubds(self, subds):
        for d in subds:
            self.subds[d] = Dir(d)
        
class Time(float):
    def __str__(self):
        return str(fTime(time.localtime(self)))
    def __format__(self, format_spec):
        return format(str(self), format_spec)

class fTime:
    def __init__(self, localtime):
        self.dayOfWeek = fDayOfWeek(localtime)
        self.dayOfYear = fDayOfYear(localtime)
        self.timeOfDay = fTimeOfDay(localtime)
    def __str__(self):
        return "{0} {1} {2}".format(self.dayOfWeek, self.dayOfYear, self.timeOfDay)
    def __format__(self, format_spec):
        return format(str(self), format_spec)
        
class fDayOfWeek:
    def __init__(self, localtime):
        self.__day = localtime.tm_wday
    def __str__(self):
        return ['Mon', 'Tue', 'Wed', 'Th', 'Fri', 'Sat', 'Sun'][self.__day]
    def __format__(self, format_spec):
        return format(str(self), format_spec)

class fDayOfYear:
    def __init__(self, localtime):
        self.__year = localtime.tm_year
        self.__month = localtime.tm_mon
        self.__day = localtime.tm_mday
    def __str__(self):
        return "{0}/{1}/{2}".format(self.__year, self.__month, self.__day)
    def __format__(self, format_spec):
        return format(str(self), format_spec)

class fTimeOfDay:
    def __init__(self, localtime):
        self.__hour = localtime.tm_hour
        self.__min = localtime.tm_min
        self.__sec = localtime.tm_sec
    def __str__(self):
        return "{0}:{0:02}:{0:02}".format(self.__hour, self.__min, self.__sec)
    def __format__(self, format_spec):
        return format(str(self), format_spec)

class fSize(int):
    def __new__(cls, size):
        return int.__new__(cls, size)

    def __init__(self, size, k=1024):
        self.k = k

    def trunk(self):
        return self/self.k**self._pwr()

    def _pwr(self):
        return 0 if self == 0 else int(math.log(self) / math.log(self.k)) 

    def suffix(self):
        return ['B', 'K', 'M', 'G', 'T', 'P'][self._pwr()]
    
    def __format__(self, format_spec):
        return format(str(self), format_spec)

    def __str__(self):
        return '{0:4.2f}{1}'.format(self.trunk(), self.suffix())

    def __format__(self, format_spec):
        return format(str(self), format_spec)
    
class FileComparer:
    def __init__(self, dterr=1):
        self.dterr = dterr

    def compare(self, lf, rf):
        return self.__compare(lf.mtime(), rf.mtime(), lf.size(), rf.size(), lf.md5sum(), rf.md5sum())

    def __compare(self, lt, rt, ls, rs, lhash, rhash):
        absdiff = abs(lt-rt)
        if (absdiff<=self.dterr) and ls == rs:
            return SA
        elif (absdiff%3600==0 or absdiff%3600==self.dterr or absdiff%3600==3600-self.dterr) and ls == rs and absdiff<(3600*24):
            return DT
        elif lt==rt and ls != rs: # Same timestamp, different size
            # requires special user attention
            return SZ
        elif lhash == rhash:
            return SA # TODO these two-letters constants are awful...
        elif lt > rt: # LEFT NEWER
            return LN
        elif lt < rt: # RIGHT NEWER
            return RN
        # no else
        
class DirCmp:
    def __init__(self, mode, ldir, rdir, *args, **kwargs):
        '''ldir and rdir should be Dir objects'''
        self.mode = mode
        self.fcmp = FileComparer()
        self.args, self.kwargs = args, kwargs
        self.l = ldir
        self.r = rdir
        self.union = self.pathunion(self.l.path(), self.r.path())
        self.ldiff = minusstr(self.l.path(), self.union)
        self.rdiff = minusstr(self.r.path(), self.union)
        
    def pathunion(self, str1:str, str2:str) -> str:
        s = ''
        for i1, i2 in zip(reversed(str1.split(DIRSEP)), reversed(str2.split(DIRSEP))):
            if i2 == i1:
                s = DIRSEP + i1 + s
            else: break
        return s
    
    def refresh(self):
        self.l.refresh(*self.args, **self.kwargs)
        self.r.refresh(*self.args, **self.kwargs)

    def compare(self):
        self.refresh()
        dct = diffNode(self.mode)
               
        if len(self.l) == 0:
            dct[RO] += self.r.values()
        elif len(self.r) == 0:
            dct[LO] += self.l.values()
        else:
            for lf in self.l.values():
                try:
                    rf = self.r.pop(lf.name)
                except KeyError:
                    dct[LO].append(lf)
                else:
                    dct[self.fcmp.compare(lf, rf)].append((lf, rf))
            dct[RO] += self.r.values()
        if len(self.l.subds) == 0:
            dct[RO] += self.r.subds.values()
        elif len(self.r.subds) == 0:
            dct[LO] += self.l.subds.values()
        else:
            for ld in self.l.subds.values():
                try:
                    rd = self.r.subds.pop(ld.name)
                except KeyError:
                    dct[LO].append(ld)
                else:
                    dct.children.append(self.__class__(self.mode, ld, rd))
            dct[RO] += self.r.subds.values()
        return dct

class diffNode(dict):
    def __init__(self, mode):
        dict.__init__(self)
        self.mode = mode
        for i in MODES:
            self[i] = list()
        self.children = list()
        
    def __getitem__(self, k):
        if k in MODES and not self.mode & k:
            return list()
        else:
            return dict.__getitem__(self, k)
