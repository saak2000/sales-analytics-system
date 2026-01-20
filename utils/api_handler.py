import requests
#3.1a) fetch all products from DummyJSON API

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        api_products = []

        for product in products:
            api_products.append({
                'id': product.get('id'),
                'title': product.get('title'),
                'category': product.get('category'),
                'brand': product.get('brand'),
                'price': product.get('price'),
                'rating': product.get('rating')
            })

        print(f"✓ Successfully fetched {len(api_products)} products from API")
        return api_products

    except requests.exceptions.RequestException as e:
        print("✗ Failed to fetch products from API")
        print("Error:", str(e))
        return []

#3.1b) create product mapping from API data
def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    """
    product_mapping = {}

    for product in api_products:
        product_id = product.get('id')

        if product_id is not None:
            product_mapping[product_id] = {
                'title': product.get('title'),
                'category': product.get('category'),
                'brand': product.get('brand'),
                'rating': product.get('rating')
            }

    return product_mapping

#3.2) Enrich sales data with API product info
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """
    enriched_transactions = []

    for tx in transactions:
        enriched_tx = tx.copy()

        try:
            # Extract numeric ID from ProductID (P101 -> 101)
            product_id_str = tx.get('ProductID', '')
            product_id = int(product_id_str.replace('P', ''))

            api_product = product_mapping.get(product_id)

            if api_product:
                enriched_tx['API_Category'] = api_product.get('category')
                enriched_tx['API_Brand'] = api_product.get('brand')
                enriched_tx['API_Rating'] = api_product.get('rating')
                enriched_tx['API_Match'] = True
            else:
                enriched_tx['API_Category'] = None
                enriched_tx['API_Brand'] = None
                enriched_tx['API_Rating'] = None
                enriched_tx['API_Match'] = False

        except Exception:
            enriched_tx['API_Category'] = None
            enriched_tx['API_Brand'] = None
            enriched_tx['API_Rating'] = None
            enriched_tx['API_Match'] = False

        enriched_transactions.append(enriched_tx)

    return enriched_transactions


# Save enriched data back to file
def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    """
    headers = [
        'TransactionID', 'Date', 'ProductID', 'ProductName',
        'Quantity', 'UnitPrice', 'CustomerID', 'Region',
        'API_Category', 'API_Brand', 'API_Rating', 'API_Match'
    ]

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('|'.join(headers) + '\n')

            for tx in enriched_transactions:
                row = []
                for h in headers:
                    value = tx.get(h)
                    row.append("" if value is None else str(value))
                file.write('|'.join(row) + '\n')

        print(f"✓ Enriched data saved to: {filename}")

    except Exception as e:
        print("✗ Failed to save enriched data")
        print("Error:", str(e))
