#!/usr/bin/env python3

	# We initialize the object with the letters recognized by the alphabet of the automaton
class Alphabet(object):

	def __init__(self, letters=None):
		super(Alphabet, self).__init__()

		self.letters = letters if letters is not None else set()

	def copy(self):
		alphabet_copy = Alphabet()
		for letter in self.letters:
			letter.copy(alphabet_copy)

	def get_letter(self, character):
		for letter in self.letters:
			if letter.character == character:
				return letter

		return None
