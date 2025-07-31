# This code is part of a Flask application that manages hotel reservations. Aqui estara la conexion a la base de datos y las funciones para manejar reservas.

from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',         # Cambia si tu usuario es diferente
        password='',         # Pon tu contraseña si tienes
        database='hotel'     # El nombre de tu base de datos
    )


def guardar_reserva_db(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reservas (nombre, correo, fecha, fecha_salida, noches, habitacion, precio, total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (
            data['nombre'],
            data['correo'],
            data['fecha'],
            data.get('fecha_salida', None),
            data['noches'],
            data['habitacion'],
            data['precio'],
            data['total']
        )
    )
    conn.commit()
    cursor.close()
    conn.close()


def cargar_reservas_db():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservas")
    reservas = cursor.fetchall()
    cursor.close()
    conn.close()
    return reservas

def buscar_reservas_por_fecha(inicio, fin):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM reservas
        WHERE fecha BETWEEN %s AND %s
    """, (inicio, fin))
    reservas = cursor.fetchall()
    cursor.close()
    conn.close()
    return reservas