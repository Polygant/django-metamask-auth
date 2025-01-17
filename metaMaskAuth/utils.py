import binascii
import random
import string
from web3.auto import w3
from eth_keys.exceptions import BadSignature
from eth_account.messages import encode_defunct
from django.core.exceptions import BadRequest
from .api_settings import api_settings
from django.utils import timezone


def verify_singature(nonce, signature):
    try:
        w3.eth.account.recover_message(encode_defunct(text=nonce), signature=signature)
        return True
    except (BadSignature, binascii.Error):
        raise BadRequest()


def generate_random():
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(api_settings.NONCE_LEN)
    )


def validate_nonce(wallet):
    """
    Returns True if a given token is within the age expiration limit.
    """

    if not wallet.nonce_stale:
        seconds = (timezone.now() - wallet.refreshed_at).total_seconds()
        nonce_expiry_time = getattr(api_settings, "NONCE_EXPIRE_TIME", 900)
        if seconds <= nonce_expiry_time:
            return True
    return False
