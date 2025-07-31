# This code is part of a Flask application that manages hotel reservations. Aqui estara la conexion a la base de datos y las funciones para manejar reservas.

from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
from datetime import datetime
import traceback  # Agregado para debug


def obtener_conexion():
    return mysql.connector.connect(
        host='localhost',
        user='root',         # Cambia si tu usuario es diferente
        password='',         # Pon tu contraseña si tienes
        database='hotel'     # El nombre de tu base de datos
    )



def guardar_reserva_db(data):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        # Fecha de reserva actual
        fecha_reserva = datetime.now().strftime('%Y-%m-%d')

        sql = """INSERT INTO reservas (id_usuario, fecha_ingreso, fecha_salida, tipo_habitacion, precio, fecha_reserva)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        valores = (
            data['id_usuario'],
            data['fecha_ingreso'],
            data['fecha_salida'],
            data['tipo_habitacion'],
            data['precio'],
            fecha_reserva
        )

        print("Ejecutando SQL:", sql)
        print("Con valores:", valores)

        cursor.execute(sql, valores)
        conn.commit()
        print("Reserva insertada correctamente")

    except Exception as e:
        print("Error al insertar reserva:", e)
        traceback.print_exc()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
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
        SELECT u.usuario AS nombre, r.fecha_ingreso, r.fecha_salida, r.tipo_habitacion, r.precio, r.fecha_reserva
        FROM reservas r
        JOIN usuarios u ON r.id_usuario = u.id
        WHERE r.fecha_reserva BETWEEN %s AND %s
        ORDER BY r.fecha_reserva DESC
    """, (inicio, fin))
    reservas = cursor.fetchall()
    cursor.close()
    conn.close()
    return reservas

