from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
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

    # チェックポインターを設定
    checkpointer = MemorySaver()

    # 作成したグラフのコンパイル
    compiled_graph = workflow.compile(checkpointer=checkpointer)

    # ステートの初期化
    # configuableは独自のdictを定義する事ができるRunnableConfig側で定義された予約キー
    # LangGraphではチェックポイント記録時に誰がいつ実行したかを識別するためにthread_idを定義してinvoke時に渡す必要がある
    config = {"configurable": {"thread_id": "exmaple-1"}}
    initial_state = State(query="生成AIについて教えてください")
    result = compiled_graph.invoke(initial_state, config)

    # グラフの画像保存
    with open("graph.png", "wb") as f:
        f.write(compiled_graph.get_graph().draw_png())

    # メッセージの出力
    print(result["messages"][-1])

    # チェックポイントの出力
    # for checkpoint in checkpointer.list(config):
    #     print(checkpoint)

    # 最新のチェックポイントの出力
    # print_checkpoint_dump(checkpointer, config)


if __name__ == "__main__":
    main()
