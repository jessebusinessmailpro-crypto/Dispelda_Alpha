import streamlit as st
import sys
import os

# On s'assure que le système trouve les fichiers au même endroit
sys.path.append(os.getcwd())

# --- CORRECTION DES IMPORTS (On enlève "backend.") ---
try:
    from test_final_boss import AlphaEngine
    from ai_agent import StrategicAnalyst
    # Note : Si tu n'as pas de fichier store.py, on utilise un dictionnaire temporaire
    try:
        from store import SQLiteStore
    except ImportError:
        class SQLiteStore: # Version de secours si store.py est absent
            def __init__(self): pass
except ImportError as e:
    st.error(f"⚠️ Erreur de fichier : {e}")
    st.stop()

# --- INITIALISATION UNIQUE ---
if 'engine' not in st.session_state:
    try:
        st.session_state.store = SQLiteStore()
        st.session_state.engine = AlphaEngine(st.session_state.store)
        st.session_state.agent = StrategicAnalyst()
    except Exception as e:
        st.error(f"Erreur d'initialisation : {e}")

# --- CONFIG PAGE ---
st.set_page_config(page_title="DISPELDA ONE", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #00ff41; }
    .stButton>button { background-color: #00ff41; color: black; font-weight: bold; width: 100%; border: none; }
    .stButton>button:hover { background-color: #00cc33; color: white; }
    .stSlider label { color: #00ff41 !important; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ DISPELDA // STANDALONE SYSTEM")

# --- INTERFACE ---
col1, col2 = st.columns([1, 2])

with col1:
    st.header("CONTRÔLE TACTIQUE")
    val_civil = st.slider("Instabilité Civile (Risk)", 0.0, 100.0, 50.0)
    val_supply = st.slider("Chaîne Logistique (Health)", 0.0, 100.0, 50.0)
    
    if st.button("LANCER ANALYSE STRATÉGIQUE"):
        # CONSTRUCTION DONNÉES
        raw_data = [
            {"id": "UI", "metric": "civil_risk", "val": val_civil},
            {"id": "UI", "metric": "supply_health", "val": val_supply}
        ]
        
        with st.spinner("🧠 Intelligence en cours de calcul..."):
            try:
                # CALCUL DU MOTEUR
                result = st.session_state.engine.analyze(raw_data)
                score = result['risk_scoring']['risk_score_final']
                
                # APPEL IA (Consomme tes crédits OpenAI)
                sitrep = st.session_state.agent.generate_sitrep(raw_data, score)
                
                # STOCKAGE
                st.session_state.last_result = result
                st.session_state.last_sitrep = sitrep
            except Exception as e:
                st.error(f"Erreur lors de l'analyse : {e}")

with col2:
    if 'last_result' in st.session_state:
        res = st.session_state.last_result
        score = res['risk_scoring']['risk_score_final']
        level = res['risk_scoring']['level']
        
        color = "#ff4b4b" if level == "CRITICAL" else "#ffa500" if level == "WARNING" else "#00ff41"
        
        st.markdown(f"<h1 style='color:{color}; text-align: center; border: 2px solid {color}; padding: 10px;'>NIVEAU : {level} ({score})</h1>", unsafe_allow_html=True)
        st.markdown("---")
        st.subheader("📝 RAPPORT TACTIQUE IA")
        st.write(st.session_state.last_sitrep)
    else:
        st.info("📡 Système en attente de paramètres. Ajustez les sliders et lancez l'analyse.")
