import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Loading the Data
orders_data = pd.read_excel("C:/Users/HP/Downloads/orders.xlsx")
payments_data = pd.read_excel("C:/Users/HP/Downloads/order_payment.xlsx")
customer_data = pd.read_excel("C:/Users/HP/Downloads/customers.xlsx")

#Describing the Data
orders_data.info()
payments_data.info()
customer_data.info()

#Checking for Null Values, Dropping or Filling Them with Values
payments_data = payments_data.dropna(subset="payment_value")
print(payments_data.isnull().sum())

orders_data = orders_data.fillna("N/A")
print(orders_data.isnull().sum())

customer_data = customer_data.fillna("N/A")
print(customer_data.isnull().sum())

#Dropping Duplicate Values
print(payments_data.duplicated().sum())
print(orders_data.duplicated().sum())
print(customer_data.duplicated().sum())

payments_data = payments_data.drop_duplicates()
orders_data = orders_data.drop_duplicates()

#Filtering the Data
invoiced_orders_data = orders_data[orders_data["order_status"] == "invoiced"]
invoiced_orders_data = invoiced_orders_data.reset_index(drop=True)

credit_card_payments = payments_data[
    (payments_data["payment_type"] == "credit_card") &
    (payments_data["payment_value"] > 1000)]

customer_data_state = customer_data[customer_data["customer_state"] == "SP"]

#Merging the Data
merged_data = pd.merge(orders_data, payments_data, on="order_id")
joined_data = pd.merge(merged_data, customer_data, on="customer_id")

#Data Visualization
joined_data["month_year"] = joined_data["order_purchase_timestamp"].dt.to_period("M")
joined_data["week_year"] = joined_data["order_purchase_timestamp"].dt.to_period("W")
joined_data["year"] = joined_data["order_purchase_timestamp"].dt.to_period("Y")

joined_data.to_excel("C:/Users/HP/Downloads/joined_data.xlsx", index=False)

grouped_data = joined_data.groupby("month_year")["payment_value"].sum()
grouped_data = grouped_data.reset_index()

grouped_data["month_year"] = grouped_data["month_year"].astype(str)

plt.plot(grouped_data["month_year"], grouped_data["payment_value"], color="red", marker="o")

#Editing the Plot
plt.xlabel("Month-Year")
plt.ylabel("Payment Values")
plt.title("Payment Value by Month and Year")
plt.ticklabel_format(useOffset=False, style="plain", axis="y")
plt.xticks(rotation=90, fontsize=8)
plt.yticks(fontsize=8)
plt.show()

#Creating a Scattered Plot

scattered_df = joined_data.groupby("customer_unique_id").agg({"payment_value": "sum", "payment_installments": "sum"})
plt.scatter(scattered_df["payment_value"], scattered_df["payment_installments"])
plt.xlabel("Payment Values", fontsize=8)
plt.ylabel("Payment Installments", fontsize=8)
plt.title("Payment Value vs Payment Installments")
plt.show()

#Using Seaborn for an Alternative Scattered Plot
sns.set_theme(style="darkgrid")
sns.scatterplot(data=scattered_df, x="payment_value", y="payment_installments")
plt.xlabel("Payment Values", fontsize=8)
plt.ylabel("Payment Installments", fontsize=8)
plt.title("Payment Value vs Payment Installments")
plt.show()

#Bar Chart
bar_chart_df = joined_data.groupby(["payment_type", "month_year"])["payment_value"].sum()
bar_chart_df = bar_chart_df.reset_index()

pivot_data = bar_chart_df.pivot(index="month_year", columns="payment_type", values="payment_value")
pivot_data.plot(kind="bar", stacked="True")
plt.ticklabel_format(useOffset=False, style="plain", axis="y")
plt.ylabel("Payment Value")
plt.xlabel("Month of Payment")
plt.title("Payment per Payment Type by Month")
plt.show()
