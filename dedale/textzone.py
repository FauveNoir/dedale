import html
from PyQt6.QtWidgets import  QTextEdit
from pygments import highlight
from pygments.lexers import guess_lexer, JsonLexer, HtmlLexer
from pygments.formatters import HtmlFormatter
from PyQt6.QtGui import QTextCursor, QTextOption
from PyQt6.QtCore import Qt,  QSize

from PyQt6.QtCore import QVariantAnimation
import functools

class SyntaxHighlighterWidget(QTextEdit):
	def __init__(self, text=None, parent=None):
			super().__init__(parent)
			self.setReadOnly(True)
			self.setCursorWidth(0)  # Supprime le curseur de texte
			self.setStyleSheet("""
				QTextEdit {
					margin-left: 0;
					padding: 0;
					border: none;             /* Supprimer la bordure */
					background-color: none;  /* Fond blanc */
				}
			""")
			# Supprimer les barres de défilement et activer le retour à la ligne automatique
			self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Pas de barre de défilement vertical
			self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Pas de barre de défilement horizontal
			self.setWordWrapMode(QTextOption.WrapMode.WordWrap) 
			self.setText(text)

	def setText(self, text):
		if text == None:
			text = ""
		# Tenter de détecter le langage
		try:
			lexer = guess_lexer(text)
		except:
			lexer = None

		# Si non détecté, on ne met pas de coloration
		if lexer is None:
			highlighted_code = html.escape(text)  # Affiche le texte brut sans HTML
		else:
			# Appliquer la coloration syntaxique
			formatter = HtmlFormatter(style="solarized-light", linenos=False, full=True)
			highlighted_code = highlight(text, lexer, formatter)
			highlighted_code = f"""
			<html>
				<head>
					<style>{formatter.get_style_defs('.highlight')}
						.highlight pre {{
							background: transparent;
							border: none;
							white-space: pre-wrap; 
						}}
						* {{
							font-size: 12px;
							font-familly: "Anonymous Pro", FiraCode, "DejaVu Sans Mono", Monospace;
						}}
					</style>
				</head>
				<body class="highlight" style="border: none;background: transparent;">{highlighted_code}</body>
			</html>
			"""
		self.setHtml(highlighted_code)  # Affichage du HTML formaté

		#self.sizeHint()
		self.document().setTextWidth(self.viewport().width())  # Forcer la largeur du texte
		self.textChanged.connect(self.adjust_height)

	def adjust_height(self):
		"""Ajuste la hauteur du widget en fonction du contenu"""
		self.document().setTextWidth(self.viewport().width())  # Forcer la largeur du texte
		self.document().adjustSize()
		doc_height = self.document().size().height()  # Hauteur du document
		margin = 20  # Marge pour éviter la coupure du texte
		self.setFixedHeight(int(doc_height) + margin)

def helper_function(widget, color):
	widget.setStyleSheet("border-radius: 4px;border: none;background-color: {}".format(color.name()))


def apply_color_animation(widget, start_color, end_color, duration=1000):
	anim = QVariantAnimation(
		widget,
		duration=duration,
		startValue=start_color,
		endValue=end_color,
	)
	anim.valueChanged.connect(functools.partial(helper_function, widget))
	anim.start()
