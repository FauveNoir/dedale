import magic
from urllib.parse import urlparse
from langdetect import detect
import validators
import pycountry
import locale
import gi
gi.require_version("Gio", "2.0")
from gi.repository import Gio


easterEggValues={
	"Hippocampéléphantocamélos" : "Animal",
}


def get_mime_type(text):
	if text == None:
		return None
	blob = text.encode()  # Convertir en bytes
	mime = magic.Magic(mime=True)  # Détection MIME uniquement
	return mime.from_buffer(blob)

def get_mime_description(mime_type):
	""" Retourne une description lisible d'un type MIME depuis shared-mime-info """
	mime_info = Gio.content_type_get_description(mime_type)
	return mime_info if mime_info else "Type MIME inconnu"


def detect_url_type(text):
	parsed = urlparse(text)
	if parsed.scheme:  # Si un schéma (protocole) est présent
		return parsed.scheme.lower()
	else:
		return None


def isUrlValid(text):
	scheme = detect_url_type(text)  # Analyse l'URL

	# Extraire le schéma (protocole) en minuscule
	# Dictionnaire des validateurs en fonction du schéma
	validation_functions = {
		"http": validators.url,
		"https": validators.url,
		"ftp": validators.url,  # validators.url supporte aussi FTP
		"mailto": validators.email,
		"file": lambda x: True,  # On suppose que les URLs locales sont valides
		"urn": validators.uuid,  # Vérifie si c'est un UUID valide
	}
	if scheme in validation_functions.keys():
		is_valid = validation_functions[scheme](text)
	else:
		is_valid = None
	return is_valid

def prepareUrlText(text):
	if isUrlValid(text) == True:
		return f"Lien {detect_url_type(text)} valide"
	elif isUrlValid(text) == False:
		return f"Lien {detect_url_type(text)} invalide"
	return f"Lien {detect_url_type(text)}"


def prepareTitle(text):
	mimetype=get_mime_type(text)
	if text == None:
		return ""
	if mimetype not in {None, "text/plain"}:
		return get_mime_description(mimetype)
	elif detect_url_type(text) != None:
		return prepareUrlText(text)
	elif text.isdigit():
		return "Nombre entier"
	elif text in easterEggValues.keys():
		return easterEggValues[text]
	else:
		return "Texte libre"
