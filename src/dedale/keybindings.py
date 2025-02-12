#!/usr/bin/python3

from dedale.__init__ import *
from dedale.global_vars import *
# Cas particuliers des mapings où le keycode ne correspond pas au symbole produit.
KEY_MAPPING = {
	# label, caractère
	"Enter": "\n",
	"Return": "\r",
	"Space": " ",
}

def reverseDictionnary(dictionnary):
	# Inverse les clés et valeurs du dictionnaire
	return {v: k for k, v in dictionnary.items()}

def transformKeyToCharacter(key_name):
	# Transformee les codes lisibles en caractères
	return KEY_MAPPING.get(key_name, key_name)

def transform_character_to_key(character_name):
	# Transformes les caractères reçus au claviers en labels lisibles
	reverseKeyMapping=reverseDictionnary(KEY_MAPPING)
	return reverseKeyMapping.get(character_name, character_name)

########################################################################

class Binding:
	# Classe des racourcis dactyliques.
	# key : touche associée
	# code : nom de la variable de l’objet créé
	# description : Description de l’usage tel qu’elle apparaitra à l’utilisateur dans les interfaces d’aide
	# nameInConfigFile : Nom de la fonction à utiliser par le fichier de configuration. Par défaut c’est code qui est utilisé afin de maintenir la plus grande homogénéité entre le code python et le fichier de configuration.
	#                 /!\ Ne déclarer éxplicitement une valeur pour `nameInConfigFile` que s’il éxiste une raison valable.
	# instructions : Nom de la fonction à déclencher lors de la pression sur le binding.
	def __init__(self, keys=None, code=None, description=None, nameInConfigFile=None, instructions=None):
		self.setKeys(keys)
		self.description = description
		self.code = code
		self.instructions=instructions

		if nameInConfigFile == None:
			self.nameInConfigFile = self.code
		else:
			self.nameInConfigFile = nameInConfigFile

		listOfKeybindings[self.code]=self # Adjonction à la liste des genres de jeux

	def setKeys(self, keys):
		# Transforme les codes lisibles en caractères
		self.keys=[]
		for aKey in keys:
			self.keys.append(aKey)

	def executeInstructions(self):
		# Éxectue la fontion associée au binding
		setBottomBarContent(f"{self.key} : Aucune action associée.")

	def makeHtmlDt(self):
		htmlDt=""
		i=0
		for aKey in self.keys:
			i+=1
			if i < len(self.keys):
				separator=", "
			else:
				separator=""
			htmlDt+=f"<kbd>{aKey}</kbd>{separator}"
		return htmlDt

	def prepareHtmlDecriptionEntry(self):
		descriptionEntry=f"""
	<dt>{self.makeHtmlDt()}</dt>
	<dd>{self.description}</dd>
	"""
		return descriptionEntry

	def prepareConfigFileValue(self):
		return ", ".join(self.keys)

	def configFileLine(self):
		configFileLine=f" # {self.description}\n{self.nameInConfigFile} = {self.prepareConfigFileValue()}"
		return configFileLine

########################################################################

def setBindings(instance):
	Binding(keys=["a"], code="toggleToQrcode", description="Symboliser en QRcode", instructions=lambda: instance.setSymbology(listOfSybologies["qrcode"]))
	Binding(keys=["u"], code="toggleToDatamatrix", description="Symboliser en Datamatrix", instructions=lambda: instance.setSymbology(listOfSybologies["datamatrix"]))
	#Binding(keys=["i"], code=, description="", instructions=None) # aztec
	#Binding(keys=["e"], code=, description="", instructions=None) # maxicode
	#Binding(keys=["c"], code=, description="", instructions=None) # pdf417
	#Binding(keys=["b"], code=, description="", instructions=None) # code one
	#Binding(keys=["é"], code=, description="", instructions=None) # Jab
	#Binding(keys=["p"], code=, description="", instructions=None) # Han Xin Code
	#Binding(keys=["x"], code=, description="", instructions=None) # Dotcode
	Binding(keys=["c"], code="edit", description="Ouvrir le texte dans un éditeur", instructions=instance.openEditor)
#	Binding(keys=["o"], code="openClient", description="Ouvrir l’identifiant ou la ressource symbolisée dans un client idoine", instructions=instance.openClient)
	Binding(keys=["y", "Ctrl+C"], code="copyTextToClipboard", description="Copier le texte dans le presse-papier", instructions=instance.copyTextToClipboard)
	Binding(keys=["Shift+y", "Ctrl+Shift+C" ], code="copySymbologyToClipboard", description="Copier la symbologie dans le presse-papier", instructions=instance.copySymbologyToClipboard)
	Binding(keys=["p", "Ctrl+v"], code="pasteFromClipboard", description="Symboliser le contenu du presse-papier", instructions=instance.pasteFromClipboard)
	Binding(keys=["h"], code="showHelp", description="Montrer l’aide", instructions=instance.showHelp)
	Binding(keys=["q"], code="close", description="Quitter", instructions=instance.close)
	Binding(keys=["d"], code="donate", description="Faire un don", instructions=instance.donate)

