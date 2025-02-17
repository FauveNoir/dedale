#!/usr/bin/python3

from dedale.generation import declareSymbologies, putSvgInClipboardAsPng
from dedale.args import getParser, parseArgs, stringToConvert
import argparse
from argparse import _StoreAction

declareSymbologies()
parser = getParser()

import re

def generate_synopsis_html(parser):
	# Obtenir le synopsis brut
	usage = parser.format_usage().strip()

	# Supprimer "usage: ..." du début
	usage = re.sub(r'^usage:\s+\S+\s+', '', usage)

	# Construire un dictionnaire des options
	options = {}
	for action in parser._actions:
		if action.option_strings:
			short_opt = action.option_strings[0]  # Prend la première forme (-c)
			long_opt = action.option_strings[1]  # Prend la forme longue (--config)
			options[short_opt] = (long_opt, action.metavar)  # Associe le paramètre


	# Remplacer les options par un lien HTML et mettre les paramètres dans <var>
	def replace_option(match):
		opt = match.group(0)  # Option détectée (-c, -S, etc.)
		if opt in options:
			long_opt, metavar = options[opt]
			if metavar:  # Si l'option a un paramètre, l'entourer de <var>
				return f'<a class="option" href="#option{long_opt}">{opt}</a> <var>{metavar}</var>'
			else:
				return f'<a class="option" href="#option{long_opt}">{opt}</a>'
		return opt  # Si l'option n'est pas reconnue, ne rien modifier

	# Remplacement des options détectées par leur version HTML
	synopsis_html = re.sub(r'(-\w+)', replace_option, usage)

	# Encapsuler dans une div
	return f'{synopsis_html}'

print(generate_synopsis_html(parser))
