import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Finance Tracker", layout="wide")
st.title("Personal Finance Tracker 💰")

uploaded_file = st.file_uploader("Upload your expenses CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    st.subheader("Your Data")
    st.dataframe(df)
    
    # Total spent
    total = df['amount'].sum()
    st.metric("Total Spent", f"${total:,.2f}")
    
    # Pie chart by category
    st.subheader("Spending by Category")
    category_totals = df.groupby('category')['amount'].sum()
    fig, ax = plt.subplots()
    ax.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%')
    st.pyplot(fig)
else:
    st.info("Upload a CSV with columns: date, category, amount")