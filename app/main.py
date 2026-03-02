from fastapi import FastAPI, HTTPException
import json
from .schemas import DecisionRequest, DecisionResponse
from .engine import run_level2

app = FastAPI(title="Make your decisions like a consultant")



@app.post("/simulate", response_model=DecisionResponse)
async def simulate(req: DecisionRequest):
    try:
        return run_level2(req)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Model returned non-JSON. Lower temperature or tighten prompts.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))