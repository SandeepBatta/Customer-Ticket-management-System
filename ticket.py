import streamlit as st
from datetime import datetime
from database import insert_ticket

def show_ticket_form():
    # Initialize the Streamlit app
    st.title('Customer Support Ticket Form')

    # Using form for input
    with st.form("ticket_form"):
        st.write("Please fill in the details for the new support ticket.")

        # Fields to input data
        user_id = st.number_input('User ID', min_value=1, step=1)
        sale_id = st.number_input('Sale ID', min_value=1, step=1)
        ticket_type = st.selectbox('Ticket Type', options=[
            'Technical issue',
            'Billing inquiry',
            'Cancellation request',
            'Refund request',
            'Product inquiry'
        ])
        subject = st.text_input('Subject')
        description = st.text_area('Description')
        create_time = st.text_input('Create Time', value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        priority = st.selectbox('Priority', options=['Low', 'Medium', 'High', 'Critical'])

        # Submit button for the form
        submit_button = st.form_submit_button("Submit Ticket")

        # Processing form data
        if submit_button:
            ticket_data = {
                "userid": user_id,
                "saleid": sale_id,
                "type": ticket_type,
                "subject": subject,
                "description": description,
                "create_time": create_time,
                "status": "open",
                "priority": priority,
                "channel": "website",
            }
            insert_ticket(ticket_data)  # Simulate a database operation
            st.success("Ticket submitted successfully!")
