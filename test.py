def order_pizza(size, *toppings):
    print(f"Ordered a {size} pizza!")
    if toppings:
        print("It has toppings")
    else:
        print("No toppings added")

order_pizza("large")
