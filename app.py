import streamlit as st
from datetime import datetime

from database import (
    create_tables,
    create_ticket,
    get_all_tickets,
    update_ticket,
    get_ticket_history
)


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="EduSupport",
    page_icon="🎓",
    layout="wide"
)

create_tables()


# -----------------------------
# Header
# -----------------------------

st.title("🎓 EduSupport")
st.subheader(
    "Student Support & Ticket Management System"
)


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("Navigation")

role = st.sidebar.radio(
    "Select Role",
    [
        "🎓 Student",
        "👨‍💼 Staff"
    ]
)


# ==================================================
# STUDENT
# ==================================================

if role == "🎓 Student":

    st.header("Create New Support Ticket")

    student_name = st.text_input(
        "Student Name"
    )

    student_id = st.text_input(
        "Student ID"
    )

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

    subject = st.text_input(
        "Subject"
    )

    description = st.text_area(
        "Describe your problem",
        height=150
    )

    if st.button(
        "Submit Ticket",
        type="primary"
    ):

        if not student_name.strip():
            st.error(
                "Please enter your name."
            )

        elif not student_id.strip():
            st.error(
                "Please enter your Student ID."
            )

        elif not subject.strip():
            st.error(
                "Please enter the subject."
            )

        elif not description.strip():
            st.error(
                "Please describe your problem."
            )

        else:

            ticket_id = create_ticket(
                student_name.strip(),
                student_id.strip(),
                category,
                priority,
                subject.strip(),
                description.strip()
            )

            st.success(
                f"Ticket created successfully! "
                f"Your Ticket ID is {ticket_id}"
            )

            st.info(
                "Please keep your Ticket ID for future reference."
            )


# ==================================================
# STAFF
# ==================================================

else:

    st.header("👨‍💼 Staff Dashboard")

    tickets = get_all_tickets()


    # -----------------------------
    # Dashboard Statistics
    # -----------------------------

    total = len(tickets)

    new_count = sum(
        1 for t in tickets
        if t[7] == "NEW"
    )

    progress_count = sum(
        1 for t in tickets
        if t[7] == "IN PROGRESS"
    )

    pending_count = sum(
        1 for t in tickets
        if t[7] == "PENDING"
    )

    resolved_count = sum(
        1 for t in tickets
        if t[7] == "RESOLVED"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total",
        total
    )

    col2.metric(
        "New",
        new_count
    )

    col3.metric(
        "In Progress",
        progress_count
    )

    col4.metric(
        "Pending",
        pending_count
    )

    col5.metric(
        "Resolved",
        resolved_count
    )

    st.divider()


    # -----------------------------
    # Search and Filter
    # -----------------------------

    st.subheader("Ticket Management")

    search = st.text_input(
        "🔎 Search by Ticket ID, Student ID or Subject"
    )

    status_filter = st.selectbox(
        "Filter by Status",
        [
            "ALL",
            "NEW",
            "ASSIGNED",
            "IN PROGRESS",
            "PENDING",
            "RESOLVED",
            "CLOSED"
        ]
    )

    priority_filter = st.selectbox(
        "Filter by Priority",
        [
            "ALL",
            "Low",
            "Medium",
            "High",
            "Urgent"
        ]
    )


    # -----------------------------
    # Filter Tickets
    # -----------------------------

    filtered_tickets = []

    for ticket in tickets:

        ticket_id = ticket[0]
        student_id = ticket[2]
        subject = ticket[5]
        priority = ticket[4]
        status = ticket[7]

        matches_search = (
            not search
            or search.lower() in ticket_id.lower()
            or search.lower() in student_id.lower()
            or search.lower() in subject.lower()
        )

        matches_status = (
            status_filter == "ALL"
            or status == status_filter
        )

        matches_priority = (
            priority_filter == "ALL"
            or priority == priority_filter
        )

        if (
            matches_search
            and matches_status
            and matches_priority
        ):
            filtered_tickets.append(ticket)


    if not filtered_tickets:

        st.info(
            "No tickets match the selected filters."
        )


    # -----------------------------
    # Display Tickets
    # -----------------------------

    for ticket in filtered_tickets:

        (
            ticket_id,
            student_name,
            student_id,
            category,
            priority,
            subject,
            description,
            status,
            assigned_to,
            created_at,
            updated_at,
            pending_reason,
            resolution_note,
            due_at
        ) = ticket


        # -----------------------------
        # SLA / Ageing
        # -----------------------------

        try:

            created_time = datetime.strptime(
                created_at,
                "%Y-%m-%d %H:%M:%S"
            )

            due_time = datetime.strptime(
                due_at,
                "%Y-%m-%d %H:%M:%S"
            )

            current_time = datetime.now()

            age_hours = (
                current_time - created_time
            ).total_seconds() / 3600

            if current_time > due_time:

                sla_text = "⚠️ SLA BREACHED"

            else:

                remaining = (
                    due_time - current_time
                ).total_seconds() / 3600

                sla_text = (
                    f"⏱️ {remaining:.1f} hours remaining"
                )

        except:

            age_hours = 0
            sla_text = "SLA information unavailable"


        # -----------------------------
        # Ticket Expander
        # -----------------------------

        with st.expander(
            f"{ticket_id} | {subject} | "
            f"{priority} | {status}"
        ):

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Student:** {student_name}"
                )

                st.write(
                    f"**Student ID:** {student_id}"
                )

                st.write(
                    f"**Category:** {category}"
                )

                st.write(
                    f"**Priority:** {priority}"
                )

                st.write(
                    f"**Subject:** {subject}"
                )

                st.write(
                    f"**Description:** {description}"
                )


            with col2:

                st.write(
                    f"**Status:** {status}"
                )

                st.write(
                    f"**Assigned To:** "
                    f"{assigned_to or 'Not Assigned'}"
                )

                st.write(
                    f"**Created:** {created_at}"
                )

                st.write(
                    f"**Last Updated:** {updated_at}"
                )

                st.write(
                    f"**Ticket Age:** "
                    f"{age_hours:.1f} hours"
                )

                st.write(
                    f"**SLA:** {sla_text}"
                )


            st.divider()


            # -----------------------------
            # Staff Update
            # -----------------------------

            st.subheader("Update Ticket")

            staff_name = st.selectbox(
                "Assign Staff",
                [
                    "Not Assigned",
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


            # -----------------------------
            # Pending Reason
            # -----------------------------

            new_pending_reason = st.text_area(
                "Pending Action / Reason",
                value=pending_reason or "",
                placeholder=(
                    "Enter the reason if the ticket "
                    "is waiting for an action."
                ),
                key=f"pending_{ticket_id}"
            )


            # -----------------------------
            # Resolution Note
            # -----------------------------

            new_resolution_note = st.text_area(
                "Resolution / Closure Note",
                value=resolution_note or "",
                placeholder=(
                    "Enter how the issue was resolved."
                ),
                key=f"resolution_{ticket_id}"
            )


            # -----------------------------
            # Save
            # -----------------------------

            if st.button(
                "Save Changes",
                key=f"save_{ticket_id}"
            ):

                if (
                    new_status == "PENDING"
                    and not new_pending_reason.strip()
                ):

                    st.error(
                        "Please enter a pending reason."
                    )

                elif (
                    new_status in [
                        "RESOLVED",
                        "CLOSED"
                    ]
                    and not new_resolution_note.strip()
                ):

                    st.error(
                        "Please enter a resolution note."
                    )

                else:

                    update_ticket(
                        ticket_id,
                        staff_name,
                        new_status,
                        new_pending_reason.strip(),
                        new_resolution_note.strip()
                    )

                    st.success(
                        f"{ticket_id} updated successfully!"
                    )

                    st.rerun()


            # -----------------------------
            # Activity History
            # -----------------------------

            st.subheader("Activity History")

            history = get_ticket_history(
                ticket_id
            )

            if history:

                for item in history:

                    action = item[0]
                    details = item[1]
                    history_time = item[2]

                    st.write(
                        f"**{history_time}** — "
                        f"{action}: {details}"
                    )

            else:

                st.info(
                    "No activity history available."
                )
