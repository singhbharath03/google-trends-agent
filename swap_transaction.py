import json
import base64

from solders.transaction import VersionedTransaction
from constants import SOL_INPUT_MINT
from keypair import get_keypair
from token_account import get_user_token_account
from tools.http import req_post, req_get


async def build_and_send_swap_transaction(
    wallet_address, input_token_mint, output_token_mint, amount_with_decimals
):
    print("check")
    # First check if the wallet address matches our keypair
    if wallet_address != str(get_keypair().pubkey()):
        print("check 2")
        print(
            f"Error: Cannot sign for wallet {wallet_address}. Our keypair is for {get_keypair().pubkey()}"
        )
        print(
            "You can only execute transactions for the wallet corresponding to the private key"
        )
        return None

    print("1 ")
    resp = await build_swap_transaction(
        wallet_address,
        input_token_mint,
        output_token_mint,
        amount_with_decimals,
    )
    print("resp ", resp)

    if not resp or "data" not in resp or not resp["data"]:
        print("Error: Failed to build swap transaction")
        return None

    # Get the fresh transaction
    raw_txn_data = resp["data"][0]["transaction"]
    decoded_txn = base64.b64decode(raw_txn_data)

    # Parse the transaction
    unsigned_tx = VersionedTransaction.from_bytes(decoded_txn)

    # Extract the message from the transaction
    message = unsigned_tx.message

    # Create a new versioned transaction with our keypair for signing
    signed_tx = VersionedTransaction(message, [get_keypair()])

    # Serialize the signed transaction
    final_tx_bytes = bytes(signed_tx)

    # Encode to base64 for sending
    final_tx_base64 = base64.b64encode(final_tx_bytes).decode("utf-8")

    # Use the send_transaction function which handles base64 encoded transactions
    try:
        resp = await send_transaction(final_tx_base64)
        print("Transaction submitted successfully:", resp)
        return resp
    except Exception as e:
        print("Error sending transaction:", e)
        return None


async def build_swap_transaction(
    wallet_address,
    input_token_mint,
    output_token_mint,
    amount_with_decimals,
):
    swap_response_json = await get_swap_route_plan(
        input_token_mint, output_token_mint, amount_with_decimals
    )

    return await build_txn_from_swap_response(
        wallet_address, input_token_mint, output_token_mint, swap_response_json
    )


async def build_txn_from_swap_response(
    wallet_address,
    input_token_mint,
    output_token_mint,
    swap_response_json,
):
    url = "https://dev-api.sega.so/swap/transaction/swap-base-in"

    wrap_sol = False
    unwrap_sol = False

    input_token_account = None
    output_token_account = None
    if input_token_mint == SOL_INPUT_MINT:
        wrap_sol = True
        output_token_account = await get_user_token_account(
            wallet_address, output_token_mint
        )
    elif output_token_mint == SOL_INPUT_MINT:
        unwrap_sol = True
        input_token_account = await get_user_token_account(
            wallet_address, input_token_mint
        )
    else:
        input_token_account = await get_user_token_account(
            wallet_address, input_token_mint
        )
        output_token_account = await get_user_token_account(
            wallet_address, output_token_mint
        )

    extras_dict = {}
    if input_token_account:
        extras_dict["inputAccount"] = input_token_account
    if output_token_account:
        extras_dict["outputAccount"] = output_token_account

    payload = {
        "wallet": wallet_address,
        "computeUnitPriceMicroLamports": "10500",
        "swapResponse": swap_response_json,
        "txVersion": "V0",
        "wrapSol": wrap_sol,
        "unwrapSol": unwrap_sol,
        **extras_dict,
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en-IN;q=0.9,en;q=0.8",
        "content-type": "application/json",
        "origin": "https://dev.sega.so",
        "priority": "u=1, i",
        "referer": "https://dev.sega.so/",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    }

    return await req_post(url, headers=headers, data=payload)


async def get_swap_route_plan(
    input_token_mint, output_token_mint, amount_with_decimals: int, slippage_bps=5000
):
    url = f"https://dev-api.sega.so/swap/compute/swap-base-in?inputMint={input_token_mint}&outputMint={output_token_mint}&amount={amount_with_decimals}&slippageBps={slippage_bps}&txVersion=V0"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en-IN;q=0.9,en;q=0.8",
        "origin": "https://dev.sega.so",
        "priority": "u=1, i",
        "referer": "https://dev.sega.so/",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    }

    return await req_get(url, headers=headers)


async def send_transaction(base64_txn_data):
    url = "https://api.testnet.v1.sonic.game/"

    payload = {
        "method": "sendTransaction",
        "jsonrpc": "2.0",
        "params": [
            base64_txn_data,
            {
                "encoding": "base64",
                "maxRetries": 3,
                "skipPreflight": False,
                "preflightCommitment": "processed",
            },
        ],
        "id": "722cc8fd-8479-4d86-997b-e80f5ca5f81f",
    }

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en-IN;q=0.9,en;q=0.8",
        "content-type": "application/json",
        "origin": "https://dev.sega.so",
        "priority": "u=1, i",
        "referer": "https://dev.sega.so/",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "solana-client": "js/0.0.0-development",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    }

    response = await req_post(url, headers=headers, data=payload)

    print("response ", response)
    return response["result"]
