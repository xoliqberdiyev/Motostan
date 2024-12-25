import requests

r = requests.get('https://dicloud.uz:38871/hayat_moto/hs/products1/get_products',auth=('Administrator','Odilsoft!'))

def get_product_data():
    if r.status_code == 200:
        raw_text = r.text.strip().split(';')  # Split by semicolon to separate products
        products = []

        for line in raw_text:
            if line.strip():
                product = {}
                for item in line.split(', '):
                    if ': ' in item:
                        key, value = item.split(': ', 1)
                        product[key.strip()] = value.strip()
                products.append(product)
        return products
