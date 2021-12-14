# adventofcode 2021
# crushallhumans
# puzzle N
# 12/n/2021

import os
import re
import sys
import math
import json
import unittest

DEBUG = False

def puzzle(param_set, allows_doubled_small = False):
	param_set = reprocess_input(param_set)
	c = 8888
	d = DAG()
	d.allows_doubled_small = allows_doubled_small
	for i in param_set:
		d.add_connection(i)
	paths = d.find_paths()
	return len(paths)

def one_star(param_set):
	print("---------------one_star--------------------")
	return puzzle(param_set)

def two_star(param_set):
	print("---------------two_star--------------------")
	return puzzle(param_set, True)

def reprocess_input(param_set):
	if isinstance(param_set,str):
		l = []
		l = [input_line.strip() for input_line in param_set.splitlines()]
		param_set = l
	return param_set	

class DAG:
	caves = {}
	connects = []
	paths = []
	allows_doubled_small = False

	def __init__(self):
		self.caves = {}
		self.paths = []
		self.connects = []
		self.allows_doubled_small = False

	def add_connection(self,i):
		a = i.split('-')
		for j in range(0,2):
			cave = a[j]
			if a[j] not in self.caves:
				self.caves[cave] = []
		z = [[0,1],[1,0]]
		for i in z:
			if self.caves[a[i[0]]] not in self.caves[a[i[1]]]:	
 				self.caves[a[i[1]]].append(a[i[0]])

	def find_paths(self, start = 'start', end = 'end', path = [], depth = 0):
		if start not in self.caves:
			raise Exception("No such cave: ",start)
		if end not in self.caves:
			raise Exception("No such cave: ",end)

		path = path + [start]

		if DEBUG: print ("\t"*depth,start,self.caves[start], path)

		if start == end:
			return [path]

		all_paths = []
		for i in self.caves[start]:
			equal_small = False
			if self.allows_doubled_small:
				total_small = 0
				keys_small = {}
				for j in path:
					if j.lower() == j:
						total_small += 1
						keys_small[j] = True
				if DEBUG: print ("\t"*(depth+2),' ! ',total_small,len(keys_small.keys()))
				if total_small == len(keys_small.keys()) and (total_small > 0):
					equal_small = True
				else:
					equal_small = False

			if DEBUG: print ("\t"*(depth+1),i, '' if equal_small else 'False')

			if (
				i.upper() == i or 	# can always traverse into an uppercase cave
				i not in path or 	# can always traverse into a new (in-path) cave
				(
					self.allows_doubled_small and 	# allowing one doubled small cave
					equal_small == True and			# doubled not yet used
					i != 'start'					# can't double the start cave
				)
			):
				append_paths = self.find_paths(i,end,path,depth+1)
				for j in append_paths:
					if j not in all_paths:
						all_paths.append(j)

		return all_paths

def puzzle_text():
	print("""--- Day 12: Passage Pathing ---
With your submarine's subterranean subsystems subsisting suboptimally, the only way you're getting out of this cave anytime soon is by finding a path yourself. Not just a path - the only way to know if you've found the best path is to find all of them.

Fortunately, the sensors are still mostly working, and so you build a rough map of the remaining caves (your puzzle input). For example:

start-A
start-b
A-c
A-b
b-d
A-end
b-end
This is a list of how all of the caves are connected. You start in the cave named start, and your destination is the cave named end. An entry like b-d means that cave b is connected to cave d - that is, you can move between them.

So, the above cave system looks roughly like this:

    start
    /   \
c--A-----b--d
    \   /
     end
Your goal is to find the number of distinct paths that start at start, end at end, and don't visit small caves more than once. There are two types of caves: big caves (written in uppercase, like A) and small caves (written in lowercase, like b). It would be a waste of time to visit any small cave more than once, but big caves are large enough that it might be worth visiting them multiple times. So, all paths you find should visit small caves at most once, and can visit big caves any number of times.

Given these rules, there are 10 paths through this example cave system:

start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end
(Each line in the above list corresponds to a single path; the caves visited by that path are listed in the order they are visited and separated by commas.)

Note that in this cave system, cave d is never visited by any path: to do so, cave b would need to be visited twice (once on the way to cave d and a second time when returning from cave d), and since cave b is small, this is not allowed.

Here is a slightly larger example:

dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
The 19 paths through it are as follows:

start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end
Finally, this even larger example has 226 paths through it:

fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
How many paths through this cave system are there that visit small caves at most once?


--- Part Two ---
After reviewing the available paths, you realize you might have time to visit a single small cave twice. Specifically, big caves can be visited any number of times, a single small cave can be visited at most twice, and the remaining small caves can be visited at most once. However, the caves named start and end can only be visited exactly once each: once you leave the start cave, you may not return to it, and once you reach the end cave, the path must end immediately.

Now, the 36 possible paths through the first example above are:

start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,end
start,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,end
start,b,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end
The slightly larger example above now has 103 paths through it, and the even larger example now has 3509 paths through it.

Given these new rules, how many paths through this cave system are there?""")



class testCase(unittest.TestCase):
	global DEBUG
	DEBUG = True

	test_set = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

	def test_one_star(self):
		self.assertEqual(
			one_star(
				self.__class__.test_set
			),
			10
		)


	def test_one_star_19(self):
		self.assertEqual(
			one_star("""dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
			),
			19
		)

	def test_one_star_226(self):
		self.assertEqual(
			one_star("""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""
			),
			226
		)




	def test_two_star(self):
		self.assertEqual(
			two_star(
				self.__class__.test_set
			),
			36
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
		ret = one_star(input_set)
		print (ret)

		ret = two_star(input_set)
		print (ret)
