import json
from tools.http import req_post


async def get_user_token_account(wallet_address, mint):
    url = "https://api.testnet.v1.sonic.game/"

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenAccountsByOwner",
        "params": [wallet_address, {"mint": mint}, {"encoding": "jsonParsed"}],
    }

    headers = {"Content-Type": "application/json"}

    response = await req_post(url, headers=headers, data=payload)

    return response["result"]["value"][0]["pubkey"]
