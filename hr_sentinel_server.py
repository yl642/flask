from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

db = []


def add_patient_to_db(id, email, age):
    new_patient = {"patient_id": id, "attending_email": email,
                   "patient_age": age, "heart_rate": []}
    db.append(new_patient)
    # TO DO: log
    print(db)
    return True


@app.route('/api/new_patient', methods=["POST"])
def post_new_patient():
    in_dict = request.get_json()
    check_in_dict = verify_new_patient_info(in_dict)
    if type(check_in_dict) is str:
        return check_in_dict, 400
    add_patient_to_db(check_in_dict["patient_id"],
                      check_in_dict["attending_email"],
                      check_in_dict["patient_age"])
    return "Patient added", 200


def verify_new_patient_info(in_dict):
    int_keys = ["patient_id", "patient_age"]
    for key in int_keys:
        if key in in_dict.keys():
            try:
                in_dict[key] = int(in_dict[key])
            except ValueError:
                return "'{}' value not correct type".format(key)
        else:
            return "'{}' key not found".format(key)
    if "attending_email" not in in_dict.keys():
        return "'attending_email' key not found"
    if type(in_dict["attending_email"]) is not str:
        return "'attending_email' value not correct type"
    return in_dict


def check_tachycardic(id, hr):
    for patient in db:
        if patient["patient_id"] == id:
            age = patient["patient_age"]
            break
    ages = [2, 4, 7, 11, 15]
    idx = [151, 137, 133, 130, 119, 100]
    for i in range(len(ages)):
        if age <= ages[i]:
            if hr <= idx[i]:
                return False
            return True
    if hr <= idx[-1]:
        return False
    return True


def add_heart_rate(id, hr):
    now = datetime.now()
    now_str = datetime.strftime(now, "%Y-%m-%d %H:%M:%S.%f")
    for patient in db:
        if patient["patient_id"] == id:
            patient["heart_rate"].append((now_str, hr))
    # TO DO: Email & log
    is_tachy = check_tachycardic(id, hr)
    if is_tachy is True:
        print("Sent Email!!!")
    print(db)
    return True


@app.route("/api/heart_rate", methods=["POST"])
def post_heart_rate():
    in_dict = request.get_json()
    check_in_dict = verify_heart_rate_info(in_dict)
    if type(check_in_dict) is str:
        return check_in_dict, 400
    add_heart_rate(check_in_dict["patient_id"],
                   check_in_dict["heart_rate"])
    return "Heart rate added", 200


def verify_heart_rate_info(in_dict):
    expected_keys = ["patient_id", "heart_rate"]
    for key in expected_keys:
        if key not in in_dict.keys():
            return "'{}' key not found".format(key)
        try:
            in_dict[key] = int(in_dict[key])
        except ValueError:
            return "'{}' value not correct type".format(key)
    return in_dict


def is_patient_in_db(patient_id):
    for patient in db:
        if str(patient["patient_id"]) == patient_id:
            return True
    return False


def get_status(patient_id):
    for patient in db:
        if patient["patient_id"] == patient_id:
            if len(patient["heart_rate"]) == 0:
                return "Patient {} has no heart rate data right now".format(
                    patient_id)
            hr_info = patient["heart_rate"][-1]
            break
    status = ["not tachycardic", "tachycardic"]
    out_dict = {"heart_rate": hr_info[1],
                "status": status[check_tachycardic(patient_id, hr_info[1])],
                "timestamp": hr_info[0]}
    return out_dict


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_status_id(patient_id):
    if is_patient_in_db(patient_id) is not True:
        return "Patient {} is not found on server".format(patient_id), 400
    info_dict = get_status(int(patient_id))
    if type(info_dict) is str:
        return info_dict, 400
    return info_dict, 200


if __name__ == "__main__":
    app.run()
