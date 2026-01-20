from utils.file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

import os


def main():
    """
    Main execution function
    """
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # -------------------------------------------------
        # [1/10] Read sales data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")

        if not raw_lines:
            print("✗ No data read. Exiting program.")
            return

        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # -------------------------------------------------
        # [2/10] Parse and clean data
        print("\n[2/10] Parsing and cleaning data...")
        parsed_transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed_transactions)} records")

        if not parsed_transactions:
            print("✗ No valid records after parsing. Exiting program.")
            return

        # -------------------------------------------------
        # [3/10] Filter options
        print("\n[3/10] Filter Options Available:")
        _, _, preview_summary = validate_and_filter(parsed_transactions)

        regions = preview_summary.get('regions', [])
        amount_min = preview_summary.get('amount_min')
        amount_max = preview_summary.get('amount_max')

        print("Regions:", ", ".join(regions))
        print(f"Amount Range: ₹{int(amount_min)} - ₹{int(amount_max)}")

        choice = input("\nDo you want to filter data? (y/n): ").strip().lower()

        region_filter = None
        min_amount = None
        max_amount = None

        if choice == 'y':
            region_input = input("Enter region (or press Enter to skip): ").strip()
            if region_input and region_input not in regions:
                print(f"⚠ Invalid region '{region_input}'. No region filter applied.")
            else:
                region_filter = region_input if region_input else None

            min_input = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_input = input("Enter maximum amount (or press Enter to skip): ").strip()

            min_amount = float(min_input) if min_input else None
            max_amount = float(max_input) if max_input else None

        # -------------------------------------------------
        # [4/10] Validate & filter
        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(
            parsed_transactions,
            region=region_filter,
            min_amount=min_amount,
            max_amount=max_amount
        )

        print(f"✓ Valid: {summary['final_count']} | Invalid: {summary['invalid']}")

        if not valid_transactions:
            print("✗ No valid transactions available for analysis.")
            print("✗ Please adjust filter criteria and try again.")
            return

        # -------------------------------------------------
        # [5/10] Part 2 – Analysis
        print("\n[5/10] Analyzing sales data...")

        total_revenue = calculate_total_revenue(valid_transactions)
        region_analysis = region_wise_sales(valid_transactions)
        top_products = top_selling_products(valid_transactions)
        customers = customer_analysis(valid_transactions)
        daily_trend = daily_sales_trend(valid_transactions)
        peak_day = find_peak_sales_day(valid_transactions)
        low_products = low_performing_products(valid_transactions)

        print("✓ Analysis complete")

        # -------------------------------------------------
        # [6/10] Part 3 – Fetch API products
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()

        if not api_products:
            print("✗ API data unavailable. Continuing without enrichment.")
            return

        print(f"✓ Fetched {len(api_products)} products")

        product_mapping = create_product_mapping(api_products)

        # -------------------------------------------------
        # [7/10] Enrich sales data
        print("\n[7/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)

        matched_count = sum(1 for tx in enriched_transactions if tx.get('API_Match'))
        percentage = (matched_count / len(enriched_transactions)) * 100

        print(f"✓ Enriched {matched_count}/{len(enriched_transactions)} transactions "
              f"({percentage:.1f}%)")

        # -------------------------------------------------
        # [8/10] Save enriched data
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions)

        # -------------------------------------------------
        # [9/10] Generate report (Part 4 placeholder)
        print("\n[9/10] Generating report...")
        print("✓ (Report generation will be implemented in Part 4)")

        # -------------------------------------------------
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ An unexpected error occurred.")
        print("Error details:", str(e))


if __name__ == "__main__":
    main()
