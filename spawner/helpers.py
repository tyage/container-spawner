from flask_wtf import FlaskForm, RecaptchaField
import random
import string
from docker.errors import APIError


class SpawnerFormWithRecaptcha(FlaskForm):
    recaptcha = RecaptchaField()


def random_port(min: int, max: int):
    # TODO: exclude used port
    return random.randint(min, max)


def random_string(length: int = 16):
    letters = string.ascii_letters + string.digits
    return "".join(random.sample(string.ascii_letters, length))


def spawner_form(recaptcha_public_key=None, recaptcha_private_key=None):
    if recaptcha_public_key and recaptcha_private_key:
        return SpawnerFormWithRecaptcha()
    else:
        return FlaskForm()


def spawn_container_with_random_port(docker_client, image_name, source_port,
                                     port_min, port_max, args={}, trials=10):
    # override some args with random string
    if not 'ports' in args:
        args['ports'] = {}

    # try some times until we hit the unused port
    last_error = APIError
    for i in range(trials):
        exposed_port = random_port(port_min, port_max)
        args['ports'][source_port] = exposed_port
        try:
            container = docker_client.containers.run(image_name, **args)
            return container, exposed_port
        except APIError as error:
            # if it failed, try again
            last_error = error

    # return last error if all trials failed
    raise last_error
