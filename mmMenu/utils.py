import os
import uuid
from PIL import Image
from mmMenu.models import FoodWeHave


def randomFilename(filename):
    ext = os.path.splitext(filename)[1]
    newFilename = uuid.uuid4().hex + ext
    return newFilename


def resizeImage(filename):
    im = Image.open(filename)
    w, h = im.size

    if w > h:
        mid = w/2
        sx = mid-h/2
        sy = 0
        ex = mid+h/2
        ey = h
    else:
        mid = h/2
        sx = 0
        sy = mid-w/2
        ex = w
        ey = mid+w/2

    box = (sx, sy, ex, ey)
    im_resize = im.crop(box)
    im_resize.save(filename)


def foodIsAva(food):
    haveFood = FoodWeHave.query.filter_by(name=food.name).all()

    if haveFood:
        return True
    else:
        return False


def dishIsAva(dish):
    foods = dish.foods
    for food in foods:
        if not food.isAvailable and food.isNecessary:
            return False
    return True
