"""Extract the public columns of the AA usage spreadsheet into _data/usage.json.

Keeps only studies dated on or before today, and only: label, date, samples,
short citation, link, and whether the study is from outside the Bafna lab.
Internal notes and AmpliconRepository status columns are dropped.

Usage: python3 -I scripts/extract_usage.py <spreadsheet.xlsx>
"""
import datetime, json, pathlib, re, sys
import openpyxl

OUT = pathlib.Path(__file__).resolve().parent.parent / "_data" / "usage.json"
# Short citations for rows whose author field is a list of names or a first name.
WHO = {
    "DCIS": "Chmelova et al., Nature Communications",
    "HCMI models and tumors": "ElHarouni et al., Nature",
    "Bladder cancer (TCGA rerun)": "Yesudhas et al., bioRxiv",
    "Cervical cancer (HTMCP)": "MacLennan et al., bioRxiv",
    "Prostate cancer (WCDT + CASCADE)": "Moreno-Rodriguez et al., Genome Biology",
    "Lung cancer": "Khandekar et al., bioRxiv",
    "PanPedCan": "Sridhar et al., medRxiv",
    "Urothelial carcinoma|2025-03-11": "Lv et al., Cancer Discovery",
    "Glioma|2025-05-21": "Akdemir et al., bioRxiv",
    "Small cancer cell lung cancer": "Choudhuri et al., Cancer Discovery",
}
LABEL = {"Small cancer cell lung cancer": "Small cell lung cancer", "Hematalogical malignancies": "Hematological malignancies",
         "Original AA paper": "AmpliconArchitect paper", "CCLE": "Cancer cell lines (CCLE)", "DCIS": "Ductal carcinoma in situ",
         "Esophageal Squamous cell carcinoma": "Esophageal squamous cell carcinoma", "Testicular Cancer": "Testicular cancer",
         "Prostate Cancer": "Prostate cancer", "Pancreatic Organoids": "Pancreatic organoids", "Renal Cell Carcinoma": "Renal cell carcinoma",
         "SCLC": "Small cell lung cancer", "Kataegis pancancer": "Pan-cancer (clustered mutations)", "PDX Models": "Pediatric PDX models",
         "3D-landscape TCGA (hg38)": "Pan-cancer 3D genome (TCGA)", "Cell lines": "Cancer cell lines"}
# PubMed links for rows whose reference is a citation without a URL.
PMID = {"Pan-cancer (TCGA)": "32807987", "Head-and-neck cancer (HPV-driven)": "34548317",
        "Kataegis pancancer": "35140399", "Barrett's and Esophageal adenocarcinoma": "37046089"}

def link(ref):
    ref = str(ref or "")
    m = re.search(r"https?://\S+", ref)
    if m: return m.group(0).rstrip(".")
    m = re.search(r"doi:\s*(10\.\S+)", ref, re.I)
    return "https://doi.org/" + m.group(1).rstrip(".") if m else ""

def short(who):
    who = re.sub(r"\s*\(preprint\)", "", str(who)).replace("biorXiv", "bioRxiv").replace("Clinical Cancer research", "Clinical Cancer Research")
    name, _, journal = who.partition(",")
    name = name.replace(" et al.", "").split()[-1] if " " in name.replace(" et al.", "") else name.replace(" et al.", "")
    return f"{name} et al., {journal.strip()}" if journal else name

wb = openpyxl.load_workbook(sys.argv[1], data_only=True)
today = datetime.datetime.now()
rows = []
for r in wb.worksheets[0].iter_rows(min_row=3, values_only=True):
    label, date, n, _, who, ref, bafna = r[:7]
    if not label or not isinstance(date, datetime.datetime) or n is None or date > today:
        continue
    key = f"{label}|{date:%Y-%m-%d}"
    rows.append({
        "label": LABEL.get(label, label),
        "date": f"{date:%Y-%m-%d}",
        "samples": int(n),
        "citation": WHO.get(key) or WHO.get(label) or short(who),
        "url": link(ref) or (f"https://pubmed.ncbi.nlm.nih.gov/{PMID[label]}/" if label in PMID else ""),
        "external": bafna == "No",
        "preprint": bool(re.search(r"rxiv|researchsquare|preprint|10\.64898", f"{who} {ref}", re.I)),
    })
rows.sort(key=lambda x: x["date"])
OUT.write_text(json.dumps(rows, indent=1) + "\n")
print(len(rows), "studies,", sum(x["samples"] for x in rows), "samples,", sum(x["external"] for x in rows), "external")
