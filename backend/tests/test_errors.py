from fastapi.testclient import TestClient

from app.domain.errors import ValidationError


def test_error_mapping_includes_trace_id(client: TestClient) -> None:
    @client.app.get("/raise-validation")
    def raise_validation() -> None:
        raise ValidationError("Invalid command.", details={"field": "message"})

    response = client.get("/raise-validation", headers={"X-Request-ID": "trace-123"})

    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "validation_error",
            "message": "Invalid command.",
            "details": {"field": "message"},
            "trace_id": "trace-123",
        }
    }
