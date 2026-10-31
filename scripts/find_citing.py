"""Find papers that may have used AmpliconArchitect / AmpliconSuite, for the weekly usage update.

Searches Europe PMC for papers that cite the AmpliconArchitect or AmpliconSuite papers, or that
mention the tools in their full text, first published since the date in scripts/usage_reviewed.json.
Papers already in _data/usage.json or already reviewed are skipped.

Usage:
  python3 -I scripts/find_citing.py                 # list new candidates as JSON
  python3 -I scripts/find_citing.py snippets ID     # print full-text passages that mention the tools
                                                    # (ID is a candidate's id or DOI; tries Europe PMC,
                                                    # NCBI, bioRxiv, then the publisher's page)
Papers marked "unclear" in usage_reviewed.json are listed again each run, so they get another look.
"""
import datetime, json, pathlib, re, sys, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
USAGE = ROOT / "_data" / "usage.json"
REVIEWED = ROOT / "scripts" / "usage_reviewed.json"
API = "https://www.ebi.ac.uk/europepmc/webservices/rest"
CITED = {"30674876": "AmpliconArchitect (Deshpande 2019)", "42888240": "AmpliconSuite (Luebeck 2026)"}
# AmpliconRepository is included so reuse of existing results shows up when reading a paper; reuse does not count.
# Matched case-sensitively so "amplicon architecture" doesn't count as a mention.
TOOLS = r"AmpliconArchitect|AmpliconSuite|AmpliconClassifier|AmpliconRepository|Amplicon Architect\b|Amplicon Suite|Amplicon Repository"


# Sentences naming the tools' own papers are citations, not evidence of use.
OWN_PAPERS = r"Exploring the landscape of focal amplifications|AmpliconSuite: an end-to-end workflow"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "jluebeck.github.io usage update (https://jluebeck.github.io)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode()


def search(query):
    out, cursor = [], "*"
    while True:
        q = urllib.parse.urlencode({"query": query, "format": "json", "resultType": "core", "pageSize": 100, "cursorMark": cursor})
        d = json.loads(get(f"{API}/search?{q}"))
        out += d["resultList"]["result"]
        nxt = d.get("nextCursorMark")
        if not nxt or nxt == cursor or not d["resultList"]["result"]:
            return out
        cursor = nxt


def ids(r):
    """Every identifier we might match a paper on, lower-cased."""
    s = {str(r.get(k)).lower() for k in ("doi", "pmid", "pmcid", "id") if r.get(k)}
    return s


def known_ids():
    seen = set()
    for row in json.loads(USAGE.read_text()):
        url = row.get("url", "").lower()
        m = re.search(r"10\.\d{4,9}/[^\s?#]+", url)
        if m:
            seen.add(m.group(0).rstrip("/"))
        m = re.search(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", url)
        if m:
            seen.add(m.group(1))
        m = re.search(r"nature\.com/articles/(s\d+-\d+-\d+-\w+)", url)
        if m:
            seen.add("10.1038/" + m.group(1))
    return seen


def candidates():
    state = json.loads(REVIEWED.read_text())
    since, today = state["since"], datetime.date.today().isoformat()
    window = f"FIRST_PDATE:[{since} TO {today}]"
    found = {}
    for pmid, name in CITED.items():
        for r in search(f"CITES:{pmid}_MED AND {window}"):
            found.setdefault(r["id"], (r, set()))[1].add("cites " + name)
    terms = " OR ".join('"' + t + '"' for t in TOOLS.split("|"))
    for r in search(f"({terms}) AND {window}"):
        found.setdefault(r["id"], (r, set()))[1].add("mentions a tool in full text")
    unclear = {k.lower(): v for k, v in state["reviewed"].items() if v.get("decision") == "unclear"}
    skip = known_ids() | {k.lower() for k in state["reviewed"]} - set(unclear)
    out = []
    for r, why in found.values():
        if ids(r) & skip:
            continue
        authors = r.get("authorString", "")
        out.append({
            "id": r.get("pmcid") or r["id"],
            "doi": r.get("doi", ""),
            "pmid": r.get("pmid", ""),
            "title": r.get("title", ""),
            "authors": authors,
            "journal": (r.get("journalInfo") or {}).get("journal", {}).get("title") or r.get("bookOrReportDetails", {}).get("publisher") or "",
            "preprint": r.get("source") == "PPR",
            "date": r.get("firstPublicationDate", ""),
            "bafna_lab_author": bool(re.search(r"\b(Bafna|Luebeck)\b", authors)),
            "full_text": bool(r.get("pmcid")) or r.get("hasTextMinedTerms") == "Y" or r.get("inEPMC") == "Y",
            "why": sorted(why),
            "link": f"https://doi.org/{r['doi']}" if r.get("doi") else f"https://europepmc.org/article/{r.get('source')}/{r['id']}",
            "previously": next((unclear[i]["note"] for i in ids(r) if i in unclear), None),
        })
    return sorted(out, key=lambda x: x["date"])


def full_text(pid):
    """Full-text XML from Europe PMC, falling back to NCBI PMC for PMCIDs; None if neither has it."""
    try:
        return get(f"{API}/{pid}/fullTextXML")
    except Exception:
        pass
    if pid.upper().startswith("PMC"):
        try:
            xml = get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=" + pid[3:])
            if "<body" in xml:
                return xml
        except Exception:
            pass
    return None


def preprint_xml(doi):
    """bioRxiv/medRxiv full-text XML via their API; None if unavailable (they often rate-limit)."""
    for server in ("biorxiv", "medrxiv"):
        try:
            d = json.loads(get(f"https://api.biorxiv.org/details/{server}/{doi}"))
            coll = d.get("collection") or []
            if coll and coll[-1].get("jatsxml"):
                return get(coll[-1]["jatsxml"])
        except Exception:
            pass
    return None


def publisher_page(doi):
    try:
        html = get("https://doi.org/" + doi)
    except Exception:
        return None
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I)
    return html if len(html) > 20000 else None  # short pages are login walls or redirects


def snippets(key):
    """key: a candidate id (PMCID, PPR id, PMID) or a DOI."""
    doi = key if key.startswith("10.") else None
    xml = None if doi else full_text(key)
    if xml is None and not doi:
        r = search(f"EXT_ID:{key} OR PMCID:{key} OR DOI:{key}") if not key.upper().startswith("PPR") else search(f"EXT_ID:{key} AND SRC:PPR")
        doi = (r[0].get("doi") if r else None)
    if xml is None and doi:
        xml = preprint_xml(doi) if re.match(r"10\.(1101|64898)/", doi) else None
        xml = xml or publisher_page(doi)
    if xml is None:
        sys.exit(f"No readable full text for {key} from Europe PMC, NCBI, bioRxiv or the publisher. Read it with a web-fetch tool at its link, or mark it unclear.")
    xml = re.sub(r"<ref-list.*?</ref-list>", " ", xml, flags=re.S)  # matches in the reference list aren't evidence of use
    text = re.sub(r"<[^>]+>", " ", xml)
    text = re.sub(r"\s+", " ", text)
    sents = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    for i, s in enumerate(sents):
        if re.search(TOOLS, s) and not re.search(OWN_PAPERS, s, re.I):
            print("…", " ".join(sents[max(0, i - 1):i + 2]), "\n")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "snippets":
        snippets(sys.argv[2])
    else:
        print(json.dumps(candidates(), indent=1, ensure_ascii=False))
