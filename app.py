
from datetime import date

import requests
import streamlit as st


API_URL = "https://smartspend-api-sd05.onrender.com"

st.set_page_config(
    page_title="SmartSpend",
    page_icon="💰",
    layout="wide"
)

st.title("💰 SmartSpend")
st.caption("Track expenses. Manage your monthly budget.")




today = date.today()

selected_date = st.sidebar.date_input(
    "Select month",
    value=today,
    format="DD/MM/YYYY"
)

month = selected_date.strftime("%Y-%m")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Add Expense", "Manage Expenses", "Manage Budget"]
)


def get_expenses(selected_month):
    response = requests.get(
        f"{API_URL}/expenses",
        params={"month": selected_month},
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def get_budget(selected_month):
    response = requests.get(
        f"{API_URL}/budget",
        params={"month": selected_month},
        timeout=10
    )
    response.raise_for_status()
    return response.json()


try:
    
    if page == "Dashboard":
        st.subheader(f"Dashboard — {month}")

        expenses = get_expenses(month)
        budget_info = get_budget(month)

        # Summary cards
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Monthly Budget",
            f"₹{budget_info['monthly_budget']:,.2f}"
        )

        col2.metric(
            "Total Spending",
            f"₹{budget_info['total_spending']:,.2f}"
        )

        col3.metric(
            "Remaining Budget",
            f"₹{budget_info['remaining_budget']:,.2f}"
        )
        # Monthly Budget Allocation
                # Monthly Budget Allocation
        st.divider()
        st.subheader("Monthly Budget Allocation")

        monthly_budget = budget_info["monthly_budget"]
        total_spending = budget_info["total_spending"]
        remaining = budget_info["remaining_budget"]

        if monthly_budget > 0:

            # Divide Monthly Budget
            expense_allocation = monthly_budget * 0.70
            savings_allocation = monthly_budget * 0.30

            # Calculate Amount Used
            expense_used = min(total_spending, expense_allocation)
            savings_used = max(0, total_spending - expense_allocation)

            # Calculate Progress
            expense_progress = expense_used / expense_allocation
            savings_progress = savings_used / savings_allocation

            # Remaining Savings
            savings_remaining = max(
                0, savings_allocation - savings_used
            )

            # Expense Allocation
            st.subheader("🔵 Expense Allocation (70%)")

            st.write(
                f"₹{expense_used:,.2f} / ₹{expense_allocation:,.2f}"
            )

            st.progress(min(expense_progress, 1.0))

            st.caption(
                f"{expense_progress * 100:.1f}% of expense allocation used"
            )

            if total_spending > expense_allocation:
                st.error(
                    "🔴 Expense allocation exceeded! "
                    f"You have crossed your ₹{expense_allocation:,.2f} limit."
                )

            elif expense_progress >= 1:
                st.error(
                    "🔴 Your entire expense allocation has been used!"
                )

            elif expense_progress >= 0.75:
                st.warning(
                    "🟠 You are approaching your expense allocation limit."
                )

            elif expense_progress >= 0.50:
                st.info(
                    "🔵 Halfway reached! You have used at least 50% "
                    "of your expense allocation."
                )

            else:
                st.success(
                    "🟢 Your expense spending is under control."
                )

            # Savings Allocation
            st.subheader("🟢 Savings Allocation (30%)")

            st.write(
                f"₹{savings_used:,.2f} / ₹{savings_allocation:,.2f}"
            )

            st.progress(min(savings_progress, 1.0))

            st.caption(
                f"{savings_progress * 100:.1f}% of savings allocation used"
            )

            if savings_used > savings_allocation:
                st.error(
                    "🔴 Your savings allocation has been exhausted "
                    "and your total monthly budget has been exceeded."
                )

            elif savings_progress >= 1:
                st.error(
                    "🔴 Your entire savings allocation has been used!"
                )

            elif savings_used > 0:
                st.warning(
                    f"🟠 You have used ₹{savings_used:,.2f} "
                    "from your savings allocation."
                )

            else:
                st.success(
                    "🟢 Your savings allocation is untouched."
                )

            st.caption(
                f"₹{savings_remaining:,.2f} of your savings allocation remains."
            )

            # Total Budget Summary
            st.divider()
            st.subheader("Total Budget Summary")

            col1, col2 = st.columns(2)

            col1.metric(
                "Total Spending",
                f"₹{total_spending:,.2f}"
            )

            col2.metric(
                "Remaining Budget",
                f"₹{remaining:,.2f}"
            )

        else:
            st.warning("Please set a monthly budget greater than zero.")

        st.divider()
        # Category summary
        st.subheader("Spending by Category")

        if expenses:
            category_totals = {}

            for expense in expenses:
                category = expense["category"]
                amount = expense["amount"]

                if category in category_totals:
                    category_totals[category] += amount
                else:
                    category_totals[category] = amount

            st.bar_chart(category_totals)

            # Latest expenses preview
            st.divider()
            st.subheader("Recent Expenses")
            st.caption(
                "A quick preview. Open Manage Expenses for the full history."
            )

            recent_expenses = sorted(
                expenses,
                key=lambda expense: (expense["date"], expense["id"]),
                reverse=True
            )

            for expense in recent_expenses[:3]:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.markdown(f"**{expense['title']}**")
                        st.caption(
                            f"{expense['category']} • {expense['date']}"
                        )

                    with col2:
                        st.markdown(
                            f"**₹{expense['amount']:,.2f}**"
                        )

        else:
            st.info(
                "No expenses recorded for this month. "
                "Go to Add Expense to get started."
            )


    elif page == "Add Expense":
        st.subheader("Add a New Expense")

        with st.form("expense_form", clear_on_submit=True):
            title = st.text_input("Expense title")

            amount = st.number_input(
                "Amount (₹)",
                min_value=0.01,
                value=100.0
            )

            category = st.selectbox(
                "Category",
                [
                    "Food", "Transport", "Shopping", "Bills",
                    "Education", "Health", "Entertainment", "Other"
                ]
            )

            expense_date = st.date_input(
                "Expense date",
                value=today
            )

            submitted = st.form_submit_button("Save Expense")

        if submitted:
            if not title.strip():
                st.error("Please enter an expense title.")
            else:
                expense = {
                    "title": title.strip(),
                    "amount": amount,
                    "category": category,
                    "date": expense_date.isoformat()
                }

                try:
                    response = requests.post(
                        f"{API_URL}/expenses",
                        json=expense,
                        timeout=10
                    )

                    if response.ok:
                        st.success("Expense saved successfully!")
                        st.rerun()
                    else:
                        st.error("Expense could not be saved.")

                except requests.RequestException:
                    st.error("Could not connect to the server.")

    
    elif page == "Manage Expenses":
        st.subheader(f"Manage Expenses — {month}")

        expenses = get_expenses(month)

        if expenses:
            # Summary section
            total_spending = 0

            for expense in expenses:
                total_spending += expense["amount"]

            col1, col2 = st.columns(2)

            col1.metric(
                "Total Expenses",
                len(expenses)
            )

            col2.metric(
                "Monthly Spending",
                f"₹{total_spending:,.2f}"
            )

            st.divider()

            # Expense history table
            st.subheader("Expense History")

            st.dataframe(
                [
                    {
                        "ID": expense["id"],
                        "Title": expense["title"],
                        "Amount (₹)": expense["amount"],
                        "Category": expense["category"],
                        "Date": expense["date"]
                    }
                    for expense in expenses
                ],
                width="stretch",
                hide_index=True
            )

            st.divider()
            st.subheader("Manage Individual Expenses")

            for expense in expenses:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.markdown(f"### {expense['title']}")
                        st.write(
                            f"**Amount:** ₹{expense['amount']:,.2f}"
                        )
                        st.caption(
                            f"ID: {expense['id']}  |  "
                            f"{expense['category']}  |  "
                            f"{expense['date']}"
                        )

                    with col2:
                        st.write("")
                        st.write("")
                        st.button(
                            "Edit",
                            key=f"edit_{expense['id']}",
                            on_click=lambda expense_id=expense["id"]:
                                st.session_state.update(
                                    {"editing_expense_id": expense_id}
                                )
                        )

                        if st.button(
                            "Delete",
                            key=f"delete_{expense['id']}"
                        ):
                            try:
                                response = requests.delete(
                                    f"{API_URL}/expenses/{expense['id']}",
                                    timeout=10
                                )

                                if response.ok:
                                    st.success("Expense deleted!")
                                    st.rerun()
                                else:
                                    st.error("Could not delete expense.")

                            except requests.RequestException:
                                st.error("Could not connect to the server.")

                    # Show the edit form only for the selected expense
                    if st.session_state.get("editing_expense_id") == expense["id"]:
                        st.divider()
                        st.markdown("#### Edit Expense Details")

                        with st.form(f"edit_form_{expense['id']}"):
                            edit_title = st.text_input(
                                "Title",
                                value=expense["title"]
                            )

                            edit_amount = st.number_input(
                                "Amount (₹)",
                                min_value=0.01,
                                value=float(expense["amount"])
                            )

                            categories = [
                                "Food", "Transport", "Shopping", "Bills",
                                "Education", "Health", "Entertainment", "Other"
                            ]

                            edit_category = st.selectbox(
                                "Category",
                                categories,
                                index=(
                                    categories.index(expense["category"])
                                    if expense["category"] in categories
                                    else 7
                                )
                            )

                            edit_date = st.date_input(
                                "Date",
                                value=date.fromisoformat(expense["date"])
                            )

                            save_changes = st.form_submit_button(
                                "Save Changes"
                            )

                        if save_changes:
                            if not edit_title.strip():
                                st.error("Please enter an expense title.")
                            else:
                                try:
                                    response = requests.put(
                                        f"{API_URL}/expenses/{expense['id']}",
                                        json={
                                            "title": edit_title.strip(),
                                            "amount": edit_amount,
                                            "category": edit_category,
                                            "date": edit_date.isoformat()
                                        },
                                        timeout=10
                                    )

                                    if response.ok:
                                        st.session_state.pop(
                                            "editing_expense_id", None
                                        )
                                        st.success("Expense updated!")
                                        st.rerun()
                                    else:
                                        st.error(
                                            "Could not update expense. "
                                            "Check the FastAPI edit endpoint."
                                        )

                                except requests.RequestException:
                                    st.error("Could not connect to the server.")

                        if st.button(
                            "Cancel Editing",
                            key=f"cancel_{expense['id']}"
                        ):
                            st.session_state.pop(
                                "editing_expense_id", None
                            )
                            st.rerun()

        else:
            st.info("No expenses found for this month. Add one to get started!")


    elif page == "Manage Budget":
        st.subheader(f"Manage Budget — {month}")

        budget_info = get_budget(month)

        st.metric(
            "Current Monthly Budget",
            f"₹{budget_info['monthly_budget']:,.2f}"
        )

        with st.form("budget_form"):
            new_budget = st.number_input(
                "Monthly budget (₹)",
                min_value=0.01,
                value=float(budget_info["monthly_budget"]),
                step=500.0
            )

            update_clicked = st.form_submit_button("Update Budget")

        if update_clicked:
            try:
                response = requests.put(
                    f"{API_URL}/budget",
                    json={
                        "month": month,
                        "monthly_budget": new_budget
                    },
                    timeout=10
                )

                if response.ok:
                    st.success("Budget updated successfully!")
                    st.rerun()
                else:
                    st.error("Could not update budget.")

            except requests.RequestException:
                st.error("Could not connect to the server.")

except requests.RequestException:
    st.error(
        "Could not connect to the SmartSpend API. "
        "Make sure FastAPI is running."
    )
