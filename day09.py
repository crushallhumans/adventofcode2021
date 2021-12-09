# adventofcode 2021
# crushallhumans
# puzzle 9
# 12/9/2021

import os
import re
import sys
import json
import math
import unittest

DEBUG = False

def one_star(param_set):
	param_set = reprocess_input(param_set)
	c = 8888
	h = HeightMap()
	for i in param_set:
		h.add_row(i)
	h.calculate_adjacent_areas()
	print(h)
	return h.sum_low_areas()


def two_star(param_set):
	param_set = reprocess_input(param_set)
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

class HeightMap:
	rows = []
	adjacent_areas = []

	def __init__(self):
		self.rows = []
		self.adjacent_areas = {}

	def __str__(self):
		x = []
		for i in range(0,len(self.rows)):
			prnt = ''
			for j in range(0,len(self.rows[i])):
				idx = "%d,%d"%(i,j)
				if self.adjacent_areas[idx]['low']:
					prnt += "\033[1m"
				prnt += self.rows[i][j]
				if self.adjacent_areas[idx]['low']:
					prnt += "\033[0m"
			x.append(prnt)
		return "\n".join(x)

	def add_row(self,i):
		self.rows.append(list(i))

	def sum_low_areas(self):
		total = 0
		for i in self.adjacent_areas.keys():
			if self.adjacent_areas[i]['low']:
				total += int(self.adjacent_areas[i]['val']) + 1
		return total

	def calculate_adjacent_areas(self):
		num_rows = len(self.rows)
		num_cols = len(self.rows[0])
		for i in range(0,num_rows):
			adj_rows = []
			if i > 0:
				adj_rows.append(i-1)
			if i < (num_rows-1):
				adj_rows.append(i+1)
			for j in range(0,num_cols):
				adj_cols = []
				if j > 0:
					adj_cols.append(j-1)
				if j < (num_cols-1):
					adj_cols.append(j+1)

				val = self.rows[i][j]
				self.adjacent_areas["%d,%d"%(i,j)] = {
					"val": val,
					"low": True,
					"adjacents": [],
					"basins": []
				}
				idx = "%d,%d"%(i,j)
				print(idx, adj_rows, adj_cols)
				h = self.adjacent_areas[idx]
				for ii in adj_rows:
					adj = self.rows[ii][j]
					h['adjacents'].append(adj)
					if val >= adj:
						h['low'] = False

				# don't contain - diagonals don't count
				for jj in adj_cols:
					adj = self.rows[i][jj]
					h['adjacents'].append(adj)
					if val >= adj:
						h['low'] = False

				if h['low']:

				# bah! this builds a basin out from the low point itself
				#  but! to build a basin one must treat each subsequent point <9 as its own basin!
				#   this is for the MORNING TIME

					build_basin_y_pos = True
					build_basin_y_neg = True
					y_pos = adj_rows[-1] + 1
					while build_basin_y_pos:
						if y_pos < len(self.rows) and int(self.rows[y_pos][j]) < 9:
							h['basins'].append(self.rows[y_pos][j])
							y_pos += 1
						else:
							build_basin_y_pos = False
					y_pos = adj_rows[0] - 1
					while build_basin_y_neg:
						if y_pos >= 0 and int(self.rows[y_pos][j]) < 9:
							h['basins'].append(self.rows[y_pos][j])
							y_pos -= 1
						else:
							build_basin_y_neg = False


					build_basin_x_pos = True
					build_basin_x_neg = True
					x_pos = adj_cols[-1] + 1
					while build_basin_x_pos:
						if x_pos < len(self.rows[i]) and int(self.rows[i][x_pos]) < 9:
							h['basins'].append(self.rows[i][x_pos])
							x_pos += 1
						else:
							build_basin_x_pos = False
					x_pos = adj_cols[0] - 1
					while build_basin_x_neg:
						if x_pos >= 0 and int(self.rows[i][x_pos]) < 9:
							h['basins'].append(self.rows[i][x_pos])
							x_pos -= 1
						else:
							build_basin_x_neg = False


		print(json.dumps(self.adjacent_areas, indent = 2))




def puzzle_text():
	print("""
--- Day N: X ---

""")



class testCase(unittest.TestCase):
	global DEBUG
	DEBUG = True

	test_set = """2199943210
3987894921
9856789892
8767896789
9899965678"""

	def test_one_star(self):
		self.assertEqual(
			one_star(
				self.__class__.test_set
			),
			15
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
