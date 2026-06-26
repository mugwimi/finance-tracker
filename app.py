import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

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

        required_cols = ['date', 'category', 'amount']
        if not all(col in df.columns for col in required_cols):
            st.error(f"CSV must contain columns: {', '.join(required_cols)}")
        else:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')

            # Sidebar filters
            st.sidebar.header("Filters")

            # Date range filter
            min_date = df['date'].min().date()
            max_date = df['date'].max().date()
            start_date = st.sidebar.date_input("Start date", min_date, min_value=min_date, max_value=max_date)
            end_date = st.sidebar.date_input("End date", max_date, min_value=min_date, max_value=max_date)

            # Category filter
            categories = st.sidebar.multiselect(
                "Filter categories",
                options=df['category'].unique(),
                default=df['category'].unique()
            )

            # Apply filters
            mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date) & (df['category'].isin(categories))
            filtered_df = df[mask]

            if filtered_df.empty:
                st.warning("No transactions found for selected filters.")
            else:
                # Budget tracker
                st.sidebar.header("Budget")
                budget = st.sidebar.number_input("Monthly budget ($)", min_value=0, value=1000, step=50)
                spent = filtered_df['amount'].sum()
                remaining = budget - spent
                pct_used = min(spent / budget * 100, 100) if budget > 0 else 0

                st.sidebar.metric("Spent", f"${spent:,.2f}")
                st.sidebar.metric("Remaining", f"${remaining:,.2f}")
                st.sidebar.progress(pct_used / 100)
                st.sidebar.write(f"{pct_used:.1f}% of budget used")

                # Main area
                st.subheader("Filtered Transactions")
                st.dataframe(filtered_df, use_container_width=True)

                # Download button
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download filtered CSV",
                    data=csv,
                    file_name=f"expenses_{start_date}_to_{end_date}.csv",
                    mime="text/csv"
                )

                # Metrics row
                col1, col2, col3, col4 = st.columns(4)
                total = filtered_df['amount'].sum()
                avg_transaction = filtered_df['amount'].mean()
                num_transactions = len(filtered_df)
                top_category = filtered_df.groupby('category')['amount'].sum().idxmax()

                col1.metric("Total Spent", f"${total:,.2f}")
                col2.metric("Avg Transaction", f"${avg_transaction:,.2f}")
                col3.metric("Transactions", num_transactions)
                col4.metric("Top Category", top_category)

                # Charts
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Spending by Category")
                    category_totals = filtered_df.groupby('category')['amount'].sum()
                    fig, ax = plt.subplots()
                    ax.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%')
                    ax.axis('equal')
                    st.pyplot(fig)

                with col2:
                    st.subheader("Spending Over Time")
                    daily_spending = filtered_df.groupby('date')['amount'].sum()
                    st.line_chart(daily_spending)

                # Category breakdown table
                st.subheader("Category Breakdown")
                breakdown = filtered_df.groupby('category')['amount'].agg(['sum', 'count']).sort_values('sum', ascending=False)
                breakdown.columns = ['Total Spent', 'Transactions']
                breakdown['Total Spent'] = breakdown['Total Spent'].apply(lambda x: f"${x:,.2f}")
                st.dataframe(breakdown, use_container_width=True)

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("👆 Upload a CSV file to get started")
    st.markdown("**Sample CSV format:**")
    st.code("date,category,amount\n2024-01-15,Groceries,54.20\n2024-01-16,Transport,15.50\n2024-01-17,Entertainment,25.00", language="csv")
    st.markdown("Save this as `expenses.csv` and upload it to test.")