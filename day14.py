# adventofcode 2021
# crushallhumans
# puzzle 14
# 1/6/2022 - ?

import os
import re
import sys
import math
import time
import unittest
from copy import deepcopy

DEBUG = False

def one_star(param_set, steps = 10):
	print("---------------one_star--------------------")
	return execute(param_set, steps)

def two_star(param_set):
	print("---------------two_star--------------------")
	return execute(param_set,40)

def execute(param_set, steps):
	param_set = reprocess_input(param_set)

	start = param_set.pop(0)
	param_set.pop(0)
	element_map = {}
	for i in param_set:
		e = i.split(' -> ')
		element_map[e[0]] = e[1]

	c = 8888
	t0 = time.time()
	count = {}
	for i in range(0,len(start)-1):
		xx = "%s%s"%(start[i],start[i+1])
		count[xx] = 1
	if DEBUG: print(start,count)
	for i in range(0,steps):
		count = polymerize(start,element_map,i,count)
		if DEBUG: print (count)
		lencount = 0
		for j in count.keys():
			lencount += 2 * count[j]
		if DEBUG: print (i, (lencount/2)+1)
		if DEBUG: print(i,time.time()-t0)

	letter_counts = {}
	for i in count:
		a = i[0]
		b = i[1]
		if a not in letter_counts:
			letter_counts[a] = 0
		if b not in letter_counts:
			letter_counts[b] = 0
		letter_counts[a] += count[i]
		letter_counts[b] += count[i]
	for i in letter_counts:
		letter_counts[i] = math.ceil(letter_counts[i]/2)
	if DEBUG: print(letter_counts)

	lo = 999999999999999999
	hi = 0
	for i in letter_counts:
		if letter_counts[i] > hi:
			hi = letter_counts[i]
		if letter_counts[i] < lo:
			lo = letter_counts[i]
	return hi - lo

	# for j in count:
	# 	if j not in ['highest','highest_key','lowest','lowest_key']:
	# 		if count[j] > count['highest']:
	# 			count['highest'] = count[j]
	# 			count['highest_key'] = j
	# 		if count[j] <= count['lowest']:
	# 			count['lowest'] = count[j]
	# 			count['lowest_key'] = j
	#return count[count['highest_key']] - count[count['lowest_key']]


def reprocess_input(param_set):
	if isinstance(param_set,str):
		l = []
		l = [input_line.strip() for input_line in param_set.splitlines()]
		param_set = l
	return param_set	

def polymerize(s,m,step, count):
	#x = '' if len(s) < 10 else s[-10:]
	#print("%d --> %s..%s"%(step,s[0:10],x))
	c = 0
	l = len(s)
	r = ""

	ck = deepcopy(count)
	outer_adds = {}
	for i in ck:
		xs = ''
		x2 = ''
		r = ''
		if (i in m) and (ck[i] > 0):
			xs = "%s%s"%(i[0],m[i])
			x2 = "%s%s"%(m[i],i[1])
			if DEBUG: print(i,m[i],xs,x2)
			if xs not in count:
				count[xs] = 0
			if x2 not in count:
				count[x2] = 0
			if DEBUG: print("BEFORE -> ",i,count[i],xs,count[xs],x2,count[x2])
			count[xs] += ck[i]
			count[x2] += ck[i]
			if count[i] > 0:
				count[i] -= ck[i]
			if DEBUG: print("AFTERR -> ",i,count[i],xs,count[xs],x2,count[x2])

# 	for i in range(0,l-1):
# 		if c < l:
# 			e0 = s[i]
# 			e1 = s[i+1]
# 			e = "%s%s"%(e0,e1)
# 			#print(e)
# 			a = m[e]
# 			#print("(%s)"%a)
# 			r += "%s%s"%(e0,a)
# 			#print("-> ",r)
# 			if a not in count:
# 				count[a] = 0
# 			count[a] += 1
# #			for j in [e0,a]:
# 				#print("? ",j)
# #				if j not in count:
# #					count[j] = 0
# #				count[j] += 1
# 		c += 1
# #	r += "%s"%e1
# #	count[e1] += 1

	return count

def puzzle_text():
	print("""
--- Day 14: Extended Polymerization ---
The incredible pressures at this depth are starting to put a strain on your submarine. The submarine has polymerization equipment that would produce suitable materials to reinforce the submarine, and the nearby volcanically-active caves should even have the necessary input elements in sufficient quantities.

The submarine manual contains instructions for finding the optimal polymer formula; specifically, it offers a polymer template and a list of pair insertion rules (your puzzle input). You just need to work out what polymer would result after repeating the pair insertion process a few times.

For example:

NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
The first line is the polymer template - this is the starting point of the process.

The following section defines the pair insertion rules. A rule like AB -> C means that when elements A and B are immediately adjacent, element C should be inserted between them. These insertions all happen simultaneously.

So, starting with the polymer template NNCB, the first step simultaneously considers all three pairs:

The first pair (NN) matches the rule NN -> C, so element C is inserted between the first N and the second N.
The second pair (NC) matches the rule NC -> B, so element B is inserted between the N and the C.
The third pair (CB) matches the rule CB -> H, so element H is inserted between the C and the B.
Note that these pairs overlap: the second element of one pair is the first element of the next pair. Also, because all pairs are considered simultaneously, inserted elements are not considered to be part of a pair until the next step.

After the first step of this process, the polymer becomes NCNBCHB.

Here are the results of a few steps using the above rules:

Template:     NNCB
After step 1: NCNBCHB
After step 2: NBCCNBBBCBHCB
After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB
This polymer grows quickly. After step 5, it has length 97; After step 10, it has length 3073. After step 10, B occurs 1749 times, C occurs 298 times, H occurs 161 times, and N occurs 865 times; taking the quantity of the most common element (B, 1749) and subtracting the quantity of the least common element (H, 161) produces 1749 - 161 = 1588.

Apply 10 steps of pair insertion to the polymer template and find the most and least common elements in the result. What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?
""")



class testCase(unittest.TestCase):
	global DEBUG
	DEBUG = True

	test_set = ("""NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""
	)

	def test_one_star(self):
		self.assertEqual(
			one_star(
				self.__class__.test_set
			),
			1588
		)




if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		DEBUG = False
		filename_script = os.path.basename(__file__)
		print("---------------%s--------------------"%filename_script)
		filename = filename_script.split('.')[0]
		input_set = ()
		with open("/Users/crushing/Development/crushallhumans/adventofcode2021/inputs/2021/%s.txt" % filename) as input_file:
		    input_set = [input_line.strip() for input_line in input_file]
		ret = one_star(input_set.copy())
		print (ret)

		ret = two_star(input_set)
		print (ret)
