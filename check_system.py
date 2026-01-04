import os
from dotenv import load_dotenv
from backend.engine import CoreEngine
from backend.store import SQLiteStore
from backend.ai_agent import StrategicAnalyst

def run_health_check():
    print("🛡️ DISPELDA CORE // DIAGNOSTIC INITIAL")
    print("-" * 40)
    
    # 1. Test Environnement
    load_dotenv()
    if os.getenv("OPENAI_API_KEY"):
        print("✅ ENVIRONNEMENT : Clé OpenAI détectée.")
    else:
        print("❌ ENVIRONNEMENT : Clé OpenAI manquante dans .env")

    # 2. Test Mémoire (DB)
    try:
        store = SQLiteStore()
        print("✅ MÉMOIRE : Base de données accessible.")
    except Exception as e:
        print(f"❌ MÉMOIRE : Erreur DB -> {e}")

    # 3. Test Moteur (Logic)
    try:
        engine = CoreEngine()
        test_data = [{"val": 10}, {"val": 12}, {"val": 50}] # Simule une anomalie
        res = engine.execute(test_data)
        if res.get("risk_scoring"):
            print(f"✅ MOTEUR : Calcul opérationnel (Score: {res['risk_scoring']['final_score']})")
    except Exception as e:
        print(f"❌ MOTEUR : Défaillance de calcul -> {e}")

    # 4. Test Intelligence (IA)
    try:
        agent = StrategicAnalyst()
        if agent.active:
            print("✅ INTELLIGENCE : Liaison OpenAI établie.")
        else:
            print("⚠️ INTELLIGENCE : Agent en mode dégradé (Offline).")
    except Exception as e:
        print(f"❌ INTELLIGENCE : Erreur critique Agent -> {e}")

    print("-" * 40)
    print("DIAGNOSTIC TERMINÉ.")

if __name__ == "__main__":
    run_health_check()
