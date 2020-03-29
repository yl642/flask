import pytest
from datetime import datetime
from hr_sentinel_server import db


@pytest.mark.parametrize('input, output', [
    ({"patient_id": 1, "attending_email": "dr_user_id@domain.com",
      "patient_age": 12},
     {"patient_id": 1, "attending_email": "dr_user_id@domain.com",
      "patient_age": 12}),
    ({"patient_id": '1', "attending_email": "dr_user_id@domain.com",
      "patient_age": '12'},
     {"patient_id": 1, "attending_email": "dr_user_id@domain.com",
      "patient_age": 12}),
    ({"patient_id": '1a', "attending_email": "dr_user_id@domain.com",
      "patient_age": 12}, "'patient_id' value not correct type"),
    ({"patient_id": 1, "attending_email": "dr_user_id@domain.com"},
     "'patient_age' key not found"),
    ({"patient_id": '1', "attending_email": 123,
      "patient_age": '12'}, "'attending_email' value not correct type"),
    ({"patient_id": '1', "patient_age": '12'},
     "'attending_email' key not found"),
])
def test_verify_new_patient_info(input, output):
    from hr_sentinel_server import verify_new_patient_info
    answer = verify_new_patient_info(input)
    assert answer == output


@pytest.mark.parametrize('id, email, age, out', [
    (1, "dr_user_id@domain.com", 12,
     [{"patient_id": 1, "attending_email": "dr_user_id@domain.com",
       "patient_age": 12, "heart_rate": []}]),
    (3, "dr_user_id@domain.com", 22,
     [{"patient_id": 1, "attending_email": "dr_user_id@domain.com",
       "patient_age": 12, "heart_rate": []},
      {"patient_id": 3, "attending_email": "dr_user_id@domain.com",
       "patient_age": 22, "heart_rate": []}]),
])
def test_add_patient_to_db(id, email, age, out):
    from hr_sentinel_server import add_patient_to_db
    add_patient_to_db(id, email, age)
    assert db == out


@pytest.mark.parametrize('input, output', [
    ({"patient_id": 1, "heart_rate": 100},
     {"patient_id": 1, "heart_rate": 100}),
    ({"patient_id": '1', "heart_rate": '100'},
     {"patient_id": 1, "heart_rate": 100}),
    ({"patient_id": '1a', "heart_rate": 100},
     "'patient_id' value not correct type"),
    ({"patient_id": 1},
     "'heart_rate' key not found"),
])
def test_verify_heart_rate_info(input, output):
    from hr_sentinel_server import verify_heart_rate_info
    answer = verify_heart_rate_info(input)
    assert output == answer


@pytest.mark.parametrize('id, hr, out', [
    (1, 100,
     [{"patient_id": 1, "attending_email": "dr_user_id@domain.com",
       "patient_age": 12, "heart_rate": [(datetime.strftime(datetime.now(),
                                          "%Y-%m-%d %H:%M:%S.%f"), 100)]},
      {"patient_id": 3, "attending_email": "dr_user_id@domain.com",
       "patient_age": 22, "heart_rate": []}]),
    (3, 80,
     [{"patient_id": 1, "attending_email": "dr_user_id@domain.com",
       "patient_age": 12, "heart_rate": [(datetime.strftime(datetime.now(),
                                          "%Y-%m-%d %H:%M:%S.%f"),
                                          100)]},
      {"patient_id": 3, "attending_email": "dr_user_id@domain.com",
       "patient_age": 22, "heart_rate": [(datetime.strftime(datetime.now(),
                                          "%Y-%m-%d %H:%M:%S.%f"),
                                          80)]}]),
    (3, 110,
     [{"patient_id": 1, "attending_email": "dr_user_id@domain.com",
       "patient_age": 12, "heart_rate": [(datetime.strftime(datetime.now(),
                                          "%Y-%m-%d %H:%M:%S.%f"),
                                          100)]},
      {"patient_id": 3, "attending_email": "dr_user_id@domain.com",
       "patient_age": 22, "heart_rate": [(datetime.strftime(datetime.now(),
                                          "%Y-%m-%d %H:%M:%S.%f"),
                                          80),
                                         (datetime.strftime(datetime.now(),
                                          "%Y-%m-%d %H:%M:%S.%f"),
                                          110)
                                         ]}]),
])
def test_add_heart_rate(id, hr, out):
    from hr_sentinel_server import add_heart_rate
    keys = ["patient_id", "attending_email", "patient_age"]
    add_heart_rate(id, hr)
    assert len(db) == len(out)
    for idx in range(len(db)):
        for key in keys:
            assert db[idx][key] == out[idx][key]
        assert len(db[idx]["heart_rate"]) == len(out[idx]["heart_rate"])
        for i in range(len(db[idx]["heart_rate"])):
            assert len(db[idx]["heart_rate"][i]) == \
                   len(out[idx]["heart_rate"][i])
            db_time = db[idx]["heart_rate"][i][0]
            out_time = out[idx]["heart_rate"][i][0]
            db_hr = db[idx]["heart_rate"][i][1]
            out_hr = out[idx]["heart_rate"][i][1]
            db_time = datetime.strptime(db_time, "%Y-%m-%d %H:%M:%S.%f")
            out_time = datetime.strptime(out_time, "%Y-%m-%d %H:%M:%S.%f")
            delta = (db_time - out_time).total_seconds()
            assert abs(delta) < 1
            assert db_hr == out_hr


@pytest.mark.parametrize('id, hr, output', [
    (1, 110, False), (3, 110, True), (1, 120, True), (1, 90, False),
])
def test_check_tachycardic(id, hr, output):
    from hr_sentinel_server import check_tachycardic
    answer = check_tachycardic(id, hr)
    assert answer == output


@pytest.mark.parametrize('id, output', [
    ('1', True), ('2', False), ('3', True), ('4', False),
])
def test_is_patient_in_db(id, output):
    from hr_sentinel_server import is_patient_in_db
    answer = is_patient_in_db(id)
    assert output == answer


@pytest.mark.parametrize('id, output', [
    (1,
     {"heart_rate": 100,
      "status": "not tachycardic",
      "timestamp": db[0]["heart_rate"][-1][0]}),
    (3,
     {"heart_rate": 110,
      "status": "tachycardic",
      "timestamp": db[1]["heart_rate"][-1][0]}),
    (2, "Patient 2 has no heart rate data right now"),
])
def test_get_status_id(id, output):
    from hr_sentinel_server import add_patient_to_db
    from hr_sentinel_server import get_status
    add_patient_to_db(2, "dr@dm.com", 40)
    answer = get_status(id)
    assert output == answer
