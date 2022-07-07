# adventofcode 2021
# crushallhumans
# puzzle 16
# 7/7/2021

import os
import re
import sys
import math
import unittest
import pprint

DEBUG = True


def one_star(param_set):
	print("---------------one_star--------------------")
	param_set = reprocess_input(param_set)
	c = 8888
	for i in param_set:
		continue
	return c


def two_star(param_set):
	print("---------------two_star--------------------")
	param_set = reprocess_input(param_set)
	c = 7777
	for i in param_set:
		continue
	return c

def reprocess_input(param_set):
	if isinstance(param_set,str):
		l = []
		l = [input_line.strip() for input_line in param_set.splitlines()]
		param_set = l
	return param_set	

class BITSMessage:
	hexbin = {
		'0':'0000',
		'1':'0001',
		'2':'0010',
		'3':'0011',
		'4':'0100',
		'5':'0101',
		'6':'0110',
		'7':'0111',
		'8':'1000',
		'9':'1001',
		'A':'1010',
		'B':'1011',
		'C':'1100',
		'D':'1101',
		'E':'1110',
		'F':'1111',
	}
	binhex = {}

	original = ''
	original_header = ''
	original_codedm = ''
	packet_version = -1
	packet_type_id = -1
	packet_type_id_effective = -1
	message = ''
	type_id_methods = {}

	packet_version_len = 3
	packet_type_id_len = 3
	message_section_len = 5
	type_id_versioned_method_dict = {
		'6':{
			'method_definitions':{
				'0':'_decode_operator',
				'4':'_decode_literal',
			},
			'legal_methods':['4']
		},
		'1':{
			'method_definitions':{
				'6':'_decode_operator',
			},
			'legal_methods':['6']
		},
		'7':{
			'method_definitions':{
				'3':'_decode_operator',
			},
			'legal_methods':['3']
		}
	}


	def __init__(self, original_input = ''):
		self.original = original_input
		for k,v in self.hexbin.items():
			self.binhex[str(int(v))] = k

	def __str__(self):
		x = []
		x.append('h: ' + self.original)
		x.append('b: ' + self.to_bin())
		x.append('decode: ' + self.decode())
		x.append('original_header: ' + self.original_header)
		x.append('original_codedm: ' + self.original_codedm)
		x.append('packet_version: ' + self.packet_version)
		x.append('packet_type_id: ' + str(self.packet_type_id))
		x.append('packet_type_id_effective: ' + str(self.packet_type_id_effective))		
		x.append('type_id_methods: ' + str(self.type_id_methods))
		x.append('binhex: ' + pprint.pformat(self.binhex))
		return "\n".join(x)

	def to_bin(self):
		temp_arr = []
		for i in self.original:
			temp_arr.append(self.hexbin[i])
		return "".join(temp_arr)

	def decode(self):
		b = self.to_bin()
		self.packet_version = self.binhex[
			b[
				0 : self.packet_version_len
			]
		]
		self.original_header += b[
			0 : self.packet_version_len
		]
		self.packet_type_id = self.packet_type_id_effective = self.binhex[
			b[
				self.packet_version_len : self.packet_version_len + self.packet_type_id_len
			]		
		]
		self.original_header += b[
			self.packet_version_len : self.packet_version_len + self.packet_type_id_len
		]

		self.original_codedm = b[
			self.packet_version_len + self.packet_type_id_len :
		]

		if self.packet_version in self.type_id_versioned_method_dict:
			self.type_id_methods = self.type_id_versioned_method_dict[
				self.packet_version
			]['method_definitions']
			if self.packet_type_id not in self.type_id_versioned_method_dict[self.packet_version]['legal_methods']:
				self.packet_type_id_effective = '0'
		else:
			raise(Exception('Unknown packet version: ' + self.packet_version))

		self.message = getattr(self, self.type_id_methods[self.packet_type_id_effective])()

		return self.message

	def _decode_operator(self):
		return 'KINETIC_OPERATOR'

	def _decode_literal(self):
		return 'LITERALLY_FALSE'



def puzzle_text():
	print("""
--- Day 16: Packet Decoder ---
As you leave the cave and reach open waters, you receive a transmission from the Elves back on the ship.

The transmission was sent using the Buoyancy Interchange Transmission System (BITS), a method of packing numeric expressions into a binary sequence. Your submarine's computer has saved the transmission in hexadecimal (your puzzle input).

The first step of decoding the message is to convert the hexadecimal representation into binary. Each character of hexadecimal corresponds to four bits of binary data:

0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
A = 1010
B = 1011
C = 1100
D = 1101
E = 1110
F = 1111
The BITS transmission contains a single packet at its outermost layer which itself contains many other packets. The hexadecimal representation of this packet might encode a few extra 0 bits at the end; these are not part of the transmission and should be ignored.

Every packet begins with a standard header: the first three bits encode the packet version, and the next three bits encode the packet type ID. These two values are numbers; all numbers encoded in any packet are represented as binary with the most significant bit first. For example, a version encoded as the binary sequence 100 represents the number 4.

Packets with type ID 4 represent a literal value. Literal value packets encode a single binary number. To do this, the binary number is padded with leading zeroes until its length is a multiple of four bits, and then it is broken into groups of four bits. Each group is prefixed by a 1 bit except the last group, which is prefixed by a 0 bit. These groups of five bits immediately follow the packet header. For example, the hexadecimal string D2FE28 becomes:

110100101111111000101000
VVVTTTAAAAABBBBBCCCCC
Below each bit is a label indicating its purpose:

The three bits labeled V (110) are the packet version, 6.
The three bits labeled T (100) are the packet type ID, 4, which means the packet is a literal value.
The five bits labeled A (10111) start with a 1 (not the last group, keep reading) and contain the first four bits of the number, 0111.
The five bits labeled B (11110) start with a 1 (not the last group, keep reading) and contain four more bits of the number, 1110.
The five bits labeled C (00101) start with a 0 (last group, end of packet) and contain the last four bits of the number, 0101.
The three unlabeled 0 bits at the end are extra due to the hexadecimal representation and should be ignored.
So, this packet represents a literal value with binary representation 011111100101, which is 2021 in decimal.

Every other type of packet (any packet with a type ID other than 4) represent an operator that performs some calculation on one or more sub-packets contained within. Right now, the specific operations aren't important; focus on parsing the hierarchy of sub-packets.

An operator packet contains one or more packets. To indicate which subsequent binary data represents its sub-packets, an operator packet can use one of two modes indicated by the bit immediately after the packet header; this is called the length type ID:

If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.
Finally, after the length type ID bit and the 15-bit or 11-bit field, the sub-packets appear.

For example, here is an operator packet (hexadecimal string 38006F45291200) with length type ID 0 that contains two sub-packets:

00111000000000000110111101000101001010010001001000000000
VVVTTTILLLLLLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBBBBBB
The three bits labeled V (001) are the packet version, 1.
The three bits labeled T (110) are the packet type ID, 6, which means the packet is an operator.
The bit labeled I (0) is the length type ID, which indicates that the length is a 15-bit number representing the number of bits in the sub-packets.
The 15 bits labeled L (000000000011011) contain the length of the sub-packets in bits, 27.
The 11 bits labeled A contain the first sub-packet, a literal value representing the number 10.
The 16 bits labeled B contain the second sub-packet, a literal value representing the number 20.
After reading 11 and 16 bits of sub-packet data, the total length indicated in L (27) is reached, and so parsing of this packet stops.

As another example, here is an operator packet (hexadecimal string EE00D40C823060) with length type ID 1 that contains three sub-packets:

11101110000000001101010000001100100000100011000001100000
VVVTTTILLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBCCCCCCCCCCC
The three bits labeled V (111) are the packet version, 7.
The three bits labeled T (011) are the packet type ID, 3, which means the packet is an operator.
The bit labeled I (1) is the length type ID, which indicates that the length is a 11-bit number representing the number of sub-packets.
The 11 bits labeled L (00000000011) contain the number of sub-packets, 3.
The 11 bits labeled A contain the first sub-packet, a literal value representing the number 1.
The 11 bits labeled B contain the second sub-packet, a literal value representing the number 2.
The 11 bits labeled C contain the third sub-packet, a literal value representing the number 3.
After reading 3 complete sub-packets, the number of sub-packets indicated in L (3) is reached, and so parsing of this packet stops.

For now, parse the hierarchy of the packets throughout the transmission and add up all of the version numbers.

Here are a few more examples of hexadecimal-encoded transmissions:

8A004A801A8002F478 represents an operator packet (version 4) which contains an operator packet (version 1) which contains an operator packet (version 5) which contains a literal value (version 6); this packet has a version sum of 16.
620080001611562C8802118E34 represents an operator packet (version 3) which contains two sub-packets; each sub-packet is an operator packet that contains two literal values. This packet has a version sum of 12.
C0015000016115A2E0802F182340 has the same structure as the previous example, but the outermost packet uses a different length type ID. This packet has a version sum of 23.
A0016C880162017C3686B18A3D4780 is an operator packet that contains an operator packet that contains an operator packet that contains five literal values; it has a version sum of 31.
Decode the structure of your hexadecimal-encoded BITS transmission; what do you get if you add up the version numbers in all packets?
""")



class testCase(unittest.TestCase):
	global DEBUG
	DEBUG = True

	test_set = (
		0,
		1
	)

	def testBITS(self):
		testBITSObject = BITSMessage('D2FE28')
		if DEBUG: print(testBITSObject)
		self.assertEqual(
			testBITSObject.to_bin(),
			'110100101111111000101000'
		)

	def test_one_star(self):
		self.assertEqual(
			one_star(
				self.__class__.test_set
			),
			8888
		)

	def test_two_star(self):
		self.assertEqual(
			two_star(
				self.__class__.test_set
			),
			7777
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
		ret = one_star(input_set)
		print (ret)

		ret = two_star(input_set)
		print (ret)
