***
## Definiciones

- **Corpus (pl. corpora).** Se refiere a un conjunto de datos, recopilados de manera cuidadosa, a veces anotados y/o curados. 
- **Documentos/Instancias.** Los elementos que componen un corpus se conocen como documentos o instancias.
	- Para hacer un paralelismo con los datasets que generalmente utilizamos en ML, un documento es equivalente a una observación.
<figure>
	<img src='attachments/corpus-documents.png' height=300 width=300 style="display: block; margin: 0 auto;"/>
</figure>
***
# ReGex

- Formalmente, una expresión regular es una notación algebraica que nos permite caracterizar una línea de texto.
	- En otras palabras, es una herramienta que nos permite describir patrones en un texto.
- Son particularmente útiles para buscar patrones en los textos de nuestro corpus. Por ejemplo, podríamos pasarle una expresión regular a una función para que busque a lo largo de nuestro corpus y nos devuelva los textos que contienen dicha expresión.
- En este [artículo](https://www.datacamp.com/cheat-sheet/regular-expresso?utm_source=google&utm_medium=paid_search&utm_campaignid=21057859163&utm_adgroupid=157296746777&utm_device=c&utm_keyword=&utm_matchtype=&utm_network=g&utm_adpostion=&utm_creative=733936255835&utm_targetid=aud-1903815585993:dsa-2219652735816&utm_loc_interest_ms=&utm_loc_physical_ms=9070458&utm_content=ps-other~latam-en~dsa~tofu~cheat-sheet-data-science&accountid=9624585688&utm_campaign=230119_1-ps-other~dsa~tofu_2-b2c_3-latam-en_4-prc_5-na_6-na_7-le_8-pdsh-go_9-nb-e_10-na_11-na&gad_source=1&gad_campaignid=21057859163&gbraid=0AAAAADQ9WsGV959nRh4xZDfm_vKLOcKHF&gclid=Cj0KCQjwiqbBBhCAARIsAJSfZkadfOgxs8udFor_j0ypehF2iJ_SyGAml-ZQxM1swQ1gEJTxv6ffLrsaAoerEALw_wcB) podemos encontrar las expresiones regulares más utilizadas.

# Text normalization

