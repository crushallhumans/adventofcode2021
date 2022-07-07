# adventofcode 2021
# crushallhumans
# puzzle 15
# 5/2/2022 - ?

import os
import re
import sys
import math
from time import sleep
import unittest
from copy import deepcopy

from dijkstra import get_risk

DEBUG = False

def one_star(param_set):
	print("---------------one_star--------------------")
	x = execute(param_set)
	if DEBUG: sleep(5)
	return x

def two_star(param_set):
	print("---------------two_star--------------------")
	return execute(param_set, 5)

def execute(param_set, multiplier = 0):
	param_set = reprocess_input(param_set)
	if multiplier > 0:
		param_set = extend_data(param_set, multiplier)		
	return get_risk(param_set, DEBUG)


def reprocess_input(param_set):
	l = []
	if DEBUG: param_set = param_set.splitlines()
	for input_line in param_set:
		l.append([int(i) for i in input_line.strip()])
	return l

def extend_data(data, multiplier):
    '''returns the data as a 2d array extended 5 times in each direction'''
    d = len(data)
    max_list_size = len(data) * multiplier
    extended_data = [[0 for _ in range(max_list_size)] for _ in range(max_list_size)] # pad an empty array with zeros

    for y_index, y in enumerate(extended_data):
        for x_index, x in enumerate(y):
            n = data[y_index % d][x_index % d]
            extended_data[y_index][x_index] = (
            	n + ((y_index // d) + (x_index // d)) - 1
            ) % 9 + 1 
            # formula: i = (n - 1) % 9 + 1
    
    return extended_data



def puzzle_text():
	print("""
--- Day 15: Chiton ---
You've almost reached the exit of the cave, but the walls are getting closer together. Your submarine can barely still fit, though; the main problem is that the walls of the cave are covered in chitons, and it would be best not to bump any of them.

The cavern is large, but has a very low ceiling, restricting your motion to two dimensions. The shape of the cavern resembles a square; a quick scan of chiton density produces a map of risk level throughout the cave (your puzzle input). For example:

1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
You start in the top left position, your destination is the bottom right position, and you cannot move diagonally. The number at each position is its risk level; to determine the total risk of an entire path, add up the risk levels of each position you enter (that is, don't count the risk level of your starting position unless you enter it; leaving it adds no risk to your total).

Your goal is to find a path with the lowest total risk. In this example, a path with the lowest total risk is highlighted here:

1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
The total risk of this path is 40 (the starting position is never entered, so its risk is not counted).

What is the lowest total risk of any path from the top left to the bottom right?

""")



class testCase(unittest.TestCase):
	global DEBUG
	DEBUG = True

	test_set = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

	def test_one_star(self):
		self.assertEqual(
			one_star(
				self.__class__.test_set
			),
			40
		)

	def test_two_star(self):
		self.assertEqual(
			two_star(
				self.__class__.test_set
			),
			315
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
