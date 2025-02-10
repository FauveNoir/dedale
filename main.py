import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QSpacerItem, QSizePolicy
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtGui import QKeyEvent, QClipboard, QFont, QKeySequence, QShortcut
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from PyQt6.QtCore import Qt,  QMimeData
from PyQt6.QtCore import QTimer
from PyQt5.QtCore import QUrl, QCoreApplication
# Autre
import argparse
import sys
import select
import subprocess
import html
import pyperclip as pc
import webbrowser

from PyQt6.QtGui import QColor
# Dédale
from dedale.globals import *
from dedale.generation import declareSymbologies
from dedale.titlezone import prepareTitle
from dedale.textzone import SyntaxHighlighterWidget, apply_color_animation
from dedale.helpzone import HelpWidget
from dedale.keybindings import setBindings, Binding

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

		self.chargeKeybindings()

		# Ajuster la taille de l'image
		self.resizeEvent(None)

	def chargeKeybindings(self):
		setBindings(self)
		definedKeybindings=[]
		for aBinding in listOfKeybindings.values():
			print(aBinding.code)
			for aKey in aBinding.keys:
				print(aKey)
				qShortcut=QShortcut(QKeySequence(aKey), self)
				definedKeybindings.append(qShortcut)
				definedKeybindings[-1].activated.connect(aBinding.instructions)

	def donate(self):
#		print(f"Pour soutenir {APP_FANCY_NAME} et faire en sorte qu’il continue et s’améliore, merci de faire un don à <{APP_AUTHOR_DONATION_LINK}>. (^.^)")
		url = "https://www.example.com"
		subprocess.Popen(["python3", "-c", f"import webbrowser; webbrowser.open('{url}')"])
		# Ouvrir un lien dans le navigateur
#		QDesktopServices.openUrl(QUrl("https://www.example.com"))
		QApplication.quit()
		# Fermer l'application
#		sys.exit()

	def openEditor(self):
		pass

	def openClient(self):
		pass

	def showHelp(self):
		self.helpZone.show()

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
		try:
			subprocess.run(["xclip", "-selection", "clipboard", "-t", "image/png", "-i", self.temp_file.name])
			self.blink_qrcode()
		except:
			pass

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

