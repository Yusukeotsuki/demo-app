import json
import time
from typing import Any

from jpbchat.azure_openai_handler import AzureOpenAIHandler  # noqa: E402
from jpbchat.index_retriever import IndexRetriever
from jpbchat.phrase_converter import PhraseConverter  # noqa: E402
from jpbchat.placeholder_replacer import PlaceholderReplacer  # noqa: E402
from langchain.storage import LocalFileStore  # noqa: E402
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field


# ステート管理クラス
class State(BaseModel):
    query: str = Field(default="")
    retriever_docs: list = Field(default=[])
    selected_doc: list = Field(default=[])
    answers: str = Field(default="")
    review_result: bool = Field(default=False)
    predict_faqs: str = Field(default="")
    predict_faqs_ids: str = Field(default="")
    proc_pattern: str = Field(default="")


class WorkflowManager:
    def __init__(self, config):
        self.config = config

        # Azure OpenAI Handler を初期化（Embedding などもここから取得）
        self.aoai_handler = AzureOpenAIHandler(
            config=self.config.azure_open_ai,
            store=LocalFileStore(self.config.indexer.cache_dir),
        )

        # ベクトル検索用のRetrieverを初期化
        self.retriever = IndexRetriever(
            config=self.config.retriever, embedding=self.aoai_handler.embedding
        )

        # 顧客情報を読み込み、プレースホルダー変換用にセットアップ
        # # NOTE:本番実装時は不要
        # with open("data/customer_info_sample.json", "r") as f:
        #     customer_info = json.load(f)
        # self.placeholder_replacer = PlaceholderReplacer(customer_info=customer_info)

        # サブクエリ文を変換するためのユーティリティ
        self.phrase_converter = PhraseConverter(config=self.config.phrase_converter)

        # LangGraphのワークフローを作成
        self.workflow = self._create_graph()

    def _create_graph(self):
        """LangGraphのグラフを定義し、各ノードと遷移を登録する"""
        workflow = StateGraph(State)

        # ワークフローノード（ステップ）を追加
        workflow.add_node("retrieval", self._retriever_node)
        workflow.add_node("select_faq", self._select_faq_node)
        workflow.add_node("review", self._review_node)
        workflow.add_node("select_candidates", self._select_candidates_node)
        workflow.add_node("replace_placeholder", self._replace_placeholder_node)

        # 処理の開始点を指定
        workflow.set_entry_point("retrieval")

        # 通常のノード遷移を定義
        workflow.add_edge("retrieval", "select_faq")

        # 抽出したFAQの処理フローの値に応じて条件分岐
        workflow.add_conditional_edges(
            "select_faq",
            lambda state: state.proc_pattern in ["2", "3"],
            {True: "review", False: "replace_placeholder"},
        )
        # workflow.add_edge("select_faq", "review")
        # reviewの結果に応じて条件分岐
        workflow.add_conditional_edges(
            "review",
            lambda state: any(review_result for review_result in state.review_result),
            {True: "replace_placeholder", False: "select_candidates"},
        )

        # select_candidates → replace_placeholder への遷移
        workflow.add_edge("select_candidates", "replace_placeholder")

        return workflow.compile()

    async def preprocess(self, query) -> dict[str, Any]:
        """クエリを前処理して、サブクエリ（部分質問）のリストを生成"""
        sub_queries = await self.aoai_handler.preprocess(
            query=query
        )  # 非同期処理（LLM使用）

        # サブクエリを自然な形に変換（ルールベースまたはLLMベースの変換）
        sub_queries = [
            self.phrase_converter.convert(text=sub_query) for sub_query in sub_queries
        ]
        return sub_queries

    async def _retriever_node(self, state: State) -> dict[str, Any]:
        """各サブクエリに対してベクトル検索を実施し、関連FAQドキュメントを取得"""
        retriever_docs = self.retriever.invoke(query=state.query)
        return {"retriever_docs": retriever_docs}

    async def _select_faq_node(self, state: State) -> dict[str, Any]:
        """各検索結果から最も適切なFAQ候補を1件選出"""
        selected_doc = await self.aoai_handler.select_faq(
            docs=state.retriever_docs,
            query=state.query,
            max_length=200,  # 非同期（LLM利用）
        )
        return {"selected_doc": selected_doc}

    def _doc_to_faq_id(self, doc):
        """FAQドキュメントからIDを構成"""
        return f'{doc.metadata["original_faq_filename"]}_{int(doc.metadata["faq_id"])}'

    async def _review_node(self, state: State) -> dict[str, Any]:
        """FAQ選定結果をレビューして妥当か判定。ID・本文・回答を抽出"""
        proc_pattern = str(int(state.selected_doc[0].metadata.get("pattern", 0)))
        review_result = await self.aoai_handler.review(
            query=state.query, doc=state.selected_doc[0]
        )

        return {"proc_pattern": proc_pattern, "review_result": review_result}

    async def _select_candidates_node(self, state: State) -> dict[str, Any]:
        """レビュー結果が「不適切」と判定された場合、候補FAQをさらに選出"""
        candidate_docs = await self.aoai_handler.select_candidates(
            query=state.query,
            docs=state.retriever_docs,
            doc=state.selected_doc,
        )
        return {"candidate_docs": candidate_docs}

    async def _replace_placeholder_node(self, state: State):
        """FAQの回答文中のプレースホルダーを顧客情報で置換"""
        # # プレースホルダー置換実行
        # state.selected_doc[0].metadata["answer"] = self.placeholder_replacer.replace(
        #     state.selected_doc[0].metadata["answer"]
        # )

        # 最終的なアウトプットをstateに格納
        predict_faq_ids = (
            self._doc_to_faq_id(state.selected_doc[0])
            if state.selected_doc[0]
            else None
        )
        predict_faqs = (
            state.selected_doc[0].page_content if state.selected_doc[0] else None
        )
        answers = state.selected_doc[0].metadata["answer"]
        return {
            "predict_faq_ids": predict_faq_ids,
            "predict_faqs": predict_faqs,
            "answers": answers,
        }

    async def ainvoke_multi(self, query: str):
        """クエリを前処理し、サブクエリごとにワークフローを順次実行する"""

        # クエリをサブクエリに分割
        sub_queries = await self.preprocess(query=query)

        # 各サブクエリに対してワークフローを個別実行
        results = []
        for sub_query in sub_queries:
            initial_state = State(query=sub_query)
            result = await self.workflow.ainvoke(initial_state)
            results.append(result)

        return results
