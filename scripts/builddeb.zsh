#!/bin/zsh
############################################################################
# Options
############################################################################

DEBDIRECTORY=$(pwd)/deb
PROJECTNAME=""
SOURCEDIR=src
SECONDCOMMANDNAME=""
DEBFILESDIR=debfiles

while [[ $# -gt 0 ]]; do
	case "$1" in
		--output-directory)
			shift
			DEBDIRECTORY="$1"
			;;
		--project-name)
			shift
			PROJECTNAME="$1"
			;;
		--second-command-name)
			shift
			SECONDCOMMANDNAME="$1"
			;;
		--source-files-dir)
			shift
			DEBFILESDIR="$1"
			;;
		*)
			echo "Option inconnue : $1"
			exit 1
			;;
	esac
	shift
done

############################################################################
# Vérification des variables
############################################################################


echo "Répertoire de sortie : " ${DEBDIRECTORY}
echo "Nom du projet : " ${PROJECTNAME}
echo "Commande secondaire : " ${SECONDCOMMANDNAME}
echo "Répertoire des fichiers prépartoires : " ${DEBFILESDIR}

############################################################################
# Fonctions
############################################################################


function processTitle()
{
	echo "############################################################################"
	echo "# $@"
	echo "############################################################################"
}


############################################################################
# 
############################################################################

processTitle "Supression du repertoire"
rm --verbose --recursive ${DEBDIRECTORY}/

processTitle "Mise en place de la hiérarchie"
mkdir --verbose --parent ${DEBDIRECTORY}/DEBIAN # Contient control
mkdir --verbose --parent ${DEBDIRECTORY}/usr/bin/ # Containt main.py sous son nom deffinitif
mkdir --verbose --parent ${DEBDIRECTORY}/usr/lib/python3/dist-packages/${PROJECTNAME} # Contient la bibliothèque de modules
mkdir --verbose --parent ${DEBDIRECTORY}/usr/share/doc/${PROJECTNAME}/ # Copyright et licence

processTitle "Situation après création de l’arborescence"
exa -T deb
#mkdir --verbose --parent ${DEBDIRECTORY}/usr/share/man/man1/ # Manuel
#mkdir --verbose --parent ${DEBDIRECTORY}/usr/share/zsh/vendor-completions/ # Autocompletion pour zsh
#mkdir --verbose --parent ${DEBDIRECTORY}/usr/share/bash-completion/completions # Autocompletion pour bash

processTitle "Copie des fichiers de construction à leur emplacement idoine"
cp --verbose ${DEBFILESDIR}/control ${DEBDIRECTORY}/DEBIAN/
cp --verbose ${DEBFILESDIR}/copyright ${DEBDIRECTORY}/usr/share/doc/${PROJECTNAME}/
cp --verbose ${DEBFILESDIR}/LICENSE ${DEBDIRECTORY}/usr/share/doc/${PROJECTNAME}/
gzip --verbose --no-name -9 --to-stdout ${DEBFILESDIR}/changelog > ${DEBDIRECTORY}/usr/share/doc/${PROJECTNAME}/changelog.gz

processTitle "Copie des éxecutables"
cp --verbose ${SOURCEDIR}/main.py ${DEBDIRECTORY}/usr/bin/${PROJECTNAME}
ln -s ${DEBDIRECTORY}/usr/bin/${PROJECTNAME} ${DEBDIRECTORY}/usr/bin/${SECONDCOMMANDNAME}
chmod +x ${DEBDIRECTORY}/usr/bin/${PROJECTNAME}
for file in $(git ls-files ${SOURCEDIR}/${PROJECTNAME}/) ; do cp --verbose $file ${DEBDIRECTORY}/usr/lib/python3/dist-packages/${PROJECTNAME} ; done

processTitle "Copie de la page de manuel"
#gzip --verbose --no-name -9 --to-stdout ${DEBFILESDIR}/${PROJECTNAME}.troff > ${DEBDIRECTORY}/usr/share/man/man1/${PROJECTNAME}.1.gz
#chmod 644 ${DEBDIRECTORY}/usr/share/man/man1/${PROJECTNAME}.1.gz
#
#processTitle "Copie de l’autocompletion pour zsh"
#cp --verbose ${DEBFILESDIR}/zsh-completion.zsh ${DEBDIRECTORY}/usr/share/zsh/vendor-completions/_${PROJECTNAME}
#
#processTitle "Copie de l’autocompletion pour bash"
#cp --verbose ${DEBFILESDIR}/bash-completion.bash ${DEBDIRECTORY}/usr/share/bash-completion/completions/${PROJECTNAME}

processTitle "Situation finale"
exa -T deb

processTitle "Construction du paquet"
dpkg-deb --root-owner-group --build deb ${PROJECTNAME}.deb
lintian ${PROJECTNAME}.deb
