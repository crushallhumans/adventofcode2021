# adventofcode 2021
# crushallhumans
# puzzle 8
# 12/8/2021

import os
import re
import sys
import json
import math
import unittest

DEBUG = False

def one_star(param_set):
	param_set = reprocess_input(param_set)
	seg = SevenSegment()
	for i in param_set:
		seg.add_entry(i)
	if DEBUG: print(seg)
	return seg.sum_unique_digits()


def two_star(param_set):
	param_set = reprocess_input(param_set)
	seg = SevenSegment()
	for i in param_set:
		seg.add_entry(i)
	if DEBUG: print(seg)
	return seg.build_decoder_map()

def reprocess_input(param_set):
	if isinstance(param_set,str):
		l = []
		l = [input_line.strip() for input_line in param_set.splitlines()]
		param_set = l
	return param_set	


def puzzle_text():
	print("""--- Day 8: Seven Segment Search ---
You barely reach the safety of the cave when the whale smashes into the cave mouth, collapsing it. Sensors indicate another exit to this cave at a much greater depth, so you have no choice but to press on.

As your submarine slowly makes its way through the cave system, you notice that the four-digit seven-segment displays in your submarine are malfunctioning; they must have been damaged during the escape. You'll be in a lot of trouble without them, so you'd better figure out what's wrong.

Each digit of a seven-segment display is rendered by turning on or off any of seven segments named a through g:

  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
So, to render a 1, only segments c and f would be turned on; the rest would be off. To render a 7, only segments a, c, and f would be turned on.

The problem is that the signals which control the segments have been mixed up on each display. The submarine is still trying to display numbers by producing output on signal wires a through g, but those wires are connected to segments randomly. Worse, the wire/segment connections are mixed up separately for each four-digit display! (All of the digits within a display use the same connections, though.)

So, you might know that only signal wires b and g are turned on, but that doesn't mean segments b and g are turned on: the only digit that uses two segments is 1, so it must mean segments c and f are meant to be on. With just that information, you still can't tell which wire (b/g) goes to which segment (c/f). For that, you'll need to collect more information.

For each display, you watch the changing signals for a while, make a note of all ten unique signal patterns you see, and then write down a single four digit output value (your puzzle input). Using the signal patterns, you should be able to work out which pattern corresponds to which digit.

For example, here is what you might see in a single entry in your notes:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf
(The entry is wrapped here to two lines so it fits; in your notes, it will all be on a single line.)

Each entry consists of ten unique signal patterns, a | delimiter, and finally the four digit output value. Within an entry, the same wire/segment connections are used (but you don't know what the connections actually are). The unique signal patterns correspond to the ten different ways the submarine tries to render a digit using the current wire/segment connections. Because 7 is the only digit that uses three segments, dab in the above example means that to render a 7, signal lines d, a, and b are on. Because 4 is the only digit that uses four segments, eafb means that to render a 4, signal lines e, a, f, and b are on.

Using this information, you should be able to work out which combination of signal wires corresponds to each of the ten digits. Then, you can decode the four digit output value. Unfortunately, in the above example, all of the digits in the output value (cdfeb fcadb cdfeb cdbaf) use five segments and are more difficult to deduce.

For now, focus on the easy digits. Consider this larger example:

be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |
fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |
cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |
efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |
gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |
gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |
cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |
ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |
gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |
fgae cfgab fg bagce
Because the digits 1, 4, 7, and 8 each use a unique number of segments, you should be able to tell which combinations of signals correspond to those digits. Counting only digits in the output values (the part after | on each line), in the above example, there are 26 instances of digits that use a unique number of segments (highlighted above).

In the output values, how many times do digits 1, 4, 7, or 8 appear?


--- Part Two ---
Through a little deduction, you should now be able to determine the remaining digits. Consider again the first example above:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf
After some careful analysis, the mapping between signal wires and segments only make sense in the following configuration:

 dddd
e    a
e    a
 ffff
g    b
g    b
 cccc
So, the unique signal patterns would correspond to the following digits:

acedgfb: 8
cdfbe: 5
gcdfa: 2
fbcad: 3
dab: 7
cefabd: 9
cdfgeb: 6
eafb: 4
cagedb: 0
ab: 1
Then, the four digits of the output value can be decoded:

cdfeb: 5
fcadb: 3
cdfeb: 5
cdbaf: 3
Therefore, the output value for this entry is 5353.

Following this same process for each entry in the second, larger example above, the output value of each entry can be determined:

fdgacbe cefdb cefbgd gcbe: 8394
fcgedb cgb dgebacf gc: 9781
cg cg fdcagb cbg: 1197
efabcd cedba gadfec cb: 9361
gecf egdcabf bgf bfgea: 4873
gebdcfa ecba ca fadegcb: 8418
cefg dcbef fcge gbcadfe: 4548
ed bcgafe cdgba cbgef: 1625
gbdfcae bgc cg cgb: 8717
fgae cfgab fg bagce: 4315
Adding all of the output values in this larger example produces 61229.

For each entry, determine all of the wire/segment connections and decode the four-digit output values. What do you get if you add up all of the output values?

""")

class SevenSegment:
	example = """
	   0:      1:      2:      3:      4:
	 aaaa    ....    aaaa    aaaa    ....
	b    c  .    c  .    c  .    c  b    c
	b    c  .    c  .    c  .    c  b    c
	 ....    ....    dddd    dddd    dddd
	e    f  .    f  e    .  .    f  .    f
	e    f  .    f  e    .  .    f  .    f
	 gggg    ....    gggg    gggg    ....

	  5:      6:      7:      8:      9:
	 aaaa    aaaa    aaaa    aaaa    aaaa
	b    .  b    .  .    c  b    c  b    c
	b    .  b    .  .    c  b    c  b    c
	 dddd    dddd    ....    dddd    dddd
	.    f  e    f  .    f  e    f  .    f
	.    f  e    f  .    f  e    f  .    f
	 gggg    gggg    ....    gggg    gggg"""


	theories="""

	 1 is unique
	 4 is unique
	 7 is unique
	 8 is unique

	 6-long, 3 digits:
	 '0', '6', and '9' are '8' minus 1seg
	 	the 1seg missing from '0' is in both '6' and '9'
	 	the 1seg missing from '6' is in both '0' and '9'
	 	the 1seg missing from '9' is in both '0' and '6'

	 5-long, 3 digits:
	 '2', '3', and '5'
	 	'2' and '3' are different from one aother by 1seg
	 	'5' and '3' are different from one another by 1seg

	 	sorted?
ab     : 1
ab d   : 7
ab  ef : 4
a cd fg: 2
abcd f : 3
 bcdef : 5
abcde g: 0
 bcdefg: 6
abcdef : 9
abcdefg: 8

	"a" is the segment in 7 that is not in 1
	"c" is the segment that is in 1,4,7,8 but not in 6
	"c" is the segment that is in 2 and 3 but not in 5
	"e" is the segment that is in 6 but not 9
	"e" is the segment that is in 2 but not 3 or 5
	"f" is in everything but "2"

	"""

	implicit_order = ['a','b','c','d','e','f','g'] # a=0, b=1, etc
	digit_map = [
	    #a b c d e f g
		[1,1,1,0,1,1,1], #0, uses 6 e  2  -0
		[0,0,1,0,0,1,0], #1, uses 2 a0
		[1,0,1,1,1,0,1], #2, uses 5 d   5 -2
		[1,0,1,1,0,1,1], #3, uses 5 d   5 -3
		[0,1,1,1,0,1,0], #4, uses 4 c0
		[1,1,0,1,0,1,1], #5, uses 5 d   5 -5
		[1,1,0,1,1,1,1], #6, uses 6 e  2  -6
		[1,0,1,0,0,1,0], #7, uses 3 b0
		[1,1,1,1,1,1,1], #8, uses 7 f0
		[1,1,1,1,0,1,1]  #9, uses 6 e  2  -9
	]
	digit_map_elaborate = {}

	blank_digit_map = [
		[],
		[],
		[],
		[],
		[],
		[],
		[],
		[],
		[],
		[],
	]	
	digit_sums = [
		6,
		2,
		5,
		5,
		4,
		5,
		6,
		3,
		7,
		6
	]
	unique_digits = {
		2: 1,
		3: 7,
		4: 4,
		7: 8
	}
	decoded_order = ['z','z','z','z','z','z','z']

	entries = []
	def __init__(self):
		self.entries = []
		self.decoded = False
		self.digit_map_elaborate_decoded = {}
		n = 0
		for i in self.digit_map:
			self.digit_map_elaborate[n] = self.build_elaborate_line(i, n, self.implicit_order)
			n += 1
		#print(json.dumps(self.digit_map_elaborate,indent=4))

	def __str__(self):
		return json.dumps(self.entries)

	def build_elaborate_line(self,i,n,order):
		a = {}
		c = 0
		for j in i:
			if order[c] == 'z':
				raise "Order not decoded for %d: %s" % (c, order)
			a[c] = [order[c],True if self.digit_map[n][c] == 1 else False]
			c += 1
		return a

	def add_entry(self,i):
		if DEBUG: print (i)
		s = i.split(' | ')
		signals = s[0].split(' ')
		display = s[1].split(' ')
		self.entries.append({
			'signals': signals,
			'display': display,
			'decoded_order': ['z','z','z','z','z','z','z'],
			'digit_map_elaborate_decoded': {},
			'digit_dictionary': {},
			'display_values': [],
			'display_value': 0,
			'decoded': False
		})

	def sum_unique_digits(self):
		total = 0
		for i in self.entries:
			for j in i['display']:
				if len(j) in self.unique_digits.keys():
					total += 1
		return total

	def sum_display_digits(self):
		total = 0
		if self.decoded == True:
			for i in self.entries:
				for j in i['display']:
					total += self.decode_digit_with_map(j, i['digit_map'])
		return total

	def decode_digit_with_map(self,i,map):
		return 0

	def build_decoder_map(self):
		total = 0
		for i in self.entries:
			self.build_decoder_map_line(i)
			total += i['display_value']

		if DEBUG: print (self)
		return total

	def build_decoder_map_line(self,entry):
		decoded_order = self.decoded_order.copy()

		unique_digit_signals = []
		split_signals = []
		split_unique_symbols = {}
		split_nonunique_symbles = {
			5:[],
			6:[]
		}
		segment_totals = {}
		for i in self.implicit_order:
			segment_totals[i] = 0

		for i in entry['signals']:
			x = list(str(i))
			split_signals.append(x)
			if len(i) in self.unique_digits.keys():
				unique_digit_signals.append([i,x,len(i)])
				split_unique_symbols[self.unique_digits[len(i)]] = x
			else:
				split_nonunique_symbles[len(i)].append(x)
			for j in x:
				segment_totals[j] += 1




	# * "a0" is the segment in 7 that is not in 1
	# "c2" is the segment that is in 1,4,7,8 but not in 6
	# "c2" is the segment that is in 2 and 3 but not in 5
	# "f5" is in everything but 2
	# {'a': 4, 'b': 8, 'c': 7, 'd': 8, 'e': 9, 'f': 7, 'g': 6}
	# oh shit, it's all based on totals....
	# 	* "f5" appears 9 times in the 10-char sequence
	#	* "b1" appears 6 times in the 10-char sequence
	#   * "e4" appears 4 times in the 10-char sequence
	#	* "c2" appears 8 times - so does "a0", but that's identifiable elsewhere
	#	* "g6" appears 7 times, but not in 4
	#	* "d5" is the remainder - appears 7 times and also in 4

		# find a0 - that of 7 that's not in 1
		decoded_order[0] = list(set(split_unique_symbols[7]) - set(split_unique_symbols[1]))[0]

		# find "f5", "b1", and "e4" from segment totals
		for i in segment_totals:
			j = segment_totals[i]
			#"f5"
			if j == 9:
				decoded_order[5] = i
			#"b1"
			elif j == 6:
				decoded_order[1] = i
			#"e4"
			elif j == 4:
				decoded_order[4] = i
			#"c2"
			elif j == 8 and i != decoded_order[0]:
				decoded_order[2] = i
			#"g6"
			elif j == 7 and i not in split_unique_symbols[4]:
				decoded_order[6] = i
			#"d3"
			elif j == 7 and i in split_unique_symbols[4]:
				decoded_order[3] = i


		if DEBUG: print(decoded_order)

		### commented out - first pass at decoding, didn't work
		## !! can't rely on similarity between signals / order within a single signal is irrelevant
		# for i in unique_digit_signals:
		# 	if DEBUG: print("---> ",i)
		# 	j = self.unique_digits[len(i)]
		# 	original_digit_map = self.digit_map[j]
		# 	if DEBUG: print(i,j,original_digit_map)
		# 	c = 0
		# 	d = 0
		# 	for k in original_digit_map:
		# 		if DEBUG: print("?? ",c, k, original_digit_map[k])
		# 		if original_digit_map[c] > 0:
		# 			if DEBUG: print(d)
		# 			if DEBUG: print(i[d])
		# 			if decoded_order[c] == 'z':
		# 				decoded_order[c] = i[d]
		# 			d += 1
		# 		c += 1
		# 	if DEBUG: print(decoded_order)

		entry['decoded'] = True
		for i in decoded_order:
			if i == 'z':
				entry['decoded'] = False
				break

		if entry['decoded'] == True:
			entry['decoded_order'] = decoded_order
			n = 0
			for i in self.digit_map:
				entry['digit_map_elaborate_decoded'][n] = self.build_elaborate_line(i, n, entry['decoded_order'])
				n += 1

		decoded_digits = {}
		for i in entry['digit_map_elaborate_decoded'].keys():
			newkey = ''
			for j in entry['digit_map_elaborate_decoded'][i].keys():
				k = entry['digit_map_elaborate_decoded'][i][j]
				if k[1] == True:
					newkey += '' + k[0]
			decoded_digits[newkey] = i
			decoded_digits[''.join(sorted(newkey))] = i

		entry['digit_dictionary'] = decoded_digits

		display_values = []
		for i in entry['display']:
			j = ''.join(sorted(i))
			display_values.append(str(entry['digit_dictionary'][j]))
				
		entry['display_values'] = display_values
		entry['display_value'] = int(''.join(display_values))

		if DEBUG: print(json.dumps(entry,indent=4))


class testCase(unittest.TestCase):
	global DEBUG
	DEBUG = True

	test_set = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

	def test_one_star(self):
		self.assertEqual(
			one_star(
				self.__class__.test_set
			),
			26
		)

	def test_two_star(self):
		self.assertEqual(
			two_star(
				self.__class__.test_set
			),
			61229
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
