# 🛡️ Sistema de Reservas Hotel Dorado — Proyecto Final Ciberseguridad

Proyecto final del módulo de **Ciberseguridad - Nivel Básico** de la plataforma [TalentoCUN](https://talentocun.tech/talentocun/index.php), en el que transformamos una aplicación web básica en una solución **segura y funcional** para la gestión de reservas hoteleras.
Se aplicaron buenas prácticas de seguridad, cifrado, autenticación y protección de datos tanto en frontend como en backend.

## Integrantes:
* Andrés Felipe Martínez González (x_L)
*Janer Andrey Piñeros Arana

---

## 🔐 Características de Seguridad Implementadas

✅ Estas fueron las mejoras clave aplicadas al proyecto original:

* 🔑 **Cifrado de contraseñas** con `bcrypt` almacenadas en MySQL.
* 🔒 **Certificado SSL** aplicado para navegación segura vía HTTPS.
* 🧾 **Autenticación robusta** con sesiones seguras gestionadas por Flask.
* 📧 **Notificación automática por correo electrónico**, utilizando SMTP autenticado con contraseña de aplicación.
* 🗂️ **Separación de lógica de frontend (JS/CSS/HTML)** para reducir el riesgo de inyecciones.
* ❌ **Eliminación de credenciales hardcodeadas** y variables sensibles en el código fuente.
* 🛡️ **Mitigación de vulnerabilidades comunes** como XSS y CSRF mediante diseño estructurado y validaciones del lado servidor.

---

## 🛠️ Tecnologías Utilizadas

* **Python (Flask)** – Framework web para backend
* **MySQL** – Base de datos relacional
* **HTML5 / CSS3 / JavaScript** – Frontend del sistema
* **bcrypt** – Librería de hashing para contraseñas
* **smtplib + email.message** – Envío de correos desde el backend
* **OpenSSL** – Generación de certificado de seguridad local

---

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/proyecto-hotel-dorado.git
cd proyecto-hotel-dorado
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar la base de datos

Importa el archivo `hotel.sql` incluido en el repositorio usando tu gestor de bases de datos MySQL (como **phpMyAdmin** o mediante la línea de comandos).
Este archivo contiene la estructura de tablas necesarias y datos de ejemplo para comenzar a trabajar.

### 4. Configurar credenciales de correo

En el archivo `db_manager.py` , actualiza las credenciales con tu **correo electrónico** y la **contraseña de aplicación** generada desde tu proveedor (por ejemplo, Gmail).

