# Welcome to Secure Code Game Season-1/Level-3!

# You know how to play by now, good luck!

import os
from flask import Flask, request

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    TaxPayer('foo', 'bar').get_tax_form_attachment(request.args["input"])
    TaxPayer('foo', 'bar').get_prof_picture(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore


def _profile_picture_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'assets', 'prof_picture.png')


def _tax_form_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'assets', 'tax_form.pdf')


class TaxPayer:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.prof_picture = None
        self.tax_form_attachment = None

    # returns the path of an optional profile picture that users can set
    def get_prof_picture(self, path=None):
        if not path:
            return None

        # Only the known profile-picture asset is accepted. User-controlled
        # data is never used to construct the path passed to open().
        if path != 'assets/prof_picture.png':
            return None

        prof_picture_path = _profile_picture_path()
        with open(prof_picture_path, 'rb') as pic:
            picture = bytearray(pic.read())

        # assume that image is returned on screen after this
        return prof_picture_path

    # returns the path of an attached tax form that every user should submit
    def get_tax_form_attachment(self, path=None):
        if not path:
            raise Exception("Error: Tax form is required for all users")

        # Compare user input to the single trusted canonical asset. User data
        # is never passed through a filesystem path operation or to open().
        tax_form_path = _tax_form_path()
        if path != tax_form_path:
            return None

        with open(tax_form_path, 'rb') as form:
            tax_data = bytearray(form.read())

        # assume that tax data is returned on screen after this
        return tax_form_path
