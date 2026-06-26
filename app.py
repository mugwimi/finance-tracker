import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Finance Tracker", 
    page_icon="💰",
    layout="wide"
)

st.title("Personal Finance Tracker 💰")
st.markdown("Upload your CSV to analyze spending by category")

uploaded_file = st.file_uploader(
    "Upload your expenses CSV", 
    type="csv",
    help="CSV must have columns: date, category, amount"
)

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        
        # Validate required columns
        required_cols = ['date', 'category', 'amount']
        if not all(col in df.columns for col in required_cols):
            st.error(f"CSV must contain columns: {', '.join(required_cols)}")
        else:
            # Convert date column
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # Show data
            st.subheader("Your Transactions")
            st.dataframe(df, use_container_width=True)
            
            # Metrics row
            col1, col2, col3 = st.columns(3)
            total = df['amount'].sum()
            avg_transaction = df['amount'].mean()
            num_transactions = len(df)
            
            col1.metric("Total Spent", f"${total:,.2f}")
            col2.metric("Avg Transaction", f"${avg_transaction:,.2f}")
            col3.metric("Transactions", num_transactions)
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Spending by Category")
                category_totals = df.groupby('category')['amount'].sum()
                fig, ax = plt.subplots()
                ax.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%')
                ax.axis('equal')
                st.pyplot(fig)
            
            with col2:
                st.subheader("Spending Over Time")
                daily_spending = df.groupby('date')['amount'].sum()
                st.line_chart(daily_spending)
                
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("👆 Upload a CSV file to get started")
    st.markdown("""
    **Sample CSV format:**