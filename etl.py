import pandas as pd
from sqlalchemy import create_engine
import sys

# Database connection string
DB_URI = "postgresql://user:password@localhost:5432/ecommerce_db"

def extract_data(filepath):
    return pd.read_csv(filepath)

def transform_data(df):
    # 1. Filter out FAILED transactions
    df = df[df['status'] == 'COMPLETED'].copy()
    
    # 2. Clean names (Title Case to fix "John doe" vs "John Doe")
    df['user_name'] = df['user_name'].str.title()
    
    # 3. Standardize dates to YYYY-MM-DD
    df['purchase_date'] = pd.to_datetime(df['purchase_date']).dt.date
    
    # 4. Handle missing prices (Fill with 0 or drop)
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
    
    return df

def load_data(df, engine):
    # Load dim_customers
    customers = df[['user_id', 'user_name']].drop_duplicates()
    customers.to_sql('dim_customers', engine, if_exists='append', index=False)

    # Load dim_products
    products = df[['item_id', 'item_name', 'price']].drop_duplicates(subset=['item_id'])
    products.to_sql('dim_products', engine, if_exists='append', index=False)

    # Load fact_transactions
    facts = df[['log_id', 'user_id', 'item_id', 'purchase_date', 'price']]
    facts = facts.rename(columns={'log_id': 'transaction_id', 'price': 'revenue'})
    facts.to_sql('fact_transactions', engine, if_exists='append', index=False)

if __name__ == "__main__":
    engine = create_engine(DB_URI)
    print("Extracting...")
    raw_df = extract_data('data/raw_logs.csv')
    print("Transforming...")
    clean_df = transform_data(raw_df)
    print("Loading...")
    load_data(clean_df, engine)
    print("ETL Complete.")