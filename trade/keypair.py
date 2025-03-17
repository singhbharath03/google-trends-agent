from functools import lru_cache
import os
import base58
from config import get_settings
from solders.keypair import Keypair


@lru_cache(maxsize=1)
def get_keypair():
    private_key_bytes = base58.b58decode(get_settings().private_key)

    # convert private key to keypair
    keypair = Keypair.from_bytes(private_key_bytes)

    return keypair
