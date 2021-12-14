# adventofcode 2021
# crushallhumans
# puzzle 13
# 12/13/2021

import os
import re
import sys
import math
import json
import unittest

DEBUG = False

def puzzle(param_set,return_after_one = True):
	param_set = reprocess_input(param_set)

	folds = []
	find_folds = True
	fold_sig = 'fold along '
	while find_folds:
		f = param_set.pop()
		try:
			if f.index(fold_sig) == 0:
				folds.insert(0,f)
			else:
				find_folds = False
		except:
			find_folds = False

	C = CartesianTheater()
	for i in param_set:
		C.add_point(i)

	for i in folds:
		C.add_fold(i)		

	C.build_rows_and_cols_from_points()

	print(C.folds)

	return C.do_folds(return_after_one)

def one_star(param_set):
	print("---------------one_star--------------------")
	return puzzle(param_set)


def two_star(param_set):
	print("---------------two_star--------------------")
	return puzzle(param_set,False)

def reprocess_input(param_set):
	if isinstance(param_set,str):
		l = []
		l = [input_line.strip() for input_line in param_set.splitlines()]
		param_set = l
	return param_set	

class CartesianTheater():
	max_x = -1
	max_y = -1
	points = {}
	inited = False
	rows = []
	cols = []
	folds = []
	folded_points = []
	def __init__(self):
		self.max_x = 0
		self.max_y = 0
		self.points = {}
		self.rows = []
		self.cols = []
		self.folds = []
		self.folded_points = []
		self.inited = False

	def __str__(self):
		if not self.inited:
			return "need at least one row or point"

		print_points = self.points
		# if len(folded_points) > 0:
		# 	print_points = folded_points[-1]

		s = ''
		for i in range(0,self.max_y+1):
			for j in range(0,self.max_x+1):
				match = "%d,%d"%(j,i)
				if match in print_points.keys():
					s += '#'
				else:
					s += '.'
			s += "\n"
		s += "\n"
		if DEBUG: s += json.dumps(print_points)

		return s

	def add_row(self,i):
		self.rows.append(list(i))
		if not self.max_x:
			self.max_x = len(list(i))
		self.max_y += 1
		self.inited = True

	def add_point(self,i):
		s = i.split(',')
		if len(s) > 1:
			self.points[i] = '#'
			#print (s)
			if int(s[0]) > self.max_x:
				self.max_x = int(s[0])
			if int(s[1]) > self.max_y:
				self.max_y = int(s[1])
			self.inited = True

	def build_cols(self):
		for i in range(0,self.max_x+1):
			col = []
			for j in self.rows:
				col.append(j[i])
			self.cols.append(col)
		c = 0

	def build_points(self):
		for i in self.cols:
			d = 0
			for j in i:
				self.points["%d,%d"%(c,d)] = j
				d += 1
			c += 1

	def build_rows_and_cols_from_points(self, prev_max_x = 0, prev_max_y = 0):
		if prev_max_y > 0:
			self.max_y = prev_max_y
		if prev_max_x > 0:
			self.max_x = prev_max_x
		#width = 0
		for i in range(0,self.max_y+1):
			row = []
			for j in range(0,self.max_x+1):
				match = "%d,%d"%(j,i)
				if match in self.points.keys():
					row.append('#')
				else:
					row.append('.')
			# print('!!! ',j,prev_max_x)
			# if j < prev_max_x:
			# 	for jj in range(j,prev_max_x):
			# 		row.append('.')
			self.rows.append(row)
			width = len(row)
		# print('??? ',i,prev_max_y)
		# if i < prev_max_y:
		# 	for ii in range(i,prev_max_y):
		# 		self.rows.append(['.']*width)
		self.build_cols()
		if DEBUG: print(self)


	def add_fold(self,i):
		s = i.split('fold along ')
		ss = s[1].split('=')
		self.folds.append(ss)

	def do_folds(self, return_after_one = True):
		c = 0
		ret = 0
		Cf = self
		for i in self.folds:
			if c == 0:
				Cf = Cf.do_fold(i)
				if return_after_one:
					print("return_after_one")
					return len(Cf.points.keys())
					break
			else:
				print('folding inner',i)
				print(Cf)
				Cf = Cf.do_fold(i)
				print(Cf)
			c += 1
		return len(Cf.points.keys())

	def do_fold(self,fold):
		points = {}
		if DEBUG: print(fold)
		axis = int(fold[1])
		operating_grid = self.cols #assume y
		prev_max_x = self.max_x
		prev_max_y = axis-1

		if fold[0] == 'x':
			if DEBUG: print ("using rows")
			operating_grid = self.rows
			prev_max_x = axis-1
			prev_max_y = self.max_y
			if self.max_x != axis*2:
				raise Exception("bad x axis: ",self.max_x,axis)
		else:
			if self.max_y != axis*2:
				raise Exception("bad y axis: ",self.max_y,axis)



		new_points = {}


		#if DEBUG: print(len(operating_grid))
		for i in range(0,len(operating_grid)):
			ii = operating_grid[i]
			#if DEBUG: print(i,ii)
			k = 0
			#if DEBUG: print(len(ii))
			for j in range(len(ii)-1,axis,-1):
				jj = ii[j]
				kk = ii[k]
				#if DEBUG: print(jj,kk," ",end='')
				idx = "%d,%d"%(i,k)
				if fold[0] == 'x':
					idx = "%d,%d"%(k,i)
				if jj != '.' or kk != '.' :
					new_points[idx] = '#'
					#if DEBUG: print("%s = %s "%(idx,new_points[idx]),end='')
				#else:
					#if DEBUG: print("%s = %s "%(idx,'.'),end='')
				k += 1
				#if DEBUG: print("")
			#if DEBUG: print("")

		Cf = CartesianTheater()
		for i in new_points.keys():
			Cf.add_point(i)
		Cf.build_rows_and_cols_from_points(prev_max_x, prev_max_y)
		if DEBUG: print("new cf!")
		#print(Cf)
		#self.folded_points.append(Cf)
		return Cf


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

def puzzle_text():
	print("""--- Day 13: Transparent Origami ---
You reach another volcanically active part of the cave. It would be nice if you could do some kind of thermal imaging so you could tell ahead of time which caves are too hot to safely enter.

Fortunately, the submarine seems to be equipped with a thermal camera! When you activate it, you are greeted with:

Congratulations on your purchase! To activate this infrared thermal imaging
camera system, please enter the code found on page 1 of the manual.
Apparently, the Elves have never used this feature. To your surprise, you manage to find the manual; as you go to open it, page 1 falls out. It's a large sheet of transparent paper! The transparent paper is marked with random dots and includes instructions on how to fold it up (your puzzle input). For example:

6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
The first section is a list of dots on the transparent paper. 0,0 represents the top-left coordinate. The first value, x, increases to the right. The second value, y, increases downward. So, the coordinate 3,0 is to the right of 0,0, and the coordinate 0,7 is below 0,0. The coordinates in this example form the following pattern, where # is a dot on the paper and . is an empty, unmarked position:

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........
Then, there is a list of fold instructions. Each instruction indicates a line on the transparent paper and wants you to fold the paper up (for horizontal y=... lines) or left (for vertical x=... lines). In this example, the first fold instruction is fold along y=7, which designates the line formed by all of the positions where y is 7 (marked here with -):

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
-----------
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........
Because this is a horizontal line, fold the bottom half up. Some of the dots might end up overlapping after the fold is complete, but dots will never appear exactly on a fold line. The result of doing this fold looks like this:

#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........
Now, only 17 dots are visible.

Notice, for example, the two dots in the bottom left corner before the transparent paper is folded; after the fold is complete, those dots appear in the top left corner (at 0,0 and 0,1). Because the paper is transparent, the dot just below them in the result (at 0,3) remains visible, as it can be seen through the transparent paper.

Also notice that some dots can end up overlapping; in this case, the dots merge together and become a single dot.

The second fold instruction is fold along x=5, which indicates this line:

#.##.|#..#.
#...#|.....
.....|#...#
#...#|.....
.#.#.|#.###
.....|.....
.....|.....
Because this is a vertical line, fold left:

#####
#...#
#...#
#...#
#####
.....
.....
The instructions made a square!

The transparent paper is pretty big, so for now, focus on just completing the first fold. After the first fold in the example above, 17 dots are visible - dots that end up overlapping after the fold is completed count as a single dot.

How many dots are visible after completing just the first fold instruction on your transparent paper?


--- Part Two ---
Finish folding the transparent paper according to the instructions. The manual says the code is always eight capital letters.

What code do you use to activate the infrared thermal imaging camera system?""")



class testCase(unittest.TestCase):
	global DEBUG
	DEBUG = True

	test_set = ("""6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""")

	def test_one_star(self):
		self.assertEqual(
			one_star(
				self.__class__.test_set
			),
			17
		)

	def test_two_star(self):
		self.assertEqual(
			two_star(
				self.__class__.test_set
			),
			16
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

		ret = two_star(input_set.copy())
		print (ret)
