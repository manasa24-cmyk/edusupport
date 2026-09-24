import streamlit as st
from database import (
    create_tables,
    create_ticket,
    get_all_tickets,
    update_ticket
)

create_tables()

st.set_page_config(
    page_title="EduSupport",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 EduSupport")
st.subheader("Student Support & Ticket Management System")

st.sidebar.title("Navigation")

role = st.sidebar.radio(
    "Select Role",
    ["🎓 Student", "👨‍💼 Staff"]
)

if role == "🎓 Student":

    st.header("Create New Ticket")

    student_name = st.text_input("Student Name")
    student_id = st.text_input("Student ID")

    category = st.selectbox(
        "Category",
        [
            "Fees",
            "Attendance",
            "ID Card",
            "Documents",
            "Certificates",
            "Other"
        ]
    )

    priority = st.selectbox(
        "Priority",
        [
            "Low",
            "Medium",
            "High",
            "Urgent"
        ]
    )

    subject = st.text_input("Subject")

    description = st.text_area(
        "Describe your problem",
        height=150
    )

    if st.button("Submit Ticket"):

        if not student_name:
            st.error("Please enter your name.")

        elif not student_id:
            st.error("Please enter your Student ID.")

        elif not subject:
            st.error("Please enter the subject.")

        elif not description:
            st.error("Please describe your problem.")

        else:

            ticket_id = create_ticket(
                student_name,
                student_id,
                category,
                priority,
                subject,
                description
            )

            st.success(
                f"Ticket created successfully! Ticket ID: {ticket_id}"
            )

else:

    st.header("👨‍💼 Staff Dashboard")

    tickets = get_all_tickets()

    if not tickets:

        st.info("No tickets available.")

    else:

        st.subheader("All Support Tickets")

        for ticket in tickets:

            (
                ticket_id,
                student_name,
                student_id,
                category,
                priority,
                subject,
                status,
                assigned_to,
                created_at
            ) = ticket

            with st.expander(
                f"{ticket_id} | {subject} | {status}"
            ):

                st.write(f"**Student:** {student_name}")
                st.write(f"**Student ID:** {student_id}")
                st.write(f"**Category:** {category}")
                st.write(f"**Priority:** {priority}")
                st.write(f"**Subject:** {subject}")
                st.write(f"**Status:** {status}")
                st.write(
                    f"**Assigned To:** "
                    f"{assigned_to or 'Not Assigned'}"
                )
                st.write(f"**Created:** {created_at}")

                st.divider()

                staff_name = st.selectbox(
                    "Assign Staff",
                    [
                        "Anita - Fees",
                        "Rahul - Student Services",
                        "Priya - Administration"
                    ],
                    key=f"staff_{ticket_id}"
                )

                new_status = st.selectbox(
                    "Update Status",
                    [
                        "NEW",
                        "ASSIGNED",
                        "IN PROGRESS",
                        "PENDING",
                        "RESOLVED",
                        "CLOSED"
                    ],
                    key=f"status_{ticket_id}"
                )

                if st.button(
                    "Save Changes",
                    key=f"save_{ticket_id}"
                ):

                    update_ticket(
                        ticket_id,
                        staff_name,
                        new_status
                    )

                    st.success(
                        f"{ticket_id} updated successfully!"
                    )

                    st.rerun()