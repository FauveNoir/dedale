########################################################################
# Variables globales
########################################################################

APP_CODE_NAME="dedale"
APP_FANCY_NAME="Dedale"
APP_SHORT_DESCRIPTION="Utilitaire de présentation dynamique de symbologies (QRcode et Datamatrix)"
APP_LONG_DESCRIPTION=f"{APP_SHORT_DESCRIPTION} pour stations de travail en vue d’échange rapide d’information."
APP_VERSION="0.2.0"
APP_AUTHOR="Fauve"
APP_LICENCE="AGPLv3"
APP_AUTHOR_MAIL="fauve.ordinator@taniere.info"
APP_AUTHOR_DONATION_LINK="https://paypal.me/ihidev"
APP_URL="http://taniere.info"
APP_LOGO_SVG_SQUARE="""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   width="224.06902mm"
   height="224.05817mm"
   viewBox="0 0 224.06902 224.05816"
   version="1.1"
   id="svg50058"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <defs
     id="defs50055" />
  <g
     id="layer1"
     transform="translate(61.0255,-4.88675)">
    <path
       id="path2353"
       style="stroke:none;stroke-width:0.79375;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke markers fill;stop-color:#000000"
       d="m -61.0255,4.88675 v 224.05816 h 209.13194 14.93708 v -29.87467 h -14.93708 v 14.93759 H -46.08842 V 19.82382 h 194.19486 v 164.30935 h 14.93708 V 4.88675 Z m 29.87622,29.87466 v 14.93707 h 29.87569 v 44.81174 h -14.93862 -14.93707 v 14.93707 H 13.66349 V 34.76141 Z m 59.75191,0 v 74.68588 H 58.47832 73.41591 V 94.51022 H 43.5397 V 49.69848 H 73.41591 V 34.76141 Z m 59.7519,0 v 14.93707 h 29.87622 V 94.51022 H 88.35453 v 14.93707 h 29.87622 14.93707 V 34.76141 Z M -31.14928,64.63556 v 14.93707 h 14.93707 V 64.63556 Z m 89.6276,0 V 79.57263 H 73.41591 V 64.63556 Z m 29.87621,0 v 14.93707 h 14.93708 V 64.63556 Z m -119.50381,59.7488 v 74.68588 h 14.93707 V 169.1961 h 14.93862 v 29.87414 h 14.93708 v -74.68588 z m 59.75191,0 v 74.68588 H 58.47832 73.41591 V 184.13317 H 43.5397 v -59.74881 z m 29.87569,0 v 29.87467 14.93707 h 14.93759 v -44.81174 z m 29.87621,0 v 29.87467 44.81121 h 44.81329 v -14.93707 h -29.87621 v -44.81173 c 9.95873,-2.2e-4 19.91748,-5e-5 29.87621,0 v -14.93708 z m -104.56674,14.93759 h 14.93862 v 14.93708 h -14.93862 z m 134.44296,14.93708 v 14.93707 h 14.93707 v -14.93707 z" />
  </g>
</svg>"""
APP_LOGO_SVG_HORISONTAL="""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Logo Dedal horisontal -->
<svg
   width="403.32526mm"
   height="134.43469mm"
   viewBox="0 0 403.32526 134.43469"
   version="1.1"
   id="svg50058"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <defs
     id="defs50055" />
  <g
     id="layer1"
     transform="translate(58.78892,-34.39689)">
    <path
       id="path47759"
       style="stroke:none;stroke-width:0.79375;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke markers fill;stop-color:#000000"
       d="m -58.78892,34.39689 v 134.43469 h 403.32526 v -29.87466 h -14.93708 v 14.93759 H -43.85184 V 49.33396 h 373.4511 v 74.68589 h 14.93708 V 34.39689 Z m 29.47934,29.47727 v 14.93708 h 29.8757 v 44.81173 h -14.93863 -14.93707 v 14.93707 H 15.50319 V 63.87416 Z m 60.14879,0.39688 v 74.68588 H 60.7149 75.65249 V 124.01985 H 45.77628 V 79.20811 H 75.65249 V 64.27104 Z m 59.7519,0 v 14.93707 h 29.87622 v 44.81174 H 90.59111 v 14.93707 h 29.87622 14.93707 V 64.27104 Z m 59.75191,0 v 74.68588 h 14.93708 v -29.87415 h 14.93862 v 29.87415 h 14.93707 V 64.27104 Z m 59.75243,0 v 74.68588 h 29.87569 14.93759 V 124.01985 H 225.032 V 64.27104 Z m 29.87569,0 v 29.87466 14.93707 h 14.93759 V 64.27104 Z m 29.87518,0 v 29.87466 44.81122 h 44.81329 V 124.01985 H 284.7834 V 79.20811 c 9.95869,-2.2e-4 19.91752,-5e-5 29.87621,0 V 64.27104 Z M 165.2801,79.20863 h 14.93862 V 94.1457 H 165.2801 Z M -29.30958,93.74831 v 14.93707 h 14.93707 V 93.74831 Z m 90.02448,0.39687 v 14.93708 H 75.65249 V 94.14518 Z m 29.87621,0 v 14.93708 h 14.93708 V 94.14518 Z m 209.13142,5.2e-4 v 14.93707 h 14.93708 V 94.1457 Z" />
  </g>
</svg>"""

