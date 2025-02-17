<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="html" indent="yes"/>

	<!-- Récupération des variables globales -->
	<xsl:variable name="name" select="/man/head/name"/>
	<xsl:variable name="codeName" select="/man/head/codeName"/>
	<xsl:variable name="altCodeName" select="/man/head/altCodeName"/>
	<xsl:variable name="shortDesc" select="/man/head/shortDesc"/>
	<xsl:variable name="website" select="/man/head/website"/>
	<xsl:variable name="repository" select="/man/head/repository"/>
	<xsl:variable name="author" select="/man/head/author"/>
	<xsl:variable name="authorCivilName" select="/man/head/authorCivilName"/>
	<xsl:variable name="mansection" select="/man/head/mansection"/>
	<xsl:variable name="donationLink" select="/man/head/donationLink"/>
	<xsl:param name="date"/>
	<xsl:param name="optionsContent"/>
	<xsl:param name="keybindingsContent"/>
	<xsl:param name="synopsisContent"/>



	<!-- Références aux variables depuis le docmuent XML -->
	<xsl:template match="ref[@select='name']">
		<b class="constant"><xsl:value-of select="$name"/></b>
	</xsl:template>

	<xsl:template match="ref[@select='codeName']">
		<xsl:value-of select="$codeName"/>
	</xsl:template>

	<xsl:template match="ref[@select='altCodeName']">
		<xsl:value-of select="$altCodeName"/>
	</xsl:template>

	<!-- Traitement des balises transparentes -->
	<xsl:template match="p | q | span | dl | dt | dd">
		<xsl:copy>
			<xsl:apply-templates  select="node()" />
		</xsl:copy>
	</xsl:template>

	<!-- Blocs de code -->
	<xsl:template match="pre">
		<pre class="language-{@language}">
			<code class="language-{@language}">
				<xsl:apply-templates  select="node()" />
			</code>
		</pre>
	</xsl:template>

<xsl:template match="img">
	<xsl:copy>
		<xsl:copy-of select="@*" />
	</xsl:copy>
</xsl:template>


	<!-- Transformation des liens en liens cliquables -->
	<xsl:template name="transform-to-link">
		<xsl:param name="text" select="."/>
		<a class="link" href="{ $text }">
			<xsl:value-of select="$text" />
		</a>
	</xsl:template>

	<xsl:template match="link">
		<xsl:param name="text" select="."/>
		<a class="link" href="{ $text }">
			<xsl:value-of select="$text" />
		</a>
	</xsl:template>

	<!-- Template pour l'élément option -->
	<xsl:template match="option">
		<dt>
			<a name="option{big}"/>
			<a href="#option{big}">
				<span class="option">
					<xsl:value-of select="small" />
				</span>
				<xsl:if test="var">
					<xsl:text> </xsl:text>
					<var><xsl:value-of select="var" /></var>
				</xsl:if>
				</a>,
				<a href="#option{big}">
					<span class="option">
						<xsl:value-of select="big" />
					</span>
					<xsl:if test="var">
						<xsl:text> </xsl:text>
						<var><xsl:value-of select="var" /></var>
					</xsl:if>
				</a>
			</dt>
			<dd><xsl:value-of select="description" /></dd>
		</xsl:template>

		<xsl:template match="manentry">
			<a href="{@link}">
				<span class="externalCommand usermanual">
					<xsl:value-of select="@name"/><!--
				-->(<xsl:value-of select="@section"/>)<!--
			--></span><!--
		--></a>
		</xsl:template>

	<xsl:template match="man/body/seealso">
	<!-- Génération du titre -->
	<h2>
		<xsl:variable name="tagName" select="name()"/>
		<xsl:variable name="title" select="concat(translate(substring($tagName, 1, 1), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), substring($tagName, 2))"/>
		<xsl:value-of select="$title"/>
	</h2>
	
	
		<p>
		<xsl:for-each select="./manentry">
				<xsl:apply-templates select="."/>
				<xsl:if test="position() != last()">, </xsl:if>
		</xsl:for-each>.
		</p>
	</xsl:template>


	<xsl:template match="keybinding/keys">
		<xsl:for-each select="item">
			<kbd>
				<xsl:value-of select="."/>
				<xsl:if test="position() != last()">, </xsl:if>
			</kbd>
		</xsl:for-each>
	</xsl:template>


	<xsl:template match="keybinding">
		<dt>
			<a name="bindings-{./code}"/>
			<a href="#bindings-{./code}">
				<xsl:apply-templates select="keys"/>
			</a>
		</dt>
		<dd><xsl:value-of select="desc" /></dd>
	</xsl:template>

	<!-- ancrage des titres -->
	<xsl:template name="anchoring">
		<xsl:param name="text" select="."/>
		<xsl:variable name="normalized-text" select="replace(normalize-unicode($text, 'NFKD'), '\P{IsBasicLatin}', '')"/>
		<xsl:variable name="anchor" select="translate($normalized-text, ' ', '_')"/>
		<a name="{$anchor}"></a>
		<a href="#{$anchor}">
			<xsl:value-of select="$text"/>
		</a>
	</xsl:template>

	<xsl:template match="h2 | h3 | h4" name="headingAnchor">
		<xsl:param name="text" select="."/>
		<xsl:copy>
			<xsl:call-template name="anchoring">
				<xsl:with-param name="text" select="$text" />
			</xsl:call-template>
		</xsl:copy>
	</xsl:template>


	<!-- Traitement des sections standardrd -->
	<xsl:template match="name | synopsis | description | terminology | options | examples | bindings | configuration | installation | todo | screenshots | seealso">
		<xsl:variable name="temp">
			<h2>
				<xsl:variable name="tagName" select="name()"/>
				<xsl:variable name="title" select="concat(translate(substring($tagName, 1, 1), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), substring($tagName, 2))"/>
				<xsl:value-of select="$title"/>
			</h2>
		</xsl:variable>
		<xsl:apply-templates select="$temp"/>
		<xsl:apply-templates  select="node()" />
	</xsl:template>

	<xsl:template match="man/body/synopsis/node()">
		<div class="synopsis">
			{<b class="constant"><xsl:value-of select="$codeName"/></b>|<b class="constant"><xsl:value-of select="$altCodeName"/></b>}
			<xsl:copy-of select="parse-xml($synopsisContent)/root/node()"/>
		</div>
	</xsl:template>

	<xsl:template match="man/body/options/node()">
		<dl>
			<xsl:apply-templates select="parse-xml($optionsContent)"/>
		</dl>
	</xsl:template>

	<xsl:template match="man/body/bindings/node()">
		<dl>
			<xsl:apply-templates select="parse-xml($keybindingsContent)"/>
		</dl>
	</xsl:template>

	<xsl:template match="body/name" >
		<xsl:variable name="temp">
			<h2>Name</h2>
			<p>
				<span class="titleName"><xsl:value-of select="$name"/></span> — <span class="titleDescription"><xsl:value-of select="$shortDesc"/></span>
			</p>
		</xsl:variable>
		<xsl:apply-templates select="$temp"/>
	</xsl:template>

	<!-- Traitement global -->
	<xsl:template match="man/head">
	</xsl:template>

	<xsl:template match="man/body">
		<html>
			<head>
				<xsl:copy-of select="$htmlHeaders"/>
			</head>
			<body>
				<xsl:copy-of select="$bodyHeaders"/>
				<article>
					<xsl:apply-templates/>
					<xsl:apply-templates select="$extra-sections"/>
				</article>
				<xsl:copy-of select="$bodyFooter"/>
			</body>
			<xsl:copy-of select="$afterBody"/>
		</html>
	</xsl:template>

	<!-- Sections suplémentaires -->
	<xsl:variable name="extra-sections">
		<h2>Liens</h2>
		<h3>Site web</h3>
		<p>
			<link>
				<xsl:value-of select="$website" />
			</link>
		</p>
		<h3>Dépot git</h3>
		<p>
			<link>
				<xsl:value-of select="$repository" />
			</link>
		</p>
		<h3>Dons</h3>
		<p>Pour soutenir <xsl:value-of select="$name"/> et faire en sorte qu’il continue et s’améliore, merci de faire un don sur
		<link>
			<xsl:value-of select="$donationLink" />
			</link>.
		</p>

		<h2>Auteur</h2>
		<p>Écrit par <xsl:value-of select="$author"/> alias
		<xsl:value-of select="$authorCivilName" />.
	</p>
</xsl:variable>

<xsl:variable name="htmlHeaders">
	<meta name="author" content="{ $author }" />

	<link rel="shortcut icon" href="./favicon.png" />
	<title><xsl:value-of select="$name"/> — <xsl:value-of select="$shortDesc"/></title>

	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<link href="./default.css" rel="stylesheet" />
	<link href="./molokai.css" rel="stylesheet" />

	<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
</xsl:variable>

<xsl:variable name="bodyHeaders">
	<nav class="header">
		<span>
			<xsl:value-of select="$name"/>(<xsl:value-of select="$mansection"/>)
		</span>
		<span>
			<xsl:choose>
				<xsl:when test="$mansection = '1'">Commandes générales</xsl:when>
				<xsl:when test="$mansection = '2'">Appels système</xsl:when>
				<xsl:when test="$mansection = '3'">Fonctions de bibliothèque</xsl:when>
				<xsl:when test="$mansection = '4'">Fichiers spéciaux</xsl:when>
				<xsl:when test="$mansection = '5'">Formats de fichiers et conventions</xsl:when>
				<xsl:when test="$mansection = '6'">Jeux et économiseurs d'écran</xsl:when>
				<xsl:when test="$mansection = '7'">Divers</xsl:when>
				<xsl:when test="$mansection = '8'">Commandes d'administration système</xsl:when>
				<xsl:otherwise>Section inconnue</xsl:otherwise>
			</xsl:choose>
			<xsl:value-of select="' '"/>
		</span>
		<span>
			<xsl:value-of select="$name"/>(<xsl:value-of select="$mansection"/>)
		</span>
	</nav>
</xsl:variable>
<xsl:variable name="bodyFooter">
	<!-- Section footer -->
	<nav class="footer">
		<span></span>

		<span>
			<xsl:value-of select="$date"/>
		</span><xsl:value-of select="' '"/>

		<span>
			<xsl:value-of select="$name"/>(<xsl:value-of select="$mansection"/>)
		</span>
	</nav>
</xsl:variable>

<xsl:variable name="afterBody">
	<script>
		/* Faire en sorte que les descriptions dd se trouvant à droite de label dt suffisement soient hissés à la même hauteur.*/

		let maxWidthForSameLineDescription;

		if (window.innerWidth &lt; 600) {
		maxWidthForSameLineDescription = 3;
		} else {
		maxWidthForSameLineDescription = 7;
		}

		function chToPx(ch) {
		const fontSize = parseFloat(getComputedStyle(document.documentElement).fontSize); // Taille de la police en px
		const chWidth = fontSize * 0.5; // Approximativement la largeur d'un "0" en ch, selon la police
		return ch * chWidth;
		}
		document.querySelectorAll("dt").forEach(dt => {
		console.log(dt)
		if (dt.offsetWidth &lt; chToPx(maxWidthForSameLineDescription) ) {
		const dd = dt.nextElementSibling;
		if (dd &amp;&amp; dd.tagName.toLowerCase() === "dd") {
		dd.style.marginTop = "-1.1em";
		}
		}
		});
	</script>
</xsl:variable>

</xsl:stylesheet>

