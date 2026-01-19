from utils.file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)


def main():
    """
    Main execution function – PART 1 ONLY
    """

    print("=" * 40)
    print("SALES ANALYTICS SYSTEM")
    print("=" * 40)

    try:
        # [1/10] Read sales data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")

        if not raw_lines:
            print("✗ No data read. Exiting program.")
            return

        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # [2/10] Parse and clean data
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")

        if not transactions:
            print("✗ No valid records after parsing. Exiting program.")
            return

        # [3/10] Display filter options
        print("\n[3/10] Filter Options Available:")

        # First validation run (no filters) to show options
        _, _, summary_preview = validate_and_filter(transactions)

        # Ask user if filtering is required
        choice = input("\nDo you want to filter data? (y/n): ").strip().lower()

        region = None
        min_amount = None
        max_amount = None

        if choice == 'y':
            region_input = input("Enter region (or press Enter to skip): ").strip()
            region = region_input if region_input else None

            min_input = input("Enter minimum amount (or press Enter to skip): ").strip()
            min_amount = float(min_input) if min_input else None

            max_input = input("Enter maximum amount (or press Enter to skip): ").strip()
            max_amount = float(max_input) if max_input else None

        # [4/10] Validate and apply filters
        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(
            transactions,
            region=region,
            min_amount=min_amount,
            max_amount=max_amount
        )

        print(f"✓ Valid: {summary['final_count']} | Invalid: {summary['invalid']}")

        print("\nPart 1 completed successfully.")
        print("Data is cleaned, validated, and ready for analysis.")

    except Exception as e:
        print("\nAn unexpected error occurred.")
        print("Error details:", str(e))


if __name__ == "__main__":
    main()
