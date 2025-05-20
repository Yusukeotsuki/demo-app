# Copyright (c) 2024 Accenture. All Rights Reserved.
import os

from jpbchat.entities.config import AzureOpenAIConfig
from jpbchat.template.prompt import (
    PREPROCESS_PROMPT,
    ORGANIZE_INFORMATION_PROMPT,
    PREPROCESS_SYSTEM,
    REVIEW_PROMPT,
    REVIEW_SYSTEM,
    SECECT_FAQ_PROMPT,
    SECECT_FAQ_SYSTEM,
    SELECT_CANDIDATES_PROMPT,
    SELECT_CANDIDATES_SYSTEM,
    SELECT_SUB_ANSWER_PROMPT,
    SELECT_SUB_ANSWER_SYSTEM,
)
from langchain.embeddings.cache import CacheBackedEmbeddings
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings


class AzureOpenAIHandler:
    def __init__(self, config: AzureOpenAIConfig, store=None) -> None:
        self.config = config
        self.store = store
        self.embedding = self.build_embedding()
        self.llm = self.build_llm()

    def build_embedding(self):
        embedding = AzureOpenAIEmbeddings(
            # azure_deployment=os.getenv("EMBEDDING_DEPLOYMENT_NAME"),
            azure_deployment="gpt-4o-mini",
            # azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_endpoint="https://test-jpb.openai.azure.com/",
            # api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            # api_version=os.getenv("OPENAI_API_VERSION"),
            api_key="4KMb9GgqUHiLe4g6ei8Y4Tn5jM1NOZgTr8zGbbm90U5ej"
            "9YFA3IRJQQJ99BEACi0881XJ3w3AAABACOGRKaS",
            api_version="2024-12-01-preview",
            timeout=self.config.embedding.timeout,
            max_retries=self.config.embedding.max_retries,
        )
        if self.store:
            embedding = CacheBackedEmbeddings.from_bytes_store(
                embedding,
                self.store,
                namespace=embedding.model,
                batch_size=100,  # キャッシュを保存する間隔
            )
        return embedding

    def build_llm(self):
        return AzureChatOpenAI(
            # azure_deployment=os.environ["LLM_DEPLOYMENT_NAME"],
            # azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            # api_key=os.environ["AZURE_OPENAI_API_KEY"],
            # api_version=os.environ["OPENAI_API_VERSION"],
            azure_deployment="gpt-4o-mini",
            azure_endpoint="https://test-jpb.openai.azure.com/",
            api_key="4KMb9GgqUHiLe4g6ei8Y4Tn5jM1NOZgTr8zGbbm90U5ej"
            "9YFA3IRJQQJ99BEACi0881XJ3w3AAABACOGRKaS",
            api_version="2024-12-01-preview",
            temperature=self.config.llm.temperature,
            max_tokens=self.config.llm.max_tokens,
            timeout=self.config.llm.timeout,
            max_retries=self.config.llm.max_retries,
            frequency_penalty=self.config.llm.frequency_penalty,
            presence_penalty=self.config.llm.presence_penalty,
            stop=self.config.llm.stop,
            seed=self.config.llm.seed,
        )

    def invoke(self, system, prompt, variables):
        chat_template = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                ("human", prompt),
            ]
        )
        message = chat_template.format_messages(**variables)
        response = self.llm.invoke(message)
        return response

    async def ainvoke(self, system, prompt, variables):
        chat_template = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                ("human", prompt),
            ]
        )
        message = chat_template.format_messages(**variables)
        response = await self.llm.ainvoke(message)
        return response

    # ===============================
    # 情報整理エージェント
    # ===============================
    def organize_information(self, input):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("human", ORGANIZE_INFORMATION_PROMPT.strip()),
            ]
        )
        chain = prompt | self.llm | StrOutputParser()
        response = chain.invoke({"input": input})
        return response

    # ===============================
    # FAQ選定
    # ===============================
    def _select_faq_get_passages(self, docs, max_length=200):
        passages = ""
        for i, doc in enumerate(docs):
            content = f"Title: {doc.page_content}"
            content = content[: int(max_length)].strip()
            passages += f"[{i+1}] {content}\n\n"
        return passages

    async def select_faq(self, docs, query, max_length=200):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SECECT_FAQ_SYSTEM.strip()),
                ("human", SECECT_FAQ_PROMPT.strip()),
            ]
        )
        chain = prompt | self.llm | JsonOutputParser()
        response = await chain.ainvoke(
            {
                "passages": self._select_faq_get_passages(docs, max_length),
                "query": query,
                "num": len(docs),
            }
        )
        rank = response["result"]
        if len(rank) >= 1:
            sorted_rank = [i for i in rank if i in range((len(docs) + 1))]
            return [docs[i - 1] for i in sorted_rank]
        else:
            return []

    # ===============================
    # 回答レビュー
    # ===============================
    async def review(self, query, doc):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", REVIEW_SYSTEM.strip()),
                ("human", REVIEW_PROMPT.strip()),
            ]
        )
        chain = prompt | self.llm | JsonOutputParser()
        response = await chain.ainvoke(
            {
                "query": query,
                "faq_question": doc.page_content,
                "faq_answer": doc.metadata["answer"],
            }
        )
        if response["judgement_result"].lower() == "ng":
            response["judgement_result"] = False
        else:
            response["judgement_result"] = True
        return response

    # ===============================
    # 回答候補選定
    # ===============================
    async def select_candidates(self, docs, query, doc, max_length=200):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    SELECT_CANDIDATES_SYSTEM.strip(),
                ),
                (
                    "human",
                    SELECT_CANDIDATES_PROMPT.strip(),
                ),
            ]
        )
        chain = prompt | self.llm | JsonOutputParser()
        response = await chain.ainvoke(
            {
                "query": query,
                "num": len(docs),
                "passages": self._select_faq_get_passages(docs, max_length),
                "reviewed_question": doc.page_content,
            }
        )
        rank = response["result"]
        if len(rank) >= 1:
            sorted_rank = [i for i in rank if i in range((len(docs) + 1))]
            return [docs[i - 1] for i in sorted_rank]
        else:
            return []

    # ===============================
    # 更問い（回答粒度適正化）
    # ===============================
    def select_sub_answer(self, query, faq_answer, candidate_answer) -> str:
        # 回答テキストにある更問い内容の軸に対する内容がすでに問合せに含まれているかを確認する
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SELECT_SUB_ANSWER_SYSTEM.strip()),
                ("human", SELECT_SUB_ANSWER_PROMPT.strip()),
            ]
        )
        chain = prompt | self.llm | JsonOutputParser()
        response = chain.invoke(
            (
                {
                    "query": query,
                    "faq_answer": faq_answer,
                    "candidate_answer": candidate_answer,
                }
            )
        )
        response["result"] = response.get("result") != "No"
        return response
