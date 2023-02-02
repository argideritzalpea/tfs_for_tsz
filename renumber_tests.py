import re
import sys

# This file will read in testsuites from stdin and rewrite them, correctly numbered, to stdout
# note: may not work unless every suite has some number to begin with, so just add some number to
# everything before running this

# suggested use: cat testsuite.txt | python3 renumber_tests.py > testsuite_new.txt
# (probably best to not  overwrite the old testsuites unless they're backed up, until you've validated
# the changes)

PATTERN = r'(?:\s*#\s*\d+\b)(.*)'

def renumber(in_stream=sys.stdin, out_stream=sys.stdout, idx=1):
	fprint = lambda *x, **y: print(*x, file=out_stream, **y)
	for line in in_stream:
		line = line.strip()
		if line.startswith('#'):
			grps = re.match(PATTERN, line).groups()
			fprint(f'#{idx}', grps[0], sep='')
			idx += 1
		else:
			fprint(line)

def main():
	renumber()

if __name__ == '__main__':
	main()

