import re

class Plugin:
	active = True

	def __init__(self, controller):
		self.controller = controller

	def solve_anagram(self, anagram):
		anagrams = []
		anagram = list(anagram)
		anagram.sort()

		for n in open('/usr/share/dict/words', 'r'):
		    j = list(n.strip("\n"))
		    j.sort()

		    if j == anagram:
		        anagrams.append(n)

		return anagrams

	def on_message(self, msg):
		anagram_grammar = re.match(r'^--anagram ([\w]+)', msg)

		if anagram_grammar:
			for anagram in self.solve_anagram(anagram_grammar.group(1)):
				self.controller.send_message(anagram)