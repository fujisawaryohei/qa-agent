from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from model import config_llm
from role import ROLES
from state import State


def selection_node(state: State) -> dict[str, Any]:
    query = state.query
    role_options = "\n".join(
        [f"{k}. {v['name']}: {v['description']}" for k, v in ROLES.items()]
    )
    prompt = ChatPromptTemplate.from_template(
        """
        質問を分析し、最も適切な回答担当ロールを選択してください。

        選択肢:
        {role_options}

        回答は選択肢の番号(1,2または3)のみを返してください。

        質問:
        {query}
    """.strip()
    )
    chain = (
        prompt | config_llm().with_config(configurable=dict(max_tokens=10)) | StrOutputParser()
    )
    role_number = chain.invoke({"role_options": role_options, "query": query})

    selected_role = ROLES[role_number.strip()]["name"]
    return {"current_role": selected_role}
