from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.store import SQLiteStore
import sqlite3

app = FastAPI(title="DISPELDA ALPHA API")

# Autoriser ton Dashboard (Vercel) à parler à ton serveur
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # On pourra restreindre à l'URL de ton site plus tard
    allow_methods=["*"],
    allow_headers=["*"],
)

store = SQLiteStore()

@app.get("/status")
def get_status():
    """ Envoie le score actuel et le dernier SITREP au Dashboard """
    conn = sqlite3.connect("dispelda_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT score, level, timestamp FROM analysis_history ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "score": row[0],
            "level": row[1],
            "last_update": row[2],
            "system_status": "ONLINE"
        }
    return {"message": "No data available", "system_status": "BOOTING"}

@app.post("/acknowledge")
def acknowledge(feedback: str = "REAL_CRISIS"):
    """ Reçoit l'ordre du bouton 'Acquitter' du Dashboard """
    store.acknowledge_all(feedback_type=feedback)
    return {"status": "success", "message": f"Alert acknowledged with feedback: {feedback}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
