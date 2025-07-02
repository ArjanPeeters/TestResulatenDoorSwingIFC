import streamlit as st
import pandas as pd
from datetime import date
import re

st.set_page_config(layout="wide")  # ⬅️ Brede modus inschakelen

# ===== Invoervelden voor bestandsnaam =====
st.title("Deur-swingline testmatrix")

col1, col2 = st.columns(2)
with col1:
    checksoftware = st.text_input("🛠️ Checksoftware", placeholder="Bijv. Solibri v9.13")
with col2:
    controle_datum = st.date_input("📅 Datum van controle", value=date.today())

st.markdown("Geef per combinatie aan wat het resultaat is (correct, fout, genegeerd, etc.).")

# Sanitize bestandsnaam
def sanitize_filename(s):
    return re.sub(r"[^a-zA-Z0-9_\-]", "_", s)

# Matrixdefinities
test_matrix = [
    ("Default deur Autodesk", "Works fine"),
    ("Swinglines nested", "Swinglines are ignored"),
    ("Swinglines shared nested", "Flipping and mirroring is going wrong. Rotation 180 degrees works fine"),
    ("Operation: SINGLE_SWING_RIGHT", "Operation works good. In Solibri the swing plan is shown over the total width. When a door has a skylight this will be ignored."),
    ("Operation: SINGLE_SWING_RIGHT nested", "Fout met flippen en spiegelen. Roteren gaat goed"),
    ("Unhosted swinglines", "Flipping and mirroring is going wrong. Rotation 180 degrees works fine"),
    ("Unhosted swinglines shared", "Flipping and mirroring is going wrong. Rotation 180 degrees works fine"),
    ("Swinglines shared nested: RCP upwards", "Flipping and mirroring is going wrong. Rotation 180 degrees works fine"),
    ("Swinglines shared nested: RCP downwards", "Flipping and mirroring is going wrong. Rotation 180 degrees works fine"),
]

kolommen = [
    "Default", "Flipped X", "Flipped Y", "Rotated 180",
    "Mirror X", "Mirror Y", "Group Default", "Group Rotated 180",
    "Group Mirror X", "Group Mirror Y"
]

status_opties = ["", "✅ Correct", "⚠️ Fout", "❌ Genegeerd", "❓ Onbekend"]

# Load bestaande data
try:
    df = pd.read_csv("tijdelijke_testresultaten.csv", index_col=0)
except FileNotFoundError:
    df = pd.DataFrame(index=[t[0] for t in test_matrix], columns=kolommen)

# ===== Kolomheaders bovenaan renderen =====
st.markdown("#### Testmatrix")
kolom_headers = st.columns(len(kolommen) + 1)
kolom_headers[0].markdown("**Testcase**")
for i, kolom in enumerate(kolommen):
    kolom_headers[i+1].markdown(f"**{kolom}**")

# ===== Matrixinvoer per rij =====
for test_naam, toelichting in test_matrix:
    rij = st.columns(len(kolommen) + 1)
    rij[0].markdown(f"**{test_naam}**")
    for i, kolom in enumerate(kolommen):
        key = f"{test_naam}_{kolom}"
        huidige_waarde = df.loc[test_naam, kolom] if not pd.isna(df.loc[test_naam, kolom]) else ""
        df.loc[test_naam, kolom] = rij[i+1].selectbox(
            "",
            status_opties,
            index=status_opties.index(huidige_waarde) if huidige_waarde in status_opties else 0,
            key=key
        )

# ===== Opslaan met aangepaste bestandsnaam =====
st.markdown("---")
if st.button("💾 Opslaan"):
    if not checksoftware:
        st.warning("Vul eerst de naam van de checksoftware in.")
    else:
        filename = f"{sanitize_filename(checksoftware)}_{controle_datum.strftime('%Y%m%d')}.csv"
        df.to_csv(filename)
        df.to_csv("tijdelijke_testresultaten.csv")  # Voor herladen bij volgende keer
        st.success(f"Resultaten opgeslagen als: `{filename}`")
