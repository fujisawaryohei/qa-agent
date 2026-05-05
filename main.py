from dotenv import load_dotenv
from langgraph.graph import END, StateGraph

from node import answering_node, check_node, selection_node
from state import State


def main():
    load_dotenv()
    # グラフの初期化
    workflow = StateGraph(State)

    # ノードの定義
    workflow.add_node("selection", selection_node)
    workflow.add_node("answering", answering_node)
    workflow.add_node("check", check_node)

    # ノードの始点の定義
    workflow.set_entry_point("selection")

    # ノード間のエッジの定義
    workflow.add_edge("selection", "answering")
    workflow.add_edge("answering", "check")

    # ノードの終点の定義
    workflow.add_conditional_edges(
        "check", lambda state: state.current_judge, {True: END, False: "selection"}
    )

    # 作成したグラフのコンパイル
    compiled = workflow.compile()

    # ステートの初期化
    initial_state = State(query="生成AIについて教えてください")
    result = compiled.invoke(initial_state)

    # グラフの画像保存
    with open("graph.png", "wb") as f:
        f.write(compiled.get_graph().draw_png())
    print(result["messages"][-1])


if __name__ == "__main__":
    main()
