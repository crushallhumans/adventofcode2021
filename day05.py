# adventofcode 2021
# crushallhumans
# puzzle 5
# 12/5/2021

import os
import re
import sys
import json
import math
import unittest

DEBUG = False

class CartesianTheater():
	max_x = -1
	max_y = -1
	points = {}
	inited = False
	def __init__(self):
		self.max_x = -1
		self.max_y = -1
		self.points = {}
		self.inited = False

	def __str__(self):
		if not self.inited:
			return "need at least one segment"

		s = ''
		for i in range(0,self.max_y+1):
			for j in range(0,self.max_x+1):
				match = "%d,%d"%(j,i)
				if match in self.points.keys():
					s += str(self.points[match])
				else:
					s += '.'
			s += "\n"
		s += "\n"
		s += json.dumps(self.points)

		return s

	def add_segment(self, segment, consider_diagonals = False):
		# ignore diagonals
		if consider_diagonals or (segment[0] == segment[2]) or (segment[1] == segment[3]):

			if DEBUG: print ("segments: ",segment)

			if (segment[0] > self.max_x):
				self.max_x = segment[0]
			if (segment[2] > self.max_x):
				self.max_x = segment[2]

			if (segment[1] > self.max_y):
				self.max_y = segment[1]
			if (segment[3] > self.max_y):
				self.max_y = segment[3]

			len_x = segment[2] - segment[0]
			len_y = segment[3] - segment[1]
			if DEBUG: print ("lengths: ",len_x,len_y)

			inclusive_x = 1 if len_x > 0 else -1
			inclusive_y = 1 if len_y > 0 else -1

			sequence_x = [segment[0]] if len_x == 0 else list(range(segment[0], segment[2]+inclusive_x, 1 if len_x > 0 else -1))
			sequence_y = [segment[1]] if len_y == 0 else list(range(segment[1], segment[3]+inclusive_y, 1 if len_y > 0 else -1))

			if DEBUG: print ("sequences: ",sequence_x,sequence_y)

			points = []
			#45deg diagonal
			if len(sequence_x) == len(sequence_y):
				for i in range(0,len(sequence_x)):
					match = "%d,%d" % (sequence_x[i],sequence_y[i])
					points.append(match)
			#straight
			else:
				for i in sequence_x:
					for j in sequence_y:
						match = "%d,%d" % (i,j)
						points.append(match)

			for i in points:
				if DEBUG: print(i)
				if i in self.points.keys():
					self.points[i] += 1
				else:
					self.points[i] = 1

			self.inited = True

	def score(self):
		score = 0
		for i in self.points.keys():
			if self.points[i] > 1:
				score += 1
		return score


def one_star(param_set):
	param_set = reprocess_input(param_set)
	param_set = parse_lines_into_points(param_set)
	cart = CartesianTheater()

	for i in param_set:
		cart.add_segment(i)

	if DEBUG: print(cart)

	c = cart.score()
	return c


def two_star(param_set):
	param_set = reprocess_input(param_set)
	param_set = parse_lines_into_points(param_set)
	cart = CartesianTheater()

	for i in param_set:
		cart.add_segment(i, True)

	if DEBUG: print(cart)

	c = cart.score()
	return c

def reprocess_input(param_set):
	if isinstance(param_set,str):
		l = []
		l = [input_line.strip() for input_line in param_set.splitlines()]
		param_set = l
	return param_set	

def parse_lines_into_points(param_set):
	reparse = re.compile(r'^(\d+),(\d+) -> (\d+),(\d+)$')

	new_param_set = []
	for i in param_set:
		m = reparse.match(i)
		lst = map(lambda x: int(x), m.groups())
		new_param_set.append(list(lst))

	return new_param_set


def puzzle_text():
	print("""
--- Day 5: Hydrothermal Venture ---
You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. In other words:

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....
In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two lines overlap?


--- Part Two ---
Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:

An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....
You still need to determine the number of points where at least two lines overlap. In the above example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?
""")



class testCase(unittest.TestCase):
	global DEBUG
	DEBUG = True

	test_set = ("""0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
	)

	def test_one_star(self):
		self.assertEqual(
			one_star(
				self.__class__.test_set
			),
			5
		)

	def test_two_star(self):
		self.assertEqual(
			two_star(
				self.__class__.test_set
			),
			12
		)



if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		DEBUG = False
		filename_script = os.path.basename(__file__)
		print (filename_script)
		filename = filename_script.split('.')[0]
		input_set = ()
		with open("/Users/crushing/Development/crushallhumans/adventofcode2021/inputs/2021/%s.txt" % filename) as input_file:
		    input_set = [input_line.strip() for input_line in input_file]
		ret = one_star(input_set)
		print (ret)

		ret = two_star(input_set)
		print (ret)
