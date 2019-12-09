from test import get_products_dict as tt
import timeit




def func():
    products = [
        {
            "source": "greedy",
            "name": "A",
            "net_price": 10
        },
        {
            "source": "greedy",
            "name": "B",
            "net_price": 4
        },
        {
            "source": "greedy",
            "name": "A",
            "net_price": 15
        }
    ]

    products_dict = {
        "A": {
            "products": [],
            "price": 25
        },
        "B": {
            "products": [],
            "price": 4
        }
    }


    res = tt(products)
    # res = tt(products)
    print(res)

# elapsed_time = timeit.timeit(func, number=100)/100
# print(elapsed_time)
func()