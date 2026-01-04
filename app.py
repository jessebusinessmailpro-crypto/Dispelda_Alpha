import streamlit as st
import os
from openai import OpenAI

# --- CONFIGURATION SÉCURITÉ ---
# Ton mot de passe pour protéger ton argent OpenAI
MOT_DE_ PASSE = "DISPELDA2026"

def check_password():
    if "password_correct" not in st.session_state:
        st.title("🛡️ ACCÈS SÉCURISÉ DISPELDA")
        pwd = st.text_input("Entrez le code tactique", type="password")
        if st.button("S'IDENTIFIER"):
            if pwd == MOT_DE_PASSE:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Code incorrect")
        return False
    return True

if check_password():
    # --- LE CERVEAU DE L'IA ---
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # --- L'INTERFACE ---
    st.set_page_config(page_title="DISPELDA ONE", layout="wide")
    st.title("🛡️ DISPELDA // SYSTÈME ACTIF")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("PARAMÈTRES")
        val_civil = st.slider("Risque Civil", 0, 100, 50)
        val_supply = st.slider("Santé Logistique", 0, 100, 50)
        
        if st.button("LANCER L'ANALYSE"):
            with st.spinner("L'IA analyse la situation..."):
                # Calcul simple du score
                score = (val_civil + (100 - val_supply)) / 2
                
                # Appel OpenAI
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "Tu es un expert en défense."},
                              {"role": "user", "content": f"Score de risque: {score}. Civil: {val_civil}, Logistique: {val_supply}. Donne un verdict court."}]
                )
                st.session_state.result = response.choices[0].message.content
                st.session_state.score = score

    with col2:
        if "result" in st.session_state:
            st.metric("SCORE DE RISQUE", f"{st.session_state.score}/100")
            st.subheader("RAPPORT IA")
            st.info(st.session_state.result)
        else:
            st.write("En attente de données...")
