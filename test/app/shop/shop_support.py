from django.db.models import Sum

from .models import TeleVision, Phones, PersonalComputers


# Select model for database access.
def choose_model(category, get_brand, get_model):
    if category == "mobile":
        right_model = Phones.objects.all().filter(
            brand=get_brand, model=get_model)
    elif category == "pc":
        right_model = PersonalComputers.objects.all().filter(
            brand=get_brand, model=get_model)
    elif category == "tv":
        right_model = TeleVision.objects.all().filter(
            brand=get_brand, model=get_model)

    return right_model


# Initialize correct model to the update product parameters.
def init_model_to_update_product(category, get_id, form_brand, form_model,
                                 form_description, form_price, form_available):

    if category == "mobile":
        product_to_update = Phones(
            id=get_id,
            brand=form_brand,
            model=form_model,
            description=form_description,
            price=form_price,
            available=form_available)

    elif category == "pc":
        product_to_update = PersonalComputers(
            id=get_id,
            brand=form_brand,
            model=form_model,
            description=form_description,
            price=form_price,
            available=form_available)

    elif category == "tv":
        product_to_update = TeleVision(
            id=get_id,
            brand=form_brand,
            model=form_model,
            description=form_description,
            price=form_price,
            available=form_available)

    return product_to_update


# Create context for send to the 'editproduct' page.
def make_context_to_edit_product(product_info, category, username):
    for item in product_info:
        prod_brand = item.brand
        prod_model = item.model
        prod_description = item.description
        prod_price = item.price
        prod_available = item.available

    context = {
        "category": category,
        "username": username,
        "brand": prod_brand,
        "model": prod_model,
        "description": prod_description,
        "price": prod_price,
        "available": prod_available,
    }

    return context


# Adding product to the cart.
def added_processing(request, prod_id, prod_category):

    # Initialize cart (added info) inside session.
    if not request.session.get("user_cart"):
        user_cart = request.session.setdefault("user_cart", {})
        products = user_cart.setdefault("products", [])
        product_details = [prod_category, prod_id, 1]
        products.append(product_details)

    # Or getting info if instance available inside session.
    else:
        user_cart = request.session.get("user_cart")
        products = request.session.get("user_cart")["products"]

        # Update quantity of product in the cart.
        added_new_product = False
        for item in products:
            if item[0] == prod_category and item[1] == prod_id:
                item[2] += 1
                added_new_product = True

        # Or added one more product to the cart.
        if not added_new_product:
            product_details = [prod_category, prod_id, 1]
            products.append(product_details)

    # Getting price of product which added to the cart (for calculations).
    if prod_category == "mobile":
        product = Phones.objects.get(id=prod_id)
    elif prod_category == "tv":
        product = TeleVision.objects.get(id=prod_id)
    elif prod_category == "pc":
        product = PersonalComputers.objects.get(id=prod_id)

    # Updating total sum (prices) of the all products inside cart.
    user_cart_total = user_cart.get("total") or 0
    user_cart["total"] = user_cart_total + round(float(product.price), 2)
    items_in_cart = user_cart.get("item_quantity") or 0
    user_cart["item_quantity"] = items_in_cart + 1

    product.quantity -= 1
    if product.quantity == 0:
        product.available = "No"
    product.save()
    # Modified session.
    request.session.modified = True

    print(user_cart)  # TEST
    return product.quantity


def check_items_in_cart(request):
    check_items_in_cart = request.session.get("user_cart")
    if not check_items_in_cart:
        products_quantity = 0
    else:
        products_quantity = check_items_in_cart.get("item_quantity")

    return products_quantity


#
def details_prod_info(products_in_cart):

    all_products = []
    for element in products_in_cart:
        print("ELLLLELELELE", element)
        # Getting price of product which added to the cart (for calculations).
        if element[0] == "mobile":
            info = Phones.objects.get(id=element[1])
        elif element[0] == "tv":
            info = TeleVision.objects.get(id=element[1])
        elif element[0] == "pc":
            info = PersonalComputers.objects.get(id=element[1])
        list_item = {
            "category": element[0],
            "brand": info.brand,
            "model": info.model,
            "amount": element[2],
            "price": info.price,
            "sum": info.price * element[2],
        }

        all_products.append(list_item)

    return all_products
