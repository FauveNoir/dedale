import configparser
import os
import appdirs

from dedale.__init__ import *
from dedale.global_vars import *

########################################################################
# Répertoire de configuration
########################################################################

# Obtenez le répertoire de configuration de l'application
CONFIG_DIR = None
#CONFIGFILE_FULL_PATH = CONFIG_DIR + "/" + APP_CODE_NAME

########################################################################
# Préparation de la configuration par défaut
########################################################################

def prepareDefaultContent():
	defaultContent="language=fre"
	for aKey in listOfKeybindings.values():
		defaultContent+= "\n" + aKey.configFileLine()
	return defaultContent

########################################################################
# initialisation
########################################################################

def isConfigFileExisting():
	return os.path.exists(CONFIG_DIR)

def createMinimalFile():
	# Crée un fichier minimal avec du contenu
	try:
		with open(CONFIG_DIR, 'w') as f:
			f.write(prepareDefaultContent())
		print(f"Le fichier « {CONFIG_DIR} » a été créé avec succès.")
	except IOError:
		print(f"Erreur : Impossible de créer le fichier « {CONFIG_DIR} ».")


def testIfConfigFileExistAndCreateItIfNone():
	# Crée le fichier à l’emplacement associé si ce dernier n’y est pas déjà
	if not isConfigFileExisting():
		createMinimalFile()


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
	config.read_string("[DEFAULT]\n" + open(CONFIG_DIR).read())

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
		global CONFIG_DIR
		CONFIG_DIR=appdirs.user_config_dir() + "/" + APP_CODE_NAME + "rc"
		applyFileConfigurationsBindings()

def applyRelevantConfiguration(askedConfigFile):
	if askedConfigFile == None:
		applyFileConfigurationsBindingsIfDefaultFileExist()
	else:
		global CONFIG_DIR
		CONFIG_DIR = askedConfigFile
		applyFileConfigurationsBindings()
