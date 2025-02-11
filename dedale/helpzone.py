from PyQt6.QtWidgets import QWidget, QTextBrowser, QVBoxLayout
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
		self.text_browser.setHtml(html_content)

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
		layout.addWidget(self.text_browser)
		self.setLayout(layout)
	def show(self):
		html_content = fullHtmlContent()
		self.text_browser.setHtml(html_content)

presentation="""
Dédale est un utilitaire de présentation dynamique de symbologies (QRcode et Datamatrix) pour stations de travail en vue d’échange rapide d’information.

http://taniere.info

GPLv3

"""
