from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Conexión a la base de datos MySQL
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            database="CustomerReadDb",
            user="root",  # Cambia según tu configuración
            password="dani0919"  # Cambia según tu configuración
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Endpoint para obtener un cliente por ID
@app.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM Customers WHERE CustomerID = %s"
        cursor.execute(query, (customer_id,))
        customer = cursor.fetchone()
        cursor.close()
        conn.close()
        if customer:
            return jsonify({
                "CustomerID": customer[0],
                "FirstName": customer[1],
                "LastName": customer[2],
                "Email": customer[3],
                "PhoneNumber": customer[4],
                "Address": customer[5],
                "CreatedAt": customer[6],
                "UpdatedAt": customer[7]
            }), 200
        else:
            return jsonify({"message": "Customer not found"}), 404
    return jsonify({"message": "Failed to connect to database"}), 500

# Endpoint para listar todos los clientes
@app.route('/customers', methods=['GET'])
def get_all_customers():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM Customers"
        cursor.execute(query)
        customers = cursor.fetchall()
        cursor.close()
        conn.close()
        if customers:
            customer_list = []
            for customer in customers:
                customer_list.append({
                    "CustomerID": customer[0],
                    "FirstName": customer[1],
                    "LastName": customer[2],
                    "Email": customer[3],
                    "PhoneNumber": customer[4],
                    "Address": customer[5],
                    "CreatedAt": customer[6],
                    "UpdatedAt": customer[7]
                })
            return jsonify(customer_list), 200
        else:
            return jsonify({"message": "No customers found"}), 404
    return jsonify({"message": "Failed to connect to database"}), 500

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
