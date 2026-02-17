import pyotp
import qrcode
import os

class SecurityUtils:
    @staticmethod
    def generate_2fa_secret():
        return pyotp.random_base32()

    @staticmethod
    def get_totp_uri(secret, username):
        return pyotp.totp.TOTP(secret).provisioning_uri(
            name=username,
            issuer_name="WP Archive"
        )

    @staticmethod
    def verify_code(secret, input_code):
        if not secret or not input_code:
            return False
        totp = pyotp.TOTP(secret)
        return totp.verify(input_code)

    @staticmethod
    def generate_qr_image(uri, file_path="temp_qr.png"):
        try:
            img = qrcode.make(uri)
            img.save(file_path)
            return file_path
        except Exception as e:
            print(f"QR Generation Error: {e}")
            return None

