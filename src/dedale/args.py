#!/usr/bin/python3

import argparse
import sys
import select
import subprocess

# Dédale
from dedale.__init__ import *
from dedale.global_vars import *

def getParser():
	parser = argparse.ArgumentParser(description="Gestion des options en ligne de commande.")

	# Options sans valeur
#	parser.add_argument("-v", "--verbose", action="store_true", help="Activer le mode verbeux")
#	parser.add_argument("-h", "--help", action="help", help="Afficher l'aide")
	
	# Options exclusives (dark-mode / light-mode)
	#mode_group = parser.add_mutually_exclusive_group()
	#mode_group.add_argument("--dark-mode", action="store_true", help="Activer le mode sombre")
	#mode_group.add_argument("--light-mode", action="store_true", help="Activer le mode clair")

	# Options avec valeur
	parser.add_argument("-c", "--config-file", type=str, help="Spécifier un fichier de configuration")
	parser.add_argument("-S", "--symbology", type=str, help="Spécifier une symbologie", choices=listOfSybologies.keys())

	# Argument positionnel pour une chaîne sans option
	groupSources = parser.add_mutually_exclusive_group()
	groupSources.add_argument("-s", "--from-selection", action="store_true", help="Utiliser la sélection active")
	groupSources.add_argument("-b", "--from-clipboard", action="store_true", help="Utiliser le contenu du presse-papier")
	groupSources.add_argument("text", nargs="?", type=str, help="Texte fourni sans option")

	return parser

def parseArgs():

	parser = getParser()

	args =parser.parse_args()

	pipeData=stdinInput()

	if args.text == None:
		if pipeData != None:
			args.text = pipeData

	return args

def stdinInput():
	if select.select([sys.stdin], [], [], 0.1)[0]:  # Timeout de 0.1s pour éviter le blocage
		return sys.stdin.read()
	return None



def get_selected_text():
	try:
		return subprocess.check_output(["xclip", "-o"], text=True).strip()
	except subprocess.CalledProcessError:
		return None

def get_clipboarded_text():
	try:
		return subprocess.check_output(["xclip", "-selection", "clipboard", "-o"], text=True).strip()
	except subprocess.CalledProcessError:
		return None

def stringToConvert(args):
	if args.from_selection == True:
		return get_selected_text()
	if args.from_clipboard == True:
		return get_clipboarded_text()
	if args.text != None:
		return args.text
