Convert URLs of digitisations from popular cultural heritage databases (Gallica, IRHT) into metadata about the digitisation.


```bash
$ python src/main.py -c URL_COLUMN -i CSV_INFILE -o JSON_OUTPUT
```

1. Clone this repository.
2. Set up and activate a virtual Python environment (v3.12).
3. Install the requirements `pip install -r requirements.txt`
4. Run the [main.py](src/main.py) script on your CSV of properly formatted URLs.

---

**Input format (CSV)**

- URLs from Gallica should be in the following format: `https://gallica.bnf.fr/ark:/12148/btv1b53000321m`

- URLs from the IRHT should be in the following format: `https://arca.irht.cnrs.fr/ark:/63955/md655d86p718`

Note: The ARK in the IRHT's URL referes to the manuscript in their database, and is not the ARK of the digitization, of which there might be zero or serveral. The ARK in Gallica's URL refers to the digitization, and is not the ARK of the manuscript.

Any URLs not from the data sources for which this tool is currently built to process will be ignored and absent from the results file.

---

**Output format (JSON)**

The URLs' results are rendered in a JSON file and grouped according to the domain of the cultural heritage database.

Gallica results: 

```json
{
    "gallica.bnf.fr": {
        "https://gallica.bnf.fr/ark:/12148/btv1b10509725v": {
            "ark": "ark:/12148/btv1b10509725v",
            "manifest_url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b10509725v/manifest.json",
            "description": "Luce de Gast , Le Roman de Tristan .",
            "repository": null,
            "digitised_by": "Bibliothèque nationale de France",
            "source_images": "https://gallica.bnf.fr/ark:/12148/btv1b10509725v",
            "metadata_source": "http://oai.bnf.fr/oai2/OAIHandler?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:bnf.fr:gallica/ark:/12148/btv1b10509725v",
            "shelfmark": "Bibliothèque nationale de France. Département des Manuscrits. Français 750",
            "title": "Luce de Gast , Le Roman de Tristan .",
            "date": "1272",
            "language": "français",
            "format": "Italie du Sud ou Terre Sainte. - Ecriture gothique (Pierre de Tiergeville), 2 colonnes. - 68 initiales historiées colorées sur fond or dont le champ interne est divisé en deux ou trois registres certaines avec dragons et antennes à feuillage (voir Manuscrits enluminés d’origine italienne) aux feuillets 1, 2, 2v, 3v, 5v, 14, 18, 21v, 42v, 64, 64v, 93v, 95, 97v, 103, 190, 119, 123v, 128, 139v, 148, 148v, 150, 158, 164, 173, 173v, 178v, 185, 191, 195v, 202v, 205, 208v, 213v ; 217v, 228v, 229v, 234v, 247v, 254v, 255, 255v, 260v, 264v, 265, 267v, 268, 268v, 270v, 271v, 272v, 274, 277v, 280v, 281v, 287v, 291, 294, 296v, 300, 303v, 304v, 306v, 309v, 311v, 312. Initiales ornées aux feuillets 195v et 196. Décoration filigranée d’imitation française à l’encre rouge et bleue, bouts-de-ligne aux feuillets 21, 271, 309. (voir Manuscrits enluminés d’origine italienne ). - Parchemin. - 316 feuillets. - 340 x 235 mm. - Reliure de veau fauve sur ais de bois au chiffre de Charles IX, traces de boulons et de fermoirs",
            "catalogue_notice": "http://archivesetmanuscrits.bnf.fr/ark:/12148/cc51000s",
            "work_notice": null,
            "ensemble_notice": null
        },
    }
}
```

IRHT results:

```json
{
    "arca.irht.cnrs.fr": {
        "https://arca.irht.cnrs.fr/ark:/63955/md9673666g7t": {
            "id": 7138,
            "href": "https://api.irht.cnrs.fr/manuscripts/7138",
            "ark_href": "https://api.irht.cnrs.fr/manuscripts/ark:/63955/md9673666g7t",
            "ark": "ark:/63955/md9673666g7t",
            "notice_url": "https://arca.irht.cnrs.fr/ark:/63955/md9673666g7t",
            "shelfmark": "France, Dijon, Bibliothèque municipale, 527 (0300)",
            "support": "parchemin",
            "content": "Tristan en prose",
            "dimensions": "417 x 320",
            "nbpage": "163 f.",
            "dating": "15e s. (ca. 1450-1460)",
            "alt_shelfmarks": [
                "France, Chantilly, Bibliothèque et archives du château, 648 (404)"
            ],
            "illustrations": [
                "iconographie",
                "ornement"
            ],
            "languages": [
                "français",
                "oil"
            ],
            "related_links": [],
            "complete_reproduction": {
                "ark_href": "https://api.irht.cnrs.fr/reproductions/ark:/63955/r78cpr2lwz6g",
                "ark": "ark:/63955/r78cpr2lwz6g",
                "manifest_url": null
            }
        },
    }
}
```