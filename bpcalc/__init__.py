import os
import json
from flask import Flask
from flask_talisman import Talisman
from bpcalc.bpenums import BPCategory, BPLimits


# Get flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', os.urandom(12))

permissions_policy = {
    'geolocation': '()',
    'microphone': '()'
}
csp = {
    'default-src': '\'self\' cdn.jsdelivr.net'
}
Talisman(
    app,
    force_https=False,
    content_security_policy=csp,
    permissions_policy=permissions_policy
)


def validate_values(systolic, diastolic):
    """Ensure systolic and diastolic input values make sense."""
    errors = []
    if systolic < diastolic:
        errors += ["Systolic preasure must be higher than diastolic preasure"]
    if not BPLimits.YMIN <= systolic <= BPLimits.YMAX:
        errors += ["Systolic value must be between {min} and {max}"
                   .format(min=BPLimits.YMIN, max=BPLimits.YMAX)]
    if not BPLimits.XMIN <= diastolic <= BPLimits.XMAX:
        errors += ["Diastolic value must be between {min} and {max}"
                   .format(min=BPLimits.XMIN, max=BPLimits.XMAX)]
    return errors if len(errors) > 0 else None


def get_bp_category(systolic, diastolic):
    """
    Return a blood preasure category determed by
    systolic and diastolic values.
    """
    if systolic < BPLimits.IDEAL_YSTART and diastolic < BPLimits.IDEAL_XSTART:
        return BPCategory.LOW
    if systolic < BPLimits.PRE_HIGH_YSTART and diastolic < BPLimits.PRE_HIGH_XSTART:
        return BPCategory.IDEAL
    if systolic < BPLimits.HIGH_YSTART and diastolic < BPLimits.HIGH_XSTART:
        return BPCategory.PRE_HIGH
    return BPCategory.HIGH


@app.route("/")
@app.route("/<systolic>/<diastolic>")
@app.route("/<systolic>/<diastolic>/<email>")
def index(systolic=None, diastolic=None, email=None):
    """Index route containing BPCalculator."""
    print(systolic, diastolic, email)
    error = None
    try:
        systolic = float(systolic)
        diastolic = float(diastolic)
        error = validate_values(systolic, diastolic)
    except (ValueError, TypeError):
        error = ["Valid values must be entered"]
    success = error is None
    category = None
    if success:
        category = get_bp_category(systolic, diastolic)
    response = json.dumps({
        "error": error,
        "category": str(category)
    })
    return response


@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response
