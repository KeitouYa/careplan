# Care Plan Generator - Healthcare Automation Platform

A full-stack healthcare application that automates patient care plan generation using LLM technology. Built to help specialty pharmacies reduce manual care plan creation time from **20-40 minutes to seconds**, improving efficiency and ensuring compliance with Medicare and pharmaceutical reporting requirements.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-4.x-green)
![React](https://img.shields.io/badge/React-18-61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)

---

## Features

### For Medical Assistants
- **Order Submission** - Input patient information, medications, and clinical records via validated web forms
- **Duplicate Detection** - Automatic warnings for duplicate patients and orders before processing
- **Real-time Status** - Track order processing status (Pending → Processing → Completed)
- **File Download** - Download generated care plans as formatted text files

### For Pharmacists
- **LLM-Generated Care Plans** - AI-powered generation of professional care plans with:
  - Problem list / Drug therapy problems (DTPs)
  - SMART goals
  - Pharmacist interventions
  - Monitoring plans & lab schedules
- **Manual Upload** - Option to upload custom care plans when needed
- **Data Export** - Export order data for Medicare and pharmaceutical reporting

### For System Administrators
- **Full Observability** - Prometheus metrics, Grafana dashboards, centralized logging
- **Infrastructure as Code** - Terraform configurations for AWS deployment
- **Containerized Deployment** - Docker Compose for consistent environments

---

## Tech Stack

### Backend

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Runtime environment |
| Django + DRF | REST API framework |
| Celery | Async task processing |
| Redis | Message broker & result backend |
| PostgreSQL | Relational database |
| Claude / OpenAI API | LLM integration (Adapter pattern) |
| structlog | Structured logging |
| Prometheus Client | Metrics collection |

### Frontend

| Technology | Purpose |
|------------|---------|
| React 18 + TypeScript | UI framework with type safety |
| Vite | Build tool & dev server |
| TailwindCSS | Utility-first styling |
| React Query (TanStack) | Server state management & caching |
| React Router v6 | Client-side routing |
| React Hook Form + Zod | Form handling & validation |
| Lucide React | Icon library |

### DevOps & Observability

| Technology | Purpose |
|------------|---------|
| Docker + Docker Compose | Containerization |
| Prometheus | Metrics collection |
| Grafana | Visualization dashboards |
| Loki + Promtail | Log aggregation |
| Terraform | Infrastructure as Code (AWS) |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Frontend                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                       │
│  │  OrdersPage  │  │ NewOrderPage │  │  DetailPage  │                       │
│  │  (List View) │  │   (Form)     │  │ (Care Plan)  │                       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                       │
│         └─────────────────┼─────────────────┘                               │
│                           │                                                  │
│              ┌────────────┴────────────┐                                    │
│              │   React Query + Axios   │                                    │
│              │      API Layer          │                                    │
│              └────────────┬────────────┘                                    │
└──────────────────────────┼──────────────────────────────────────────────────┘
                           │ HTTP/REST
┌──────────────────────────┼──────────────────────────────────────────────────┐
│                          ▼              Backend                              │
│             ┌────────────────────────┐                                      │
│             │   Django REST Framework │                                      │
│             │       ViewSets          │                                      │
│             └────────────┬────────────┘                                      │
│                          │                                                   │
│    ┌─────────────────────┼─────────────────────┐                            │
│    │                     │                     │                            │
│    ▼                     ▼                     ▼                            │
│ ┌──────────┐      ┌────────────┐       ┌─────────────┐                      │
│ │ Duplicate│      │  Celery    │       │  Prometheus │                      │
│ │ Detection│      │  Worker    │       │   Metrics   │                      │
│ └──────────┘      └─────┬──────┘       └─────────────┘                      │
│                         │                                                    │
│                         ▼                                                    │
│              ┌─────────────────────┐                                        │
│              │    LLM Service      │                                        │
│              │  (Adapter Pattern)  │                                        │
│              │ ┌───────┐ ┌───────┐ │                                        │
│              │ │Claude │ │OpenAI │ │                                        │
│              │ └───────┘ └───────┘ │                                        │
│              └─────────────────────┘                                        │
│                                                                              │
│    ┌──────────┐    ┌──────────┐    ┌──────────┐                             │
│    │PostgreSQL│    │  Redis   │    │  Loki    │                             │
│    │    DB    │    │  Queue   │    │  Logs    │                             │
│    └──────────┘    └──────────┘    └──────────┘                             │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
careplan-generator/
├── backend/                          # Django backend
│   ├── apps/
│   │   ├── care_plans/              # Care plan generation
│   │   │   ├── llm_service.py       # LLM adapter (Claude/OpenAI)
│   │   │   ├── tasks.py             # Celery async tasks
│   │   │   ├── prompts.py           # LLM prompt templates
│   │   │   └── skeleton_analyzer.py # Dynamic prompt optimization
│   │   ├── orders/                  # Order management
│   │   │   ├── duplicate_detection.py
│   │   │   └── services.py
│   │   ├── patients/                # Patient records (MRN, diagnoses)
│   │   ├── providers/               # Healthcare providers (NPI validation)
│   │   ├── reports/                 # Data export functionality
│   │   └── core/                    # Shared utilities, validators
│   ├── config/                      # Django settings
│   └── tests/                       # pytest test suite
│
├── frontend/                         # React frontend
│   └── src/
│       ├── components/
│       │   ├── ui/                  # Button, Input, Select, etc.
│       │   ├── forms/               # FormField components
│       │   └── modals/              # DuplicateWarningModal
│       ├── pages/
│       │   ├── OrdersPage.tsx       # Order list with status
│       │   ├── NewOrderPage.tsx     # Order creation form
│       │   └── OrderDetailPage.tsx  # Care plan viewer
│       ├── hooks/                   # useOrders (React Query)
│       ├── services/                # API client (Axios)
│       ├── types/                   # TypeScript interfaces
│       └── utils/                   # Validators (Zod schemas)
│
├── monitoring/                       # Observability stack
│   ├── prometheus.yml               # Metrics scraping config
│   ├── grafana/                     # Dashboard provisioning
│   ├── loki.yml                     # Log aggregation config
│   └── promtail.yml                 # Log shipping config
│
├── terraform/                        # AWS infrastructure
│   └── main.tf                      # EC2, RDS, S3, SQS, Lambda
│
└── docker-compose.yml               # Local development stack
```

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- LLM API Key (Anthropic Claude or OpenAI)

### 1. Clone and Configure

```bash
git clone <repository-url>
cd careplan-generator

# Copy environment template
cp backend/.env.example backend/.env
```

Edit `backend/.env` and add your API key:
```env
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=your-api-key-here
# Or for OpenAI:
# LLM_PROVIDER=openai
# OPENAI_API_KEY=your-api-key-here
```

### 2. Start Backend Services

```bash
docker-compose up -d
```

This starts:
| Service | Port | Description |
|---------|------|-------------|
| PostgreSQL | 5432 | Database |
| Redis | 6379 | Message broker |
| Backend API | 8000 | Django REST API |
| Celery Worker | - | Async task processor |
| Prometheus | 9090 | Metrics |
| Grafana | 3001 | Dashboards |
| Loki | 3100 | Log aggregation |

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
| Backend API | http://localhost:8000/api/v1 |
| Grafana | http://localhost:3001 (admin/admin) |
| Prometheus | http://localhost:9090 |

---

## API Endpoints

### Providers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/providers/` | List all providers |
| POST | `/api/v1/providers/` | Create provider |
| GET | `/api/v1/providers/{id}/` | Get provider details |

### Patients
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/patients/` | List all patients |
| POST | `/api/v1/patients/` | Create patient |
| GET | `/api/v1/patients/{mrn}/` | Get patient by MRN |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/orders/` | List all orders |
| POST | `/api/v1/orders/` | Create order (triggers care plan generation) |
| GET | `/api/v1/orders/{id}/` | Get order details |

### Care Plans
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/care-plans/by-order/{order_id}/` | Get care plan by order |
| GET | `/api/v1/care-plans/status/{order_id}/` | Check generation status |
| GET | `/api/v1/care-plans/download/{order_id}/` | Download care plan file |
| POST | `/api/v1/care-plans/upload/{order_id}/` | Upload custom care plan |

### Reports
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/export/` | Export all data (CSV) |

---

## Key Implementation Highlights

### 1. LLM Service with Adapter Pattern

Supports multiple LLM providers with a unified interface:

```python
# backend/apps/care_plans/llm_service.py
class BaseLLMService(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = None) -> LLMResponse:
        pass

class ClaudeLLMService(BaseLLMService):
    def generate(self, prompt: str, system_prompt: str = None) -> LLMResponse:
        message = self.client.messages.create(
            model=self.model,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        return LLMResponse(content=message.content[0].text, ...)

# Factory pattern for provider selection
def get_llm_service() -> BaseLLMService:
    provider = settings.LLM_PROVIDER.lower()
    if provider == "claude":
        return ClaudeLLMService()
    elif provider == "openai":
        return OpenAILLMService()
```

### 2. Async Task Processing with Celery

Long-running LLM calls are processed asynchronously with automatic retry:

```python
# backend/apps/care_plans/tasks.py
@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=60,           # Exponential backoff starting at 60s
    retry_backoff_max=600,      # Max 10 minutes between retries
    max_retries=3,
)
def generate_care_plan(self, order_id: str):
    order = Order.objects.get(id=order_id)
    order.status = "processing"
    order.save()

    llm_service = get_llm_service()
    response = llm_service.generate(prompt, system_prompt)

    CarePlan.objects.create(order=order, content=response.content)
    order.status = "completed"
    order.save()
```

### 3. Duplicate Detection with Hash-Based Matching

```python
# backend/apps/orders/duplicate_detection.py
def check_duplicate_order(patient_mrn, medication_name, provider_npi):
    hash_input = f"{patient_mrn}:{medication_name}:{provider_npi}"
    duplicate_hash = hashlib.sha256(hash_input.encode()).hexdigest()

    existing = Order.objects.filter(duplicate_check_hash=duplicate_hash)
    return existing.exists()
```

### 4. Form Validation with Zod + React Hook Form

```typescript
// frontend/src/utils/validators.ts
export const orderFormSchema = z.object({
  patientMrn: z.string().length(6, "MRN must be 6 digits"),
  providerNpi: z.string().length(10).refine(isValidNPI, "Invalid NPI"),
  primaryDiagnosisCode: z.string().regex(/^[A-Z]\d{2}/, "Invalid ICD-10"),
  // ...
});

// frontend/src/pages/NewOrderPage.tsx
const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(orderFormSchema),
});
```

### 5. Prometheus Metrics for Observability

```python
# Custom metrics for care plan generation
CARE_PLAN_GENERATION_TOTAL = Counter(
    "care_plan_generation_total",
    "Total care plan generation attempts",
    ["status"],  # success, error, already_exists
)
CARE_PLAN_GENERATION_DURATION = Histogram(
    "care_plan_generation_duration_seconds",
    "Time spent generating care plans",
)
LLM_TOKENS_USED = Counter(
    "llm_tokens_used_total",
    "Total LLM tokens used",
    ["type"],  # prompt, completion
)
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | - |
| `DEBUG` | Debug mode | `False` |
| `DATABASE_URL` | PostgreSQL connection | - |
| `CELERY_BROKER_URL` | Redis URL | - |
| `LLM_PROVIDER` | `claude` or `openai` | `claude` |
| `ANTHROPIC_API_KEY` | Claude API key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `LLM_MODEL` | Model name | `claude-3-sonnet-20240229` |
| `LLM_MAX_TOKENS` | Max response tokens | `4096` |
| `LLM_TEMPERATURE` | Generation temperature | `0.3` |

---

## Data Models

### Patient
```
Patient
├── id (UUID)
├── mrn (6-digit unique)
├── first_name, last_name
├── date_of_birth, sex, weight_kg
├── allergies
├── primary_diagnosis_code (ICD-10)
└── diagnoses[] (additional ICD-10 codes)
    └── medication_history[]
```

### Order
```
Order
├── id (UUID)
├── patient (FK)
├── provider (FK)
├── medication_name
├── patient_records (clinical notes)
├── status (pending/processing/completed/failed)
├── duplicate_check_hash (SHA256)
└── care_plan (1:1)
```

---

Built with Django, React, and modern cloud-native technologies.
