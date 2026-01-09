def test_chat_api_mocked(client, monkeypatch):
    def fake_call_llm_api(msg):
        return "mocked response"

    monkeypatch.setattr(
        "openai_web_client.main.call_llm_api",
        fake_call_llm_api
    )

    resp = client.post(
        "/api/chat",
        json={"message": "hello"}
    )

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["response"] == "mocked response"
