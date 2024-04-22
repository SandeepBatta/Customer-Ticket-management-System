import streamlit as st
import mysql.connector
from mysql.connector import Error
import json


def get_connection():
    with open("credentials.json") as fh:
        credentials = json.load(fh)

    user = credentials["user"]
    password = credentials["password"]
    hostname = credentials["hostname"]
    database = credentials["database"]

    # Create a connection to the MySQL database
    try:
        connection = mysql.connector.connect(
            host=hostname,
            database=database,
            user=user,
            password=password,
        )
        return connection
    except Error as e:
        st.error("Error connecting to database", e)
        st.stop()


def get_users():
    connection = get_connection()
    if connection.is_connected():
        cursor = connection.cursor()
        query = "SELECT userid, name FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return users


def get_total_pages(filters, page_size):
    connection = get_connection()
    if connection.is_connected():
        cursor = connection.cursor()

        query = "SELECT COUNT(*) FROM tickets WHERE 1=1"

        if filters["type"]:
            query += f" AND type = '{filters['type']}'"

        if filters["status"]:
            query += f" AND status = '{filters['status']}'"

        if filters["priority"]:
            query += f" AND priority = '{filters['priority']}'"

        if "user_ids" in filters and filters["user_ids"]:
            user_ids_str = ", ".join(str(user_id) for user_id in filters["user_ids"])
            query += f" AND userid IN ({user_ids_str})"

        cursor.execute(query)
        count = cursor.fetchone()[0]
        cursor.close()
        connection.close()

        total_pages = (
            (count // page_size) + 1 if count % page_size else count // page_size
        )
        return total_pages


def get_tickets(filters, page_size, page_number):
    connection = get_connection()
    if connection.is_connected():
        cursor = connection.cursor()

        query = "SELECT t.*, u.name FROM tickets t LEFT JOIN users u ON t.userid = u.userid WHERE 1=1"

        if filters["type"]:
            query += f" AND type = '{filters['type']}'"

        if filters["status"]:
            query += f" AND status = '{filters['status']}'"

        if filters["priority"]:
            query += f" AND priority = '{filters['priority']}'"

        if "user_ids" in filters and filters["user_ids"]:
            user_ids_str = ", ".join(str(user_id) for user_id in filters["user_ids"])
            query += f" AND t.userid IN ({user_ids_str})"

        # Add pagination
        query += f" ORDER BY create_time DESC LIMIT {page_size} OFFSET {(page_number - 1) * page_size}"

        cursor.execute(query)
        tickets = cursor.fetchall()
        cursor.close()
        connection.close()
        return tickets


def insert_ticket(userid, subject, description, type, priority):
    connection = get_connection()
    if connection.is_connected():
        cursor = connection.cursor()
        description = description.replace('"', "'")
        query = f"""INSERT INTO tickets (userid, type, subject, description, priority) VALUES ({userid}, '{type}', '{subject}', '{description}', '{priority}')"""
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        st.toast("Ticket created successfully.")


def update_ticket(ticketid, subject, description, type, priority, status):
    connection = get_connection()
    if connection.is_connected():
        cursor = connection.cursor()
        description = description.replace('"', "'")
        query = f"""UPDATE tickets SET subject = '{subject}', description = "{description}", priority = '{priority}', type = '{type}', status = '{status}' WHERE ticketid = {ticketid}"""
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        st.toast("Ticket Updated successfully.")


def delete_ticket(ticket_id):
    connection = get_connection()
    if connection.is_connected():
        cursor = connection.cursor()
        query = f"""DELETE FROM tickets WHERE ticketid = {ticket_id}"""
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        st.toast("Ticket deleted successfully.")
