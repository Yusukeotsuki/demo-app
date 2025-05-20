# Copyright (c) 2024 Accenture. All Rights Reserved.

from typing import List

import yaml
from pydantic import BaseModel, Field


class IndexerConfig(BaseModel):
    output_index_dir: str
    cache_dir: str
    batch_size: int = Field(..., ge=1, le=16)
    chunk_size: int = Field(..., ge=1)
    chunk_overlap: int = Field(..., ge=0)
    separators: List[str]


class RetrieverWeightsConfig(BaseModel):
    faiss: float = Field(..., ge=0, le=1)
    bm25: float = Field(..., ge=0, le=1)


class RetrieverConfig(BaseModel):
    input_index_dir: str
    retrieve_max_n: int = Field(..., ge=0)
    weights: RetrieverWeightsConfig


class RerankerConfig(BaseModel):
    max_chars: int = Field(..., ge=0)
    rerank_max_n: int = Field(..., ge=0)


class LLMConfig(BaseModel):
    temperature: float = Field(..., ge=0, le=2)
    max_tokens: int = Field(..., ge=0)
    timeout: float = Field(..., ge=0)
    max_retries: int = Field(..., ge=0)
    frequency_penalty: float = Field(..., ge=-2, le=2)
    presence_penalty: float = Field(..., ge=-2, le=2)
    stop: List[str]
    seed: int = Field(..., ge=0)


class EmbeddingConfig(BaseModel):
    timeout: float = Field(..., ge=0)
    max_retries: int = Field(..., ge=0)


class AzureOpenAIConfig(BaseModel):
    llm: LLMConfig
    embedding: EmbeddingConfig


class PhraseConverterConfig(BaseModel):
    conversion_dict_path: str
    sheet_name: str


class Config(BaseModel):
    indexer: IndexerConfig
    retriever: RetrieverConfig
    reranker: RerankerConfig
    phrase_converter: PhraseConverterConfig
    azure_open_ai: AzureOpenAIConfig


def read_config(path: str):
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return Config(**config)
