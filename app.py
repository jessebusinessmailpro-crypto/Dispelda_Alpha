import streamlit as st
import sys
import os

# On s'assure qu'on peut importer les modules du backend
sys.path.append(os.getcwd())

from backend.engine import AlphaEngine
from backend.store import SQLiteStore
from backend.ai_agent import StrategicAnalyst

# --- INITIALISATION UNIQUE ---
if 'engine' not in st.session_state:
    st.session_state.store = SQLiteStore()
    st.session_state.engine = AlphaEngine(st.session_state.store)
    st.session_state.agent = StrategicAnalyst()

# --- CONFIG PAGE ---
st.set_page_config(page_title="DISPELDA ONE", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #00ff41; }
    .stButton>button { background-color: #00ff41; color: black; font-weight: bold; width: 100%; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ DISPELDA // STANDALONE SYSTEM")

# --- INTERFACE ---
col1, col2 = st.columns([1, 2])

with col1:
    st.header("CAISSE DE COMMANDE")
    val_civil = st.slider("Instabilité Civile", 0.0, 100.0, 50.0)
    val_supply = st.slider("Chaîne Logistique", 0.0, 100.0, 50.0)
    
    if st.button("LANCER ANALYSE"):
        # CONSTRUCTION DONNÉES
        raw_data = [
            {"id": "UI", "metric": "civil_risk", "val": val_civil},
            {"id": "UI", "metric": "supply_health", "val": val_supply}
        ]
        
        # APPEL DIRECT DU MOTEUR (Pas de réseau, pas de bug)
        with st.spinner("Calcul en cours..."):
            result = st.session_state.engine.analyze(raw_data)
            score = result['risk_scoring']['risk_score_final']
            
            # APPEL IA
            sitrep = st.session_state.agent.generate_sitrep(raw_data, score)
            
            # STOCKAGE RÉSULTAT
            st.session_state.last_result = result
            st.session_state.last_sitrep = sitrep

with col2:
    if 'last_result' in st.session_state:
        res = st.session_state.last_result
        score = res['risk_scoring']['risk_score_final']
        level = res['risk_scoring']['level']
        
        color = "red" if level == "CRITICAL" else "orange" if level == "WARNING" else "green"
        
        st.markdown(f"<h1 style='color:{color}; text-align: center'>NIVEAU : {level} ({score})</h1>", unsafe_allow_html=True)
        st.markdown("---")
        st.subheader("RAPPORT TACTIQUE IA")
        st.info(st.session_state.last_sitrep)
    else:
        st.write("En attente de données...")
