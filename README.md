# Care Plan Generator

A full-stack healthcare application that automates the generation of patient care plans using LLM technology. Built to help specialty pharmacies reduce the time spent on manual care plan creation from 20-40 minutes to seconds.

## Features

- **Patient Management** - Create and manage patient records with validation
- **Order Processing** - Submit orders with automatic duplicate detection for both patients and orders
- **LLM-Powered Generation** - Automatically generate professional care plans using Claude or OpenAI
- **File Export** - Download generated care plans and export data for reporting
- **Real-time Status** - Track order processing status with async task handling

## Tech Stack

### Backend
- **Framework**: Python, Django, Django REST Framework
- **Async Tasks**: Celery + Redis
- **Database**: PostgreSQL
- **LLM Integration**: Claude API / OpenAI API (with adapter pattern)

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: React Query (TanStack Query)
- **Form Handling**: React Hook Form + Zod validation

### DevOps & Observability
- **Containerization**: Docker, Docker Compose
- **Monitoring**: Prometheus + Grafana
- **Logging**: Loki + Promtail
- **Infrastructure**: Terraform (AWS)

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  React Frontend │────▶│  Django API     │────▶│  PostgreSQL     │
│  (TypeScript)   │     │  (DRF)          │     │                 │
│                 │     │                 │     └─────────────────┘
└─────────────────┘     └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │                 │     │                 │
                        │  Celery Worker  │────▶│  LLM Service    │
                        │                 │     │  (Claude/OpenAI)│
                        └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │     Redis       │
                        │  (Message Queue)│
                        └─────────────────┘
```

## Project Structure

```
.
├── backend/
│   ├── apps/
│   │   ├── care_plans/      # Care plan generation & LLM integration
│   │   ├── orders/          # Order processing & duplicate detection
│   │   ├── patients/        # Patient management
│   │   ├── providers/       # Healthcare provider management
│   │   ├── reports/         # Data export functionality
│   │   └── core/            # Shared utilities & middleware
│   ├── config/              # Django settings
│   └── tests/               # Backend tests
├── frontend/
│   └── src/
│       ├── components/      # Reusable UI components
│       ├── pages/           # Page components (Orders, NewOrder, OrderDetail)
│       ├── hooks/           # Custom React hooks
│       ├── services/        # API client
│       └── types/           # TypeScript type definitions
├── monitoring/              # Prometheus, Grafana, Loki configs
├── terraform/               # AWS infrastructure as code
└── docker-compose.yml       # Local development setup
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+

### 1. Clone and Setup Environment

```bash
git clone <repository-url>
cd careplan-generator

# Copy environment file
cp backend/.env.example backend/.env
# Add your LLM API key (ANTHROPIC_API_KEY or OPENAI_API_KEY)
```

### 2. Start Backend Services

```bash
docker-compose up -d
```

This starts:
- PostgreSQL database
- Redis message broker
- Django API server
- Celery worker
- Prometheus, Grafana, Loki (monitoring stack)

### 3. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Access the Application

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000/api |
| Grafana | http://localhost:3001 |
| Prometheus | http://localhost:9090 |

## Key Implementation Details

### LLM Service (Adapter Pattern)
The application uses an adapter pattern to support multiple LLM providers:

```python
# backend/apps/care_plans/llm_service.py
class BaseLLMService(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = None) -> LLMResponse:
        pass

class ClaudeLLMService(BaseLLMService): ...
class OpenAILLMService(BaseLLMService): ...
```

### Async Task Processing
Long-running LLM calls are handled asynchronously via Celery:

```python
# backend/apps/care_plans/tasks.py
@shared_task
def generate_care_plan_task(order_id: str):
    # Async care plan generation
```

### Duplicate Detection
Business logic to detect duplicate patients and orders before processing.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `LLM_PROVIDER` | `claude` or `openai` |
| `ANTHROPIC_API_KEY` | Claude API key |
| `OPENAI_API_KEY` | OpenAI API key |
| `DATABASE_URL` | PostgreSQL connection string |
| `CELERY_BROKER_URL` | Redis URL for Celery |
