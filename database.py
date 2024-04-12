import streamlit as st
from sqlalchemy import create_engine, text

def get_connection():
    # Create a connection to the MySQL database
    engine = create_engine("mysql+pymysql://ctms:qwerty%40123@34.171.75.40:3306/ctms")
    return engine.connect()

def insert_ticket(data):
    conn = get_connection()
    try:
        query = text("""
            INSERT INTO tickets (userid, saleid, type, subject, description, create_time, status, priority, channel)
            VALUES (:userid, :saleid, :type, :subject, :description, :create_time, :status, :priority, :channel)
        """)
        conn.execute(query, data)
        conn.commit()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        conn.execute("ROLLBACK")
    finally:
        conn.close()
