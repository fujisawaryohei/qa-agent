from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from model import config_llm
from state import State


class Judgement(BaseModel):
    reason: str = Field(default="", description="判定理由")
    judge: bool = Field(default=False, description="判定結果")


def check_node(state: State) -> dict[str, Any]:
    query = state.query
    answer = state.messages[-1]
    prompt = ChatPromptTemplate.from_template(
        """
        以下の回答の品質をチェックし、問題がある場合は'False'、問題がない場合は'True'を回答してください。
        また、その判断理由も説明してください。

        ユーザーからの質問: {query}
        回答: {answer}
    """.strip()
    )
    chain = prompt | config_llm().with_structured_output(Judgement)
    result: Judgement = chain.invoke({"query": query, "answer": answer})

    return {"current_judge": result.judge, "judgement_reason": result.reason}
