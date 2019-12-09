l = [
    {
        'a': 1,
        'b': 10
    },
    {
        'a': 2,
        'b': 20
    },
    {
        'a': 3,
        'b': 30
    }
]

m = [
    {
        'a': 1,
        'b': 2
    },
    {
        'a': 2,
        'b': 3
    },
    {
        'a': 3,
        'b': 4
    }
]

n = [l, m]

# bund = [i.__setitem__('b', 0) for i in l]

bundled_products = []
    # all_bundle = product.bundled.all()
# for i in n:
#     [bundled_product.__setitem__('b', 0) for bundled_product in i]
#     bundled_products.extend(i)

for i in n:
    for j in i:
        j['b'] = 0
        bundled_products.append(j)

print(bundled_products)

n.extend(bundled_products)

print(n)


# all_bundle = product.bundled.all()
                # [bundled_product.__setitem__('price', 0) for bundled_product in all_bundle]
                # bundled_products.extend(all_bundle)