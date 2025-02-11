import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QSpacerItem, QSizePolicy
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtGui import QKeyEvent, QClipboard, QFont, QKeySequence, QShortcut, QDesktopServices, QColor
from PyQt6.QtCore import Qt,  QMimeData, QTimer, QCoreApplication, QByteArray

# Autre
import argparse
import sys
import select
import subprocess
import html
import pyperclip as pc
import webbrowser
import appdirs
import cairosvg


# Dédale
from dedale.__init__ import *
from dedale.global_vars import *
from dedale.generation import declareSymbologies
from dedale.titlezone import prepareTitle
from dedale.textzone import SyntaxHighlighterWidget, apply_color_animation, editText
from dedale.helpzone import HelpWidget
from dedale.keybindings import setBindings, Binding
import dedale.configfile as configfile
from dedale.configfile import testIfConfigFileExistAndCreateItIfNone,applyRelevantConfiguration

declareSymbologies()

def screenSize(app):
	screen = app.primaryScreen()
#	print('Screen: %s' % screen.name())
	size = screen.size()
#	print('Size: %d x %d' % (size.width(), size.height()))
	rect = screen.availableGeometry()
#	print('Available: %d x %d' % (rect.width(), rect.height()))
	# Calculer la largeur des éléments
	return size.width(), size.height()


class FullscreenSvgApp(QWidget):
	def __init__(self, text=None, configFile=None, symbology="qrcode"):
		super().__init__()

		if symbology == None:
			self.symbology="qrcode"
		else:
			self.symbology=symbology
		self.chargeKeybindings(configFile)
#		#testIfConfigFileExistAndCreateItIfNone()
		# Variables primitives
		self.currentSymbology=listOfSybologies[self.symbology]
		self.text=text

		# Fichier contenant la symbologie
		self.svg_text=None

		# Création des widgets
		self.svg_widget = QSvgWidget()  # Remplace par ton fichier SVG
		self.setSymbology(self.currentSymbology)
		self.textWidget()

		# Ajustement du texte
		self.text_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

		# Layout principal (HORIZONTAL)
		self.layout = QHBoxLayout()
		self.helpZone = HelpWidget()
		self.leftPanel=self.layout.addWidget(self.helpZone, 1)  # Espace vide à gauche
		self.centralPanel=self.layout.addWidget(self.svg_widget, 3)  # SVG au centre (largeur flexible)
		self.rightPanel=self.layout.addLayout(self.text_layout, 1)  # Texte + Titre à droite
		self.layout.setAlignment(self.text_layout, Qt.AlignmentFlag.AlignVCenter)  # Centre verticalement l'ensemble


		self.setLayout(self.layout)


		# Configurer la fenêtre
		self.setWindowTitle("Dédale — affichage dynamique de symbologies")
		self.showFullScreen()
		self.setStyleSheet("background-color: white;")


		# Ajuster la taille de l'image
		self.resizeEvent(None)

	def chargeKeybindings(self, configFile):
		setBindings(self)
		applyRelevantConfiguration(configFile)
		definedKeybindings=[]
		for aBinding in listOfKeybindings.values():
			for aKey in aBinding.keys:
				qShortcut=QShortcut(QKeySequence(aKey), self)
				definedKeybindings.append(qShortcut)
				definedKeybindings[-1].activated.connect(aBinding.instructions)

	def donate(self):
		print(f"Pour soutenir {APP_FANCY_NAME} et faire en sorte qu’il continue et s’améliore, merci de faire un don à <{APP_AUTHOR_DONATION_LINK}>. (^.^)")
		url = "https://www.example.com"
		subprocess.Popen(["python3", "-c", f"import webbrowser; webbrowser.open('{APP_AUTHOR_DONATION_LINK}')"])
		QApplication.quit()

	def openEditor(self):
		new_text=editText(self, self.text)
		self.setNewText(new_text)

	def openClient(self):
		pass

	def showHelp(self):
		self.helpZone.show()

	def textWidget(self):
		font = QFont("Anonymous Pro, FiraCode, DejaVu Sans Mono, Monospace")
		# Préparer le widget du texte 

		# Titre (aligné à gauche)
		self.title_label = QLabel(prepareTitle(self.text))
		self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
		self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")  # Style optionnel
		self.title_label.setFont(font)

		self.text_label=SyntaxHighlighterWidget(self.text)

		# Layout vertical pour le titre + texte
		self.text_layout = QVBoxLayout()
		self.text_layout.addStretch()  # Permet un centrage vertical de l'ensemble
		self.text_layout.addWidget(self.title_label)
		self.text_layout.addWidget(self.text_label)
		self.text_layout.addStretch()  # Permet un centrage vertical de l'ensemble
		self.text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)


	def blink_label(self):
		""" Fait clignoter le QLabel en bleu pendant 2 secondes """
		apply_color_animation(
			self.text_label,
			QColor("#2e9aff"),
			QColor("white"),
			duration=1000,
		)

	def blink_qrcode(self):
		""" Fait clignoter le QLabel en bleu pendant 2 secondes """
		apply_color_animation(
			self.svg_widget,
			QColor("#2e9aff"),
			QColor("white"),
			duration=1000,
		)

	def error_no_text_content(self):
		errorImageFile="/home/fauve/dev/dedale/dedale/error-message.svg"
		self.svg_widget.load(errorImageFile)
		self.svg_widget.repaint()

	def generateImage(self):
		self.svg_text=self.currentSymbology.generate(self.text)
		return self.svg_text

	def setImage(self):
		if self.text == None:
			print("Aucun texte à symboliser n’est fourni")
			self.error_no_text_content()
		else:
			self.generateImage()
			svg_bytes = QByteArray(self.svg_text.encode("utf-8")) 
			self.svg_widget.renderer().load(svg_bytes)
			self.svg_widget.repaint()

	def setSymbology(self, newSymbology):
		self.currentSymbology=newSymbology
		self.setImage()

	def setNewText(self, text):
		self.text=text
		self.setImage()
		self.title_label.setText(prepareTitle(self.text))
		self.text_label.setText(self.text)


	def getSmallestSize(self):
		if self.height() < self.width():
			return self.height()
		return self.width()

	def resizeEvent(self, event):
		""" Ajuste la hauteur du SVG à celle de l’écran """
		window_width, window_height=screenSize(app)
		window_width = self.getSmallestSize()
		self.svg_widget.setFixedSize(window_height-80, window_height-80)  # SVG carré
		self.layout.setContentsMargins(40, 40, 40, 40)  # Marges autour

	def copyTextToClipboard(self):
		clipboard=QApplication.clipboard()
		clipboard.setText(self.text)  # Texte à copier avec 'Y'
		self.blink_label()

	def copySymbologyToClipboard(self):
		# Lire le fichier binaire
		try:
			putSvgInClipboardAsPng(self.svg_text)
			self.blink_qrcode()
		except:
			pass

	def pasteFromClipboard(self):
		clipboard=QApplication.clipboard()
		self.setNewText(clipboard.text())

def putSvgInClipboardAsPng(svg_text):
	png_bytes = cairosvg.svg2png(bytestring=svg_text.encode("utf-8"))

	# Utiliser xclip pour copier dans le presse-papier
	process = subprocess.Popen(["xclip", "-selection", "clipboard", "-t", "image/png"], stdin=subprocess.PIPE)
	process.communicate(input=png_bytes)

	print("L’image PNG a été copiée dans le presse-papier.")



def parseArgs():
	parser = argparse.ArgumentParser(description="Gestion des options en ligne de commande.")

	# Options sans valeur
	parser.add_argument("-v", "--verbose", action="store_true", help="Activer le mode verbeux")
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

if __name__ == "__main__":
	args = parseArgs()
	askedConfigFile=args.config_file
	askedSymbology=args.symbology
	app=QApplication(sys.argv)
	text=stringToConvert(args)
	window=FullscreenSvgApp(text=text, configFile=askedConfigFile, symbology=askedSymbology)
	window.show()
	sys.exit(app.exec())

