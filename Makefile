PROJECTNAME=dedale
#cp config/triumphum.troff deb/usr/share/man/man6/triumphum.1 ; gzip deb/usr/share/man/man6/triumphum.1

#cp config/_triumphum_complete deb/usr/share/zsh/vendor-completions/
DOCKERCONTAINER=${PROJECTNAME}-test-deb
DOCKERSWAPDIRECTORY=$(PWD)/docker-test
DEBDIRECTORY=$(PWD)/deb

getcurrentversion:
	@cat .bumpversion.cfg | grep "current_version =" | sed "s/.* = \(.*\)/\1/"

builddeb:
	./scripts/builddeb.zsh --project-name ${PROJECTNAME} --second-command-name "qr" --source-files-dir debfiles


testdeb:
	@echo "# Nétoyage du repertoire si besoin"
	echo ${DOCKERSWAPDIRECTORY}
	-rm -i --verbose --recursive ${DOCKERSWAPDIRECTORY}/*
	@echo "# Création du repertoire si besoin"
	-mkdir ${DOCKERSWAPDIRECTORY}
	cp ${PROJECTNAME}.deb ${DOCKERSWAPDIRECTORY}
	@echo "# Extinction du conteneur si besoin"
	-docker stop ${DOCKERCONTAINER}
	@echo "# Lancement du conteneur"
	#docker run --name ${DOCKERCONTAINER} -it --rm -v ${DOCKERSWAPDIRECTORY}:/mnt debian:bookworm-slim "apt-get update ; dpkg -i /mnt/${PROJECTNAME}.deb ; triumphum ; bash"
	docker run --name ${DOCKERCONTAINER} -it --rm -v ${DOCKERSWAPDIRECTORY}:/mnt debian:bookworm-slim bash -c "apt-get update ; apt-get install --assume-yes man manpages man-db ; mandb ; PATH=$$PATH/:/usr/games ; dpkg -i /mnt/${PROJECTNAME}.deb ; apt-get install --fix-broken --assume-yes; triumphum ; bash"

man:
	cp config/${PROJECTNAME}.troff ${DEBDIRECTORY}/usr/share/man/man6/${PROJECTNAME}.1 ; gzip ${DEBDIRECTORY}/usr/share/man/man6/${PROJECTNAME}.1

autocomplete:
	echo "Nothing to do"

images:
	inkscape --export-text-to-path --export-filename=logo-blanc-version.vectorized.svg logo-blanc-version.svg
