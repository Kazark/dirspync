#!/usr/bin/python3
'''
Author: Kazark
Created: Aug 27 09
Modified: Oct 8 11
Version: 1.8.1
Console interface to the DirSpync library.
'''

from dsCmp import *
from dsSync import SyncOps
from dsTerm import fancy, fill

INTERACT = 2**len(MODES)
DIFF_INTERACT = INTERACT | INCLUDE_DIFF

NO = 0
YES = 1
CPSTAT = 2
DEL = 3
EACH = 4
EXIT = -1

class ioDirCmp:
    def __init__(self, dircmp):
        self.dircmp = dircmp
        self.sync = SyncOps(print, self.ask, print)
        self.cmds = {YES: ['y'],
                     CPSTAT: ['cpstat', 'copystat'],
                     DEL: ['del', 'rm'],
                     EACH: ['askeach'],
                     EXIT: ['exit', 'q']}
        self.sep1 = '='
        self.sep2 = '-'
        
    def ask(self, msg):
        return input(msg) in self.cmds[YES]
    
    def askcp(self, frum, tu, prompt=None):
        prompt = 'Copy files from %s to %s? ' if prompt==None else str(prompt)
        s = input(prompt % (frum, tu))
        if s in self.cmds[YES]:
            return YES
        elif s in self.cmds[CPSTAT]:
            return CPSTAT
        elif s in self.cmds[DEL]:
            return DEL
        elif s in self.cmds[EACH]:
            return EACH
        elif s in self.cmds[EXIT]:
            raise SystemExit
        else:
            return NO
        
    def iocmp(self):
        ## TODO this funtion needs serious help
        mode = self.dircmp.mode ## yuck hack
        if mode > INCLUDE_ALL + INTERACT:
            raise ValueError("invalid mode argument")
        dct = self.dircmp.compare()
        if dct[LO] or dct[LN] or dct[SA] or dct[SZ] or dct[RO] or dct[RN] or dct[DT]:
            print(fill('.%s ' % self.dircmp.union, self.sep1))
            if dct[LO]:
                self.lo(dct, mode)
            if dct[LN]:
                self.ln(dct, mode)
            if dct[SA]:
                self.sa(dct, mode)
            if dct[DT]:
                self.dt(dct, mode)
            if dct[SZ]:
                self.sz(dct, mode)
            if dct[RN]:
                self.rn(dct, mode)
            if dct[RO]:
                self.ro(dct, mode)
        for c in dct.children:
            ioDirCmp(c).iocmp()

    def ln(self, dct, mode):
        print(fill('%s... newer: ' % self.dircmp.ldiff, self.sep2))
        for lf, rf in dct[LN]:
            print(fancy(lf, '> '))
            print(fancy(rf, '  '))
        if mode & INTERACT:
            cmd = self.askcp(self.dircmp.ldiff, self.dircmp.rdiff)
            if cmd == YES:
                for lf, rf in dct[LN]:
                    self.sync.ncopy(lf, rf)
            elif cmd == CPSTAT:
                for lf, rf in dct[LN]:
                    self.sync.copystat(lf, rf)

    def sa(self, dct, mode):
        print(fill('Equal datestamps, equal size: ', self.sep2))
        for lf, rf in dct[SA]:
            print(fancy(lf))
            print(fancy(rf))

    def dt(self, dct, mode):
        print(fill('Probably equivalent datestamps (?), equal size: ', self.sep2))
        for lf, rf in dct[DT]:
            print(fancy(lf))
            print(fancy(rf))

    def sz(self, dct, mode): 
        print(fill('Equal datestamps, unequal sizes: ', self.sep2))
        for lf, rf in dct[SZ]:
            print(fancy(lf))
            print('%s size in byes: %d' % (self.dircmp.ldiff, lf.size()))
            print(fancy(rf))
            print('%s size in byes: %d' % (self.dircmp.rdiff, rf.size()))

    def rn(self, dct, mode):
        print(fill('%s... newer: ' % self.dircmp.rdiff, self.sep2))
        for lf, rf in dct[RN]:
            print(fancy(lf, '  '))
            print(fancy(rf, '> '))
        if mode & INTERACT:
            cmd = self.askcp(self.dircmp.rdiff, self.dircmp.ldiff)
            if cmd == YES:
                for lf, rf in dct[RN]:
                    self.sync.ncopy(rf, lf)
            elif cmd == CPSTAT:
                for lf, rf in dct[RN]:
                    self.sync.copystat(rf, lf)

    def ro(self, dct, mode):
        print(fill('%s... only: ' % self.dircmp.rdiff, self.sep2))
        for f in dct[RO]:
            print(fancy(f))
        if mode & INTERACT:
            cmd = self.askcp(self.dircmp.rdiff, self.dircmp.ldiff)
            if cmd == YES:
                for f in dct[RO]:
                    self.sync.ocopy(f, self.dircmp.l.path())
            elif cmd == DEL:
                for f in dct[RO]:
                    self.sync.delete(f.path())
            elif cmd == EACH:
                for f in dct[RO]:
                    cmd = self.askcp(f.path(), self.dircmp.ldiff)
                    if cmd == YES:
                        self.sync.ocopy(f,  self.dircmp.l.path())
                    elif cmd == DEL:
                        self.sync.delete(f.path())

    def lo(self, dct, mode):
        print(fill('%s... only: ' % self.dircmp.ldiff, self.sep2))
        for f in dct[LO]:
            print(fancy(f))
        if mode & INTERACT:
            cmd = self.askcp(self.dircmp.ldiff, self.dircmp.rdiff)
            if cmd == YES:
                for f in dct[LO]:
                    self.sync.ocopy(f, self.dircmp.r.path())
            elif cmd == DEL:
                for f in dct[LO]:
                    self.sync.delete(f.path())
            elif cmd == EACH:
                for f in dct[LO]:
                    cmd = self.askcp(f.path(), self.dircmp.rdiff)
                    if cmd == YES:
                        self.sync.ocopy(f, self.dircmp.r.path())
                    elif cmd == DEL:
                        self.sync.delete(f.path())
    
def main():
    import sys
    import os
    mode = sys.argv[1]
    if mode == 'all':
        mode = INCLUDE_ALL
    elif mode == 'diff':
        mode = INCLUDE_DIFF
    elif mode == 'interact':
        mode = DIFF_INTERACT
    else:
        mode = int(mode)
    try:
        l, r = [Dir(os.path.abspath(d), '') for d in sys.argv[2:]]
    except ValueError:
        raise ValueError("invalid arguments")
    dcmp = ioDirCmp(DirCmp(mode, l, r))
    dcmp.iocmp()

if __name__ == '__main__':
    main()

