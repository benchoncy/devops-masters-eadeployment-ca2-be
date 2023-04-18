from pytest_bdd import scenario, given, when, then, parsers
import json


@scenario('../../features/bp_calculator.feature',
          'Calculate blood preasure category')
def test_calc():
    pass


@given("a blood preasure calculator")
def goto_calc(client):
    response = client.get('/')
    assert response.status_code == 200


@when(parsers.parse("systolic is {systolic:d} and diastolic is {diastolic:d}"),
      target_fixture="data")
def bp_fill_values(systolic, diastolic):
    data = {
        "systolic": systolic,
        "diastolic": diastolic
    }
    return data


@when("form is submitted",
      target_fixture="response")
def submit(client, data):
    response = client.get(f"/{data['systolic']}/{data['diastolic']}")
    return response


@then(parsers.parse("blood preasure category is {bp_category}"))
def bp_check(response, bp_category):
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["error"] is None
    assert bp_category == data["category"]
