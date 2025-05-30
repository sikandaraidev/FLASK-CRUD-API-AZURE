from package.models.product_model import Product


def get_all_products(session):
    return session.query(Product).all()


def get_product(session, product_id):
    return session.get(Product, product_id)


def create_product(session, product_data):
    product = Product(**product_data)
    session.add(product)
    session.flush()
    return product


def update_product(session, product_id, product_data):
    product = session.query(Product).get(product_id)
    if not product:
        return None
    for key, value in product_data.items():
        setattr(product, key, value)
    session.flush()
    return product


def delete_product(session, product_id):
    product = session.get(Product, product_id)
    if not product:
        return False
    session.delete(product)
    return True
