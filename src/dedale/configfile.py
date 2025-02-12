#!/usr/bin/python3

import configparser
import os
import appdirs

from dedale.__init__ import *
from dedale.global_vars import *

########################################################################
# Répertoire de configuration
########################################################################

# Obtenez le répertoire de configuration de l'application
#CONFIG_DIR["path"] = None
#CONFIGFILE_FULL_PATH = CONFIG_DIR["path"] + "/" + APP_CODE_NAME


########################################################################
# Récupération des configurations
########################################################################
def getElementHavingParameterWithValue(givenList=None, parameter=None, value=None):
	# Parcourt la liste `givenList` pour y trouver un élément ayant un paramettre nomé `parameter` et ayant pour valeur `value`.
	if parameter is None or value is None:
		return None

	for anElement in givenList:
		if hasattr(anElement, parameter) and getattr(anElement, parameter) == value:
				return anElement
	return None

def applyFileConfigurationsBindings():
	config = configparser.ConfigParser()
	config.read_string("[DEFAULT]\n" + open(CONFIG_DIR["path"]).read())

	configValues={}
	for aBinding in listOfKeybindings.values():
		aConfigKey=aBinding.nameInConfigFile
		# TODO chercher la clé si elle existe
		if config.has_option("DEFAULT", aConfigKey):
			valueInConfigFile=config.get("DEFAULT", aConfigKey).split(", ")
			configValues[aConfigKey]=valueInConfigFile

			aBinding.setKeys(valueInConfigFile)


def applyFileConfigurationsBindingsIfDefaultFileExist():
	default_config_dir = appdirs.user_config_dir() + "/" + APP_CODE_NAME + "rc"
	if os.path.exists(default_config_dir):
#		global CONFIG_DIR
		CONFIG_DIR["path"]=appdirs.user_config_dir() + "/" + APP_CODE_NAME + "rc"
		applyFileConfigurationsBindings()

def applyRelevantConfiguration(askedConfigFile):
	if askedConfigFile == None:
		applyFileConfigurationsBindingsIfDefaultFileExist()
	else:
#		global CONFIG_DIR
		CONFIG_DIR["path"] = askedConfigFile
		applyFileConfigurationsBindings()
