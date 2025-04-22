import streamlit as st
import requests

st.set_page_config(page_title="Clarté de l’eau à Noirmoutier", layout="wide")
st.title("🌊 Clarté de l’eau de mer à Noirmoutier")
st.markdown("**Clarté influencée par :** marée, houle, débit de la Loire, vent.")

# --- Layout en colonnes ---
col1, col2 = st.columns(2)

# --- Bloc 1 : Marée ---
with col1:
    st.subheader("🌅 Marée à L'Herbaudière")
    st.components.v1.iframe("https://maree.info/120", height=400, scrolling=True)

# --- Bloc 2 : Houle + Vent ---
with col2:
    st.subheader("🌬️ Houle & Vent à Noirmoutier")
    st.components.v1.iframe("https://www.windfinder.com/forecast/ile_de_noirmoutier_la_gueriniere", height=400, scrolling=True)

# --- Bloc 3 : Débit de la Loire ---
st.subheader("🏞️ Débit de la Loire (Montjean-sur-Loire)")

station_id = "E351122001"
url = f"https://hubeau.eaufrance.fr/api/v1/hydrometrie/observations_tr?code_entite={station_id}&grandeur_hydro=Q&sort=desc&size=1"

try:
    response = requests.get(url)
    data = response.json()
    if data["data"]:
        debit = float(data["data"][0]["resultat_obs"])
        date_obs = data["data"][0]["date_obs"]
        st.info(f"Débit actuel : **{debit} m³/s** (observé le {date_obs})")
    else:
        st.warning("Données de débit non disponibles pour le moment.")
except Exception as e:
    st.error(f"Erreur lors de la récupération des données : {e}")

# --- Résumé estimatif de la clarté ---
st.subheader("🧪 Estimation de la clarté de l’eau")

if debit < 500:
    st.success("Bonne clarté : Faible débit de la Loire.")
elif debit < 1000:
    st.warning("Clarté moyenne : Débit modéré.")
else:
    st.error("Clarté réduite : Fort débit, probable turbidité.")

st.markdown("*Note : cette estimation est basée uniquement sur le débit de la Loire. Une version plus complète combinera les 4 facteurs.*")
