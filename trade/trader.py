import json

from trade.constants import SOL_INPUT_MINT
from trade.swap_transaction import build_and_send_swap_transaction
from tools.http import req_post


async def buy(wallet_address, mint, amount_with_decimals):
    """
    Buy tokens using SOL.
    Note: wallet_address must match the public key of our keypair.
    """
    return await build_and_send_swap_transaction(
        wallet_address,
        SOL_INPUT_MINT,
        mint,
        int(amount_with_decimals),
    )


async def sell(wallet_address, mint, amount_with_decimals):
    """
    Sell tokens for SOL.
    Note: wallet_address must match the public key of our keypair.
    """
    return await build_and_send_swap_transaction(
        wallet_address,
        mint,
        SOL_INPUT_MINT,
        int(amount_with_decimals),
    )
