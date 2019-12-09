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
    try:
        if products and products[0].get('source') == 'greedy':
            product_list = generate_pd_list(products, True)
        else:
            product_objs = list(Product.objects.using('slave').in_bulk([p['product_id'] for p in products]).values())
            bundled_products = []
            for product in product_objs:
                for bundled_product in product.bundled.all():
                    bundled_product.price = 0
                    bundled_products.append(bundled_product)
            product_objs.extend(bundled_products)
            product_list = generate_pd_list(product_objs, False)
    except (ValueError, KeyError, AttributeError):
        product_list = list({'title': p['name'], 'body': {'expire_in': None, 'never_expire': None}} for p in products)

    return product_list


"""
This function generates the products list.
products - product list to be iterated
flag - boolean used to identify from where this function is called ( from if or else part in the main function )
"""
def generate_pd_list(products, flag):
    product_list = []
    all_keys = []
    lang = get_language()[:2]
    for product in products:

        # initialize values
        if flag:
            key = product['name']
            price = product['net_price']
            name = key
        else:
            key = getattr(product.parent, 'name_%s' % lang)
            price = product.price
            name = product.name

        if key in all_keys:
            # get the product already added to the output product list
            product_info = product_list[all_keys.index(key)]
            # update its values
            product_info['body']['price'] += price
            product_info['body']['products'].append(mark_safe(name))
        else:
            # add new key to all_keys and the output product list
            all_keys.append(key)
            product_list.append({'title': key, 'body': {'products': [key],
                                                        'price': price}})
            # if the function is called from the else part of the main function
            if not flag:
                product_list[-1]['body']['expire_in'] = product.expire_in
                product_list[-1]['body']['never_expire'] = product.never_expire
    return product_list

