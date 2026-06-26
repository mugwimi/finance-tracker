$readme = @'
# Personal Finance Tracker 💰

A Streamlit web app to visualize and analyze personal spending from CSV files. Upload your expenses, filter by date/category, track budgets, and export filtered data.

**Live Demo:** https://mugwimi-finance-tracker.streamlit.app/

### **Features**
- 📊 **Visual Analytics** - Pie chart for category breakdown, line chart for spending over time
- 🔍 **Smart Filters** - Filter by date range and categories in sidebar
- 🎯 **Budget Tracking** - Set monthly budget with live progress bar and remaining amount
- 📥 **Export Data** - Download filtered transactions as CSV
- 📈 **Key Metrics** - Total spent, avg transaction, transaction count, top category
- 📋 **Category Breakdown** - Table view of totals and counts per category

### **Quick Start**

**Run locally:**
```bash
git clone https://github.com/mugwimi/finance-tracker.git
cd finance-tracker
pip install -r requirements.txt
streamlit run app.py