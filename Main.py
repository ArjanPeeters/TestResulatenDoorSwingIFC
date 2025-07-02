import streamlit as st
import pandas as pd

# Definieer je matrix met beschrijvingen
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

# Kolommen (transformaties)
kolommen = [
    "Default", "Flipped X", "Flipped Y", "Rotated 180",
    "Mirror X", "Mirror Y", "Group Default", "Group Rotated 180",
    "Group Mirror X", "Group Mirror Y"
]

status_opties = ["✅ Correct", "⚠️ Fout", "❌ Genegeerd", "❓ Onbekend"]

# Laad eerder ingevulde data
try:
    df = pd.read_csv("testresultaten.csv", index_col=0)
except FileNotFoundError:
    df = pd.DataFrame(index=[t[0] for t in test_matrix], columns=kolommen)

# Titel
st.title("Deur-swingline testmatrix")
st.markdown("Geef per combinatie aan wat het resultaat is (correct, fout, genegeerd, etc.).")

# Itereer per rij (type test + toelichting)
for test_naam, toelichting in test_matrix:
    st.markdown(f"### {test_naam}")
    st.markdown(f"*_{toelichting}_*")

    cols = st.columns(len(kolommen))
    for i, kolom in enumerate(kolommen):
        key = f"{test_naam}_{kolom}"
        huidige_waarde = df.loc[test_naam, kolom] if not pd.isna(df.loc[test_naam, kolom]) else status_opties[0]
        df.loc[test_naam, kolom] = cols[i].selectbox(
            kolom,
            status_opties,
            index=status_opties.index(huidige_waarde) if huidige_waarde in status_opties else 0,
            key=key
        )

st.markdown("---")
# Opslaan
if st.button("💾 Opslaan als CSV"):
    df.to_csv("testresultaten.csv")
    st.success("Resultaten opgeslagen in testresultaten.csv!")
