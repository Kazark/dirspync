'''
Author: Kazark
Purpose: Filesystem functions for DirSpync.
For further info see dirspync.py
'''

import shutil # file functions (copy, etc)
import os

from dsCmp import File

class SyncOps:
    def __init__(self, say, ask, err):
        self.say = say
        self.ask = ask
        self.err = err
        
    def ocopy(self, f, tu):
        '''tu -> the DIRECTORY to copy to
        f -> an object representing an individual file with .name string member
        and .path method.'''
        try:
            if os.path.isdir(f.path()):
                self.say('Copying directory: %s...' % f.name)
                shutil.copytree(f.path(), File(f.name, tu).path())
            else:
                self.say('Copying %s...' % f.name)
                shutil.copy2(f.path(), tu)
        except (OSError, IOError) as ex:
            self.err(ex)
            
    def ncopy(self, frum, tu):
        '''Copy the file from frum to tu.'''
        try:
            self.say('Copying %s...' % frum.name)
            shutil.copy2(frum.path(), tu.path())
        except (OSError, IOError) as ex:
            self.err(ex)
            
    def copystat(self, frum, tu):
        try:
            self.say('Copying stats of %s...' % frum.name)
            shutil.copystat(frum.path(), tu.path())
        except (OSError, IOError) as ex:
            self.err(ex)
            
    def delete(self, fpath):
        try:
            if os.path.isdir(fpath):
                if os.listdir(fpath):
                    q = 'Directory is not empty: %s. Permanently remove it? '
                else:
                    q = 'Permanently remove empty directory %s? '
                if self.ask(q % fpath):
                    self.say('Deleting %s...' % fpath)
                    shutil.rmtree(fpath) # TODO what about error handling?
            else:
                if self.ask("Permanently remove file: %s? " % fpath):
                    self.say('Deleting %s...' % fpath)
                    os.remove(fpath)
        except (OSError, IOError) as ex:
            self.err(ex)
            
