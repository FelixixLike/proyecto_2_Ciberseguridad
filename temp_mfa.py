"""import pyotp

clave = pyotp.random_base32()
print(clave)  # Copia este valor y guárdalo en tu base de datos
"""

"""
import pyotp
import qrcode

correo_admin = "admin@admin.com"  # el que uses
clave = "QLXNEUDO57VWAQFFLQSM5PCOIKB7KVOB" # la clave que generaste

totp = pyotp.TOTP(clave)
uri = totp.provisioning_uri(name=correo_admin, issuer_name="Hotel Dorado")
img = qrcode.make(uri)
img.save("static/qr_admin.png")
"""

import pyotp

totp = pyotp.TOTP("QLXNEUDO57VWAQFFLQSM5PCOIKB7KVOB")
print("Código actual:", totp.now())
