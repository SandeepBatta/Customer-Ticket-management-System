import streamlit as st
from database import (
    get_tickets,
    insert_ticket,
    update_ticket,
    delete_ticket,
    get_users,
    get_total_pages,
)

types = [
    "Billing Inquiry",
    "Cancellation Request",
    "Product Inquiry",
    "Refund Request",
    "Technical Issue",
]

priorities = ["Low", "Medium", "High", "Critical"]

status = ["Open", "Closed", "Pending Customer Response"]


def show_create_ticket():
    st.title("Create New Ticket")

    # Create a form
    with st.form("create_ticket_form", clear_on_submit=True, border=False):
        subject = st.text_input("Subject", key="ticket_subject")
        description = st.text_area("Description", key="ticket_description")

        # Get users for Admin
        if st.session_state["role"] == "Admin":
            users = get_users()
            user_options = {user[1]: user[0] for user in users}
            selected_user = st.selectbox(
                "On Behalf of...",
                list(user_options.keys()),
                index=None,
                key="selected_user",
            )
            if selected_user:
                user_id = user_options[selected_user]
        else:
            user_id = st.session_state["userid"]

        # Dropdowns for Type and Priority
        selected_type = st.selectbox(
            "Type", types, index=None, key="selected_type", help="Select Issue Type"
        )

        selected_priority = st.selectbox(
            "Priority",
            priorities,
            index=1,
            key="selected_priority",
            format_func=lambda x: x.capitalize(),
        )

        if st.form_submit_button("Create Ticket"):
            if subject and description:
                # Insert the ticket into the database
                insert_ticket(
                    user_id,
                    subject,
                    description,
                    selected_type,
                    selected_priority,
                )
            else:
                st.warning("Please fill in all fields.")


def show_update_ticket(ticket):
    with st.popover("Update Ticket"):
        st.title("Update Ticket")

        with st.form(key="Update Ticket Form" + str(ticket[0]), border=False):
            subject = st.text_input("Subject", value=ticket[4], key=ticket[0])
            description = st.text_area(
                "Description", value=ticket[5], key="desc " + str(ticket[0])
            )

            # Dropdowns for Type and Priority
            selected_type = st.selectbox(
                "Type",
                types,
                index=types.index(ticket[3]),
                key="update type " + str(ticket[0]),
            )

            selected_priority = st.selectbox(
                "Priority",
                priorities,
                index=priorities.index(ticket[9]),
                key="update priority " + str(ticket[0]),
            )

            selected_status = st.selectbox(
                "Status",
                status,
                index=status.index(ticket[7]),
                key="update status " + str(ticket[0]),
            )

            if st.form_submit_button("Update Ticket"):
                update_ticket(
                    ticket[0],
                    subject,
                    description,
                    selected_type,
                    selected_priority,
                    selected_status,
                )
                st.rerun()


def show_delete_ticket(ticket):
    if st.button(f"Delete Ticket {ticket[0]}"):
        delete_ticket(ticket[0])
        st.rerun()


def pagination(filters, page_size, page_number):
    # Pagination: Previous and Next buttons
    total_pages = get_total_pages(filters, page_size)
    if total_pages > 1:
        with st.container():
            st.write("---")
            col1, col2 = st.columns([1, 1])
            with col1:
                if page_number > 1:
                    if st.button(
                        ":green[:point_left: Previous]", use_container_width=True
                    ):
                        st.session_state["page_number"] -= 1
                        st.rerun()
                else:
                    st.write("")  # Placeholder to maintain layout
            with col2:
                if page_number < total_pages:
                    if st.button(
                        ":green[Next :point_right:]", use_container_width=True
                    ):
                        st.session_state["page_number"] += 1
                        st.rerun()
                else:
                    st.write("")  # Placeholder to maintain layout


def show_tickets():
    # Pagination parameters
    page_size = 10
    if "page_number" not in st.session_state:
        st.session_state["page_number"] = 1
    page_number = st.session_state["page_number"]

    # Get tickets based on filters
    filters = {}
    with st.form("ticket_filters_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            filters["type"] = st.selectbox("Filter by Type", types, index=None)
        with col2:
            filters["status"] = st.selectbox("Filter by Status", status, index=None)
        with col3:
            filters["priority"] = st.selectbox(
                "Filter by Priority", priorities, index=None
            )

        # Filter by Users (for Admin)
        if st.session_state["role"] == "Admin":
            users = get_users()
            selected_users = st.multiselect(
                "Filter by Users",
                [user[1] for user in users],
            )
            if selected_users:
                # Get user IDs from selected usernames
                user_ids = [user[0] for user in users if user[1] in selected_users]
                filters["user_ids"] = user_ids
        else:
            filters["user_ids"] = [st.session_state.userid]

        if st.form_submit_button("Apply Filters"):
            st.session_state["page_number"] = 1
            st.rerun()

    st.header("Tickets Information")
    with st.spinner("Wait for it..."):
        tickets = get_tickets(filters, page_size, page_number)
        for ticket in tickets:
            with st.container():
                st.write("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write("**Ticket ID:**", ticket[0])
                    st.write("**Subject:**", ticket[4])
                with col2:
                    st.write("**User:**", f":blue[{ticket[13]}]")
                    st.write("**Type:**", ticket[3])
                with col3:
                    st.write("**Status:**", f":orange[{ticket[7]}]")
                    st.write("**Priority:**", ticket[9])

                # More info expander
                with st.expander("Description"):
                    st.write(ticket[5])

                # Update and delete functionality
                col1, col2 = st.columns([1, 1])
                with col1:
                    show_update_ticket(ticket)
                with col2:
                    show_delete_ticket(ticket)

        pagination(filters, page_size, page_number)
