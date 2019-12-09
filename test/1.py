def get_products_dict(products):
    product_list=[]
    till_now=[]
    if products and products[0].get('source')=='greedy':
        for product in products:
            key=product['name']
            if key in till_now:
                temp=product_list[till_now.index(key)]
                temp['body']['price']=temp['body']['price']+product['net_price']
                temp['body']['products'].append(key)
            else:
                till_now.append(key)
                product_list.append({'title':key,'body':{'products':[key],'price':product['net_price']}})
    return product_list

print(get_products_dict([{'source':'greedy','name':'mobile','net_price':4000},{'source':'greedy','name':'laptop','net_price':40000},{'source':'greedy','name':'mobile','net_price':8000},{'source':'greedy','name':'laptop','net_price':50000} ]))

