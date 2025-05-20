from flask import Blueprint, jsonify, request
from flask import Blueprint, request, Response
import json
from app.orchestrator import run_all_agents
from app.entities.config import read_config

config = read_config("app/config/config.yaml")
from langchain.storage import LocalFileStore
from app.agents.agent_a import AgentA

store = LocalFileStore(config.indexer.cache_dir)


bp = Blueprint("main", __name__, url_prefix="/api")


@bp.route("/api/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    # Agent をインスタンス化
    agent = AgentA(config=config.azure_open_ai, store=store)
    reply = agent.run(user_input)
    reply = "AgentA :" + reply
    return jsonify({"reply": reply})


@bp.route("/chat_stream", methods=["GET"])  # ← GET を明示
def chat_stream():
    # クエリからユーザーメッセージを取る
    user_input = request.args.get("message", "")
    # user_input = request.json.get("message", "")

    agent = AgentA(config=config.azure_open_ai, store=store)

    def event_stream():
        # agent.stream() は delta テキストを逐次 yield するジェネレータ
        for delta in agent.stream(user_input):
            payload = json.dumps({"from": agent.name, "chunk": delta})
            yield f"data: {payload}\n\n"
        # ストリーム完了を通知
        yield "event: end\ndata: {}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")
