import os
from datetime import datetime
from flask import redirect, url_for, render_template, send_from_directory
from jieba import lcut_for_search
from sqlalchemy import or_, and_

from mmMenu import app, db
from mmMenu.models import Dish, Food, FoodWeHave
from mmMenu.forms import DishForm, FoodForm, EditFoodForm, FoodFormForHome, EditFoodFormForHome, DeleteFoodFormForHome, \
    DeleteFoodForm, SearchForm, EditDishForm, DeleteDishForm
from mmMenu.utils import randomFilename, resizeImage, foodIsAva, dishIsAva


@app.route('/postDish', methods=['GET', 'POST'])
def postDish():
    dishForm = DishForm()

    if dishForm.validate_on_submit():
        name = dishForm.name.data
        introduction = dishForm.introduction.data
        f = dishForm.imageLoad.data

        filename = randomFilename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        resizeImage(os.path.join(app.config['UPLOAD_PATH'], filename))

        dish = Dish(name=name, introduction=introduction,
                    imageUrl=url_for('getFile', filename=filename))
        db.session.add(dish)
        db.session.commit()
        return redirect(url_for('postFood', dishId=dish.id))

    return render_template('postDish.html', dishForm=dishForm)


@app.route('/postFood/<int:dishId>', methods=['GET', 'POST'])
def postFood(dishId):
    dish = Dish.query.get(dishId)
    foodForm = FoodForm()
    deleteFoodForm = DeleteFoodForm()
    editFoodForm = EditFoodForm()
    deleteDishForm = DeleteDishForm()

    if foodForm.validate_on_submit():
        name = foodForm.name.data
        quantityDemand = foodForm.quantityDemand.data
        unit = foodForm.unit.data
        isNecessary = foodForm.isNecessary.data

        food = Food(name=name, quantityDemand=quantityDemand, unit=unit, isNecessary=isNecessary)
        db.session.add(food)
        food.dish = dish
        food.isAvailable = foodIsAva(food)

        dish.isAvailable = dishIsAva(dish)
        db.session.commit()
        return redirect(url_for('postFood', dishId=dish.id) + "#fm")

    return render_template('postFood.html',
                           dish=dish,
                           foodForm=foodForm,
                           editFoodForm=editFoodForm,
                           deleteFoodForm=deleteFoodForm,
                           deleteDishForm=deleteDishForm)


@app.route('/uploads/<path:filename>')
def getFile(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/editFood', methods=['POST'])
def editFood():
    editFoodForm = EditFoodForm()
    if editFoodForm.validate_on_submit():
        foodId = editFoodForm.foodId.data
        name = editFoodForm.name.data
        quantityDemand = editFoodForm.quantityDemand.data
        unit = editFoodForm.unit.data
        isNecessary = editFoodForm.isNecessary.data

        food = Food.query.get(foodId)
        food.name = name
        food.quantityDemand = quantityDemand
        food.unit = unit
        food.isNecessary = isNecessary

        food.isAvailable = foodIsAva(food)

        dish = food.dish
        dish.isAvailable = dishIsAva(dish)
        dish.lastEdit = datetime.now()
        db.session.commit()

        return redirect(url_for('postFood', dishId=food.dish.id) + "#fdt")


@app.route('/index')
@app.route('/')
def index():
    dishes = Dish.query.order_by(Dish.lastEdit.desc()).all()

    return render_template('index.html', dishes=dishes)


@app.route('/homeFood', methods=['GET', 'POST'])
def homeFood():
    allFood = FoodWeHave.query.all()
    foodFormForHome = FoodFormForHome()
    editFoodFormForHome = EditFoodFormForHome()
    deleteFoodFormForHome = DeleteFoodFormForHome()
    return render_template('homeFood.html',
                           allFood=allFood,
                           foodFormForHome=foodFormForHome,
                           editFoodFormForHome=editFoodFormForHome,
                           deleteFoodFormForHome=deleteFoodFormForHome)


@app.route('/postFoodForHome', methods=['POST'])
def postFoodForHome():
    foodFormForHome = FoodFormForHome()
    if foodFormForHome.validate_on_submit():
        name = foodFormForHome.name.data
        quantity = foodFormForHome.quantity.data
        unit = foodFormForHome.unit.data
        foodWeHave = FoodWeHave(name=name, quantity=quantity, unit=unit)

        foodsInMenu = Food.query.filter_by(name=name)
        for foodInMenu in foodsInMenu:
            foodInMenu.isAvailable = True
            foodInMenuDish = foodInMenu.dish
            foodInMenuDish.isAvailable = dishIsAva(foodInMenuDish)

        db.session.add(foodWeHave)
        db.session.commit()
        return redirect(url_for('homeFood') + "#fm")


@app.route('/editFoodForHome', methods=['POST'])
def editFoodForHome():
    editFoodFormForHome = EditFoodFormForHome()
    if editFoodFormForHome.validate_on_submit():
        foodId = editFoodFormForHome.foodId.data
        name = editFoodFormForHome.name.data
        quantity = editFoodFormForHome.quantity.data
        unit = editFoodFormForHome.unit.data

        food = FoodWeHave.query.get(foodId)
        food.name = name
        food.quantity = quantity
        food.unit = unit

        db.session.commit()

        return redirect(url_for('homeFood') + '#fdt')


@app.route('/avaDishes')
def avaDishes():
    dishes = Dish.query.filter_by(isAvailable=True).order_by(Dish.lastEdit.desc())
    cnt = dishes.count()
    dishes = dishes.all()
    return render_template('indexWithoutImage.html', dishes=dishes, tag='筛选结果', cnt=cnt)


@app.route('/deleteHomeFood/<int:foodId>', methods=["POST"])
def deleteHomeFood(foodId):
    deleteFoodFormForHome = DeleteFoodFormForHome()
    if deleteFoodFormForHome.validate_on_submit():
        food = FoodWeHave.query.get(foodId)
        foodsInMenu = Food.query.filter_by(name=food.name)
        for foodInMenu in foodsInMenu:
            foodInMenu.isAvailable = False
            foodInMenuDish = foodInMenu.dish
            foodInMenuDish.isAvailable = dishIsAva(foodInMenuDish)

        db.session.delete(food)
        db.session.commit()
        return redirect(url_for('homeFood') + '#fdt')


@app.route('/deleteFood/<int:foodId>', methods=['POST'])
def deleteFood(foodId):
    deleteFoodForm = DeleteFoodForm()
    if deleteFoodForm.validate_on_submit():
        food = Food.query.get(foodId)
        dish = food.dish
        db.session.delete(food)
        dish.isAvailable = dishIsAva(dish)
        dish.lastEdit = datetime.now()
        db.session.commit()

        return redirect(url_for('postFood', dishId=dish.id) + "#fdt")


@app.context_processor
def injectSearchForm():
    searchForm = SearchForm()
    return dict(searchForm=searchForm)


@app.route('/searchResult', methods=['POST'])
def searchResult():
    searchForm = SearchForm()
    if searchForm.validate_on_submit():
        searchRule = searchForm.searchSubject.data
        searchList = lcut_for_search(searchRule)
        rules = ""
        for rule in searchList:
            rules += rule + "|"
        rules = rules.rstrip("|")
        searchedDish = Dish.query.filter(or_(Dish.name.op('regexp')(rules),
                                             Dish.introduction.op('regexp')(rules)))

        searchFood = Food.query.filter(and_(Food.name.op('regexp')(rules),
                                            ~Food.dish_id.in_([dish.id for dish in searchedDish])),
                                       )
        allSearchId = [dish.id for dish in searchedDish] + [food.dish.id for food in searchFood]
        allSearchDish = Dish.query.filter(Dish.id.in_(allSearchId))
        cnt = len(allSearchId)
        return render_template('indexWithoutImage.html', dishes=allSearchDish, tag='搜索结果', cnt=cnt)


@app.route('/editDish/<int:dishId>', methods=['GET', 'POST'])
def editDish(dishId):
    editDishForm = EditDishForm()
    dish = Dish.query.get(dishId)
    if editDishForm.validate_on_submit():
        name = editDishForm.name.data
        introduction = editDishForm.introduction.data
        dish.name = name
        dish.introduction = introduction
        dish.lastEdit = datetime.now()
        f = editDishForm.imageLoad.data

        try:
            filename = randomFilename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            resizeImage(os.path.join(app.config['UPLOAD_PATH'], filename))
            dish.imageUrl = url_for('getFile', filename=filename)
        except AttributeError:
            pass
        db.session.commit()
        return redirect(url_for('postFood', dishId=dishId))
    editDishForm.name.data = dish.name
    editDishForm.introduction.data = dish.introduction
    return render_template('editDish.html', dishForm=editDishForm, dishId=dishId)


@app.route('/deleteDish/<int:dishId>', methods=['POST'])
def deleteDish(dishId):
    deleteDishForm = DeleteDishForm()
    if deleteDishForm.validate_on_submit():
        dish = Dish.query.get(dishId)
        for food in dish.foods:
            db.session.delete(food)

        db.session.delete(dish)
        db.session.commit()
    return redirect(url_for('index'))
