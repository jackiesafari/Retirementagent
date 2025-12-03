# Florida Retirement Resources Multi-Agent System

A specialized AI framework built with Google's Agent Development Kit (ADK) to help Florida retirees navigate Medicare, Medicaid, and local resources. This multi-agent system provides accurate, empathetic assistance for complex retirement resource questions.

## 🎯 Overview

This system uses a **coordinator-agent architecture** where a central coordinator routes user queries to specialized agents:

- **Medicare Specialist**: Handles Medicare Parts A/B/C/D, enrollment, costs, and plan selection
- **Medicaid Specialist**: Assists with Florida Medicaid eligibility, applications, and long-term care
- **Local Resources Specialist**: Helps find healthcare facilities, housing, transportation, and senior centers

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────┐
│         Coordinator Agent (Main Entry Point)            │
│  Routes queries and coordinates between specialists     │
└──────────────┬──────────────────────────────────────────┘
               │
       ┌───────┼───────┐
       │       │       │
       ▼       ▼       ▼
┌──────────┐ ┌──────────┐ ┌──────────────┐
│ Medicare │ │ Medicaid │ │ Local        │
│ Agent    │ │ Agent    │ │ Resources    │
│          │ │          │ │ Agent        │
└────┬─────┘ └────┬─────┘ └──────┬───────┘
     │            │              │
     ▼            ▼              ▼
┌──────────┐ ┌──────────┐ ┌──────────────┐
│ Medicare │ │ Medicaid │ │ Local        │
│ Tools    │ │ Tools    │ │ Resources    │
│          │ │          │ │ Tools        │
└──────────┘ └──────────┘ └──────────────┘
```

### Components

#### 1. **Tools Layer** (`tools/`)
Specialized lookup functions that provide domain-specific information:

- **`medicare_tools.py`**: Medicare information and plan search
- **`medicaid_tools.py`**: Medicaid eligibility and information
- **`local_resources_tools.py`**: Local Florida resource finder

#### 2. **Agents Layer** (`agents/`)
Specialist agents that use tools to answer domain-specific questions:

- **`medicare_agent.py`**: Medicare specialist with Medicare tools
- **`medicaid_agent.py`**: Medicaid specialist with Medicaid tools
- **`local_resources_agent.py`**: Local resources specialist
- **`coordinator_agent.py`**: Main coordinator that routes to specialists

#### 3. **Application Layer** (`main.py`)
Main entry point with session management and interactive interface.

## 🚀 Getting Started

### Prerequisites

**Backend:**
- Python 3.12+
- Google ADK installed
- Virtual environment (recommended)

**Frontend:**
- Node.js 18+ and npm (or yarn)
- Expo CLI (installed globally or via npx)

### Installation

#### Backend Setup

1. **Activate your virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google ADK credentials:**
   - Follow [Google ADK setup instructions](https://github.com/google/adk)
   - Set your `GOOGLE_API_KEY` environment variable:
     ```bash
     export GOOGLE_API_KEY='your-actual-key'
     ```
   - Get your key from: https://aistudio.google.com/app/apikey

#### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd my-app
   ```

2. **Install frontend dependencies:**
   ```bash
   npm install
   ```
   or
   ```bash
   yarn install
   ```

### Running the Application

#### Option 1: Web Interface (Recommended)

This project includes a React Native/Expo frontend that provides a web-based chat interface.

1. **Start the backend API server** (in the root directory):
   ```bash
   # Make sure you're in the project root with venv activated
   uvicorn api_server_fixed:app --reload --port 8000
   ```
   The API will be available at `http://localhost:8000`

2. **Start the frontend** (in a new terminal):
   ```bash
   cd my-app
   npm start
   ```
   or
   ```bash
   cd my-app
   yarn start
   ```

3. **Access the application:**
   - Press `w` in the Expo terminal to open in web browser
   - Or scan the QR code with Expo Go app on your mobile device
   - The frontend will connect to the backend API at `http://localhost:8000/chat`

#### Option 2: Interactive CLI Mode

**Interactive Mode:**
```bash
python main.py
```

**Programmatic Usage:**
```python
from main import RetirementResourcesApp

app = RetirementResourcesApp()
response = app.chat("What are my Medicare options in Miami?")
print(response)
```

## 📋 Features

### Medicare Assistance
- Information about Medicare Parts A, B, C, and D
- Enrollment period guidance
- Cost and coverage explanations
- Plan comparison for Florida zip codes
- Medicare Advantage vs. Original Medicare
- Supplemental insurance (Medigap) information

### Medicaid Assistance
- Florida Medicaid eligibility information
- Income and asset limit guidance
- Application process assistance
- Long-term care Medicaid information
- Waiver programs and home/community-based services
- Preliminary eligibility assessments

### Local Resources
- Healthcare facility finder
- Housing resources (affordable, senior housing)
- Transportation services
- Senior centers and community resources
- Location-specific information for major Florida cities

## 🛡️ Safety & Limitations

### Important Disclaimers

⚠️ **This system provides informational guidance only. It is NOT a substitute for:**
- Official government determinations
- Medical advice from healthcare providers
- Legal advice from qualified attorneys
- Financial advice from certified advisors

### Safety Features

1. **Clear Disclaimers**: Agents always remind users to verify with official sources
2. **No Medical/Legal Advice**: System explicitly avoids providing medical or legal advice
3. **Professional Referrals**: Directs users to appropriate professionals when needed
4. **Official Source Links**: Always provides official government resources
5. **Preliminary Assessments Only**: Medicaid eligibility checks are clearly marked as preliminary

### Data Limitations

- **Mock Data**: Current implementation uses mock/sample data for demonstration
- **Production Integration**: In production, tools should connect to:
  - CMS (Centers for Medicare & Medicaid Services) APIs
  - Florida Medicaid databases
  - Official state and local resource directories

## 🔧 Configuration

### Model Selection

Default model: `gemini-2.5-flash-lite`

To use a different model for all agents:
```python
app = RetirementResourcesApp(model="gemini-2.5-flash-lite")
```

To use a different model specifically for the Medicaid agent (useful for tools like `google_search`):
```python
app = RetirementResourcesApp(
    model="gemini-2.5-flash-lite",          # Coordinator and other agents
    medicaid_model="gemini-2.0-flash-lite"  # Medicaid agent only
)
```

**Note:** The Medicaid agent includes the `google_search` tool. If you encounter errors with function calling, try using a tools-capable model (e.g., `gemini-2.5-flash`) for the `medicaid_model` parameter.

### Temperature Settings

Agents use conservative temperature settings:
- Medicare/Medicaid agents: `0.3` (more factual)
- Local Resources agent: `0.4` (slightly more flexible)
- Coordinator: `0.5` (balanced)

## 📁 Project Structure

```
Retirement agent framework/
├── main.py                 # Main application entry point
├── api_server_fixed.py     # FastAPI server for frontend integration
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── tools/                 # Tool functions
│   ├── __init__.py
│   ├── medicare_tools.py
│   ├── medicaid_tools.py
│   └── local_resources_tools.py
├── agents/                # Agent definitions
│   ├── __init__.py
│   ├── medicare_agent.py
│   ├── medicaid_agent.py
│   ├── local_resources_agent.py
│   └── coordinator_agent.py
└── my-app/                # React Native/Expo frontend
    ├── app/               # Expo Router app directory
    │   ├── index.tsx      # Home screen
    │   ├── chat.tsx       # Chat interface
    │   └── _layout.tsx    # App layout
    ├── package.json       # Frontend dependencies
    └── app.json          # Expo configuration
```

## 🔄 Extending the System

### Adding New Tools

1. Create a new tool function in `tools/`:
```python
def my_new_tool(query: str) -> str:
    """Tool description."""
    # Implementation
    return result
```

2. Add to `tools/__init__.py`:
```python
from .my_tools import my_new_tool
```

### Adding New Agents

1. Create agent file in `agents/`:
```python
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

def create_my_agent(model: str = "gemini-2.0-flash-exp") -> LlmAgent:
    agent = LlmAgent(
        name="my_agent",
        instruction="...",
        model=model,
        tools=[FunctionTool(my_new_tool)],
    )
    return agent
```

2. Add to coordinator in `agents/coordinator_agent.py`

## 📞 Official Resources

### Medicare
- **Website**: [medicare.gov](https://www.medicare.gov)
- **Phone**: 1-800-MEDICARE (1-800-633-4227)
- **Florida SHIP**: 1-800-963-5337

### Medicaid
- **Website**: [myflorida.com/accessflorida](https://www.myflorida.com/accessflorida)
- **Phone**: 1-866-762-2237
- **Agency**: Florida Agency for Health Care Administration (AHCA)

### Local Resources
- **Area Agency on Aging**: 1-800-963-5337
- **Florida Department of Elder Affairs**: [elderaffairs.org](https://elderaffairs.org)
- **Aging and Disability Resource Centers (ADRC)**: Contact local offices

## 🤝 Contributing

This is a demonstration framework. For production use:

1. Replace mock data with real API integrations
2. Add comprehensive error handling
3. Implement logging and monitoring
4. Add user authentication and privacy controls
5. Conduct thorough testing with real scenarios
6. Add compliance measures (HIPAA considerations for healthcare data)

## 📝 License

This project is provided as-is for educational and demonstration purposes.

## 🙏 Acknowledgments

Built with:
- [Google Agent Development Kit (ADK)](https://github.com/google/adk)
- [Google Gemini Models](https://ai.google.dev)

---

**⚠️ Remember**: This system provides guidance only. Always verify information with official sources and consult professionals for medical, legal, and financial decisions.

