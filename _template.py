# adventofcode 2021
# crushallhumans
# puzzle N
# 12/n/2021

import os
import sys
import math
import unittest

def basic_action(param_set):
	c = 0
	d = 0
	for i in param_set:
		for j in param_set:
			if (c != d) and ((i + j) == 2020):
				return (i,j)
			d += 1
		c += 1
	return (-1,-1)


def additional_action(param_set):
	c = 0
	d = 0
	e = 0
	for i in param_set:
		for j in param_set:
			for k in param_set:
				if (c != d) and (d != e) and (c != e) and ((i + j + k) == 2020):
					return (i,j,k)
				e += 1
			d += 1
		c += 1
	return (-1,-1)

def puzzle_text():
	print("""
--- Day N: X ---
""")

class testCase(unittest.TestCase):
	def test_basic_action(self):
		self.assertEqual(
			basic_action((1721,979,366,299,675,1456)),
			(1721,299)
		)

	def test_additional_action(self):
		self.assertEqual(
			additional_action((1721,979,366,299,675,1456)),
			(979, 366, 675)
		)

if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		filename_script = os.path.basename(__file__)
		print (filename_script)
		filename = filename_script.split('.')[0]
		input_set = ()
		with open("/Users/crushing/Development/crushallhumans/adventofcode2021/inputs/inputstring_%s.txt" % filename) as input_file:
		    input_set = [int(input_line.strip()) for input_line in input_file]
		ret = basic_action(input_set)
		print (ret)

		ret = additional_action(input_set)
		print (ret)
