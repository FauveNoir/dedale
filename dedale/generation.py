# Selection de fichiers non occupés
# Génération de qrcode
import qrcode
import qrcode.image.svg
# Génération de datamatrix
from pylibdmtx.pylibdmtx import encode
import svgwrite
from PIL import Image

from dedale.global_vars import *



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

	qr = qrcode.QRCode(version = 1,
					   box_size = 10,
					   border = 0,
					   image_factory=qrcode.image.svg.SvgPathImage)

	# Adding data to the instance 'qr'
	qr.add_data(text)

	qr.make(fit = True)
	img = qr.make_image(fill_color = 'red',
						back_color = 'white')

	svg_text = img.to_string().decode("utf-8") 
	return svg_text


def generateDataMatrix(text):

	# Générer le DataMatrix
	encoded = encode(text.encode('utf8'))
	img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)

	# Création du document SVG
	dwg = svgwrite.Drawing("/tmp/test.txt", profile="tiny", size=(int(encoded.width/5), int(encoded.height/5)))

	# Ajouter chaque pixel du DataMatrix au SVG
	i=0
	for y in range(int(encoded.height/5)):
		for x in range(int(encoded.width/5)):
			i+=1
			pixel_index = ( y * encoded.width * 3 * 5) + ( x * 3 * 5 ) # Accéder au bon index dans la liste plate
			if encoded.pixels[pixel_index] == 0:  # 0 = pixel noir (DataMatrix est en niveaux de gris)
				dwg.add(dwg.rect(insert=(x, y), size=(1, 1), fill="black"))

	svg_text = dwg.tostring()

	return svg_text

########################################################################
# Déclaration des symbiologies
########################################################################

def declareSymbologies():
	Symbology(name="QRcode", code="qrcode", generationFunction=generateQRcode)
	Symbology(name="Datamatrix", code="datamatrix", generationFunction=generateDataMatrix)

