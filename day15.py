# adventofcode 2021
# crushallhumans
# puzzle 15
# 5/2/2022 - ?

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
	return 0


def reprocess_input(param_set):
	if isinstance(param_set,str):
		l = []
		l = [input_line.strip() for input_line in param_set.splitlines()]
		param_set = l
	return param_set	


def puzzle_text():
	print("""
""")



class testCase(unittest.TestCase):
	global DEBUG
	DEBUG = True

	test_set = (""" """
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
