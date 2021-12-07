# adventofcode 2021
# crushallhumans
# puzzle 7
# 12/7/2021

import os
import re
import sys
import time
import math
import unittest

DEBUG = False

notes = """
theories:
you can always eliminate the top and bottom numbers
if you plotted these points, you could draw a trendline by averaging the difference between them
sum of that averaged line is probably closer to the answer than the start or the beginning
move out from that, testing for higher costs?

Solved!
average idea didn't work - but popping the start and end did
the members of the initial set always contain the answer in the flat/part-one puzzle?
	in part two, values outside the initial set contain the answer
bruteforce on part 2 took 51sec to run on an MacbookPro17,1 (8-core M1)
"""

def one_star(param_set, linear = False):
	param_set = reprocess_input(param_set)
	totals = {}
	position_sum = 0
	fuels = []
	for i in param_set:
		if i not in totals.keys():
			totals[i] = {
				'num': 1
			}
			position_sum += (int(i))
		else:
			totals[i]['num'] += 1
	if DEBUG: print (totals)

	max_pos = 0
	fuel_calc_k = list(totals.keys())
	fuel_calc = []
	for i in fuel_calc_k:
		if int(i) > max_pos:
			max_pos = int(i) 
		fuel_calc.append(int(i))
	fuel_calc.sort()
	fuel_calc.pop()
	fuel_calc.pop(0)
	t0 = time.time()
	if linear:
		start = fuel_calc[0]
		end = fuel_calc[-1]
		if DEBUG: print(fuel_calc,start,end)

		lent = end-start

		#memoize the fuel costs! massively more efficient
		fuel_costs = {}
		for i in range(0, max_pos):
			t = 0
			c = 1
			linear = 0
			for j in range(0,i):
				t += c
				c += 1
			fuel_costs[i] = t
		if DEBUG: print(fuel_costs)

		for i in range(start,end):
			print(i,lent,time.time()-t0)
			fuels.append(calc_set_fuel_linear(param_set,i,fuel_costs))	 
			
	else:
		for i in fuel_calc:
			fuels.append(calc_set_fuel_flat(param_set,i))

	if DEBUG: print (position_sum, len(param_set), position_sum/len(param_set))
	if DEBUG: print (fuels)
	fuels.sort()
	return(fuels.pop(0))

def two_star(param_set):
	return one_star(param_set, True)

def reprocess_input(param_set):
	if isinstance(param_set,list) and len(param_set) == 1:
		param_set = param_set[0]
	if  (isinstance(param_set,str)):
		l = []
		l = param_set.split(',')
		param_set = l
	return param_set	

def calc_set_fuel_flat(param_set, fuel_proposition):
	total = 0
	for i in param_set:
		total += abs(int(i) - int(fuel_proposition))
	return total

def calc_set_fuel_linear(param_set, fuel_proposition, fuel_costs):
	total = 0
	for i in param_set:
		if DEBUG: print(i,fuel_proposition)
		diff =  abs(int(i) - int(fuel_proposition))
		# c = 1
		# linear = 0
		# for j in range(0,diff):
		# 	linear += c
		# 	c += 1
		# 	if DEBUG: print("\t",linear)
		total += fuel_costs[diff] #linear
	return total



def puzzle_text():
	print("""--- Day 7: The Treachery of Whales ---
A giant whale has decided your submarine is its next meal, and it's much faster than you are. There's nowhere to run!

Suddenly, a swarm of crabs (each in its own tiny submarine - it's too deep for them otherwise) zooms in to rescue you! They seem to be preparing to blast a hole in the ocean floor; sensors indicate a massive underground cave system just beyond where they're aiming!

The crab submarines all need to be aligned before they'll have enough power to blast a large enough hole for your submarine to get through. However, it doesn't look like they'll be aligned before the whale catches you! Maybe you can help?

There's one major catch - crab submarines can only move horizontally.

You quickly make a list of the horizontal position of each crab (your puzzle input). Crab submarines have limited fuel, so you need to find a way to make all of their horizontal positions match while requiring them to spend as little fuel as possible.

For example, consider the following horizontal positions:

16,1,2,0,4,2,7,1,2,14
This means there's a crab with horizontal position 16, a crab with horizontal position 1, and so on.

Each change of 1 step in horizontal position of a single crab costs 1 fuel. You could choose any horizontal position to align them all on, but the one that costs the least fuel is horizontal position 2:

Move from 16 to 2: 14 fuel
Move from 1 to 2: 1 fuel
Move from 2 to 2: 0 fuel
Move from 0 to 2: 2 fuel
Move from 4 to 2: 2 fuel
Move from 2 to 2: 0 fuel
Move from 7 to 2: 5 fuel
Move from 1 to 2: 1 fuel
Move from 2 to 2: 0 fuel
Move from 14 to 2: 12 fuel
This costs a total of 37 fuel. This is the cheapest possible outcome; more expensive outcomes include aligning at position 1 (41 fuel), position 3 (39 fuel), or position 10 (71 fuel).

Determine the horizontal position that the crabs can align to using the least fuel possible. How much fuel must they spend to align to that position?


--- Part Two ---
The crabs don't seem interested in your proposed solution. Perhaps you misunderstand crab engineering?

As it turns out, crab submarine engines don't burn fuel at a constant rate. Instead, each change of 1 step in horizontal position costs 1 more unit of fuel than the last: the first step costs 1, the second step costs 2, the third step costs 3, and so on.

As each crab moves, moving further becomes more expensive. This changes the best horizontal position to align them all on; in the example above, this becomes 5:

Move from 16 to 5: 66 fuel
Move from 1 to 5: 10 fuel
Move from 2 to 5: 6 fuel
Move from 0 to 5: 15 fuel
Move from 4 to 5: 1 fuel
Move from 2 to 5: 6 fuel
Move from 7 to 5: 3 fuel
Move from 1 to 5: 10 fuel
Move from 2 to 5: 6 fuel
Move from 14 to 5: 45 fuel
This costs a total of 168 fuel. This is the new cheapest possible outcome; the old alignment position (2) now costs 206 fuel instead.

Determine the horizontal position that the crabs can align to using the least fuel possible so they can make you an escape route! How much fuel must they spend to align to that position?
""")



class testCase(unittest.TestCase):
	global DEBUG
	DEBUG = True

	test_set = "16,1,2,0,4,2,7,1,2,14"

	def test_one_star(self):
		self.assertEqual(
			one_star(
				self.__class__.test_set
			),
			37
		)

	def test_two_star(self):
		self.assertEqual(
			two_star(
				self.__class__.test_set
			),
			168
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
