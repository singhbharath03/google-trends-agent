# main.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Import from config
from config import Settings, get_settings, settings

# Import the trader functions
from trader import buy, sell


# Request model for buy/sell operations
class SwapRequest(BaseModel):
    wallet_address: str
    mint: str
    amount_with_decimals: float


# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug_mode,
)


@app.get("/")
async def root(settings: Settings = Depends(get_settings)):
    return {
        "message": f"Welcome to {settings.app_name}",
        "debug_mode": settings.debug_mode,
    }


@app.post("/trade/buy")
async def trade_buy(request: SwapRequest):
    try:
        result = await buy(
            request.wallet_address, request.mint, request.amount_with_decimals
        )
        return {"status": "success", "transaction": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/trade/sell")
async def trade_sell(request: SwapRequest):
    try:
        result = await sell(
            request.wallet_address, request.mint, request.amount_with_decimals
        )
        return {"status": "success", "transaction": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.debug_mode)
