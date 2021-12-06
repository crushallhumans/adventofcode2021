# adventofcode 2021
# crushallhumans
# puzzle 6
# 12/6/2021

import os
import re
import sys
import time
import math
import unittest

DEBUG = False

def one_star(param_set, days = 80):
	if DEBUG: print("\n\none_star, days: " + str(days))
	dbg = DEBUG
	if days > 18:
		dbg = False
	param_set = reprocess_input(param_set)
	fish = []
	for i in param_set:
		for j in i.split(','):
			fish.append(int(j))
	day = 0
	lifecycle_root	= 6
	lifecycle_new 	= 8
	# measure wall time
	t0 = time.time()
	while day < days:
		if dbg: print(day,fish,(time.time()-t0))
		add = 0
		c = 0
		for i in fish:
			if i > 0:
				fish[c] -= 1
			elif i == 0:
				add += 1
				fish[c] = lifecycle_root
			c += 1
		for i in range(0,add):
			fish.append(lifecycle_new)

		day += 1

	return len(fish)


def two_star(param_set, days = 256):
	if DEBUG: print("\n\ntwo_star, days: " + str(days))
	dbg = DEBUG
	if days > 18:
		dbg = False
	param_set = reprocess_input(param_set)
	fish = {}
	for i in param_set:
		for jj in i.split(','):
			j = str(jj)
			if j not in fish:
				fish[j] = 1
			else:
				fish[j] += 1
	day = 0
	lifecycle_root	= 6
	lifecycle_new 	= 8
	if str(lifecycle_new) not in fish:
		fish[str(lifecycle_new)] = 0
	if str(lifecycle_root) not in fish:
		fish[str(lifecycle_root)] = 0

	while day < days:
		if dbg: print(str(day) + "\t\t" + str(represent_fish_dict(fish)))
		add = fish['0'] if '0' in fish.keys() else 0

		# going up from zero, push the register above into the current
		# if no register above exists, zero the current
		for i in range(0,lifecycle_new):
			upper = str(i+1)
			if upper in fish:
				prior = fish[str(i)] if str(i) in fish else 0
				fish[str(i)] = fish[upper]
			elif str(i) in fish:
				fish[str(i)] = 0

		# new fish always start from zero, so assign
		fish[str(lifecycle_new)] = add

		# regenerated fish can come from zero or (new-1), so add
		fish[str(lifecycle_root)] += add

		day += 1

	return (sum(fish.values()))

def represent_fish_dict(fish):
	x = ''
	for i in range(0,9):
		if str(i) in fish:
			x += "'" + str(i) + "':\t" + str(fish[str(i)]) + " \t"
		else: 
			x += "'" + str(i) + "':\t0 \t"
	return x


def reprocess_input(param_set):
	if isinstance(param_set,str):
		l = []
		l = [input_line.strip() for input_line in param_set.splitlines()]
		param_set = l
	return param_set	


def puzzle_text():
	print("""--- Day 6: Lanternfish ---
The sea floor is getting steeper. Maybe the sleigh keys got carried this way?

A massive school of glowing lanternfish swims past. They must spawn quickly to reach such large numbers - maybe exponentially quickly? You should model their growth rate to be sure.

Although you know nothing about this specific species of lanternfish, you make some guesses about their attributes. Surely, each lanternfish creates a new lanternfish once every 7 days.

However, this process isn't necessarily synchronized between every lanternfish - one lanternfish might have 2 days left until it creates another lanternfish, while another might have 4. So, you can model each fish as a single number that represents the number of days until it creates a new lanternfish.

Furthermore, you reason, a new lanternfish would surely need slightly longer before it's capable of producing more lanternfish: two more days for its first cycle.

So, suppose you have a lanternfish with an internal timer value of 3:

After one day, its internal timer would become 2.
After another day, its internal timer would become 1.
After another day, its internal timer would become 0.
After another day, its internal timer would reset to 6, and it would create a new lanternfish with an internal timer of 8.
After another day, the first lanternfish would have an internal timer of 5, and the second lanternfish would have an internal timer of 7.
A lanternfish that creates a new fish resets its timer to 6, not 7 (because 0 is included as a valid timer value). The new lanternfish starts with an internal timer of 8 and does not start counting down until the next day.

Realizing what you're trying to do, the submarine automatically produces a list of the ages of several hundred nearby lanternfish (your puzzle input). For example, suppose you were given the following list:

3,4,3,1,2
This list means that the first fish has an internal timer of 3, the second fish has an internal timer of 4, and so on until the fifth fish, which has an internal timer of 2. Simulating these fish over several days would proceed as follows:

Initial state: 3,4,3,1,2
After  1 day:  2,3,2,0,1
After  2 days: 1,2,1,6,0,8
After  3 days: 0,1,0,5,6,7,8
After  4 days: 6,0,6,4,5,6,7,8,8
After  5 days: 5,6,5,3,4,5,6,7,7,8
After  6 days: 4,5,4,2,3,4,5,6,6,7
After  7 days: 3,4,3,1,2,3,4,5,5,6
After  8 days: 2,3,2,0,1,2,3,4,4,5
After  9 days: 1,2,1,6,0,1,2,3,3,4,8
After 10 days: 0,1,0,5,6,0,1,2,2,3,7,8
After 11 days: 6,0,6,4,5,6,0,1,1,2,6,7,8,8,8
After 12 days: 5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8
After 13 days: 4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8
After 14 days: 3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8
After 15 days: 2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7
After 16 days: 1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8
After 17 days: 0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8
After 18 days: 6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8
Each day, a 0 becomes a 6 and adds a new 8 to the end of the list, while each other number decreases by 1 if it was present at the start of the day.

In this example, after 18 days, there are a total of 26 fish. After 80 days, there would be a total of 5934.

Find a way to simulate lanternfish. How many lanternfish would there be after 80 days?


--- Part Two ---
Suppose the lanternfish live forever and have unlimited food and space. Would they take over the entire ocean?

After 256 days in the example above, there would be a total of 26984457539 lanternfish!

How many lanternfish would there be after 256 days?

""")



class testCase(unittest.TestCase):
	global DEBUG
	DEBUG = True

	test_set = "3,4,3,1,2"

	def test_one_star_18(self):
		self.assertEqual(
			one_star(
				self.__class__.test_set, 18
			),
			26
		)
	def test_one_star_80(self):
		self.assertEqual(
			one_star(
				self.__class__.test_set, 80
			),
			5934
		)

	# still running, all done with exercise!
	# def test_one_star_256(self):
	# 	self.assertEqual(
	# 		one_star(
	# 			self.__class__.test_set, 256
	# 		),
	# 		26984457539
	# 	)

	def test_two_star_18(self):
		self.assertEqual(
			two_star(
				self.__class__.test_set, 18
			),
			26
		)
	def test_two_star_80(self):
		self.assertEqual(
			two_star(
				self.__class__.test_set, 80
			),
			5934
		)
	def test_two_star_256(self):
		self.assertEqual(
			two_star(
				self.__class__.test_set, 256
			),
			26984457539
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

		ret = two_star(input_set, 256)
		print (ret)
