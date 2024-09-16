from flask import Flask, render_template, request, redirect, url_for, session
import secrets

app = Flask("__name__")

# key session
secret_key = secrets.token_hex(24)
app.secret_key = secret_key


def converter_unit(units, value, unit_from, unit_to):
    # same unit
    if unit_from == unit_to:
        return value
    # converter to refer_unit
    refer_unit = float(value) * units[unit_from]

    # converter to destiny
    return refer_unit / units[unit_to]


def convert_temp(value, unit_from, unit_to):
    value = float(value)
    if unit_from == unit_to:
        return value

    # convert from the original unit to Celsius
    if unit_from == "c":
        value_in_celsius = value
    elif unit_from == "f":
        value_in_celsius = (value - 32) * 5 / 9
    else:
        value_in_celsius = value - 273.15

    # convert from Celsius to the target unit
    if unit_to == "c":
        return value_in_celsius
    elif unit_to == "f":
        return (value_in_celsius * 9 / 5) + 32
    else:
        return value_in_celsius + 273.15


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/length", methods=["GET", "POST"])
def length():
    # key unit value in meter
    LENGTH = {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1,
        "km": 1000,
        "inch": 0.0254,
        "foot": 0.3048,
        "yard": 0.9144,
        "mile": 1609.344,
    }
    # List units
    units = LENGTH.keys()

    # Prev post is none if result copy and delete in session
    result = session.pop("result", None)

    if request.method == "POST":
        value = request.form.get("length")
        unit_from = request.form.get("unit_from")
        unit_to = request.form.get("unit_to")

        # check post values
        if (
            (not value or value.isalpha())
            or unit_from not in units
            or unit_to not in units
        ):
            return redirect(url_for("length"))

        result = converter_unit(
            units=LENGTH, value=value, unit_from=unit_from, unit_to=unit_to
        )
        view_result = f"{value}{unit_from} = {result}{unit_to}"
        # add result in session
        session["result"] = view_result
        return redirect(url_for("length"))

    return render_template("./pages/length.html", units=units, result=result)


@app.route("/weight", methods=["GET", "POST"])
def weight():
    # key unit value in grams
    WEIGHT = {
        "mg": 0.001,
        "gr": 1,
        "kg": 1000,
        "ounce": 28.35,
        "pound": 453.59,
    }
    # List units
    units = WEIGHT.keys()

    # Prev post is none if result copy and delete in session
    result = session.pop("result", None)

    if request.method == "POST":
        value = request.form.get("weight")
        unit_from = request.form.get("unit_from")
        unit_to = request.form.get("unit_to")

        if (
            (not value or value.isalpha())
            or unit_from not in units
            or unit_to not in units
        ):
            return redirect(url_for("weight"))

        result = converter_unit(
            units=WEIGHT, value=value, unit_from=unit_from, unit_to=unit_to
        )
        view_result = f"{value}{unit_from} = {result}{unit_to} "
        # add result in session
        session["result"] = view_result
        return redirect(url_for("weight"))
    return render_template("./pages/weight.html", units=units, result=result)


@app.route("/temperature",methods=["GET", "POST"])
def temperature():
    units = ["c", "f"]
    result = session.pop("result", None)

    if request.method == "POST":
        value = request.form.get("temp")
        unit_from = request.form.get("unit_from")
        unit_to = request.form.get("unit_to")

        # check post values
        if (
            (not value or value.isalpha())
            or unit_from not in units
            or unit_to not in units
        ):
            return redirect(url_for("temperature"))
        result = convert_temp(value=value, unit_from=unit_from, unit_to=unit_to)
        view_result = f"{value}°{unit_from} = {result}°{unit_to}"
        # add result in session
        session["result"] = view_result
        return redirect(url_for("temperature"))
    return render_template("./pages/temperature.html", units=units, result=result)
