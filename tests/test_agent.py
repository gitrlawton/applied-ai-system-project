import time
import json
from langchain_core.messages import ToolMessage
from src.agent import agent, reset_agent_state


def test_agent_runs_all_steps():
    reset_agent_state()
    result = agent.invoke({"messages": [("user", "chill study music")]})
    step_names = [msg.name for msg in result["messages"] if isinstance(msg, ToolMessage)]

    assert "parse_intent"        in step_names
    assert "build_music_profile" in step_names
    assert "get_recommendations" in step_names
    assert "evaluate_results"    in step_names


def test_agent_returns_five_recommendations():
    time.sleep(2)
    reset_agent_state()
    result = agent.invoke({"messages": [("user", "high energy workout music")]})
    tool_messages = [msg for msg in result["messages"] if isinstance(msg, ToolMessage)]
    step_names = [msg.name for msg in tool_messages]

    assert "get_recommendations" in step_names

    recommendations = []
    for msg in reversed(tool_messages):
        if msg.name == "get_recommendations":
            recommendations = json.loads(msg.content)
            break

    assert len(recommendations) == 5
    assert all("title" in rec and "score" in rec for rec in recommendations)
