import sys
import os
from datetime import datetime

# Assurer l'accès au dossier backend
sys.path.append(os.getcwd())

# Import des composants finalisés
from backend.engine import CoreEngine
from backend.ai_agent import StrategicAnalyst

def run_final_test():
    print("🚀 [LOG] DÉMARRAGE DU TEST UNITAIRE GLOBAL...")
    
    # 1. Initialisation
    engine = CoreEngine()
    agent = StrategicAnalyst()
    
    # 2. Données de Crise (Anomalie brutale)
    # On simule par exemple une hausse de température critique dans un entrepôt
    donnees_tactiques = [
        {"sensor_id": "STK_01", "val": 18.5},
        {"sensor_id": "STK_01", "val": 19.2},
        {"sensor_id": "STK_01", "val": 25.4},
        {"sensor_id": "STK_01", "val": 45.8} # Le choc est ici
    ]

    print("📊 [LOG] Injection des données dans le moteur ALPHA...")
    
    # 3. Exécution du moteur mathématique
    resultat = engine.execute(donnees_tactiques)
    
    if "risk_scoring" in resultat:
        score = resultat['risk_scoring']['final_score']
        level = resultat['risk_scoring']['level']
        
        print(f"✅ [MOTEUR] Score calculé : {score} | Niveau : {level}")
        
        # 4. Génération du Rapport IA (SITREP)
        print("🧠 [LOG] Liaison avec l'IA pour interprétation stratégique...")
        sitrep = agent.generate_sitrep(donnees_tactiques, score)
        
        print("\n" + "="*60)
        print("🔴 RAPPORT DE MISSION DISPELDA")
        print("="*60)
        print(f"HORODATAGE : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"INDICE DE MENACE : {score}/1.0 ({level})")
        print("-" * 60)
        print(f"DÉPÊCHE TACTIQUE (SITREP) :\n\n{sitrep}")
        print("="*60)
        
    else:
        print(f"❌ [ERREUR] Le moteur a renvoyé : {resultat}")

if __name__ == "__main__":
    run_final_test()
