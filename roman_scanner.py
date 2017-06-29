#!/usr/bin/python

"""roman_scanner.py: Basic framework to scan online plain text documents for roman numeral
and report where they are found.
"""
import re
import urllib2


class ScanForRoman(object):

    def __init__(self, url):
        self.text = self.get_content_from_url(url)
        self.url = url
        self.roman_list = []
        self.scan_for_roman(self.text)

    def get_content_from_url(self, url):
        """Get text content from URL"""
        response = urllib2.urlopen(url)
        return response.read()

    def get_roman_numerals_from_line(self, str):
        """Get the roman numerals from a line

        It will return: roman numerals in capital and in lower case letters

        """
        roman_list = []
        str = str.replace('\r','')

        # Regular Expression explanation :
        # (\.\b) : with doc and word end (boundary) e.g VI. bla
        # (\.$) : with at the end of the line IV.|
        # (\,) : with comma and word end e.g. IV, bla
        # (?!\S) : without any string after the number

        # With capital letters
        p = re.compile("(?<!\S)[IVXLCDM]+((?!\S)|(\.\b)|(\.$)|(\,\b))")
        for m in p.finditer(str):
            roman_list.append([m.start(), m.group()])

        # With lower case letters
        p = re.compile("(?<!\S)[ivxlcdm]+((?!\S)|(\.\b)|(\.$)|(\,\b))")
        for m in p.finditer(str):
            str_val = m.group()
            if not str_val in ['did', 'ill', 'id', 'dim', 'vivid', 'civic', 'mill', 'civil', 'mild', 'di', 'villi']:
                roman_list.append([m.start(), m.group()])

        return roman_list

    def scan_for_roman(self, text):
        """Scan for roman numerals to a text"""
        print(self.url)

        for idx, val in enumerate(text.split('\n')):
            roman_list = self.get_roman_numerals_from_line(val)
            for item in roman_list:
                print('Line {idx}, position {pos} : {val}, {line}'.format(
                    idx=idx+1,
                    pos=item[0],
                    val=item[1],
                    line=val
                ))


if __name__ == '__main__':
    scanner = ScanForRoman(url='http://www.gutenberg.org/files/54610/54610-0.txt')
    scanner = ScanForRoman(url='http://www.gutenberg.org/files/54611/54611-0.txt')
    scanner = ScanForRoman(url='http://www.gutenberg.org/cache/epub/54612/pg54612.txt')
    scanner = ScanForRoman(url='http://www.gutenberg.org/files/54613/54613-0.txt')

