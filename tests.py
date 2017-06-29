#!/usr/bin/python
# -*- coding: utf8 -*-

"""This is the test suite for testing the RomanConvertor script. To execute the tests:
    ./tests.py
"""
import os
import unittest
import signal

from subprocess import Popen, PIPE


class TestRomanConvertor(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.dirname(os.path.realpath(__file__ ))
        script_path = os.path.join(current_dir, 'RomanConvertor')
        self.pipe = Popen([script_path], stdin=PIPE,stdout=PIPE, preexec_fn=os.setsid)

    def tearDown(self):
        # Kill the process
        os.killpg(os.getpgid(self.pipe.pid), signal.SIGTERM)

    def get_response(self, input_str):
        """Get response, remove newline, return integer"""
        # Write the stdin
        self.pipe.stdin.write(input_str.encode('utf-8') + '\n')

        if ' ' in input_str:
            out = ''
            for line in input_str.split(' '):
                out += self.pipe.stdout.readline()
        else:
            out = self.pipe.stdout.readline()
        out = out[:-1]
        out = out.replace('\n',' ')
        return out

    def test_count_till_10(self):
        """Test to count 1 till 10"""
        num_dict = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10}
        for key,value in num_dict.iteritems():
            self.assertEqual(self.get_response(key), str(value))

    def test_basic_combinations(self):
        """Test basic combinations"""
        num_dict = {'X': 10, 'XX': 20, 'XXX': 30, 'XL': 40, 'L': 50, 'LX': 60, 'LXX': 70, 'LXXX': 80, 'XC': 90,
                    'C': 100, 'CC': 200, 'CCC': 300, 'CD': 400, 'D': 500, 'DC': 600, 'DCC': 700, 'DCCC': 800, 'CM': 900,
                    'M': 1000}
        for key,value in num_dict.iteritems():
            self.assertEqual(self.get_response(key), str(value))

    def test_advanced_combinations(self):
        """Test advanced combinations"""
        num_dict = {'MCMLXXXIV': 1984, 'DCCLXVII': 767, 'MCMXCIV': 1994 }
        for key,value in num_dict.iteritems():
            self.assertEqual(self.get_response(key), str(value))

    def test_multiple_numbers(self):
        """Test multiple numbers"""
        self.assertEqual(self.get_response('V IV X'), '5 4 10')

    @unittest.expectedFailure
    def test_large_numbers(self):
        """Test large numbers"""
        self.assertEqual(self.get_response('V̅'), '5000')

    def test_invalid_not_capital_roman_letters(self):
        """Test invalid not capital roman letter"""
        self.assertEqual(self.get_response('v'), '0')

    @unittest.expectedFailure
    def test_invalid_alphanumerical(self):
        """Test invalid alphanumerical"""
        self.assertEqual(self.get_response('CRA'), '0')


if __name__ == '__main__':
    unittest.main()
