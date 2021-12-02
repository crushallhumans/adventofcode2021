# adventofcode 2021
# crushallhumans
# puzzle 2
# 12/2/2021

import os
import sys
import math
import unittest

DEBUG = False

def one_star(param_set):
	param_set = parse_inputs(param_set)
	position = {
		'x': 0,
		'y': 0
	}
	for i in param_set:
		dim = i[0]
		vec = i[1]
		pos = i[2]

		position[dim] += (vec * pos)

	return position['x'] * position['y']

def two_star(param_set):
	param_set = parse_inputs(param_set)
	position = {
		'x': 0,
		'y': 0,
		'a': 0
	}
	for i in param_set:
		dim = i[0]
		vec = i[1]
		pos = i[2]

		if dim == 'x':
			position['x'] += pos
			position['y'] += pos * position['a']
		else:
			position['a'] += (vec * pos)
		if DEBUG: print(position)

	return position['x'] * position['y']


def parse_inputs(param_set):
	instruction_set = []
	valid_commands = {
		'forward':	['x',	1],
		'down':		['y',	1],
		'up':		['y',	-1],
	}

	if isinstance(param_set,str):
		l = []
		l = [input_line.strip() for input_line in param_set.splitlines()]
		param_set = l
		
	for i in param_set:
		if DEBUG: print(i)
		j = []
		cc = i.split(' ')
		if cc[0] in valid_commands.keys():
			j = valid_commands[cc[0]].copy()
			j.append(int(cc[1]))
			if DEBUG: print(j)
			instruction_set.append(j)
		else:
			raise Exception("invalid command: %s" % cc[0])

	if DEBUG: print(instruction_set)
	return instruction_set



def puzzle_text():
	print("""
--- Day 2: Dive! ---
Now, you need to figure out how to pilot this thing.

It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:

forward X increases the horizontal position by X units.
down X increases the depth by X units.
up X decreases the depth by X units.
Note that since you're on a submarine, down and up affect your depth, and so they have the opposite result of what you might expect.

The submarine seems to already have a planned course (your puzzle input). You should probably figure out where it's going. For example:

forward 5
down 5
forward 8
up 3
down 8
forward 2
Your horizontal position and depth both start at 0. The steps above would then modify them as follows:

forward 5 adds 5 to your horizontal position, a total of 5.
down 5 adds 5 to your depth, resulting in a value of 5.
forward 8 adds 8 to your horizontal position, a total of 13.
up 3 decreases your depth by 3, resulting in a value of 2.
down 8 adds 8 to your depth, resulting in a value of 10.
forward 2 adds 2 to your horizontal position, a total of 15.
After following these instructions, you would have a horizontal position of 15 and a depth of 10. (Multiplying these together produces 150.)

Calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?
""")



class testCase(unittest.TestCase):
	global DEBUG
	DEBUG = True
	test_set = (
		"""forward 5
		down 5
		forward 8
		up 3
		down 8
		forward 2"""
	)

	def test_one_star(self):
		self.assertEqual(
			one_star(
				self.__class__.test_set
			),
			150
		)

	def test_two_star(self):
		self.assertEqual(
			two_star(
				self.__class__.test_set
			),
			900
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
