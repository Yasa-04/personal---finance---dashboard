import pandas as pd

df = pd.read_csv('../data/raw/personal_finance_2024.csv')
df = df.drop(columns=['Unnamed: 8'])
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year
print(df.head())
print(df.columns)

print(df.dtypes)
print(df.isnull().sum())

df.to_csv('../data/processed/personal_finance_cleaned.csv', index=False)
print("Cleaned data saved successfully!")