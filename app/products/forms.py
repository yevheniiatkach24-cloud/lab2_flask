from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    StringField,
    TextAreaField,
    DecimalField,
    SelectField,
    IntegerField,
    FileField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    Optional,
    ValidationError,
)


class ProductForm(FlaskForm):
    name = StringField(
        "Назва товару",
        validators=[
            DataRequired(message="Введіть назву товару."),
            Length(
                min=3,
                message="Назва має містити щонайменше 3 символи."
            ),
        ],
    )

    content = TextAreaField(
        "Опис товару",
        validators=[
            DataRequired(message="Введіть опис товару.")
        ],
        render_kw={"rows": 5, "cols": 40},
    )

    price = DecimalField(
        "Ціна (грн)",
        places=2,
        validators=[
            DataRequired(message="Введіть ціну."),
            NumberRange(
                min=0.01,
                message="Ціна має бути більшою за нуль."
            ),
        ],
    )

    category = SelectField(
        "Категорія",
        choices=[
            ("Косметика", "Косметика"),
            ("Одяг", "Одяг"),
            ("Електроніка", "Електроніка"),
            ("Інше", "Інше"),
        ],
        validators=[
            DataRequired(message="Оберіть категорію.")
        ],
    )

    quantity = IntegerField(
        "Кількість",
        validators=[
            DataRequired(message="Введіть кількість."),
            NumberRange(
                min=0,
                message="Кількість не може бути від’ємною."
            ),
        ],
    )

    image = FileField(
        "Зображення товару",
        validators=[
            Optional(),
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Дозволені лише файли JPG, JPEG і PNG."
            ),
        ],
    )

    submit = SubmitField("Зберегти")

    def validate_price(self, field):
        if field.data is not None and field.data.as_tuple().exponent < -2:
            raise ValidationError(
                "Ціна може містити не більше двох знаків після коми."
            )

    def validate_image(self, field):
        image = field.data

        if image and image.filename:
            image.stream.seek(0, 2)
            size = image.stream.tell()
            image.stream.seek(0)

            if size > 5 * 1024 * 1024:
                raise ValidationError(
                    "Розмір зображення не повинен перевищувати 5 МБ."
                )