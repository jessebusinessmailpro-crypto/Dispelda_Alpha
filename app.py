import streamlit as st
import sys
import os

# --- 1. SÉCURITÉ : SYSTÈME DE MOT DE PASSE ---
def check_password():
    def password_entered():
        # CHANGE "DISPELDA2026" PAR LE CODE DE TON CHOIX
        if st.session_state["password"] == "DISPELDA2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🛡️ ACCÈS RESTREINT // DISPELDA CORE")
        st.text_input("Veuillez entrer le code d'accès tactique", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.title("🛡️ ACCÈS RESTREINT // DISPELDA CORE")
        st.text_input("CODE INCORRECT", type="password", on_change=password_entered, key="password")
        st.error("Identification échouée.")
        return False
    else:
        return True

if check_password():
    # --- 2. IMPORTS DES MODULES (SANS 'backend.') ---
    try:
        from engine import AlphaEngine
        from ai_agent import StrategicAnalyst
        try:
            from store import SQLiteStore
        except ImportError:
            class SQLiteStore:
                def __init__(self): pass
    except ImportError as e:
        st.error(f"❌ Erreur critique : Fichier manquant sur GitHub ({e})")
        st.info("Vérifie que engine.py et ai_agent.py sont bien à la racine de ton GitHub.")
        st.stop()

    # --- 3. INITIALISATION ---
    if 'engine' not in st.session_state:
        st.session_state.store = SQLiteStore()
        st.session_state.engine = AlphaEngine(st.session_state.store)
        st.session_state.agent = StrategicAnalyst()

    # --- 4. CONFIGURATION VISUELLE ---
    st.set_page_config(page_title="DISPELDA ONE", layout="wide")
    st.markdown("""
    <style>
        .stApp { background-color: #0e1117; color: #00ff41; }
        .stButton>button { background-color: #00ff41; color: black; font-weight: bold; width: 100%; border: none; height: 3em;}
        .stButton>button:hover { background-color: #00cc33; color: white; }
        .stSlider label { color: #00ff41 !important; }
    </style>
    """, unsafe_allow_html=True)

    st.title("🛡️ DISPELDA // INTERFACE DE DÉPLOIEMENT")

    # --- 5. INTERFACE UTILISATEUR ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("PARAMÈTRES")
        val_civil = st.slider("Instabilité Civile", 0.0, 100.0, 50.0)
        val_supply = st.slider("Santé Logistique", 0.0, 100.0, 50.0)
        
        if st.button("EXÉCUTER L'ANALYSE"):
            raw_data = [
                {"id": "UI", "metric": "civil_risk", "val": val_civil},
                {"id": "UI", "metric": "supply_health", "val": val_supply}
            ]
            
            with st.spinner("Analyse du moteur Alpha en cours..."):
                try:
                    # Calcul mathématique
                    result = st.session_state.engine.analyze(raw_data)
                    score = result['risk_scoring']['risk_score_final']
                    
                    # Appel IA (Consomme tes crédits)
                    sitrep = st.session_state.agent.generate_sitrep(raw_data, score)
                    
                    st.session_state.last_result = result
                    st.session_state.last_sitrep = sitrep
                except Exception as e:
                    st.error(f"Erreur système : {e}")

    with col2:
        if 'last_result' in st.session_state:
            res = st.session_state.last_result
            score = res['risk_scoring']['risk_score_final']
            level = res['risk_scoring']['level']
            
            color = "#ff4b4b" if level == "CRITICAL" else "#ffa500" if level == "WARNING" else "#00ff41"
            
            st.markdown(f"<div style='border: 2px solid {color}; padding: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='color:{color}; text-align: center;'>SCORE DE RISQUE : {score}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='color:{color}; text-align: center;'>STATUS : {level}</h3>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.subheader("📝 SITREP INTELLIGENCE ARTIFICIELLE")
            st.write(st.session_state.last_sitrep)
        else:
            st.info("Système en attente. Modifiez les paramètres et lancez l'analyse pour générer un rapport.")
