from flask import Flask, request
from datetime import datetime

app = Flask(__name__)


@app.route("/time", methods=["GET"])
def time():
    time = datetime.now()
    time_str = datetime.strftime(time, "%H:%M:%S")
    return time_str


@app.route("/date", methods=["GET"])
def date():
    time = datetime.now()
    time_str = datetime.strftime(time, "%m-%d-%Y")
    return time_str


@app.route('/age..', methods=["POST"])
@app.route("/age..<units>", methods=["POST"])
def age(units="years"):
    in_data = request.get_json()
    time = datetime.now()
    in_date = datetime.strptime(in_data["date"], "%m/%d/%Y")
    gap = time - in_date
    if units == "years":
        return str(gap.days//365) + ' ' + units
    elif units == "days":
        return str(gap.days) + ' ' + units
    elif units == "mins":
        return str(gap.total_seconds()//60) + ' ' + units
    elif units == "secs":
        return str(gap.total_seconds()) + ' ' + units
    else:
        return 'Please specify with acceptable units ([years]/days/mins/secs)'


@app.route("/until_next_meal/", methods=["GET"])
@app.route("/until_next_meal/<meal>", methods=["GET"])
def meals(meal="breakfast"):
    time = datetime.now()
    h = int(datetime.strftime(time, "%H"))
    # time = datetime.now().time()
    # h = int(datetime.strftime(time, "%H"))
    meal_dict = {"breakfast": 8, "lunch": 12, "dinner": 18}
    if meal in meal_dict:
        if h > meal_dict[meal]:
            return str(24 + meal_dict[meal] - h) + "h to " + meal
        else:
            return str(h - meal_dict[meal]) + "h to " + meal
    # if meal == "breakfast":
    #     if h > 8:
    #         return str(32 - h) + 'h to ' + meal
    #     else:
    #         return str(8 - h) + 'h to ' + meal
    # elif meal == "lunch":
    #     if h > 12:
    #         return str(36 - h) + 'h to ' + meal
    #     else:
    #         return str(12 - h) + 'h to ' + meal
    # elif meal == "dinner":
    #     if h > 18:
    #         return str(42 - h) + 'h to ' + meal
    #     else:
    #         return str(18 - h) + 'h to ' + meal
    return 'Please specify with acceptable meals ([breakfast]/lunch/dinner)'


if __name__ == "__main__":
    app.run()
