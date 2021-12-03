# adventofcode 2021
# crushallhumans
# puzzle 3
# 12/3/2021

import os
import sys
import math
import unittest

DEBUG = False

def one_star(param_set):
	(gamma,epsilon) = diagnostic_binary_decode(param_set)

	return gamma * epsilon


def two_star(param_set):
	o2 	= diagnostic_recursive_decode(param_set)
	print ("o2: ", o2)
	co2 = diagnostic_recursive_decode(param_set, False)
	print ("co2: ", co2)
	return o2 * co2

def diagnostic_binary_decode(param_set):
	if isinstance(param_set,str):
		l = []
		l = [input_line.strip() for input_line in param_set.splitlines()]
		param_set = l

	if DEBUG: print(param_set)
	total_bits = [0] * len(param_set[0])
	for i in param_set:
		c = 0
		for j in i:
			if int(j):
				total_bits[c] += 1
			c += 1
		if DEBUG: print (total_bits)

	gamma 	= ''
	epsilon = ''
	lps = math.ceil((len(param_set)) / 2)
	for i in total_bits:
		if i >= lps:
			gamma 	+= '1'
			epsilon += '0'
		else:
			gamma 	+= '0'
			epsilon += '1'

	if DEBUG: print(gamma,epsilon)
	gb = int(gamma,2)
	eb = int(epsilon,2)
	if DEBUG: print(gb,eb)

	return (gb, eb)

def diagnostic_recursive_decode(param_set, direction = True, position = 0):
	if isinstance(param_set,str):
		l = []
		l = [input_line.strip() for input_line in param_set.splitlines()]
		param_set = l

	if DEBUG: print(param_set)
	lps = math.ceil((len(param_set)) / 2)
	c = 0
	for i in param_set:
		j = i[position]
		if int(j):
			c += 1
	if DEBUG: print (c,lps)

	position_truth = 		True  if c >= lps else False
	if (not direction):
		position_truth =    not position_truth

	if DEBUG: print (position_truth)
	new_param_set = []
	for i in param_set:
		if DEBUG: print (i[position], bool(int(i[position])))
		if bool(int(i[position])) == position_truth:
			if DEBUG: print ('keeping ',i)
			new_param_set.append(i)			


	ret = new_param_set
	if len(new_param_set) < 1:
		raise Exception("something went wrong - no params remain after filtering")
	elif len(new_param_set) > 1:
		ret = diagnostic_recursive_decode(new_param_set, direction, position + 1)
	else:
		if DEBUG: print("foo: " ,new_param_set)
		x = new_param_set[0]
		ret = int(x,2)
		if DEBUG: print(ret)

	return ret



def puzzle_text():
	print("""
--- Day 3: Binary Diagnostic ---
The submarine has been making some odd creaking noises, so you ask it to produce a diagnostic report just in case.

The diagnostic report (your puzzle input) consists of a list of binary numbers which, when decoded properly, can tell you many useful things about the conditions of the submarine. The first parameter to check is the power consumption.

You need to use the binary numbers in the diagnostic report to generate two new binary numbers (called the gamma rate and the epsilon rate). The power consumption can then be found by multiplying the gamma rate by the epsilon rate.

Each bit in the gamma rate can be determined by finding the most common bit in the corresponding position of all numbers in the diagnostic report. For example, given the following diagnostic report:

00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
Considering only the first bit of each number, there are five 0 bits and seven 1 bits. Since the most common bit is 1, the first bit of the gamma rate is 1.

The most common second bit of the numbers in the diagnostic report is 0, so the second bit of the gamma rate is 0.

The most common value of the third, fourth, and fifth bits are 1, 1, and 0, respectively, and so the final three bits of the gamma rate are 110.

So, the gamma rate is the binary number 10110, or 22 in decimal.

The epsilon rate is calculated in a similar way; rather than use the most common bit, the least common bit from each position is used. So, the epsilon rate is 01001, or 9 in decimal. Multiplying the gamma rate (22) by the epsilon rate (9) produces the power consumption, 198.

Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate, then multiply them together. What is the power consumption of the submarine? (Be sure to represent your answer in decimal, not binary.)


""")



class testCase(unittest.TestCase):
	global DEBUG
	DEBUG = True

	test_set = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

	def test_one_star(self):
		self.assertEqual(
			one_star(
				self.__class__.test_set
			),
			198
		)

	def test_two_star(self):
		self.assertEqual(
			two_star(
				self.__class__.test_set
			),
			230
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
