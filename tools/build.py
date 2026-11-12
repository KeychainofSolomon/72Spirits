"""Build the 72 spirit profiles.

    python tools/build.py REGISTER.json GOETIA.htm

REGISTER.json is Annulus's docs/registers/goetia.json (layer 1, sourced).
GOETIA.htm is the Project Gutenberg Lesser Key (Mathers/Crowley Goetia);
each spirit's own entry is cut out of it and kept verbatim in fontes/.

Writes fontes/goetia.json, profiles/NN-name.json and spiritus.json.
Everything under "ingenium" is derived by the rules in DERIVATION.md,
never invented per spirit, and is marked as derived.
"""

import hashlib
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Pride of rank (DERIVATION.md section 2.1). The Goetia orders the ranks
# King, Prince, Duke, Marquis, Earl, President, Knight.
SUPERBIA = {
    "king": (0.8, 1.0),
    "prince": (0.7, 0.9),
    "duke": (0.6, 0.8),
    "marquis": (0.5, 0.7),
    "earl": (0.4, 0.6),
    "president": (0.4, 0.6),
    "knight": (0.3, 0.5),
}

# Deceit from Annulus's veracity class (section 2.2).
FALLACIA = {
    "FIDUS": (0.0, 0.05),
    "VERAX": (0.0, 0.1),
    "TACITUS": (0.1, 0.5),
    "COACTUS": (0.5, 0.8),
    "MENDAX": (0.7, 0.9),
}
# COACTUS spirits lie unless compelled (a triangle, a name, offerings).
FALLACIA_COACTUS_COMPELLED = (0.0, 0.15)

FURY = re.compile(r"furious|fierce|terrible|wrath", re.I)
HONOUR = re.compile(r"homage|courteous|honou?r|head uncovered|abroad, standing", re.I)
OFFERING = re.compile(r"offering|sacrifice|gift", re.I)
COMPULSION = re.compile(r"compel|constrain|unless|bonds|triangle|ring", re.I)


# Natures (DERIVATION.md section 2.7): what each spirit was made to do,
# read from the kinds of his own offices. An original reading, not the
# witnesses': the names are functions, never anyone else's terms.
NATURAE = {
    "SCIENTIA": {"DOCTRINA", "LINGUAE", "RESPONSA", "MENS", "PROBATIO"},
    "VISIO": {"FUTURA", "PRAETERITA", "PRAESENTIA", "OCCULTA", "THESAURI", "AMISSA", "FURTUM", "VIRTUTES"},
    "VINCULUM": {"CONCORDIA", "DISCORDIA", "FAMILIARES", "DIGNITATES", "APPELLATIO"},
    "FORMA": {"AEDIFICATIO", "TRANSMUTATIO", "VECTIO", "INVISIBILITAS", "ILLUSIO", "TEMPESTAS", "EVERSIO", "CONSECRATIO"},
    "LIMEN": {"MORBUS", "NEX", "MORTUI", "LONGAEVITAS", "TUTELA", "CUSTODIA"},
}
# "Of whom Belial, Bileth, Asmoday, and Gaap, were Chief" (Goetia).
PRINCIPES = {68, 13, 32, 33}


def naturae(offices):
    count = {}
    for i, o in enumerate(offices):
        for name, kinds in NATURAE.items():
            if o["kind"] in kinds:
                c, first = count.get(name, (0, i))
                count[name] = (c + 1, first)
    ranked = sorted(count, key=lambda k: (-count[k][0], count[k][1]))
    return ranked[:2]


def ordo(e, reges):
    q = (e.get("quarter") or {}).get("value")
    rex = None
    for r in reges:
        if r.get("rite") == "goetia" and r.get("quarter") == q:
            names = [x["text"] for x in r.get("names", []) if "S" in x.get("witness", "")]
            rex = (names or [r["names"][0]["text"]])[0]
    return {
        "quarter": q,
        "quarter_witness": (e.get("quarter") or {}).get("witness"),
        "rex": rex,
        "princeps": e["n"] in PRINCIPES,
    }


def clamp(lo, hi):
    return [round(max(0.0, lo), 2), round(min(1.0, hi), 2)]


def goetia_entries(htm_path):
    raw = Path(htm_path).read_text(encoding="utf-8", errors="replace")
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    text = re.sub(r"[ \t]+", " ", text)
    start = text.find("(1.) Bael")
    end = text.find("These be the 72 Mighty Kings")
    if start < 0 or end < 0:
        sys.exit("the Goetia text does not hold the catalogue of the 72")
    body = text[start:end]
    pos = {}
    for n in range(1, 73):
        m = re.search(r"(?<!\d)\(%d\.?\)\s" % n, body)
        if not m:
            sys.exit(f"spirit {n} not found in the Goetia text")
        pos[n] = m.start()
    if sorted(pos.values()) != [pos[n] for n in range(1, 73)]:
        sys.exit("the Goetia entries are out of order")
    out = {}
    for n in range(1, 73):
        chunk = body[pos[n] : pos[n + 1] if n < 72 else len(body)]
        chunk = re.sub(r"\[\d+\]", "", chunk)  # footnote marks
        out[n] = re.sub(r"\s+", " ", chunk).strip()
    return out


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.;])\s+(?=[A-Z])", text) if s.strip()]


def forma(text):
    return [s for s in sentences(text) if re.search(r"appear|form of|shape|likeness|voice|rideth|riding|cometh|speaketh", s, re.I)]


def derive(e, goetia_text):
    rank = e["rank"].split("/")[0]
    ex = {}
    sup = list(SUPERBIA[rank])
    ex["superbia"] = [f"rank {e['rank']} (Sloane 3825 via the register)"]
    cb_text = " ".join(c["text"] for c in e["counterbalances"])
    if HONOUR.search(cb_text):
        sup = [sup[0] + 0.1, sup[1] + 0.1]
        ex["superbia"].append("the witnesses require him to be honoured")

    fal = FALLACIA[e["veracity"]]
    ex["fallacia"] = [f"veracity {e['veracity']}"]
    if e["veracity_condition"]:
        ex["fallacia"].append(e["veracity_condition"])

    malice = [m["text"] for m in e["malice"]]
    hos = 0.1 + 0.2 * len(malice)
    ex["hostilitas"] = (
        [f"malice: {m}" for m in malice] if malice else ["no malice recorded"]
    )

    ret = [0.1, 0.3]
    ex["reticentia"] = ["base"]
    if e["veracity"] == "TACITUS":
        ret = [0.2, 0.4]
        ex["reticentia"] = ["the witnesses are silent on his truthfulness"]
    if re.search(r"cannot be understood|will not answer", cb_text + " " + (e["veracity_condition"] or ""), re.I):
        ret = [0.6, 0.8]
        ex["reticentia"] = ["the witnesses say he withholds unless compelled"]

    fury = [s for s in malice + sentences(goetia_text) if FURY.search(s)]
    return {
        "derived": True,
        "rules": "DERIVATION.md",
        "superbia": clamp(*sup),
        "fallacia": clamp(*fal),
        "fallacia_coactus": clamp(*FALLACIA_COACTUS_COMPELLED)
        if e["veracity"] == "COACTUS"
        else None,
        "hostilitas": clamp(hos - 0.1, hos + 0.1),
        "reticentia": clamp(*ret),
        "ira_adventus": fury,
        "cultus": [c["text"] for c in e["counterbalances"] if HONOUR.search(c["text"])],
        "munera": [
            t
            for t in [c["text"] for c in e["counterbalances"]] + [e["veracity_condition"] or ""]
            if OFFERING.search(t)
        ],
        "coercitio": [c["text"] for c in e["counterbalances"] if COMPULSION.search(c["text"])],
        "naturae": naturae(e["offices"]),
        "ex": ex,
    }


def fold(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def slug(name):
    return re.sub(r"[^a-z]+", "_", name.lower()).strip("_")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    reg_path, htm_path = sys.argv[1:]
    reg_bytes = Path(reg_path).read_bytes()
    register = json.loads(reg_bytes)
    if len(register) != 72:
        sys.exit("the register does not hold 72 spirits")
    goetia = goetia_entries(htm_path)
    reges = json.loads((Path(reg_path).parent / "reges.json").read_text(encoding="utf-8"))
    (ROOT / "fontes").mkdir(exist_ok=True)
    (ROOT / "fontes" / "goetia.json").write_text(
        json.dumps(
            {
                "witness": "The Lesser Key of Solomon: Goetia (Mathers/Crowley), Project Gutenberg; public domain",
                "entries": {str(n): t for n, t in goetia.items()},
            },
            ensure_ascii=False,
            indent=1,
        )
        + "\n",
        encoding="utf-8",
    )
    fons = {
        "register": "Annulus docs/registers/goetia.json",
        "register_sha256": hashlib.sha256(reg_bytes).hexdigest(),
        "goetia": "fontes/goetia.json",
    }
    pdir = ROOT / "profiles"
    pdir.mkdir(exist_ok=True)
    allp = []
    for e in register:
        n = e["n"]
        g = goetia[n]
        if fold(e["name"])[:3] not in fold(g[:200]):
            sys.exit(f"the Goetia entry {n} does not name {e['name']}")
        p = {
            "schema": "72spirits/1",
            "n": n,
            "name": e["name"],
            "label": slug(e["name"]),
            "essentia": {k: v for k, v in e.items() if k not in ("n", "name")},
            "goetia": {"textus": g, "forma": forma(g)},
            "ingenium": derive(e, g),
            "ordo": ordo(e, reges),
            "fons": fons,
        }
        (pdir / f"{n:02d}-{p['label']}.json").write_text(
            json.dumps(p, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
        )
        allp.append(p)
    (ROOT / "spiritus.json").write_text(
        json.dumps(allp, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8"
    )
    print(f"wrote 72 profiles; register sha256 {fons['register_sha256'][:12]}")


if __name__ == "__main__":
    main()
