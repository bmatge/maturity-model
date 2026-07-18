"""Lecture d'un référentiel au format tableur (.xlsx) — stdlib uniquement.

Un .xlsx est un zip de XML : on lit la première feuille + les sharedStrings,
sans dépendance (openpyxl volontairement écarté, cf. issue #3).

Format attendu : une ligne d'en-tête puis UNE LIGNE PAR (capacité × niveau).
Colonnes reconnues (insensibles à la casse et aux accents approximatifs) :
    dimension_numero | dimension_nom | capacite_numero | capacite_nom |
    capacite_description | portee | niveau | niveau_nom | critere | signaux
Les colonnes description et signaux sont optionnelles.
"""

import re
import zipfile
from xml.etree import ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

# alias tolérés → clé canonique
HEADER_ALIASES = {
    "dimension_numero": {"dimension_numero", "dim_numero", "dimension n°", "dimension no", "num_dimension"},
    "dimension_nom": {"dimension_nom", "dimension", "dim_nom"},
    "capacite_numero": {"capacite_numero", "capacité_numero", "numero", "n°", "cap_numero", "num_capacite"},
    "capacite_nom": {"capacite_nom", "capacité", "capacite", "cap_nom"},
    "capacite_description": {"capacite_description", "description", "cap_description"},
    "portee": {"portee", "portée"},
    "niveau": {"niveau", "level"},
    "niveau_nom": {"niveau_nom", "nom_niveau", "libelle_niveau"},
    "critere": {"critere", "critère", "critere_observable", "description_niveau"},
    "signaux": {"signaux", "signaux_observables"},
}
REQUIRED = ("dimension_numero", "dimension_nom", "capacite_numero",
            "capacite_nom", "portee", "niveau", "niveau_nom", "critere")


def _col_index(cell_ref):
    """'BC12' → index de colonne 0-based (54)."""
    letters = re.match(r"[A-Z]+", cell_ref or "").group(0)
    idx = 0
    for ch in letters:
        idx = idx * 26 + (ord(ch) - 64)
    return idx - 1


def _read_rows(stream):
    """Toutes les lignes de la 1re feuille, comme listes de chaînes."""
    with zipfile.ZipFile(stream) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.iter(
                    "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")))
        sheet_names = sorted(n for n in z.namelist()
                             if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n))
        if not sheet_names:
            raise ValueError("classeur sans feuille de calcul")
        root = ET.fromstring(z.read(sheet_names[0]))

    rows = []
    for row in root.findall(".//m:sheetData/m:row", NS):
        values = {}
        for cell in row.findall("m:c", NS):
            idx = _col_index(cell.get("r", ""))
            ctype = cell.get("t", "n")
            if ctype == "inlineStr":
                text = "".join(t.text or "" for t in cell.iter(
                    "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"))
            else:
                v = cell.find("m:v", NS)
                text = v.text if v is not None and v.text is not None else ""
                if ctype == "s":
                    text = shared[int(text)] if text != "" else ""
            values[idx] = text.strip()
        if values:
            width = max(values) + 1
            rows.append([values.get(i, "") for i in range(width)])
    return rows


def _canon(header):
    h = header.strip().lower().replace("é", "e").replace("°", "").replace("  ", " ")
    for key, aliases in HEADER_ALIASES.items():
        if h in {a.replace("é", "e").replace("°", "") for a in aliases}:
            return key
    return None


def parse_referentiel_xlsx(stream, label, description="", cible="organisation"):
    """Retourne le dict référentiel (même structure que l'import JSON)."""
    rows = _read_rows(stream)
    if len(rows) < 2:
        raise ValueError("fichier vide (il faut une ligne d'en-tête + des lignes de données)")

    headers = [_canon(h) for h in rows[0]]
    mapped = {h for h in headers if h}
    missing = [c for c in REQUIRED if c not in mapped]
    if missing:
        raise ValueError(f"colonnes manquantes : {', '.join(missing)}. "
                         f"En-têtes lus : {', '.join(x for x in rows[0] if x)}")

    def get(row, key):
        for i, h in enumerate(headers):
            if h == key and i < len(row):
                return row[i]
        return ""

    dims = {}
    for n, row in enumerate(rows[1:], start=2):
        if not any(x for x in row):
            continue
        try:
            dim_num = int(float(get(row, "dimension_numero")))
            niveau = int(float(get(row, "niveau")))
        except ValueError as e:
            raise ValueError(f"ligne {n} : numéro de dimension ou niveau non numérique ({e})")
        cap_num = str(get(row, "capacite_numero"))
        if not cap_num:
            raise ValueError(f"ligne {n} : numéro de capacité vide")
        dim = dims.setdefault(dim_num, {
            "numero": dim_num, "nom": get(row, "dimension_nom"),
            "description": "", "capacites": {},
        })
        cap = dim["capacites"].setdefault(cap_num, {
            "numero": cap_num, "nom": get(row, "capacite_nom"),
            "description": get(row, "capacite_description"),
            "portee": (get(row, "portee") or "P").upper()[:1],
            "niveaux": [],
        })
        cap["niveaux"].append({
            "niveau": niveau, "nom": get(row, "niveau_nom"),
            "description": get(row, "critere"),
            "signaux_observables": get(row, "signaux"),
        })

    return {
        "label": label,
        "description": description,
        "cible": cible,
        "dimensions": [
            {**d, "capacites": sorted(d["capacites"].values(), key=lambda c: str(c["numero"]))}
            for d in sorted(dims.values(), key=lambda d: d["numero"])
        ],
    }
