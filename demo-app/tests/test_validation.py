from openai_web_client.main import validate_chat_request

def test_validate_chat_request_ok():
    valid, msg = validate_chat_request({"message": "hello"})
    assert valid is True
    assert msg == "hello"


def test_validate_chat_request_missing_message():
    valid, err = validate_chat_request({})
    assert valid is False


def test_validate_chat_request_too_long():
    valid, err = validate_chat_request({"message": "x" * 5000})
    assert valid is False
