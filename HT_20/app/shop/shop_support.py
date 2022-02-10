from django.db.models import Sum

from .models import TeleVision, Phones, PersonalComputers, ProduntsInCart


# Information of the products into user 'cart'.
def cart_get_info_for_context(current_user_id):

    check_products_amount = ProduntsInCart.objects.all().filter(
        user_id=current_user_id).aggregate(Sum("amount"))

    check_products_total_price = ProduntsInCart.objects.all().filter(
        user_id=current_user_id).aggregate(Sum("price_one_product"))

    all_products_in_cart = ProduntsInCart.objects.all().filter(
        user_id=current_user_id)

    prod_list = []
    for item in all_products_in_cart:
        prod_id = item.prod_id
        prod_category = item.category

        if prod_category == "mobile":
            product_info = list(Phones.objects.all().filter(id=prod_id))
            product_info[0].category = "Phones"
            product_info[0].amount = item.amount
            prod_list.append(product_info[0])
        elif prod_category == "pc":
            product_info = list(
                PersonalComputers.objects.all().filter(id=prod_id))
            product_info[0].category = "Computers"
            product_info[0].amount = item.amount
            prod_list.append(product_info[0])
        elif prod_category == "tv":
            product_info = list(TeleVision.objects.all().filter(id=prod_id))
            product_info[0].category = "TV"
            product_info[0].amount = item.amount
            prod_list.append(product_info[0])

    return (check_products_amount["amount__sum"],
            check_products_total_price["price_one_product__sum"], prod_list)


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
