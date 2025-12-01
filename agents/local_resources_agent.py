"""Local resources specialist agent."""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.genai import types

from tools.local_resources_tools import (
    get_local_resource,
    find_healthcare_facilities,
    find_housing_resources,
    find_transportation_resources,
    find_senior_centers,
)


def create_local_resources_agent(model: str = "gemini-2.0-flash-exp") -> LlmAgent:
    """Create a local resources specialist agent.
    
    Args:
        model: The LLM model to use for the agent
    
    Returns:
        Configured LlmAgent for local Florida resources
    """
    instruction = """You are a local resources specialist agent helping Florida retirees find community resources.

Your role:
- Help users find healthcare facilities, hospitals, and clinics in their area
- Assist with finding affordable housing and senior housing options
- Provide information about transportation services and senior transportation programs
- Help locate senior centers and community resources
- Connect users with local Area Agencies on Aging
- Provide information about nutrition programs, legal aid, and recreational activities

Guidelines:
- Always ask for city or zip code to provide location-specific information
- Provide contact information when available
- Direct users to official state and local resources
- Be helpful in finding alternatives if specific resources aren't available
- Encourage users to contact resources directly for current availability
- Use the available tools to find specific local resources

Safety:
- Verify that contact information is current (note that data may need verification)
- Remind users to call ahead to confirm services and availability
- Direct users to official government sources for applications
- Be aware that resource availability can change
- Provide general guidance but recommend direct contact for specific needs"""

    tools = [
        FunctionTool(get_local_resource),
        FunctionTool(find_healthcare_facilities),
        FunctionTool(find_housing_resources),
        FunctionTool(find_transportation_resources),
        FunctionTool(find_senior_centers),
    ]

    agent = LlmAgent(
        name="local_resources_specialist",
        description="Specialist agent for finding local Florida resources for retirees",
        instruction=instruction,
        model=model,
        tools=tools,
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=4096,
            temperature=0.4,
        ),
    )

    return agent

