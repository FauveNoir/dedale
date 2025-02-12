#!/usr/bin/python3

import configparser
import os

from dedale.__init__ import *
from dedale.global_vars import *
from dedale.configuration import *

class Parameter():
	def __init__(self, name=None, configFile=None, value=None, defaultValue=None):
		self.name=name
		if configFile==None:
			self.configFile=self.name
		else:
			self.configFile=configFile
		self.defaultValue=defaultValue
		self.value=self.defaultValue

		self.getConfiguredValue()
		globals()[self.name]=self

	def getConfiguredValue(self):
		try:
			config = configparser.ConfigParser()
			config.read_string("[DEFAULT]\n" + open(CONFIG_DIR["path"]).read())
			if config.has_option("DEFAULT", self.configFile):
				valueInConfigFile=config.get("DEFAULT", self.configFile)
				self.value=valueInConfigFile
		except:
			pass


defaultvalues={
	"fontfamily": "'Anonymous Pro', FiraCode, 'Fira Code', 'Fira Mono', Inconsolata,  Consolas, FreeMono, UMTypewriter, 'IBM Plex Mono', 'Noto Mono', DejaVu Sans Mono, Monospace, Monaco, Courier",
	"editor": "xdg-open",
	"defaultSymbology": "qrcode"
}


def deployDefaultConfiguration():
	for key, value in defaultvalues.items():
		Parameter(name=key, defaultValue=value)

deployDefaultConfiguration()
