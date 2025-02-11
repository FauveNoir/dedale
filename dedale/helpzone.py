from PyQt6.QtWidgets import QWidget, QTextBrowser, QVBoxLayout, QLabel
from PyQt6.QtCore import QByteArray
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from dedale.__init__ import *
from dedale.global_vars import *

def prepareDlSection():
	dlSection=""
	for aBinding in listOfKeybindings.values():
		dlSection+=aBinding.prepareHtmlDecriptionEntry()
	return dlSection

def helpText():
	return f"""
	<h1>Aide</h1>

	<dl>
	{prepareDlSection()}
	</dl>

	<p>
	Vous trouverez plus d’aide dans le manuel d’utilisateur à travers :
	</p>
	<pre>$ man dedale</pre>
	"""

class ScaledSvgWidget(QSvgWidget):
	def __init__(self, svg_data, max_width=100):
		super().__init__()
		self.max_width = max_width

		# Charger le SVG
		logo_bytes = QByteArray(svg_data.encode("utf-8"))
		self.renderer().load(logo_bytes)

		# Calculer et appliquer la taille initiale
		self.update_size()

	def update_size(self):
		# Récupérer la taille intrinsèque du SVG
		bbox = self.renderer().viewBoxF()
		aspect_ratio = bbox.width() / bbox.height() if bbox.height() > 0 else 1

		# Définir une largeur max de 100px tout en gardant le ratio
		width = min(self.max_width, bbox.width())
		height = width / aspect_ratio

		# Appliquer la taille
		self.setFixedSize(int(width), int(height))

	def resizeEvent(self, event):
		self.update_size()
		super().resizeEvent(event)


def fullHtmlContent():
	return f"""
		<html>
		<head>
				<style>
				*, h1 {{
					font-size: 14px;
					font-family: "Anonymous Pro", FiraCode, "DejaVu Sans Mono", Monospace;
					border: none;
				}}
				kbd {{
					display: inline-block;
					padding: 0.25rem;
					line-height: 10px;
					color: #f0f6fc;
					vertical-align: middle;
					background-color: #fafbfc;
					border: solid 2px black;
					border-bottom: solid 2px black;
					border-radius: 6px;
					box-shadow: inset 0 -1px 0 black;
					color: black;
					font-weight: bold;
				}}
				h1 {{
				font-weight: bold;
				}}
				</style>
		</head>
		<body>
		{helpText()}
		</body>
		</html>
		"""



class HelpWidget(QWidget):
	def __init__(self):
		super().__init__()

		# HTML avec du CSS intégré
		html_content = "<html><body></body></html>"

		# Créer un QTextBrowser pour afficher du contenu HTML
		self.text_browser = QTextBrowser(self)
		self.text_browser.setHtml(fullHtmlContent())

		# Layout
		layout = QVBoxLayout(self)
		self.setStyleSheet("""
			QTextEdit {
				margin: 0;
				padding: 0;
				border: none;             /* Supprimer la bordure */
				background-color: none;  /* Fond blanc */
			}
		""")

		# Zone d’aide
		layout.addWidget(self.text_browser)

		layout.addStretch()

		# Logo
		logo = ScaledSvgWidget(APP_LOGO_SVG_HORISONTAL, max_width=100)
		layout.addWidget(logo)
		layout.addWidget(logo)

		# Description
		font = QFont("Anonymous Pro, FiraCode, DejaVu Sans Mono, Monospace")
		bottomLabel = QLabel("Dédale est un utilitaire de présentation dynamique de symbologies (QRcode et Datamatrix) pour stations de travail en vue d’échange rapide d’information.")
		bottomLabel.setFont(font)
		bottomLabel.setStyleSheet("font-size: 12px; font-weight: bold;")  # Style optionnel
		bottomLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
		bottomLabel.setWordWrap(True)
		layout.addWidget(bottomLabel)

		# URL
		urlLabel = QLabel("http://taniere.info")
		urlLabel.setStyleSheet("font-size: 12px; font-weight: bold;")  # Style optionnel
		urlLabel.setFont(font)
		urlLabel.setWordWrap(True)
		layout.addWidget(urlLabel)

		# Licence
		licence = QLabel("GPL v3")
		licence.setStyleSheet("font-size: 12px; font-weight: bold;")  # Style optionnel
		licence.setFont(font)
		licence.setWordWrap(True)
		layout.addWidget(licence)

		# Ajustements
		self.setLayout(layout)
		size_policy = self.sizePolicy()
		size_policy.setRetainSizeWhenHidden(True)
		self.setSizePolicy(size_policy)
		self.hide()

	def show(self):
		self.setVisible(True)

presentation="""
Dédale est un utilitaire de présentation dynamique de symbologies (QRcode et Datamatrix) pour stations de travail en vue d’échange rapide d’information.

http://taniere.info

GPLv3

"""
