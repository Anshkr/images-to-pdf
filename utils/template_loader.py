import os
import json

TEMPLATE_DIR = "templates"


def load_template(template_name):

    folder = os.path.join(
        TEMPLATE_DIR,
        template_name
    )

    background = os.path.join(
        folder,
        "background.png"
    )

    config = os.path.join(
        folder,
        "config.json"
    )

    if not os.path.exists(background):
        return None

    if not os.path.exists(config):
        return None

    with open(config, "r") as f:

        data = json.load(f)

    return {
        "background": background,
        "config": data
    }