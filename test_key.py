import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Charger les variables d'environnement (.env)
print("--- TEST DE CONNEXION OPENAI ---")
load_status = load_dotenv()

if not load_status:
    print("❌ ERREUR: Impossible de lire le fichier .env")
    exit()

api_key = os.getenv("OPENAI_API_KEY")

# Vérification basique de la présence de la clé
if not api_key or api_key == "ta_clef_secrete_ici":
    print("❌ ERREUR: La clé n'est pas définie ou c'est encore la valeur par défaut.")
    print("Vérifie ton fichier .env")
    exit()
else:
    # On cache la clé pour l'affichage (sécurité)
    masked_key = api_key[:5] + "..." + api_key[-4:]
    print(f"✅ Clé trouvée : {masked_key}")

# 2. Tenter une connexion réelle
print("📡 Envoi d'un signal de test à OpenAI...")

try:
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Modèle rapide et pas cher pour le test
        messages=[
            {"role": "system", "content": "Tu es un assistant de test."},
            {"role": "user", "content": "Réponds juste par le mot : OPÉRATIONNEL"}
        ],
        max_tokens=10
    )
    
    reponse_ia = response.choices[0].message.content
    print("\n------------------------------------------------")
    print(f"✅ SUCCÈS ! Réponse de l'IA : {reponse_ia}")
    print("------------------------------------------------")
    print("Le canal est ouvert. Ton moteur peut maintenant utiliser l'IA.")

except Exception as e:
    print("\n❌ ÉCHEC DE LA CONNEXION :")
    print(e)
    print("\nCauses possibles : Clé incorrecte, compte à court de crédits, ou problème réseau.")
