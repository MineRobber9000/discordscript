from sly import Lexer as SlyLexer

class Lexer(SlyLexer):
	tokens = { CHARDET, LINE }
	ignore = ''

	@_(r'== ([A-Z0-9 ]+)(?=\n)')
	def CHARDET(self,t):
		t.value = t.value[3:].rstrip()
		return t

	LINE = r'(.+)(?=\n)'

	@_(r'\n+')
	def ignore_newline(self,t):
		self.lineno+=len(t.value)

import sys
def caller_id():
	return sys._getframe(2).f_code.co_name

class Parser:
	def __init__(self): pass
	def run(self,text):
		if type(text)==list: tokens = text
		else: tokens = list(Lexer().tokenize(text))
		pos = 0
		out = []
		message = {"speaker":"UNSPECIFIED","message":""}
		while pos < len(tokens):
#			print(tokens[pos].type,tokens[pos].value)
			if tokens[pos].type=="CHARDET":
				if message["message"]:
					out.append(message)
					message = {"speaker":"UNSPECIFIED","message":""}
				message["speaker"]=tokens[pos].value
			elif tokens[pos].type=="LINE":
				message["message"]+=tokens[pos].value.rstrip()+"\n"
			pos+=1
		if message["message"]:
			out.append(message)
		return out

def parses(text):
	return Parser().run(text)

def parse(fileobj):
	return Parser().run(fileobj.read())

def parse_file(filename):
	with open(filename) as f:
		return parse(f)
