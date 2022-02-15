from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import (
    Form,
    StringField,
    PasswordField,
    validators,
    SubmitField,
    TextAreaField,
    BooleanField,
    ValidationError,
    SelectMultipleField,
)
from flask_wtf.file import FileField, FileAllowed

from .. import app
from ..model import Tag


class TextField:
    def __init__(
        self,
        label,
        placeholder,
        minChar=None,
        maxChar=None,
        len_message=None,
        required_message=None,
        _class="form-control",
        _type="text",
        required=True,
    ):
        self.label = label
        self.placeholder = placeholder
        self.min = minChar
        self.max = maxChar
        self.len_message = len_message
        self.required_message = required_message
        self._class = _class
        self.type = _type
        self.required = required

    def field(self):
        """
        field : will return 2 type of text field : password and text
        """
        field = StringField if self.type == "text" else PasswordField
        return field(
            self.label,
            [
                validators.length(
                    min=0 if not self.min else self.min,
                    max=999999999999999 if not self.max else self.max,
                    message=self.len_message,
                ),
                validators.DataRequired(self.required_message)
                if self.required
                else validators.Optional(),
            ],
            render_kw={"class": self._class, "placeholder": self.placeholder},
        )


class Login(FlaskForm):
    username = TextField(
        "Username",
        "Username",
        minChar=4,
        maxChar=24,
        len_message="Username must be between 4 and 25 characters long",
        required_message="username is required",
        _type="text",
    ).field()
    password = TextField(
        "Password",
        "Password",
        minChar=8,
        len_message="minimal Length for password is 8 characters",
        required_message="password is required",
        _type="password",
    ).field()

    captcha = RecaptchaField(validators=[Recaptcha(message="captcha is missings")])
    submit = SubmitField(
        "Login",
        name="login",
        render_kw={"class": "btn btn-primary mx-auto btn-lg w-100"},
    )


class PostForm(FlaskForm):
    title = TextField(
        "Title",
        "Blog title",
        minChar=3,
        maxChar=24,
        len_message="title must be between 4 and 25 characters long",
        required_message="title is required",
    ).field()
    with app.app_context():
        tag = SelectMultipleField(
            "Tags",
            [validators.DataRequired()],
            render_kw={"class": "form-control tag w-100"},
            choices=["tag", "test"] + [tag.tag for tag in Tag().get_all(parse=False)],
        )
    keywords = TextField("Keywords", "Keywords", required=False).field()
    cover_image = FileField(
        "image",
        validators=[FileAllowed(["png", "jpg", "jpeg"], message="only image allowed")],
        render_kw={"class": "form-control", "accept": ".png,.jpg,.jpeg"},
    )
    content = TextAreaField(
        "Content",
        [
            validators.DataRequired("content is required"),
            validators.Length(
                min=10,
                max=10000,
                message="blog content must be between 100 and 10000 characters long.",
            ),
        ],
        render_kw={"class": "form-control", "placeholder": "your blog here"},
    )
    is_hidden = BooleanField("hidden", [validators.Optional()])
    submit = SubmitField(
        "Add",
        name="add",
        render_kw={"class": "btn btn-primary btn-lg"},
    )


class TagForm(FlaskForm):
    tag = TextField(
        "Tag",
        "Tag name",
        minChar=3,
        maxChar=24,
        len_message="tag must be between 4 and 25 characters long",
        required_message="tag is required",
    ).field()
    description = TextAreaField(
        "Tag description",
        [
            validators.Optional(),
            validators.Length(
                max=500,
                message="tag description limit is 500 char.",
            ),
        ],
        render_kw={"class": "form-control", "placeholder": "tag description"},
    )
    submit = SubmitField(
        "Add tag",
        name="add",
        render_kw={"class": "btn btn-primary"},
    )
