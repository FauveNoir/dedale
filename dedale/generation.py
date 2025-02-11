# Selection de fichiers non occupés
import tempfile
# Génération de qrcode
import qrcode
import qrcode.image.svg
# Génération de datamatrix
from pylibdmtx.pylibdmtx import encode
import svgwrite
from PIL import Image

from dedale.global_vars import *

def getTempFile():
	# Créer un fichier temporaire unique et sécurisé
	with tempfile.NamedTemporaryFile(prefix="dedale-", suffix=".svg", delete=False) as temp_file:
		print(f"Fichier temporaire créé : {temp_file.name}")
	return temp_file


########################################################################
# Classe
########################################################################

class Symbology:
	def __init__(self, name=None, code=None, generationFunction=None):
		self.name = name
		self.code = code
		if generationFunction:
			setattr(self, 'generate', generationFunction)

		listOfSybologies[self.code]=self


	def generate(self, text):
		# Éxectue la fontion associée au binding
		pass

########################################################################
# Fonctions de génération
########################################################################

def generateQRcode(text):
	temp_file=getTempFile()

	qr = qrcode.QRCode(version = 1,
					   box_size = 10,
					   border = 0,
					   image_factory=qrcode.image.svg.SvgPathImage)

	# Adding data to the instance 'qr'
	qr.add_data(text)

	qr.make(fit = True)
	img = qr.make_image(fill_color = 'red',
						back_color = 'white')

	img.save(temp_file.name)
	print(f"Le fichier temporaire est disponible sur {temp_file.name}")
	return temp_file


def generateDataMatrix(text):
	temp_file=getTempFile()

	# Générer le DataMatrix
	encoded = encode(text.encode('utf8'))
	img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)

	# Création du document SVG
	dwg = svgwrite.Drawing(temp_file.name, profile="tiny", size=(int(encoded.width/5), int(encoded.height/5)))

	# Ajouter chaque pixel du DataMatrix au SVG
	i=0
	for y in range(int(encoded.height/5)):
		for x in range(int(encoded.width/5)):
			i+=1
			pixel_index = ( y * encoded.width * 3 * 5) + ( x * 3 * 5 ) # Accéder au bon index dans la liste plate
			if encoded.pixels[pixel_index] == 0:  # 0 = pixel noir (DataMatrix est en niveaux de gris)
				dwg.add(dwg.rect(insert=(x, y), size=(1, 1), fill="black"))

	# Sauvegarde du SVG
	dwg.save()
	return temp_file

########################################################################
# Déclaration des symbiologies
########################################################################

def declareSymbologies():
	Symbology(name="QRcode", code="qrcode", generationFunction=generateQRcode)
	Symbology(name="Datamatrix", code="datamatrix", generationFunction=generateDataMatrix)

