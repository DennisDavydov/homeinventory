import mysql.connector

def insert_data(data):
    # Establish a connection to your MariaDB instance
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='inventory_db'
    )
    # Create a cursor object to interact with the database
    cursor = connection.cursor()
    # Sample data to be inserted
    
    # SQL query to insert data into the products table
    insert_query = "INSERT INTO products (barcode, name, manufacturer, amount, category, storage_place, expiry_type, expiry_date, unit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # Execute the query to insert data
    
    cursor.execute(insert_query, data)

    # Commit changes to the database
    connection.commit()
    if not check_database(data[0]):
        insert_query = "INSERT INTO product_templates (barcode, name, manufacturer, amount, category, storage_place, expiry_type, unit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, data[0:8])
        connection.commit()
    # Close the cursor and connection
    cursor.close()
    connection.close()
    
def check_database(barcode):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="inventory_db"
    )

    cursor=connection.cursor()
    query = f"SELECT * FROM product_templates WHERE barcode = '{barcode}'"

    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    
    return result is not None
def select_data(barcode):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="inventory_db"
    )

    cursor=connection.cursor()
    
    select_query = "select * from product_templates where barcode = %s"
    cursor.execute(select_query, (barcode,))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results
    
def remove_product(barcode, date):

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="inventory_db"
    )

    cursor=connection.cursor()
    if date == None:
        delete_query = "delete from products where barcode = %s and expiry_date is %s limit 1"
    else:
        delete_query = "delete from products where barcode = %s and expiry_date = %s limit 1"

    cursor.execute(delete_query, (barcode, date))
    connection.commit()
    cursor.close()
    connection.close()
    
