from calendar import Month

import pandas as pd
import sqlite3

from openpyxl.descriptors import ASCII

# Load the cleaned data
df = pd.read_csv('../data/processed/personal_finance_cleaned.csv')

# Create a connection to a SQLite database
conn = sqlite3.connect('../data/processed/finance.db')

# Load the dataframe into the database as a table called 'transactions'
df.to_sql('transactions', conn, if_exists='replace', index=False)

print("Data loaded into database successfully!")

# First query — Total Income vs Total Expenses
query1 = '''
SELECT 
    ROUND(SUM(CASE WHEN Type = 'income' THEN Amount ELSE 0 END), 2) AS total_income,
    ROUND(SUM(CASE WHEN Type != 'income' THEN Amount ELSE 0 END), 2) AS total_expenses,
    ROUND(SUM(Amount), 2) AS net_balance
FROM transactions
'''

result1 = pd.read_sql(query1, conn)
print("Income vs Expenses:")
print(result1)

# Spending by Category
query2 = '''
SELECT 
    Category,
    ROUND(SUM(Amount), 2) AS total_spent
FROM transactions
WHERE Type != 'income'
GROUP BY Category
ORDER BY total_spent ASC
'''

result2 = pd.read_sql(query2, conn)
print("\nSpending by Category:")
print(result2)

#Monthly Spending Trends
query3 = '''
SELECT 
      Month,
Round(Sum(CASE WHEN Type = 'income' THEN Amount ELSE 0 END), 2) AS monthly_income,
Round(Sum(CASE WHEN Type != 'income' THEN Amount ELSE 0 END), 2) AS monthly_expenses,
Round(SUM(Amount), 2) AS monthly_balance

FROM transactions

GROUP BY Month
ORDER BY Month ASC '''

Result3 = pd.read_sql(query3, conn)
print("\nMonthly Expenses")
print(Result3)

# Budget vs Actual Spending

query4 = '''
SELECT Category,
  ROUND(SUM(Budget), 2) AS total_budget,
  ROUND(SUM(Amount), 2) AS total_spent,
  ROUND(SUM(Amount)) - ROUND(SUM(Budget), 2) AS difference
FROM transactions
WHERE Type != 'income'
GROUP BY Category
ORDER BY difference ASC '''

result4 = pd.read_sql(query4, conn)
print("\nBudget vs Actual")
print(result4)

# "What were the 5 biggest single expenses in 2024?"
query5 = '''
 SELECT
      Date,
      Category,
      Subcategory,
      Description,
      Amount
 From transactions 
     WHERE Type != 'income'
     AND Category != 'Rent'
     AND Category != 'Savings'
     AND Category != 'Investments'
     ORDER BY Amount ASC 
     LIMIT 5 '''

result5 = pd.read_sql(query5, conn)
print("\nTop 5 Biggest Transactions")
print(result5)
