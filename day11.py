# adventofcode 2021
# crushallhumans
# puzzle 11
# 12/11/2021

import os
import re
import sys
import math
import unittest

DEBUG = False

def puzzle(param_set, star = "one", steps = 100):
	param_set = reprocess_input(param_set)
	L = Life()
	for i in param_set:
		L.add_row(i)
	L.build_cols_and_points()
	print(L)
	L.advance_steps(steps)
	return len(L.flashes[-1])

def one_star(param_set, steps = 100):
	return puzzle(param_set,"one", steps)


def two_star(param_set, steps = 100):
	param_set = reprocess_input(param_set)
	#return puzzle(param_set,"two", steps)
	c = 7777
	for i in param_set:
		continue
	return c

def reprocess_input(param_set):
	if isinstance(param_set,str):
		l = []
		l = [input_line.strip() for input_line in param_set.splitlines()]
		param_set = l
	return param_set	

class Life:
	points = {}
	flashes = []
	rows = []
	cols = []
	width  = 0
	height = 0
	current_flashes = {}

	def __init__(self):
		self.points = {}
		self.flashes = []
		self.current_flashes = {}
		self.rows = []
		self.cols = []
		self.width  = 0
		self.height = 0

	def __str__(self):
		x = ['Step: '+str(len(self.flashes))]
		for i in range(0,self.height):
			prnt = ''
			for j in range(0,self.width):
				idx = "%d,%d"%(j,i)
				bold = self.points[idx] == 0
				if bold:
					prnt += "\033[1m"
				prnt += str(self.points[idx])
				if bold:
					prnt += "\033[0m"
			x.append(prnt)
		x.append('')
		return "\n".join(x)

	def add_row(self,i):
		self.rows.append(list(i))
		if not self.width:
			self.width = len(list(i))
		self.height += 1

	def build_cols_and_points(self):
		for i in range(0,self.width):
			col = []
			for j in self.rows:
				col.append(int(j[i]))
			self.cols.append(col)
		c = 0
		for i in self.cols:
			d = 0
			for j in i:
				self.points["%d,%d"%(c,d)] = j
				d += 1
			c += 1

	def advance_steps(self,n):
		for i in range(0,n):
			self.advance()

	def advance(self):
		self.current_flashes = {}
		for i in self.points:
			j = self.points[i]
			self.points[i] += 1
			if j >= 9:
				self.points[i] = 0
				self.current_flashes[i] = True
		initial_flashes = self.current_flashes.copy()
		for i in initial_flashes:
			pos = i.split(',')
			self.simple_box_search([int(pos[0]),int(pos[1])])
		self.flashes.append(self.current_flashes.copy())
		print(self)

	def simple_box_search(self,pos):
		checks = [
			[ pos[0]-1,	pos[1]	 ],
			[ pos[0]+1,	pos[1]	 ],
			[ pos[0]+1,	pos[1]+1 ],
			[ pos[0]+1,	pos[1]-1 ],
			[ pos[0]-1,	pos[1]+1 ],
			[ pos[0]-1,	pos[1]-1 ],
			[ pos[0],	pos[1]-1 ],
			[ pos[0],	pos[1]+1 ],
		]
		for i in checks:
			idx = "%d,%d"%(i[0],i[1])
			if idx in self.points:
				if self.points[idx] >= 9: # and idx not in self.current_flashes:
					print("sbs ",idx,self.points[idx])
					self.points[idx] = 0
					self.current_flashes[idx] = True
					self.simple_box_search([i[0],i[1]])
				else:
					self.points[idx] += 1
		print(self)





def puzzle_text():
	print("""
--- Day N: X ---

""")



class testCase(unittest.TestCase):
	global DEBUG
	DEBUG = True

	test_set = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""

	def test_one_star_10(self):
		self.assertEqual(
			one_star(
				self.__class__.test_set,
				10
			),
			204
		)
	def test_one_star_100(self):
		self.assertEqual(
			one_star(
				self.__class__.test_set
			),
			1656
		)

	def test_two_star(self):
		self.assertEqual(
			two_star(
				self.__class__.test_set
			),
			7777
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
