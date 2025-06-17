# Fashion AI Search Platform

An intelligent fashion e-commerce platform that uses AI agents to understand customer preferences and provide personalized product recommendations with real-time justifications.

## Overview

This project combines a React frontend (`echo`) with a Python backend (`neuron`) to create an AI-powered fashion search experience. The system uses CrewAI to orchestrate multiple AI agents that refine search parameters, justify recommendations, and generate follow-up questions to better understand customer needs.

## Architecture

### Frontend (Echo)
- **Framework**: React + Vite

### Backend (Neuron)
- **Framework**: FastAPI
- **AI Engine**: CrewAI
- **Database**: Redis for session storage
- **Key Components**:
  - Multi-axis search refinement system
  - Conversational AI flow
  - Product filtering and recommendation engine

## Features

- 🤖 **AI-Powered Search**: Natural language queries converted to structured search parameters
- 💬 **Conversational Interface**: Follow-up questions to refine preferences
- 🔍 **Multi-Dimensional Filtering**: Search across category, price, size, fabric, fit, occasion, and more
- ⚡ **Real-time Responses**: Streaming AI responses with typing animations
- 🔄 **Session Management**: Persistent conversation history per user

## Search Axes

The AI system understands and refines searches across multiple dimensions:

- **Category**: tops, dresses, skirts, pants
- **Occasion**: party, vacation, everyday, work, evening
- **Sizes**: XS, S, M, L, XL
- **Fit**: slim, regular, loose, oversized, cropped, flowy
- **Fabric**: cotton, polyester, silk, wool, etc.
- **Style Details**: sleeve length, neckline, length, pant type
- **Price Range**: Min/max USD pricing

## Setup & Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- Redis server
- Ollama with Gemma 3:4b model

### Backend Setup (Neuron)

1. **Clone and navigate to the project**:
```bash
git clone <repository-url>
cd neuron
```

2. **Create virtual environment**:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set environment variables**:
```bash
export REDIS_URL="redis://localhost:6379"
export PRODUCTS_SQLITE3_DB_PATH="./db.sqlite3"
export PRODUCTS_TABLE_NAME="fashion_products"
```

5. **Set up Ollama**:
```bash
# Install Ollama (visit https://ollama.ai)
ollama pull gemma3:4b
ollama serve  # Start Ollama server on localhost:11434
```

6. **Initialize database**:
```bash
python scripts/ingest_fashion_products.py
```

7. **Start the API server**:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup (Echo)

1. **Navigate to frontend directory**:
```bash
cd echo
```

2. **Install dependencies**:
```bash
npm install
```

3. **Set environment variables**:
Create `.env` file:
```
VITE_APP_URL=http://localhost:8000
```

4. **Start development server**:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Usage

1. **Start a conversation**: Type natural language queries like "I need a dress for a wedding" or "Show me casual summer tops under $50"

2. **AI Processing**: The system will:
   - Parse your intent across multiple search dimensions
   - Filter products based on your criteria
   - Generate a justification for the recommendations
   - Ask follow-up questions to refine results

3. **Iterate**: Continue the conversation to narrow down results or explore different options

4. **Reset**: Use the "Flush" button to start a fresh session

## API Endpoints

- `POST /query` - Submit search queries
- `GET /conversation/{user_id}` - Retrieve conversation history
- `GET /products` - Fetch all products
- `POST /flush` - Clear user session

## Development

### Adding New Search Axes

1. Define the axis in `neuron/intelligence/axes/enum_axes.py`
2. Add to the axis registry in `neuron/intelligence/axes/__init__.py`
3. Update the search filtering logic in `neuron/search/explicit.py`

### Customizing AI Behavior

Modify prompts in:
- `neuron/intelligence/justification.py` - How AI explains recommendations
- `neuron/intelligence/followup.py` - How AI generates follow-up questions
- `neuron/intelligence/tasks/update_search_space.py` - How AI refines search parameters

## File Structure

```
├── echo/                     # React frontend
│   ├── src/
│   │   ├── components/       # UI components
│   │   ├── pages/           # Page components
│   │   └── assets/          # Static assets
├── neuron/                   # Python backend
│   ├── intelligence/        # AI agent system
│   │   ├── agents/         # CrewAI agents
│   │   ├── axes/           # Search dimension definitions
│   │   ├── crews/          # Agent orchestration
│   │   └── tasks/          # AI tasks
│   ├── search/             # Product search logic
│   └── server/             # API and data management
└── scripts/                # Utility scripts
```

## Technology Stack

**Frontend**:
- React 18
- Vite
- CSS3 with custom animations

**Backend**:
- FastAPI
- CrewAI
- Ollama (for development only) and OpenAI (production)
- SQLite
- Redis

**AI/ML**:
- Large Language Models for natural language processing
- Multi-agent conversation flows
- Structured output generation
