"""
Entry-point module, in case you use `python -m rhenvision_changelog`.
Why does this file exist, and why `__main__`? For more info, read:
- https://www.python.org/dev/peps/pep-0338/
- https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""

import sys
from rhenvision_changelog.cli import write_changelog, run_check_commit

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'commit-check':
        sys.exit(run_check_commit(sys.argv[1:]))
    else:
        sys.exit(write_changelog(sys.argv[1:]))
