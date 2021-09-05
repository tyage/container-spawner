from flask_wtf import FlaskForm, RecaptchaField
import random
import string

class SpawnerFormWithRecaptcha(FlaskForm):
    recaptcha = RecaptchaField()

def random_port(min: int, max: int):
    # TODO: exclude used port
    return random.randint(min, max)

def random_string(length: int = 16):
    letters = string.ascii_letters + string.digits
    return "".join(random.sample(string.ascii_letters, length))

def spawner_form(recaptcha_public_key = None, recaptcha_private_key = None):
    if recaptcha_public_key and recaptcha_private_key:
        return SpawnerFormWithRecaptcha()
    else:
        return FlaskForm()

