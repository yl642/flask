import requests

server_name = 'http://127.0.0.1:5000'


def add_patient_to_db():
    new_p = {"patient_id": '1', "attending_email": "email@email.com",
             "patient_age": 12}
    r = requests.post(server_name+"/api/new_patient", json=new_p)
    if r.status_code != 200:
        print("Error: {} - {}".format(r.status_code, r.text))
    else:
        print("Success {}".format(r.text))


def add_hr_to_patient():
    new_hr = {"patient_id": '1', "heart_rate": 120}
    r = requests.post(server_name+"/api/heart_rate", json=new_hr)
    if r.status_code != 200:
        print("Error: {} - {}".format(r.status_code, r.text))
    else:
        print("Success {}".format(r.text))


def get_status_id():
    r = requests.get(server_name + "/api/status/1")
    if r.status_code != 200:
        print("Error: {} - {}".format(r.status_code, r.text))
    else:
        print("Patient {} status: {}".format(1, r.text))


if __name__ == "__main__":
    add_patient_to_db()
    add_hr_to_patient()
    get_status_id()
