#Task 1.1 Takes care of reading sales data from file handling encoding issues
def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues

    Returns: list of raw lines (strings)
    """

    encodings = ['utf-8', 'latin-1', 'cp1252']
    lines = []

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                raw_lines = file.readlines()

            # Skip header and remove empty lines
            for line in raw_lines[1:]:
                line = line.strip()
                if line:
                    lines.append(line)

            print(f"File read successfully using encoding: {encoding}")
            return lines

        except UnicodeDecodeError:
            continue

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    print("Error: Unable to read file with supported encodings.")
    return []

#Task 1.2 Parse and clean sales data
def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """

    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        tid, date, pid, pname, qty, price, cid, region = parts

        # Clean ProductName (remove commas)
        pname = pname.replace(',', '')

        try:
            # Clean numeric fields
            qty = int(qty.replace(',', ''))
            price = float(price.replace(',', ''))
        except ValueError:
            continue

        transaction = {
            'TransactionID': tid,
            'Date': date,
            'ProductID': pid,
            'ProductName': pname,
            'Quantity': qty,
            'UnitPrice': price,
            'CustomerID': cid,
            'Region': region
        }

        transactions.append(transaction)

    return transactions

#Task 1.3: Data Validation & Filtering
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """

    valid_transactions = []
    invalid_count = 0

    regions = set()
    amounts = []

    # Validation phase
    for tx in transactions:
        try:
            if (
                tx['Quantity'] <= 0 or
                tx['UnitPrice'] <= 0 or
                not tx['TransactionID'].startswith('T') or
                not tx['ProductID'].startswith('P') or
                not tx['CustomerID'].startswith('C') or
                not tx['Region']
            ):
                invalid_count += 1
                continue

            amount = tx['Quantity'] * tx['UnitPrice']
            tx['Amount'] = amount

            regions.add(tx['Region'])
            amounts.append(amount)
            valid_transactions.append(tx)

        except KeyError:
            invalid_count += 1

    # Display available filter options
    print("Available Regions:", regions)
    print(f"Transaction Amount Range: {min(amounts)} - {max(amounts)}")

    filtered = valid_transactions[:]
    filtered_by_region = 0
    filtered_by_amount = 0

    # Apply region filter
    if region:
        before = len(filtered)
        filtered = [tx for tx in filtered if tx['Region'] == region]
        filtered_by_region = before - len(filtered)
        print(f"After region filter ({region}): {len(filtered)} records")

    # Apply amount filters
    if min_amount is not None:
        before = len(filtered)
        filtered = [tx for tx in filtered if tx['Amount'] >= min_amount]
        filtered_by_amount += before - len(filtered)

    if max_amount is not None:
        before = len(filtered)
        filtered = [tx for tx in filtered if tx['Amount'] <= max_amount]
        filtered_by_amount += before - len(filtered)

    if min_amount is not None or max_amount is not None:
        print(f"After amount filter: {len(filtered)} records")

    summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(filtered)
    }

    return filtered, invalid_count, summary
