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
	for i in param_set:
		continue
	return c


def additional_action(param_set):
	c = 0
	for i in param_set:
		continue
	return c




def puzzle_text():
	print("""
--- Day N: X ---
""")



class testCase(unittest.TestCase):
	test_set = (
		0,
		1
	)

	def test_basic_action(self):
		self.assertEqual(
			basic_action(
				self.__class__.test_set
			),
			88888888
		)

	def test_additional_action(self):
		self.assertEqual(
			additional_action(
				self.__class__.test_set
			),
			77777777
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
		with open("/Users/crushing/Development/crushallhumans/adventofcode2021/inputs/2021/%s.txt" % filename) as input_file:
		    input_set = [int(input_line.strip()) for input_line in input_file]
		ret = basic_action(input_set)
		print (ret)

		ret = additional_action(input_set)
		print (ret)
