import ssl

from product_knowledge_integrity.providers.openai_responses import OpenAIResponsesProvider, trusted_ssl_context


def test_optional_adapter_has_no_default_key_or_network_call():
    provider = OpenAIResponsesProvider(model="example-model", api_key="test-only")
    assert provider.build_payload("hello") == {"model": "example-model", "store": False, "input": "hello"}
    assert isinstance(trusted_ssl_context(), ssl.SSLContext)
