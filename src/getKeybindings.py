#!/usr/bin/python3
from dedale.global_vars import *

from dedale.keybindings import setBindings, Binding

class DumyClass():
	def __init__(self):
		self.openEditor=None
		self.copyTextToClipboard=None
		self.copySymbologyToClipboard=None
		self.pasteFromClipboard=None
		self.showHelp=None
		self.close=None
		self.donate=None

dumyObject=DumyClass()

setBindings(dumyObject)

def makeKeysItems(keys):
	keysItems=""
	for aKey in keys:
		keysItems+=f"<item>{aKey}</item>"
	return keysItems

fullXmlDescriptions=""
for aKeybinding in listOfKeybindings.values():
	aKeybindingXmlDescription=f"""<keybinding>
	<keys>{makeKeysItems(aKeybinding.keys)}</keys>
	<code>{aKeybinding.code}</code>
	<desc>{aKeybinding.description}</desc>
</keybinding>\n"""
	fullXmlDescriptions+=aKeybindingXmlDescription

print(fullXmlDescriptions)
