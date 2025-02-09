import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QSpacerItem, QSizePolicy
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtGui import QKeyEvent, QClipboard, QFont, QKeySequence, QShortcut
from PyQt6.QtCore import Qt,  QMimeData
from PyQt6.QtCore import QTimer
# Autre
import argparse
import sys
import subprocess
import html
import pyperclip as pc

from PyQt6.QtGui import QColor
# Dédale
from dedale.globals import *
from dedale.generation import declareSymbologies
from dedale.titlezone import prepareTitle
from dedale.textzone import SyntaxHighlighterWidget, apply_color_animation
from dedale.helpzone import HelpWidget

declareSymbologies()

def screenSize(app):
	screen = app.primaryScreen()
	print('Screen: %s' % screen.name())
	size = screen.size()
	print('Size: %d x %d' % (size.width(), size.height()))
	rect = screen.availableGeometry()
	print('Available: %d x %d' % (rect.width(), rect.height()))
	# Calculer la largeur des éléments
	return size.width(), size.height()


class FullscreenSvgApp(QWidget):
	def __init__(self, text=None, symbology=listOfSybologies["qrcode"]):
		super().__init__()
		# Variables primitives
		self.currentSymbology=symbology
		self.text=text

		# Fichier contenant la symbologie
		self.temp_file=None

		# Création des widgets
		self.svg_widget = QSvgWidget()  # Remplace par ton fichier SVG
		self.setSymbology(listOfSybologies["qrcode"])
		self.textWidget()

		# Ajustement du texte
		self.text_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

		# Layout principal (HORIZONTAL)
		self.layout = QHBoxLayout()
		helpZone = HelpWidget()
#		self.layout.addStretch(1)  # Espace vide à gauche
		self.leftPanel=self.layout.addWidget(helpZone, 1)  # Espace vide à gauche
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

	def textWidget(self):
		font = QFont("Anonymous Pro, FiraCode, DejaVu Sans Mono, Monospace")
		# Préparer le widget du texte 

		# Titre (aligné à gauche)
		print(self.text)
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

		stClose = QShortcut(QKeySequence("q"), self)
		stClose.activated.connect(self.close)

		stCopyTextToClipboardEmacs = QShortcut(QKeySequence("Ctrl+C"), self)
		stCopyTextToClipboardEmacs.activated.connect(self.copyTextToClipboard)
		stCopyTextToClipboardVim = QShortcut(QKeySequence("y"), self)
		stCopyTextToClipboardVim.activated.connect(self.copyTextToClipboard)

		stCopySymbologyToClipboardEmacs = QShortcut(QKeySequence("Ctrl+Shift+C"), self)
		stCopySymbologyToClipboardEmacs.activated.connect(self.copySymbologyToClipboard)
		stCopySymbologyToClipboardVim = QShortcut(QKeySequence("Shift+y"), self)
		stCopySymbologyToClipboardVim.activated.connect(self.copySymbologyToClipboard)
#
		stToQrcode = QShortcut(QKeySequence("a"), self)
		stToQrcode.activated.connect(lambda: self.setSymbology(listOfSybologies["qrcode"]))
		stToDatamatrix = QShortcut(QKeySequence("u"), self)
		stToDatamatrix.activated.connect(lambda: self.setSymbology(listOfSybologies["datamatrix"]))

		stPastFromClipboardEmacs = QShortcut(QKeySequence("p"), self)
		stPastFromClipboardEmacs.activated.connect(self.pasteFromClipboard)
		stPastFromClipboardVim = QShortcut(QKeySequence("Ctrl+v"), self)
		stPastFromClipboardVim.activated.connect(self.pasteFromClipboard)

	def blink_label(self):
		""" Fait clignoter le QLabel en bleu pendant 2 secondes """
		apply_color_animation(
			self.text_label,
			QColor("#2e9aff"),
			QColor("white"),
			duration=2500,
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
		errorImageFile="/home/fauve/dev/showqr/dedale/error-message.svg"
		self.svg_widget.load(errorImageFile)
		self.svg_widget.repaint()

	def generateImage(self):
		self.temp_file=self.currentSymbology.generate(self.text)
		return self.temp_file

	def setImage(self):
		if self.text == None:
			print("Aucun texte à symboliser n’est fourni")
			self.error_no_text_content()
		else:
			print("génération")
			self.generateImage()
			self.svg_widget.load(self.temp_file.name)
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
		subprocess.run(["xclip", "-selection", "clipboard", "-t", "image/png", "-i", self.temp_file.name])
		self.blink_qrcode()

	def pasteFromClipboard(self):
		clipboard=QApplication.clipboard()
		self.setNewText(clipboard.text())



def parseArgs():
	parser = argparse.ArgumentParser(description="Gestion des options en ligne de commande.")

	# Options sans valeur
	parser.add_argument("-v", "--verbose", action="store_true", help="Activer le mode verbeux")
	parser.add_argument("-s", "--from-selection", action="store_true", help="Utiliser la sélection active")
#	parser.add_argument("-h", "--help", action="help", help="Afficher l'aide")
	
	# Options exclusives (dark-mode / light-mode)
	mode_group = parser.add_mutually_exclusive_group()
	mode_group.add_argument("--dark-mode", action="store_true", help="Activer le mode sombre")
	mode_group.add_argument("--light-mode", action="store_true", help="Activer le mode clair")

	# Options avec valeur
	parser.add_argument("-c", "--config-file", type=str, help="Spécifier un fichier de configuration")
	parser.add_argument("-S", "--symbology", type=str, help="Spécifier une symbologie")

	# Argument positionnel pour une chaîne sans option
	parser.add_argument("text", nargs="?", type=str, help="Texte fourni sans option")

	return parser.parse_args()

def get_selected_text():
	try:
		return subprocess.check_output(["xclip", "-o"], text=True).strip()
	except subprocess.CalledProcessError:
		return None

def stringToConvert(args):
	if args.from_selection == True:
		return get_selected_text()
	if args.text != None:
		return args.text

if __name__ == "__main__":
	args = parseArgs()
	app=QApplication(sys.argv)
	text=stringToConvert(args)
	window=FullscreenSvgApp(text)
	window.show()
	sys.exit(app.exec())

