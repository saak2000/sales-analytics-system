#Task 2.1(a): Calculate Total Revenue
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    """
    total_revenue = 0.0

    for tx in transactions:
        total_revenue += tx['Quantity'] * tx['UnitPrice']

    return total_revenue


#Task 2.1(b): Region-wise Sales Analysis
def region_wise_sales(transactions):
    """
    Analyzes sales by region
    """
    region_data = {}
    total_revenue = calculate_total_revenue(transactions)

    # Aggregate sales & count
    for tx in transactions:
        region = tx['Region']
        amount = tx['Quantity'] * tx['UnitPrice']

        if region not in region_data:
            region_data[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }

        region_data[region]['total_sales'] += amount
        region_data[region]['transaction_count'] += 1

    # Calculate percentage
    for region in region_data:
        region_data[region]['percentage'] = round(
            (region_data[region]['total_sales'] / total_revenue) * 100, 2
        )

    # Sort by total_sales descending
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]['total_sales'],
            reverse=True
        )
    )

    return sorted_regions


#Task 2.1(c): Top Selling Products
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    """
    product_data = {}

    for tx in transactions:
        product = tx['ProductName']
        qty = tx['Quantity']
        revenue = tx['Quantity'] * tx['UnitPrice']

        if product not in product_data:
            product_data[product] = {
                'quantity': 0,
                'revenue': 0.0
            }

        product_data[product]['quantity'] += qty
        product_data[product]['revenue'] += revenue

    # Convert to list of tuples
    product_list = [
        (product, data['quantity'], data['revenue'])
        for product, data in product_data.items()
    ]

    # Sort by quantity descending
    product_list.sort(key=lambda x: x[1], reverse=True)

    return product_list[:n]


#Task 2.1(d): Customer Purchase Analysis
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    """
    customer_data = {}

    for tx in transactions:
        customer = tx['CustomerID']
        amount = tx['Quantity'] * tx['UnitPrice']
        product = tx['ProductName']

        if customer not in customer_data:
            customer_data[customer] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }

        customer_data[customer]['total_spent'] += amount
        customer_data[customer]['purchase_count'] += 1
        customer_data[customer]['products_bought'].add(product)

    # Final calculations
    for customer in customer_data:
        total = customer_data[customer]['total_spent']
        count = customer_data[customer]['purchase_count']

        customer_data[customer]['avg_order_value'] = round(total / count, 2)
        customer_data[customer]['products_bought'] = list(
            customer_data[customer]['products_bought']
        )

    # Sort by total_spent descending
    sorted_customers = dict(
        sorted(
            customer_data.items(),
            key=lambda x: x[1]['total_spent'],
            reverse=True
        )
    )

    return sorted_customers


#Task 2.2: Date-based Analysis 
# (a) Daily Sales Trend

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    """
    daily_data = {}

    for tx in transactions:
        date = tx['Date']
        amount = tx['Quantity'] * tx['UnitPrice']
        customer = tx['CustomerID']

        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': set()
            }

        daily_data[date]['revenue'] += amount
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['unique_customers'].add(customer)

    # Convert set to count
    for date in daily_data:
        daily_data[date]['unique_customers'] = len(
            daily_data[date]['unique_customers']
        )

    # Sort by date
    return dict(sorted(daily_data.items()))


#(b) Find Peak Sales Day
def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    """
    daily_data = daily_sales_trend(transactions)

    peak_date = max(
        daily_data.items(),
        key=lambda x: x[1]['revenue']
    )

    date = peak_date[0]
    revenue = peak_date[1]['revenue']
    transaction_count = peak_date[1]['transaction_count']

    return date, revenue, transaction_count


#Task 2.3: Product Performance
#(a) Low Performing Products
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    """
    product_data = {}

    for tx in transactions:
        product = tx['ProductName']
        qty = tx['Quantity']
        revenue = tx['Quantity'] * tx['UnitPrice']

        if product not in product_data:
            product_data[product] = {
                'quantity': 0,
                'revenue': 0.0
            }

        product_data[product]['quantity'] += qty
        product_data[product]['revenue'] += revenue

    low_products = [
        (product, data['quantity'], data['revenue'])
        for product, data in product_data.items()
        if data['quantity'] < threshold
    ]

    # Sort by quantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products
