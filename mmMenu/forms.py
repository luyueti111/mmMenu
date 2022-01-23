from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField, \
    FloatField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


class DishForm(FlaskForm):
    name = StringField(label='菜名',
                       render_kw={
                           'class': "form-control",
                           'placeholder': "菜名"
                       },
                       validators=[DataRequired()])
    introduction = TextAreaField(label='做法简介',
                                 render_kw={
                                     'class': "form-control",
                                     'placeholder': "Leave a comment here",
                                     'style': "height: 100px"
                                 })
    imageLoad = FileField(label='菜品图片',
                          render_kw={
                              'class': "form-control"
                          },
                          validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField(label='提交',
                         render_kw={
                             'class': "btn btn-outline-primary"
                         })


class FoodForm(FlaskForm):
    name = StringField(label='食材名',
                       render_kw={
                           'class': "form-control",
                           'placeholder': "食材名"
                       },
                       validators=[DataRequired()])
    quantityDemand = FloatField(label='所需食材量',
                                render_kw={
                                    'class': "form-control",
                                    'placeholder': "所需要食材量"
                                },
                                validators=[DataRequired()])
    unit = SelectField(label='单位', choices=[('斤', '斤'), ('个', '个')],
                       validators=[DataRequired()],
                       render_kw={
                           'class': "form-select"
                       })
    isNecessary = BooleanField(label='必须食材',
                               render_kw={
                                   'class': "form-check-input"
                               })
    submit = SubmitField(label='提交',
                         render_kw={
                             'class': "btn btn-outline-primary"
                         })


class EditFoodForm(FoodForm):
    submit = SubmitField(label='更新',
                         render_kw={
                             'class': "btn btn-outline-success"
                         })
    foodId = IntegerField()


class FoodFormForHome(FlaskForm):
    name = StringField(label='食材名',
                       render_kw={
                           'class': "form-control",
                           'placeholder': "食材名"
                       },
                       validators=[DataRequired()])
    quantity = FloatField(label='食材量',
                          render_kw={
                              'class': "form-control",
                              'placeholder': "食材量"
                          },
                          validators=[DataRequired()])
    unit = SelectField(label='单位', choices=[('斤', '斤'), ('个', '个')],
                       validators=[DataRequired()],
                       render_kw={
                           'class': "form-select"
                       })
    submit = SubmitField(label='提交',
                         render_kw={
                             'class': "btn btn-outline-primary"
                         })


class EditFoodFormForHome(FoodFormForHome):
    submit = SubmitField(label='更新',
                         render_kw={
                             'class': "btn btn-outline-success"
                         })
    foodId = IntegerField()


class DeleteFoodFormForHome(FlaskForm):
    submit = SubmitField(label='删除',
                         render_kw={
                             'class': "dropdown-item text-danger"
                         })


class DeleteFoodForm(DeleteFoodFormForHome):
    pass


class SearchForm(FlaskForm):
    searchSubject = StringField(label='搜索',
                                validators=[DataRequired()],
                                render_kw={
                                    "class": "form-control me-2",
                                    "placeholder": "搜索"
                                })
    submit = SubmitField(label='搜索',
                         render_kw={
                             "class": "btn btn-outline-success"
                         })


class EditDishForm(DishForm):
    imageLoad = FileField(label='菜品图片',
                          render_kw={
                              'class': "form-control"
                          },
                          validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField(label='更新',
                         render_kw={
                             'class': "btn btn-outline-success"
                         })


class DeleteDishForm(FlaskForm):
    submit = SubmitField(label='删除',
                         render_kw={
                             'class': "dropdown-item text-danger"
                         })
