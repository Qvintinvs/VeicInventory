from typing import cast

from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange


class VehicleInteractionsForm(FlaskForm):
    __id = IntegerField("Id", validators=(DataRequired(), NumberRange(min=1)))

    @property
    def id(self):
        return cast(int, self.__id)
