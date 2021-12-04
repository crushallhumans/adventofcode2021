# adventofcode 2021
# crushallhumans
# puzzle 4
# 12/4/2021

import os
import re
import sys
import json
import math
import unittest

DEBUG = False

def one_star(param_set):
	param_set = reprocess_input(param_set)

	num_seq = param_set.pop(0).split(',')
	param_set.pop(0)

	boards = build_boards(param_set)

	ret = 0
	for i in num_seq:
		ret = find_bingo(i, boards)
		if ret > 0:
			break

	return ret


def two_star(param_set):
	param_set = reprocess_input(param_set)

	num_seq = param_set.pop(0).split(',')
	param_set.pop(0)

	boards = build_boards(param_set)

	winners = []
	for i in num_seq:
		bingos = find_bingo(i, boards, True)

		if len(bingos):
			for i in bingos:
				winners.append(i[0])

	return winners.pop()





def reprocess_input(param_set):
	if isinstance(param_set,str):
		l = []
		l = [input_line.strip() for input_line in param_set.splitlines()]
		param_set = l
	return param_set



class Board():
	zero_val = 999999 
	data = {}
	bingoed = False
	def __init__(self, ident, board_len):
	    self.data = {
	    	'identifier':ident,
	    	'matches':	 {},
	    	'row_found': [0] * board_len,
	    	'col_found': [0] * board_len,
	    	'rows':		 [],
	    	'sum_total': 0,
	    	'match_sum': 0
	    }

	def __str__(self):
		return json.dumps(self.data)

	def check(self):
		return json.dumps({
	    	'identifier':self.data['identifier'],
	    	'row_found':self.data['row_found'],
	    	'col_found':self.data['col_found'],
	    	'sum_total':self.data['sum_total'],
	    	'match_sum':self.data['match_sum'],
	    	'bingoed':self.bingoed
		})

	def add_row(self, row_line):
		row_pos = len(self.data['rows'])
		new_row = []
		c = 0
		for ii in re.split("\s+",row_line):
			i = int(ii)

			# zero is a possible bingo value, but breaks summing
			# but it doesn't have to be zero, so alter it to a value outside the regular set
			if i == 0:
				i = self.zero_val

			# a number will match or not, and if so point at the row & col containing it
			self.data['matches'][str(i)] = [row_pos, c, False]

			# rows and cols are sums of their members - if they drop to zero they are bingo
			self.data['row_found'][row_pos] += i
			self.data['col_found'][c] += i

			# preserve actual zero val for totals
			self.data['sum_total'] += int(ii)

			# save raw row val, maybe we need it
			new_row.append(i)

			# column count advance
			c += 1

		# save raw row val, maybe we need it
		self.data['rows'].append(new_row)

	def get_aoc_answer(self, i):
		# AoC needs called_num * (board_total - matched_total)
		return i * (self.data['sum_total'] - self.data['match_sum'])

	def find_match(self, ii):
		ret = 0
		i = int(ii)

		# dodge zero
		if i == 0:
			i = self.zero_val

		if DEBUG: print("called %s",i)
		if (
			# does the val match
			str(i) in self.data['matches'] 
			# is it the first time it's matched
			and self.data['matches'][str(i)][2] == False 
			# has the board not yet bingoed
			and not self.bingoed
		):
			if DEBUG: 
				print ("\tMATCH board %s" % self.data['identifier'])
				print ("\t%s" % self.check())

			# log match
			match = self.data['matches'][str(i)]
			match[2] = True

			# decrement found sums
			self.data['row_found'][match[0]] -= i
			self.data['col_found'][match[1]] -= i

			# increment total match sum
			self.data['match_sum'] += int(ii)

			# check row bingo
			if self.data['row_found'][match[0]] == 0:
				if DEBUG: 
					print ("\tFUCKING ROW BINGO %s" % self.data['identifier'])
					print ("\t%s" % self.check())

				ret = self.get_aoc_answer(int(ii))
				self.bingoed = True
				return ret

			# check col bingo
			if self.data['col_found'][match[1]] == 0:
				if DEBUG: 
					print ("\tFUCKING COLUMN BINGO %s" % self.data['identifier'])
					print ("\t%s" % self.check())

				ret = self.get_aoc_answer(int(ii))
				self.bingoed = True
				return ret

		return ret


def build_boards(param_set):
	boards = []

	len_test = len(re.split("\s+",param_set[0]))

	b = 1
	board = Board(b, len_test)
	for i in param_set:
		if i == "":
			#if DEBUG: print(board)
			boards.append(board)
			b += 1
			board = Board(b, len_test)
		else:
			board.add_row(i)
	boards.append(board)

	return boards

def find_bingo(n, boards, return_all_bingos = False):
	bingo = False
	c = 0
	bingos = []
	for i in boards:
		bingo = i.find_match(n)
		if bingo:
			if not return_all_bingos:
				return bingo
			else:
				bingos.append([bingo,c])
		c += 1
	if not return_all_bingos:
		return bingo
	else:
		return bingos


def puzzle_text():
	print("""--- Day 4: Giant Squid ---
You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep that you can't see any sunlight. What you can see, however, is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen at random, and the chosen number is marked on all boards on which it appears. (Numbers may not appear on all boards.) If all numbers in any row or any column of a board are marked, that board wins. (Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time. It automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners, but the boards are marked as follows (shown here adjacent to each other to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
At this point, the third board wins because it has at least one complete row or column of marked numbers (in this case, the entire top row is marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board; in this case, the sum is 188. Then, multiply that sum by the number that was just called when the board won, 24, to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win first. What will your final score be if you choose that board?


--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms, the safe thing to do is to figure out which board will win last and choose that one. That way, no matter which boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 is eventually called and its middle column is completely marked. If you were to keep playing until this point, the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?
""")



class testCase(unittest.TestCase):
	global DEBUG
	DEBUG = True

	test_set = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""

	def test_one_star(self):
		self.assertEqual(
			one_star(
				self.__class__.test_set
			),
			4512
		)

	def test_two_star(self):
		self.assertEqual(
			two_star(
				self.__class__.test_set
			),
			1924
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
		ret = one_star(input_set.copy())
		print (ret)

		ret = two_star(input_set.copy())
		print (ret)
