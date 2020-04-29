#!/usr/bin/env python3

class Alphabet(object):

	def __init__(self, letters=None):
		super(Alphabet, self).__init__()

		self.letters = letters if letters is not None else set()

	def get_letter(self, character):
		for letter in self.letters:
			if letter.character == character:
				return letter

		return None
