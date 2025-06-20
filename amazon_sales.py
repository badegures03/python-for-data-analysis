import pandas as pd
sales_data = pd.read_excel("C:/Users/HP/Downloads/sales_data.xlsx")

#Exploring the data
sales_data.info()
sales_data.describe()
print(sales_data.columns)
print(sales_data.head())

print(sales_data.isnull().sum())
data_cleaned = sales_data.dropna(subset=["Amount"])
print(data_cleaned.isnull().sum())

#How many sales with amounts more than 1000
more_than_1000 = sales_data[sales_data["Amount"] > 1000]
print(len(more_than_1000))

#How many sales that belong to the Category "Top" and Quantity 3
top_category = sales_data[(sales_data["Category"] == "Top") & (sales_data["Qty"] == 3)]
print(len(top_category))

#Total sales by category
total_sales = sales_data.groupby("Category", as_index=False)["Amount"].sum()
total_sales = total_sales.sort_values("Amount", ascending=False)

#Avg amount by category and status
averages = sales_data.groupby(["Category", "Status"], as_index=False)["Amount"].mean()
averages = averages.sort_values("Amount", ascending=False)

#Total sales by fulfillment and shipment type
shipment_type = sales_data.groupby(["Courier Status", "Fulfilment"], as_index=False)["Amount"].sum()
shipment_type = shipment_type.sort_values("Amount", ascending=False)
shipment_type.rename(columns={"Courier Status": "Shipment"}, inplace=True)
print(shipment_type)

#Export specific data (shipment_type)
shipment_type.to_excel(r"C:\Users\HP\Downloads\shipment_type.xlsx", index=False)
