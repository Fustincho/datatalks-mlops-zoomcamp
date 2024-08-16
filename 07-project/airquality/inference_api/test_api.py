import pytest
import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 10  # Timeout in seconds


def test_predict():
    response = requests.post(
        f"{BASE_URL}/predict",
        json={
            "sid_20466": 16.0,
            "sid_34845": 0.015,
            "sid_34841": 19.0,
            "sid_35394": 0.0086,
            "sid_35577": 14.0,
            "sid_35843": 42.0,
            "sid_36047": 18.0,
            "sid_36066": 45.0,
            "sid_36064": 25.0,
            "sid_36092": 19.0,
            "sid_35606": 31.0,
        },
        timeout=TIMEOUT,
    )
    assert response.status_code == 200
    assert "prediction" in response.json()


def test_predict_batch():
    response = requests.post(
        f"{BASE_URL}/predict_batch",
        json={
            "batch": [
                {
                    "sid_20466": 16.0,
                    "sid_34845": 0.015,
                    "sid_34841": 19.0,
                    "sid_35394": 0.0086,
                    "sid_35577": 14.0,
                    "sid_35843": 42.0,
                    "sid_36047": 18.0,
                    "sid_36066": 45.0,
                    "sid_36064": 25.0,
                    "sid_36092": 19.0,
                    "sid_35606": 31.0,
                },
                {
                    "sid_20466": 22.0,
                    "sid_34845": 0.021,
                    "sid_34841": 27.0,
                    "sid_35394": 0.022,
                    "sid_35577": 20.0,
                    "sid_35843": 58.0,
                    "sid_36047": 27.0,
                    "sid_36066": 57.0,
                    "sid_36064": 33.0,
                    "sid_36092": 26.0,
                    "sid_35606": 43.0,
                },
            ]
        },
        timeout=TIMEOUT,
    )
    assert response.status_code == 200
    assert "predictions" in response.json()


def test_missing_values():
    response = requests.post(
        f"{BASE_URL}/predict",
        json={
            "sid_20466": 16.0,
            "sid_34845": None,
            "sid_34841": 19.0,
            "sid_35394": None,
            "sid_35577": 14.0,
            "sid_35843": 42.0,
            "sid_36047": 18.0,
            "sid_36066": 45.0,
            "sid_36064": None,
            "sid_36092": 19.0,
            "sid_35606": 31.0,
        },
        timeout=TIMEOUT,
    )
    assert response.status_code == 200
    assert "prediction" in response.json()


def test_invalid_data_type():
    response = requests.post(
        f"{BASE_URL}/predict",
        json={
            "sid_20466": "invalid",
            "sid_34845": 0.015,
            "sid_34841": 19.0,
            "sid_35394": 0.0086,
            "sid_35577": 14.0,
            "sid_35843": 42.0,
            "sid_36047": 18.0,
            "sid_36066": 45.0,
            "sid_36064": 25.0,
            "sid_36092": 19.0,
            "sid_35606": 31.0,
        },
        timeout=TIMEOUT,
    )
    assert response.status_code == 422  # Unprocessable Entity


if __name__ == "__main__":
    pytest.main()
