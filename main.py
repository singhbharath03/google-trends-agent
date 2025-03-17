from fastapi import FastAPI, HTTPException, Request
from llm import process_agent_action_for_market
from markets import get_all_markets
from pydantic import BaseModel
from trade.keypair import get_keypair
import uvicorn

# Import from config
from config import Settings, get_settings, settings

# Import the trader functions
from trade.trader import buy, sell


# Request model for buy/sell operations
class SwapRequest(BaseModel):
    wallet_address: str
    mint: str
    amount_with_decimals: float


# Initialize FastAPI app
app = FastAPI(
    title="Google Trends Trading Agent",
    debug=settings.debug_mode,
)


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


@app.post("/trade/llm")
async def request_llm_trade(request: Request):
    markets = await get_all_markets()

    for market in markets:
        response = await process_agent_action_for_market(
            market["slug"], market["address"], str(get_keypair().pubkey())
        )

    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.debug_mode)
