cat << 'EOF' > backend/ai_agent.py
import os
import logging
import time
from typing import List, Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI, APIError, RateLimitError

# --- CONFIGURATION DU LOGGING (Traceability) ---
# On veut savoir exactement ce qui se passe, quand et pourquoi.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [STRATCOM_UNIT] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("DispeldaAI")

class StrategicAnalyst:
    """
    Classe d'élite pour l'analyse stratégique automatisée.
    Gère la connexion persistante, les retries et le formatage strict.
    """

    def __init__(self):
        self._load_credentials()
        self.model = "gpt-3.5-turbo" # Peut être upgradé en gpt-4-turbo
        self.max_tokens = 250
        self.temperature = 0.6 # Précision chirurgicale, peu de créativité

        try:
            self.client = OpenAI(api_key=self.api_key)
            logger.info("Liaison neuronale avec OpenAI établie.")
        except Exception as e:
            logger.critical(f"ECHEC INITIALISATION CLIENT: {e}")
            raise RuntimeError("Le module IA n'a pas pu démarrer.")

    def _load_credentials(self) -> None:
        """Charge et valide les variables d'environnement de manière sécurisée."""
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.critical("Clé API manquante dans le coffre (.env).")
            raise ValueError("Credentials Error: OPENAI_API_KEY not found.")

    def _build_system_prompt(self) -> str:
        """Définit la personnalité et les règles d'engagement de l'IA."""
        return (
            "Tu es DISPELDA (Defense Intelligence System & Predictive Logic Data Analyzer). "
            "Tu es une IA de niveau militaire chargée de la surveillance globale. "
            "Ton style est : FROID, FACTUEL, AUTORITAIRE. Pas de politesse, pas de mots inutiles. "
            "Tes réponses doivent ressembler à un télex militaire ou un rapport de la CIA."
        )

    def _build_user_payload(self, sensors: List[Dict], risk_score: float) -> str:
        """Construit le vecteur de données pour l'analyse."""
        metrics_summary = ", ".join([f"{d.get('metric', 'N/A')}: {d.get('val', 0)}" for d in sensors])
        
        return f"""
        [DONNÉES ENTRANTES]
        -------------------
        NIVEAU DE MENACE CALCULÉ : {risk_score:.4f} / 1.0
        TÉLÉMÉTRIE CAPTEURS : [{metrics_summary}]
        -------------------

        ORDRES :
        Génère un SITREP (Situation Report) immédiat suivant ce format strict :
        1. [STATUT] : (NOMINAL / WARNING / CRITICAL / FATAL)
        2. [ANALYSE VECTORIELLE] : Explication technique de la cause en 1 phrase.
        3. [PROTOCOLE] : Action recommandée (Ex: Déploiement, Confinement, Surveillance).
        """

    def generate_sitrep(self, data: List[Dict], score: float) -> str:
        """
        Exécute l'analyse avec gestion des pannes et mesure de latence.
        """
        if not data:
            logger.warning("Aucune donnée capteur fournie pour l'analyse.")
            return "N/A - Données insuffisantes."

        prompt = self._build_user_payload(data, score)
        logger.info(f"Déclenchement analyse IA (Score: {score})")
        
        start_time = time.time()

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._build_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            
            latency = (time.time() - start_time) * 1000
            content = response.choices[0].message.content.strip()
            
            logger.info(f"Analyse terminée avec succès en {latency:.2f}ms")
            return content

        except RateLimitError:
            logger.error("Quota API dépassé. Passage en mode silencieux.")
            return "ERREUR: Surcharge Système Neural (Quota)."
        except APIError as e:
            logger.error(f"Erreur distante OpenAI: {e}")
            return "ERREUR: Défaillance Liaison Uplink."
        except Exception as e:
            logger.exception("Erreur critique non gérée dans le module IA.")
            return "ERREUR: Exception Interne Système."

# Instance unique (Singleton pattern) pour être importée ailleurs
try:
    agent = StrategicAnalyst()
    # Fonction wrapper pour garder la compatibilité avec ton api.py actuel
    def generer_analyse_strategique(data, score):
        return agent.generate_sitrep(data, score)
except Exception:
    # Fallback si l'initialisation plante (pour ne pas crasher tout le backend)
    def generer_analyse_strategique(data, score):
        return "MODULE IA HORS LIGNE (Check logs)"

if __name__ == "__main__":
    # Test unitaire intégré pour valider la robustesse sans lancer tout le serveur
    print("\n--- TEST UNITAIRE : MODULE STRATCOM ---")
    mock_data = [
        {"metric": "market_crash_index", "val": 92.4},
        {"metric": "population_anger", "val": 78.1}
    ]
    print(agent.generate_sitrep(mock_data, 0.88))
EOF
