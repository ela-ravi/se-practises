import streamlit as st
import pandas as pd
from collections import namedtuple
import math

# --- Named Tuple for clarity ---
Transaction = namedtuple('Transaction', ['payer', 'receiver', 'amount'])
Friend = namedtuple('Friend', ['name', 'balance'])

def calculate_settlements(balances):
    """
    Calculates the minimum number of transactions required to settle balances.

    Args:
        balances (list[Friend]): List of named tuples with 'name' and 'balance'.

    Returns:
        list[Transaction]: A list of transactions (payer, receiver, amount).
    """
    transactions = []
    
    # Separate debtors (negative balance, owes money) and creditors (positive balance, gets money)
    debtors = sorted([f for f in balances if f.balance < 0], key=lambda x: x.balance) # Lowest (most negative) first
    creditors = sorted([f for f in balances if f.balance > 0], key=lambda x: x.balance, reverse=True) # Highest (most positive) first

    # Convert to dictionaries for mutable remaining amounts
    debtors_dict = {d.name: abs(d.balance) for d in debtors}
    creditors_dict = {c.name: c.balance for c in creditors}

    # Use iterators to manage the transaction process efficiently
    debtor_names = list(debtors_dict.keys())
    creditor_names = list(creditors_dict.keys())
    
    debtor_idx = 0
    creditor_idx = 0
    
    while debtor_idx < len(debtor_names) and creditor_idx < len(creditor_names):
        debtor_name = debtor_names[debtor_idx]
        creditor_name = creditor_names[creditor_idx]
        
        # Get the current debt/credit amounts (always positive)
        debt_amount = debtors_dict[debtor_name]
        credit_amount = creditors_dict[creditor_name]
        
        # Determine the amount of the transaction
        settlement_amount = min(debt_amount, credit_amount)
        
        # Ensure we only record valid transactions
        if settlement_amount > 0.01: # Check for floating point safety
            transactions.append(Transaction(debtor_name, creditor_name, settlement_amount))
        
        # Update remaining amounts
        debtors_dict[debtor_name] -= settlement_amount
        creditors_dict[creditor_name] -= settlement_amount
        
        # Move to the next debtor if their debt is paid off
        if debtors_dict[debtor_name] < 0.01:
            debtor_idx += 1
            
        # Move to the next creditor if their credit is paid off
        if creditors_dict[creditor_name] < 0.01:
            creditor_idx += 1

    return transactions

# --- Streamlit UI Setup ---
def app():
    st.set_page_config(
        page_title="Group Expense Splitter",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    st.title("💸 Group Expense Splitter")
    st.markdown("Easily calculate who owes whom after a trip or dinner.")
    
    # --- Input Section ---
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        total_amount = st.number_input(
            "Total Amount Spent ($)",
            min_value=0.0,
            value=100.0,
            step=10.0,
            format="%.2f",
            help="The total cost of the trip, dinner, or expense."
        )
    
    with col2:
        num_friends = st.number_input(
            "Number of Friends",
            min_value=2,
            value=3,
            step=1,
            format="%d",
            help="The total number of people splitting the expense."
        )

    # --- Dynamic Friends Input ---
    st.markdown("### Individual Contributions")

    # Initialize session state for friend data if it doesn't exist or if num_friends changed
    if 'friend_data' not in st.session_state or len(st.session_state.friend_data) != num_friends:
        # Generate default names (F1, F2, ...) and zero contributions
        st.session_state.friend_data = [
            {'name': f'Friend {i+1}', 'contribution': 0.0}
            for i in range(num_friends)
        ]

    # Create dynamic input fields inside a form for better control
    with st.form("expense_form"):
        cols = st.columns(num_friends)
        
        for i, col in enumerate(cols):
            with col:
                # Use a unique key based on the index
                st.session_state.friend_data[i]['name'] = st.text_input(
                    label=f"Name {i+1}",
                    value=st.session_state.friend_data[i]['name'],
                    key=f"name_{i}",
                )
                
                st.session_state.friend_data[i]['contribution'] = st.number_input(
                    label=f"Paid ($)",
                    min_value=0.0,
                    value=st.session_state.friend_data[i]['contribution'],
                    step=5.0,
                    format="%.2f",
                    key=f"contribution_{i}",
                    help=f"How much {st.session_state.friend_data[i]['name']} paid."
                )

        calculate_button = st.form_submit_button("Calculate Split", type="primary")

    if calculate_button:
        
        # --- Pre-calculation Checks ---
        total_contribution = sum(d['contribution'] for d in st.session_state.friend_data)
        
        if abs(total_contribution - total_amount) > 0.01:
            st.error(f"⚠️ Input Error: Total contributions (${total_contribution:.2f}) do not match the Total Amount Spent (${total_amount:.2f}).")
            st.warning("Please adjust the contributions so they sum up to the total amount.")
            return

        if num_friends == 0 or total_amount == 0:
            st.warning("Please enter a valid Total Amount and Number of Friends (at least 2).")
            return
            
        # --- Core Calculation ---
        equal_share = total_amount / num_friends
        
        st.markdown("---")
        st.subheader("Results")
        st.info(f"The equal share per person is **${equal_share:,.2f}**")

        # Calculate net balance for each friend
        balances = []
        for d in st.session_state.friend_data:
            net_balance = d['contribution'] - equal_share
            balances.append(Friend(d['name'], net_balance))

        # --- Display Balances (Who owes/gets) ---
        st.markdown("#### Balance Overview")
        
        debtors_summary = []
        creditors_summary = []

        for friend in balances:
            if friend.balance < -0.01:
                debtors_summary.append(f"**{friend.name}** owes **${abs(friend.balance):,.2f}**")
            elif friend.balance > 0.01:
                creditors_summary.append(f"**{friend.name}** gets back **${friend.balance:,.2f}**")
            else:
                st.write(f"✅ **{friend.name}** is settled (paid exactly the equal share).")
        
        if debtors_summary:
            st.markdown("##### Debtors (Owe Money)")
            for item in debtors_summary:
                st.error(f"🔻 {item}")

        if creditors_summary:
            st.markdown("##### Creditors (Get Money Back)")
            for item in creditors_summary:
                st.success(f"🔺 {item}")

        # --- Settlement Plan ---
        st.markdown("---")
        st.subheader("Optimal Settlement Plan")
        
        transactions = calculate_settlements(balances)
        
        if not transactions:
            st.balloons()
            st.success("Everyone has already paid exactly their share! No transactions needed.")
            return
            
        # Group transactions by the payer (debtor) for the requested output format
        payer_groups = {}
        for payer, receiver, amount in transactions:
            if payer not in payer_groups:
                payer_groups[payer] = []
            payer_groups[payer].append((receiver, amount))

        for payer, payments in payer_groups.items():
            payment_details = []
            for receiver, amount in payments:
                payment_details.append(f"**${amount:,.2f}** to **{receiver}**")
            
            # Final output format: F1 -> owes -> 500 to F2 and 2500 to F3
            st.markdown(f"**{payer}** must pay: " + ", and ".join(payment_details) + ".")


if __name__ == "__main__":
    app()