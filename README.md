# Dirspync
## DIRectory SYNCing tool written in PYthon

This command-line tool is not your standard backup program, though it can be
used to back up. It allows you to easily synchronize files across multiple
directories (usually on different devices) while still retaining fine-grained
control over which files are copied where. Unlike most backup tools, which are
designed to run automatically in the background, this runs only when you invoke
it, and requests your approval before it does anything. I have used this to back
up to external hard drives or thumbdrives and over the network with SSHFS.

This is a tool I wrote when I was a much less experienced programmer and much of
it is legacy code, though I have recently begun to revisit it. It still needs a
lot more automated testing, refactoring and documentation.
