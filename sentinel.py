import time
import sys
from backend.engine import CoreEngine
from backend.ai_agent import StrategicAnalyst
from backend.store import SQLiteStore

def run_sentinel():
    print("🛡️ DISPELDA ALPHA CORE // SÉCURITÉ FINANCIÈRE ACTIVÉE")
    try:
        store = SQLiteStore()
        engine = CoreEngine(store)
        agent = StrategicAnalyst()
        is_in_crisis = False
        print("✅ SYSTEM READY. MONITORING ACTIVE.")
    except Exception as e:
        print(f"❌ FATAL ERROR DURING BOOT: {e}")
        sys.exit(1)

    while True:
        try:
            # Simulation (Donnée 85 = Danger)
            mock_data = [{"val": 200}, {"val": 210}, {"val": 205}]
            
            res = engine.execute(mock_data)
            score = res['risk_scoring']['final_score']
            level = res['risk_scoring']['level']
            bias = res['risk_scoring']['bias_applied']

            if level == "CRITICAL":
                if store.has_active_unacknowledged_alert():
                    if not is_in_crisis:
                        print(f"🚨 NOUVELLE MENACE ! [APPEL IA PAYANT] Score: {score}")
                        sitrep = agent.generate_sitrep(mock_data, score)
                        print(f"🧠 AI SITREP: {sitrep}")
                        store.save_analysis(score, level)
                        is_in_crisis = True
                    else:
                        print(f"🕒 EN ATTENTE DU CLIENT... [ZÉRO CONSO OPENAI] Bias: -{bias*100}%")
                else:
                    # Le client a acquitté, on reste discret
                    print(f"🤫 CLIENT AU COURANT (ACQUITTÉ). [ZÉRO CONSO OPENAI] Score: {score}")
            
            elif level == "NOMINAL" and is_in_crisis:
                print("✅ RÉSOLUTION DÉTECTÉE. [APPEL IA PAYANT POUR RAPPORT FINAL]")
                agent.generate_sitrep(mock_data, score)
                is_in_crisis = False
            
            else:
                # Tout va bien
                print(f"🟢 SYSTÈME NOMINAL. [ZÉRO CONSO OPENAI] Score: {score}")

            time.sleep(15)

        except KeyboardInterrupt:
            print("\n🛑 ARRÊT DE DISPELDA...")
            break
        except Exception as e:
            print(f"⚠️ CORE WARNING: {e}. Retrying in 15s...")
            time.sleep(15)

if __name__ == "__main__":
    run_sentinel()
