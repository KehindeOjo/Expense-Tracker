# 1. IMPORT LIBRARIES 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# 2. LOAD THE DATASET 
df = pd.read_csv('data/my_expenses.csv', parse_dates=['Date'])

# 3. CLEANING & BASIC PROCESSING
df['Amount'] = df['Amount'].abs()  # Ensure all amounts are positive
df['Type'] = df['Type'].str.capitalize()

# 4. SUMMARY METRICS 
total_income = df[df['Type'] == 'Income']['Amount'].sum()
total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
net_savings = total_income - total_expense

print(f"Total Income: ₦{total_income:,.2f}")
print(f"Total Expenses: ₦{total_expense:,.2f}")
print(f"Net Savings: ₦{net_savings:,.2f}")

# 5. EXPENSES BY CATEGORY 
category_expense = df[df['Type'] == 'Expense'].groupby('Category')['Amount'].sum().sort_values(ascending=False)

plt.figure(figsize=(8,5))
sns.barplot(x=category_expense.values, y=category_expense.index, palette='viridis')
plt.title('Expenses by Category')
plt.xlabel('Amount (₦)')
plt.ylabel('Category')
plt.tight_layout()
plt.savefig('plots/expenses_by_category.png')
plt.show()

# 6. INCOME VS EXPENSE OVER TIME
daily_summary = df.groupby(['Date', 'Type'])['Amount'].sum().unstack().fillna(0)

daily_summary.plot(title='Daily Income vs Expense', figsize=(10,5))
plt.ylabel('Amount (₦)')
plt.tight_layout()
plt.savefig('plots/income_vs_expense_trend.png')
plt.show()

# 7. CUMULATIVE SAVINGS
df['Net'] = df['Amount'].where(df['Type'] == 'Income', -df['Amount'])
df = df.sort_values('Date')
df['Cumulative_Savings'] = df['Net'].cumsum()

plt.figure(figsize=(10,5))
plt.plot(df['Date'], df['Cumulative_Savings'], color='green')
plt.title('Cumulative Savings Over Time')
plt.xlabel('Date')
plt.ylabel('Savings (₦)')
plt.tight_layout()
plt.savefig('plots/cumulative_savings.png')
plt.show()
