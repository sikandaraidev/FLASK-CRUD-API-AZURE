from package.models.car_model import Car


def get_all_cars(session):
    return session.query(Car).all()


def get_car(session, car_id):
    return session.get(Car, car_id)


def create_car(session, car_data):
    car = Car(**car_data)
    session.add(car)
    session.flush()
    return car


def update_car(session, car_id, car_data):
    car = session.get(Car, car_id)
    if not car:
        return None
    for key, value in car_data.items():
        setattr(car, key, value)
    session.flush()
    return car


def delete_car(session, car_id):
    car = session.get(Car, car_id)
    if not car:
        return False
    session.delete(car)
    return True
