from opcode import hasexc
import bcrypt
import qrcode
from app.database import SessionLocal, engine, Base
from app.models import User
from app.security_utils import SecurityUtils

Base.metadata.create_all(bind=engine)

def create_master_admin():
    db = SessionLocal()

    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")

    #Hashing
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    secret = SecurityUtils.generate_2fa_secret()

    user = User(
        username = username,
        password_hash = hashed,
        role = "Admin",
        totp_secret = secret,
        is_active = True,
    )

    try:
        db.add(user)
        db.commit()
        print("\n[SUCCESS] Admin User Created!")
        print("-" * 30)

        uri = SecurityUtils.get_totp_uri(secret, username)
        img_name = f"admin_qr_{username}.png"
        SecurityUtils.generate_qr_image(uri, img_name)

        print(f"Scan this QR Code with your Authenticator App: {img_name}")
        print("Once scanned, you can delete the image file for security.")
        print("-" * 30)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_master_admin()

