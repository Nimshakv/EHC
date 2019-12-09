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
    product_list=[]
    till_now=[]
    try:
        if products and products[0].get('source')=='greedy':
            till_now=[]
            for product in products:
                key=product['name']
                if key in till_now:
                    temp=product_list[till_now.index(key)]
                    temp['body']['price']=temp['body']['price']+product['net_price']
                    temp['body']['products'].append(key)
                else:
                    till_now.append(key)
                    product_list.append({'title':key,'body':{'products':[key],'price':product['net_price']}})
        else:
            product_objs = list(Product.objects.using('slave').in_bulk([p['product_id'] for p in products]).values())
            bundled_products = []
            for product in product_objs:
                for bundled_product in product.bundled.all():
                    bundled_product.price = 0
                    bundled_products.append(bundled_product)
            product_objs.extend(bundled_products)
            till_now=[]
            for product in product_objs:
                key = getattr(product.parent, 'name_%s' % lang)
                if key in till_now:
                    temp=product_list[till_now.index(key)]
                    temp['body']['price']=temp['body']['price']+product.price
                    temp['body']['products'].append(product.name)
                else:
                    till_now.append(key)
                    product_list.append({'title':key,'body':{'expire_in': product.expire_in,'never_expire':product.never_expire,'products':[product.name],'price':product.price}})
    except (ValueError, KeyError, AttributeError):
        pass
    return product_list
print(get_products_dict([{'source':'greedy','name':'mobile','net_price':4000},{'source':'greedy','name':'mobile','net_price':40000}]))
