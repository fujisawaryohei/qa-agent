from langchain_anthropic import ChatAnthropic
from langchain_core.runnables import ConfigurableField


def config_llm() -> ChatAnthropic:
    max_tokens_field = ConfigurableField(id="max_tokens")
    llm = ChatAnthropic(model="claude-haiku-4-5-20251001", temperature=0)
    return llm.configurable_fields(max_tokens=max_tokens_field)
