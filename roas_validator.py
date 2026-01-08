import pandas as pd

#Read WooCommerce CSV
website_df = pd.read_csv("csv_files/woocommerce_novdec2025.csv")

#Read Meta Ads CSV
meta_df = pd.read_csv("csv_files/meta_ads-novdec2025.csv")

#Print first 5 rows (check data loaded)
print(website_df.head())
print(meta_df.head())

# Rename WooCommerce columns
website_df = website_df.rename(columns={
    "Order Number": "order_id",
    "Order Date": "order_date",
    "Order Status": "order_status",
    "Order Total Amount": "order_total",
    "City (Shipping)": "city"
})

#Check renamed columns
print("COLUMNS AFTER RENAME:")
print(website_df.columns)


# Convert order_date to real dates
website_df["order_date"] = pd.to_datetime(website_df["order_date"])

#Convert order_total to numbers
website_df["order_total"] = pd.to_numeric(website_df["order_total"], errors="coerce")

#Print data types
print("\nDATA TYPES:")
print(website_df.dtypes)

# Keep only completed & processing orders
website_df = website_df[
    website_df["order_status"].isin(["Completed", "Processing"])
]

#Confirm which statuses remain
print("\nORDER STATUSES PRESENT:")
print(website_df["order_status"].value_counts())

##Confirm date range is really Nov–Dec 2025: Finds earliest and latest order date
print("\nDATE RANGE:")
print(website_df["order_date"].min(), website_df["order_date"].max())

website_revenue = website_df["order_total"].sum()

print("\nTRUE BACKEND REVENUE (Nov–Dec 2025):")
print(round(website_revenue, 2))

#Clean Meta columns
meta_df = meta_df.rename(columns={
    "Amount spent (ZAR)": "amount_spend",
    "Purchases conversion value": "meta_revenue",
    "Purchases": "purchases",
    "Purchase ROAS (return on ad spend)": "ROAS",
    "Unique outbound CTR (click-through rate)": "unique_CTR",
    "Adds to cart": "add_to_cart",
    "Checkouts initiated": "checkouts",
    "Website landing page views": "website_landing_page_views"
})

#Check renamed columns
print("COLUMNS AFTER RENAME:")
print(meta_df.columns)

##Convert amount_spend to numbers
meta_df["amount_spend"] = pd.to_numeric(meta_df["amount_spend"], errors="coerce")

##Convert meta_revenue to numbers
meta_df["meta_revenue"] = pd.to_numeric(meta_df["meta_revenue"], errors="coerce")

#Print data types
print("\nDATA TYPES:")
print(meta_df.dtypes)

# Total backend revenue
website_revenue = website_df["order_total"].sum()

# Total ad spend & Meta revenue
total_spend = meta_df["amount_spend"].sum()
meta_reported_revenue = meta_df["meta_revenue"].sum()

print("\nTOTALS (Nov–Dec 2025)")
print("Website revenue:", round(website_revenue, 2))
print("Total ad spend:", round(total_spend, 2))
print("Meta reported revenue:", round(meta_reported_revenue, 2))

#Calculate ROAS
website_roas = website_revenue / total_spend
meta_roas = meta_reported_revenue / total_spend
roas_difference = website_roas - meta_roas

#print results
print("\nROAS RESULTS")
print("Website ROAS:", round(website_roas, 2))
print("Meta ROAS:", round(meta_roas, 2))
print("ROAS difference:", round(roas_difference, 2))

#EXPORT A REPORT
final_report_df = pd.DataFrame([{
    "period": "Nov–Dec 2025",
    "website_revenue": round(website_revenue, 2),
    "meta_reported_revenue": round(meta_reported_revenue, 2),
    "total_ad_spend": round(total_spend, 2),
    "website_roas": round(website_roas, 2),
    "meta_roas": round(meta_roas, 2),
    "roas_difference": round(roas_difference, 2)
}])

final_report_df.to_csv(
    "roas_summary_for_report.csv",
    index=False
)

print("\nROAS report created")
