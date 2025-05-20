from app.entities.config import AzureOpenAIConfig
from langchain.embeddings.cache import CacheBackedEmbeddings

from app.agents.base_agent import BaseAgent
from langchain.embeddings.cache import CacheBackedEmbeddings
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.chains import LLMChain


class AgentA(BaseAgent):
    def __init__(self, config: AzureOpenAIConfig, store=None):
        super().__init__(config, store)
        self.name = "Information_organizer"
        # プロンプトテンプレートを事前構築
        self.system = SystemMessagePromptTemplate.from_template(
            "あなたは銀行における融資業務を熟知した優秀な行員です。"
        )
        self.human = HumanMessagePromptTemplate.from_template(
            "ユーザーの問いかけ：{input}"
        )
        self.prompt = ChatPromptTemplate.from_messages([self.system, self.human])

    def run(self, input_text: str) -> str:
        # 同期実行（従来どおり）
        chain = self.prompt | self.llm | StrOutputParser()
        return chain.invoke({"input": input_text})

    def stream(self, input_text: str):
        """
        SSE 用に部分出力を行うジェネレータ。
        yield されるのはテキストの断片（delta）。
        """
        chain = LLMChain(llm=self.llm_stream, prompt=self.prompt)
        # ② chain.stream でジェネレートされたチャンクごとに回す
        for chunk in chain.stream(input=input_text):
            # chunk が dict か、それ以外（文字列）の場合を吸収
            if isinstance(chunk, dict) and "text" in chunk:
                delta = chunk["text"]
            else:
                # たとえば chunk が plain string の場合
                delta = getattr(chunk, "text", chunk)

            if delta:
                yield delta

    # # ===============================
    # # 情報整理エージェント
    # # ===============================
    # def organize_information(self, input):
    #     prompt = ChatPromptTemplate.from_messages(
    #         [
    #             ("human", ORGANIZE_INFORMATION_PROMPT.strip()),
    #         ]
    #     )
    #     chain = prompt | self.llm | StrOutputParser()
    #     response = chain.invoke({"input": input})
    #     return response
