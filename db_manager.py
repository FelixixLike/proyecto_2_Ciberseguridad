# This code is part of a Flask application that manages hotel reservations. Aqui estara la conexion a la base de datos y las funciones para manejar reservas.

from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
from datetime import datetime
import traceback  # Agregado para debug
from email.message import EmailMessage # Agregado para enviar correos
import re, bcrypt
import smtplib


def validar_password(password):
    tiene_longitud = len(password) >= 8
    tiene_numeros = len(re.findall(r"\d", password)) >= 2
    tiene_simbolos = re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\[\]]", password) is not None
    tiene_mayusculas = re.search(r"[A-Z]", password) is not None
    tiene_minusculas = re.search(r"[a-z]", password) is not None

    return all([tiene_longitud, tiene_numeros, tiene_simbolos, tiene_mayusculas, tiene_minusculas])


def obtener_conexion():
    return mysql.connector.connect(
        host='localhost',
        user='root',         
        password='',         
        database='hotel'     
    )

def validar_password(password):
    tiene_longitud = len(password) >= 8
    tiene_numeros = len(re.findall(r"\d", password)) >= 2
    tiene_simbolos = re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\[\]]", password) is not None
    tiene_mayusculas = re.search(r"[A-Z]", password) is not None
    tiene_minusculas = re.search(r"[a-z]", password) is not None
    return all([tiene_longitud, tiene_numeros, tiene_simbolos, tiene_mayusculas, tiene_minusculas])

def enviar_correo_bienvenida(destinatario, usuario):
    msg = EmailMessage()
    msg.set_content(f"¡Bienvenido {usuario}! Tu registro fue exitoso en el sistema Hotel Dorado.")
    msg['Subject'] = 'Registro exitoso'
    msg['From'] = 'correo@gmail.com'
    msg['To'] = destinatario

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('correo@gmail.com', '####')  # contraseña de aplicación sin espacios
            smtp.send_message(msg)
    except Exception as e:
        print("Error al enviar el correo:", e)

def enviar_correo_inicio_sesion(destinatario):
    msg = EmailMessage()
    msg.set_content("Hola, se ha iniciado sesión en tu cuenta del Hotel Dorado.")
    msg['Subject'] = 'Inicio de sesión detectado'
    msg['From'] = 'correo@gmail.com'
    msg['To'] = destinatario

    # Usar SMTP seguro de Gmail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('correo@gmail.com', '####')  # Usa tu contraseña de aplicación aquí
        smtp.send_message(msg)

def guardar_reserva_db(data):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reservas (fecha_ingreso, fecha_salida, tipo_habitacion, precio, correo_usuario, noches)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data['fecha_ingreso'],
        data['fecha_salida'],
        data['tipo_habitacion'],
        data['precio'],
        data['correo_usuario'],
        data['noches']  # 👈 nuevo campo
    ))

    conn.commit()
    cursor.close()
    conn.close()




def cargar_reservas_db():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservas")
    reservas = cursor.fetchall()
    cursor.close()
    conn.close()
    return reservas

def buscar_reservas_por_fecha(inicio, fin):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.usuario AS nombre, r.fecha_ingreso, r.fecha_salida, 
               r.tipo_habitacion, r.precio, r.fecha_reserva
        FROM reservas r
        JOIN usuarios u ON r.correo_usuario = u.correo
        WHERE r.fecha_reserva BETWEEN %s AND %s
    """, (inicio, fin))
    resultados = cursor.fetchall()
    conn.close()
    return resultados


