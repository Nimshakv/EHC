
"""
Assumptions:
We use Django ORM
get_language() method returns the locale string
products is a list of dictionaries
"""


def get_products_dict(products):
    """
    Returns products dict with bundled products included to be used in
    email templates.
    NOTE: DO NOT SAVE PRODUCT IN THIS METHOD, AS, WE ARE CHANGING PRICE OF
    BUNDLED PRODUCTS TO 0
    """
    # lang = get_language()[:2]
    lang = ''
    products_dict = {}
    try:
        if products and products[0].get('source') == 'greedy':
            for product in products:
                key = product['name']
                products_dict[key] = products_dict.get(key, {})
                products_dict[key].setdefault('products', []).append(key)
                products_dict[key]['price'] = products_dict[key].get('price', 0) + product['net_price']
        else:
            product_objs = list(Product.objects.using('slave').in_bulk([p['product_id'] for p in products]).values())
            bundled_products = []
            for product in product_objs:
                for bundled_product in product.bundled.all():
                    bundled_product.price = 0
                    bundled_products.append(bundled_product)
            product_objs.extend(bundled_products)
            for product in product_objs:
                key = getattr(product.parent, 'name_%s' % lang)
                products_dict[key] = products_dict.get(key, {
                                                        'expire_in': product.expire_in,
                                                        'never_expire': product.never_expire
                                                        })
                products_dict[key].setdefault('products', []).append(mark_safe(product.name))
                products_dict[key]['price'] = products_dict[key].get('price', 0) + product.price
        # Convert it to a format which is easy to handle in email templates
        products_dict = [{
                            'title': key,
                            'body': value,
                            } for key, value in products_dict.items()]
    except (ValueError, KeyError, AttributeError):
        products_dict = list({'title': p['name'], 'body': {'expire_in': None, 'never_expire': None}} for p in products)

    return products_dict
