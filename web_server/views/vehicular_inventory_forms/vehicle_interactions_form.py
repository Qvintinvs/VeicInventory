from typing import cast

from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange


class VehicleInteractionsForm(FlaskForm):
    interaction_id = IntegerField(validators=(DataRequired(), NumberRange(min=1)))

    @property
    def action_id(self):
        return cast(int, self.interaction_id.data)
