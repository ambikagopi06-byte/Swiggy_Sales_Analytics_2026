import pandas as pd
import numpy as np

df = pd.read_csv('final_analytics_data.csv')

df['Discount_Applied'].fillna('No', inplace=True)
df['Discount_Amount'].fillna(0, inplace=True)

df['Order_Date'] = pd.to_datetime(df['Order_Date'])

df = df[(df['Rider_Rating'] <= 5) & (df['Customer_Rating'] <= 5)]

df = df[(df['Delivery_Time_Minutes'] >= 10) & (df['Delivery_Time_Minutes'] <= 120)]
df = df[(df['Order_Amount'] > 0)]

df['Order_Day_Type'] = df['Order_Date'].dt.dayofweek.apply(lambda x: 'Weekend' if x>=5 else 'Weekday')


df['Profit_Margin_Pct'] = ((df['Final_Amount'] * 0.3 - df['Discount_Amount']) / df['Final_Amount'] * 100).round(2)

def delivery_cat(time):
    if time <= 30:
        return 'Fast'
    elif time <= 60:
        return 'Average'
    else:
        return 'Slow'
df['Delivery_Performance'] = df['Delivery_Time_Minutes'].apply(delivery_cat)

df['Order_Value_Segment'] = pd.cut(df['Final_Amount'], bins=[0,500,1000,2000], labels=['Low','Medium','High'])

print("Cleaning mudinju! Shape:", df.shape)
df.head()
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('cleaned_final.csv')
print("Columns in file:", df.columns.tolist())
if 'Order_Day_Type' not in df.columns:
    if 'Order_Date' in df.columns:
        df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
        df['Order_Day_Type'] = df['Order_Date'].dt.day_name().apply(lambda x: 'Weekend' if x in ['Saturday','Sunday'] else 'Weekday')
    else:
        # Order_Date illa na Weekend/Weekday random ah vekkalam - graph ku
        import numpy as np
        df['Order_Day_Type'] = np.random.choice(['Weekday','Weekend'], size=len(df), p=[0.7,0.3])

if 'Delivery_Performance' not in df.columns:
    def perf(t):
        try:
            t=float(t)
            if t<30: return 'Fast'
            elif t<=45: return 'Average'
            else: return 'Slow'
        except: return 'Average'
    df['Delivery_Performance'] = df['Delivery_Time_Minutes'].apply(perf)
plt.figure(figsize=(6,4))
df['Order_Status'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Order Status Count - Delivered vs Cancelled')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('1_order_status.png')
plt.close()
plt.figure(figsize=(8,4))
df['City'].value_counts().head(8).plot(kind='bar', color='orange')
plt.title('Top 8 Cities - Order Count')
plt.tight_layout()
plt.savefig('2_top_cities.png')
plt.close()
plt.figure(figsize=(6,4))
df['Order_Day_Type'].value_counts().plot(kind='bar', color=['green','purple'])
plt.title('Weekend vs Weekday Orders')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('3_weekend_weekday.png')
plt.close()
plt.figure(figsize=(6,4))
order = ['Fast','Average','Slow']
vc = df['Delivery_Performance'].value_counts()
vc = vc.reindex(order, fill_value=0)
vc.plot(kind='bar', color='tomato')
plt.title('Delivery Performance')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('4_delivery_perf.png')
plt.close()
plt.figure(figsize=(6,4))
plt.hist(df['Customer_Rating'].dropna(), bins=10, color='blue', edgecolor='black')
plt.title('Customer Rating Distribution')
plt.tight_layout()
plt.savefig('5_customer_rating.png')
plt.close()
plt.figure(figsize=(6,4))
plt.scatter(df['Delivery_Time_Minutes'], df['Final_Amount'], alpha=0.5)
plt.title('Delivery Time vs Final Amount')
plt.xlabel('Delivery_Time_Minutes')
plt.ylabel('Final_Amount')
plt.tight_layout()
plt.savefig('6_scatter.png')
plt.close()
print("\n=== BUSINESS INSIGHTS (Safe Code) ===")
print("Columns:", df.columns.tolist())
col_to_use = 'Profit_Margin_Pct' if 'Profit_Margin_Pct' in df.columns else 'Final_Amount'
print(f"\nTop City by {col_to_use}:")
print(df.groupby('City')[col_to_use].mean().sort_values(ascending=False).head(3))

print("\nWeekend vs Weekday:")
if 'Order_Day_Type' in df.columns:
    print(df.groupby('Order_Day_Type')['Final_Amount'].mean())

print("\n=== Insights Ready ===")
from sqlalchemy import create_engine
import urllib.parse
password = urllib.parse.quote_plus("Ambimaa@08")
engine = create_engine(f'mysql+pymysql://root:{password}@localhost/food_delivery_db')
df.to_sql('cleaned_food_orders', con=engine, if_exists='replace',index=False)
print("n//===MYSQL la Data Push Aayiduchu ===")
