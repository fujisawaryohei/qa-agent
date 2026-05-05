from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from model import config_llm
from role import ROLES
from state import State


def answering_node(state: State) -> dict[str, Any]:
    query = state.query
    role = state.current_role
    role_detail = "\n".join([f"- {v['name']}: {v['detail']}" for v in ROLES.values()])

    prompt = ChatPromptTemplate.from_template(
        """あなたは{role}として回答してください。以下の質問に対して、あなたの役割に基づいた適切な回答を提供してください。

        役割の詳細:
        {role_detail}

        質問: {query}

        回答:""".strip()
    )

    chain = prompt | config_llm() | StrOutputParser()
    answer = chain.invoke({"role": role, "role_detail": role_detail, "query": query})

    return {"messages": [answer]}
