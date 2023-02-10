import pyotp


def get_totp(base32_secret: str) -> str:
    totp = pyotp.TOTP(base32_secret)
    current_otp = totp.now()

    return current_otp
