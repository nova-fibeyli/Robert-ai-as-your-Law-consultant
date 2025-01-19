import pytest
from src.app import stream_chat

def test_stream_chat():
    result = stream_chat("llama3.2", [{"role": "user", "content": "HELP"}])
    assert "I didn’t catch that" in result
