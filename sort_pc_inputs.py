from collections import defaultdict
import re
import sys

# This file will read in the '...inputs=...' line of a single PC from stdin and rewrite it, sorted,
# with duplicates removed, to stdout. Good for merging PC's or just reorganizing them.

# suggested use: echo "verb-pc00_inputs=verb1, verb2,..." | python3 sort_pc_inputs.py

SPLIT_CHAR = ','
PATTERN = r'\s*(\D+)(\d+)\s*'

def sort_pc_inputs(in_stream=sys.stdin, out_stream=sys.stdout):
	fprint = lambda *x, **y: print(*x, file=out_stream, **y)
	for line in in_stream:
		pc_inputs = defaultdict(set) # format: { prefix : set(1, 2, 5, ...) }
		elts = line.strip().split(',')
		for elt in elts:
			grps = re.match(PATTERN, elt).groups()
			pc_inputs[grps[0]].add(int(grps[1]))

		sorted_pc_inputs = sorted({ k : sorted(v) for k,v in pc_inputs.items() }.items(), key=lambda x: x[0])
		fprint(*[f'{prefix}{idx}' for prefix, idxs in sorted_pc_inputs for idx in idxs], sep=', ')

def main():
	sort_pc_inputs()

if __name__ == '__main__':
	main()
