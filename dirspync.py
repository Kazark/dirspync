#!/usr/bin/python3
'''
Author: Kazark
Created: Aug 27 09
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
HELP = -2

class InteractiveDirectoryComparer:
    def __init__(self, dircmp):
        self.dircmp = dircmp
        self.sync = SyncOps(print, self.ask, print)
        self.cmds = {YES: ['y', 'Y'],
                     CPSTAT: ['cpstat', 'copystat'],
                     DEL: ['del', 'rm'],
                     EACH: ['askeach'],
                     EXIT: ['exit', 'q'],
                     HELP: ['?', 'help']}
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
        elif s in self.cmds[HELP]:
            print('y, Y - yes')
            print("cpstat, copystat - copy the file's stats but not its contents")
            print('del, rm - permanently delete the file')
            print('askeach - ask again for each file listed individually')
            print('exit, q - exit the program')
            print('?, help - print this message')
            print('<anything else> - no')
            return self.askcp(frum, tu, prompt)
        else:
            return NO
        
    def interactivelyCompare(self):
        mode = self.dircmp.mode
        if mode > INCLUDE_ALL + INTERACT:
            raise ValueError("invalid mode argument")
        print('Comparing ' + self.dircmp.union + '...') 
        dct = self.dircmp.compare()
        if dct[LO] or dct[LN] or dct[SA] or dct[SZ] or dct[RO] or dct[RN] or dct[DT]:
            print(fill('.%s ' % self.dircmp.union, self.sep1))
            if dct[LO]:
                self.left_only(dct, mode)
            if dct[LN]:
                self.left_newer(dct, mode)
            if dct[SA]:
                self.same(dct, mode)
            if dct[DT]:
                self.probably_same(dct, mode)
            if dct[SZ]:
                self.equal_dates_unequal_sizes(dct, mode)
            if dct[RN]:
                self.right_newer(dct, mode)
            if dct[RO]:
                self.right_only(dct, mode)
        for c in dct.children:
            InteractiveDirectoryComparer(c).interactivelyCompare()

    def left_newer(self, dct, mode):
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

    def same(self, dct, mode):
        print(fill('Equal datestamps, equal size: ', self.sep2))
        for lf, rf in dct[SA]:
            print(fancy(lf))
            print(fancy(rf))

    def probably_same(self, dct, mode):
        print(fill('Probably equivalent datestamps (?), equal size: ', self.sep2))
        for lf, rf in dct[DT]:
            print(fancy(lf))
            print(fancy(rf))

    def equal_dates_unequal_sizes(self, dct, mode): 
        print(fill('Equal datestamps, unequal sizes: ', self.sep2))
        for lf, rf in dct[SZ]:
            print(fancy(lf))
            print('%s size in byes: %d' % (self.dircmp.ldiff, lf.size()))
            print(fancy(rf))
            print('%s size in byes: %d' % (self.dircmp.rdiff, rf.size()))

    def right_newer(self, dct, mode):
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

    def right_only(self, dct, mode):
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

    def left_only(self, dct, mode):
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
    try:
        left, right = [Dir(os.path.abspath(d), '') for d in sys.argv[1:]]
    except ValueError:
        raise ValueError("invalid arguments")
    dcmp = InteractiveDirectoryComparer(DirCmp(DIFF_INTERACT, left, right))
    dcmp.interactivelyCompare()

if __name__ == '__main__':
    main()

