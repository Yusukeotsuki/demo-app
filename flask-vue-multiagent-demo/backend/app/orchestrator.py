from app.agents.agent_a import AgentA

# from app.agents.agent_b import AgentB  # Add new agents here


def run_all_agents(input_text):
    agents = [
        AgentA("AgentA"),
        # AgentB("AgentB"),
    ]
    results = [agent.run(input_text) for agent in agents]
    return "\n".join(results)
