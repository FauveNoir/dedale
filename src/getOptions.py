#!/usr/bin/python3

from dedale.generation import declareSymbologies, putSvgInClipboardAsPng
from dedale.args import getParser, parseArgs, stringToConvert
import argparse
from argparse import _StoreAction

declareSymbologies()
parser = getParser()

def isItStoreAction(anArgument):
	if isinstance(anArgument, _StoreAction):
		return True
	return False

def printVarTagIfAny(anArgument):
	if isItStoreAction(anArgument):
		return f"<var>{anArgument.dest}</var>"
	return "<!-- Aucune valeure associée -->"

for anArgument in parser._actions:
	if len(anArgument.option_strings) > 0:
		print(f"""<option>
<small>{anArgument.option_strings[0]}</small>
<big>{anArgument.option_strings[1]}</big>
{printVarTagIfAny(anArgument)}
<description>{anArgument.help}</description>
</option>""")

