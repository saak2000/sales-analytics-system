from datetime import datetime
from collections import defaultdict

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report
    """

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_records = len(transactions)

    total_revenue = calculate_total_revenue(transactions)
    avg_order_value = total_revenue / total_records if total_records else 0

    dates = sorted(tx['Date'] for tx in transactions)
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    region_data = region_wise_sales(transactions)
    top_products = top_selling_products(transactions, 5)
    customers = customer_analysis(transactions)
    daily_trend = daily_sales_trend(transactions)
    peak_day = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    enriched_success = [tx for tx in enriched_transactions if tx.get('API_Match')]
    enriched_failed = [tx['ProductName'] for tx in enriched_transactions if not tx.get('API_Match')]
    enrichment_rate = (len(enriched_success) / len(enriched_transactions) * 100) if enriched_transactions else 0

    with open(output_file, 'w', encoding='utf-8') as f:

        # 1. HEADER
        f.write("=" * 50 + "\n")
        f.write("           SALES ANALYTICS REPORT\n")
        f.write(f"         Generated: {now}\n")
        f.write(f"         Records Processed: {total_records}\n")
        f.write("=" * 50 + "\n\n")

        # 2. OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_records}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        # 3. REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Region':<10}{'Sales':<15}{'% of Total':<15}{'Transactions'}\n")

        for region, data in region_data.items():
            f.write(
                f"{region:<10}₹{data['total_sales']:,.0f}     "
                f"{data['percentage']:>6}%         "
                f"{data['transaction_count']}\n"
            )
        f.write("\n")

        # 4. TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Rank':<6}{'Product':<25}{'Qty':<10}{'Revenue'}\n")

        for i, (prod, qty, rev) in enumerate(top_products, 1):
            f.write(f"{i:<6}{prod:<25}{qty:<10}₹{rev:,.0f}\n")
        f.write("\n")

        # 5. TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Rank':<6}{'Customer':<15}{'Spent':<15}{'Orders'}\n")

        for i, (cust, data) in enumerate(list(customers.items())[:5], 1):
            f.write(
                f"{i:<6}{cust:<15}₹{data['total_spent']:,.0f}     "
                f"{data['purchase_count']}\n"
            )
        f.write("\n")

        # 6. DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Date':<12}{'Revenue':<15}{'Txns':<10}{'Customers'}\n")

        for date, data in daily_trend.items():
            f.write(
                f"{date:<12}₹{data['revenue']:,.0f}     "
                f"{data['transaction_count']:<10}"
                f"{data['unique_customers']}\n"
            )
        f.write("\n")

        # 7. PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 50 + "\n")
        f.write(f"Best Selling Day: {peak_day[0]} (₹{peak_day[1]:,.0f}, {peak_day[2]} transactions)\n\n")

        if low_products:
            f.write("Low Performing Products:\n")
            for prod, qty, rev in low_products:
                f.write(f"- {prod}: {qty} units, ₹{rev:,.0f}\n")
        else:
            f.write("No low performing products identified.\n")
        f.write("\n")

        # 8. API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Transactions:     {len(enriched_transactions)}\n")
        f.write(f"Successfully Enriched:  {len(enriched_success)}\n")
        f.write(f"Success Rate:           {enrichment_rate:.2f}%\n\n")

        if enriched_failed:
            f.write("Products Not Enriched:\n")
            for prod in sorted(set(enriched_failed)):
                f.write(f"- {prod}\n")

    print(f"✓ Sales report generated: {output_file}")
