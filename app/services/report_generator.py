import pandas as pd
from datetime import date
from models.report import Report, Commission


"""
Loads all tables to the memory. Pandas should be changed to PySpark if the data grows.
"""
class ReportGenerator:
    
    def __init__(self):
        tables = ["commissions", "order_lines", "orders", "product_promotions", 
                  "products", "promotions"]
        self.tables = {}
        for table in tables:
            self.tables[table] = pd.read_csv(f"./data/{table}.csv")
    """
    Generates a report for given date.
    """
    def generate(self, report_date: date) -> Report:     
        # prepare and join orders with orders_with_lines
        orders_df = self.tables["orders"]
        orders_df["date"] = pd.to_datetime(orders_df['created_at']).dt.date
        orders_df["order_id"] = orders_df["id"]
        orders_df = orders_df.loc[orders_df["date"] == report_date]
        
        if len(orders_df["order_id"]) == 0:
            return Report()
        
        orders_with_lines_df = pd.merge(orders_df, self.tables["order_lines"], on="order_id", how='left')
   
        # prepare commissions and join commissions with orders_with_lines
        commissions_df = self.tables["commissions"]
        commissions_df["date"] = pd.to_datetime(commissions_df['date']).dt.date
        order_lines_comm_df = pd.merge(orders_with_lines_df, commissions_df, on=["date", "vendor_id"], how='left')
        order_lines_comm_df["profit"] = order_lines_comm_df["rate"] * order_lines_comm_df["total_amount"]

        # prepare product promotions   
        product_proms_df = self.tables["product_promotions"]
        product_proms_df["date"] = pd.to_datetime(product_proms_df['date']).dt.date

        # join product promotions with order lines 
        joined = pd.merge(order_lines_comm_df, product_proms_df, on=["product_id", "date"], how='left')
        joined = joined[["promotion_id", "profit"]]

        # calculate statistics
        total_number_of_items = orders_with_lines_df["quantity"].sum()
        number_of_customers = len(orders_df["customer_id"].unique())
        total_discounted = orders_with_lines_df["discounted_amount"].sum()
        avg_discount_rate = orders_with_lines_df["discount_rate"].mean()
        avg_order_total = orders_with_lines_df["total_amount"].mean()
        total_commission = order_lines_comm_df["profit"].sum()
        comm_per_order_df = order_lines_comm_df[["order_id", "profit"]].groupby("order_id").mean()
        avg_commission_per_order = comm_per_order_df["profit"].mean()

        comms_per_day = joined.loc[joined["promotion_id"].notnull()].groupby("promotion_id").sum().to_dict()

        comm = Commission(
            total=total_commission,
            order_avg=avg_commission_per_order,
            promotions=comms_per_day["profit"]
            )
        
        return Report(
            customers=number_of_customers,
            total_discount_amount=total_discounted,
            items=total_number_of_items,
            discount_rate_avg=avg_discount_rate,
            order_total_avg=avg_order_total,
            commissions=comm
            )
    
# make ReportGenerator singleton to read the data only once from disc
report_gen = ReportGenerator()