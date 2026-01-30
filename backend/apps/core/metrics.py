"""
Centralized Prometheus metrics for the Care Plan Generator.

This module defines all application metrics in one place for:
1. Easy discovery and documentation
2. Consistent naming conventions
3. Avoiding duplicate metric registration errors

Naming Convention (Prometheus best practices):
- <namespace>_<subsystem>_<name>_<unit>
- Example: careplan_order_create_duration_seconds

Metric Types:
- Counter: cumulative values that only increase (requests, errors)
- Gauge: values that can go up or down (active connections, queue size)
- Histogram: distribution of values (latency, response sizes)
- Summary: similar to histogram but calculates quantiles client-side
"""

from prometheus_client import Counter, Gauge, Histogram, Info

# =============================================================================
# APPLICATION INFO
# =============================================================================

APP_INFO = Info(
    "careplan_app",
    "Application information",
)

# =============================================================================
# ORDER METRICS
# =============================================================================

ORDER_CREATED_TOTAL = Counter(
    "careplan_order_created_total",
    "Total number of orders created",
    ["status"],  # success, validation_error, duplicate_blocked, duplicate_warning, error
)

ORDER_CREATE_DURATION_SECONDS = Histogram(
    "careplan_order_create_duration_seconds",
    "Time spent creating an order (API response time)",
    buckets=[0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

DUPLICATE_DETECTION_TOTAL = Counter(
    "careplan_duplicate_detection_total",
    "Duplicate detection results by type",
    ["entity_type", "result"],  # entity_type: patient/provider/order, result: exact_match/conflict/warning/none
)

# =============================================================================
# CARE PLAN GENERATION METRICS
# =============================================================================

CARE_PLAN_GENERATION_TOTAL = Counter(
    "careplan_generation_total",
    "Total care plan generation attempts",
    ["status"],  # success, error, already_exists, order_not_found
)

CARE_PLAN_GENERATION_DURATION_SECONDS = Histogram(
    "careplan_generation_duration_seconds",
    "Time spent generating care plans (including LLM call)",
    buckets=[1.0, 2.5, 5.0, 10.0, 20.0, 30.0, 60.0, 120.0],
)

CARE_PLAN_QUEUE_SIZE = Gauge(
    "careplan_queue_size",
    "Number of care plans pending generation",
)

CARE_PLAN_QUEUED_TOTAL = Counter(
    "careplan_queued_total",
    "Care plan generation tasks queued",
    ["status"],  # success, error
)

CARE_PLAN_RETRY_TOTAL = Counter(
    "careplan_retry_total",
    "Care plan generation retries",
)

# =============================================================================
# LLM METRICS
# =============================================================================

LLM_REQUEST_TOTAL = Counter(
    "careplan_llm_request_total",
    "Total LLM API requests",
    ["provider", "status"],  # provider: claude/openai/mock, status: success/error/timeout
)

LLM_REQUEST_DURATION_SECONDS = Histogram(
    "careplan_llm_request_duration_seconds",
    "LLM API request latency",
    ["provider"],
    buckets=[0.5, 1.0, 2.5, 5.0, 10.0, 20.0, 30.0, 60.0],
)

LLM_TOKENS_USED_TOTAL = Counter(
    "careplan_llm_tokens_total",
    "Total LLM tokens used",
    ["provider", "token_type"],  # token_type: prompt/completion
)

LLM_COST_DOLLARS_TOTAL = Counter(
    "careplan_llm_cost_dollars_total",
    "Estimated LLM cost in dollars",
    ["provider", "model"],
)

# =============================================================================
# API METRICS (per-endpoint)
# =============================================================================

API_REQUEST_TOTAL = Counter(
    "careplan_api_request_total",
    "Total API requests",
    ["method", "endpoint", "status_code"],
)

API_REQUEST_DURATION_SECONDS = Histogram(
    "careplan_api_request_duration_seconds",
    "API request duration",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

API_ERRORS_TOTAL = Counter(
    "careplan_api_errors_total",
    "Total API errors",
    ["method", "endpoint", "error_type"],  # error_type: validation/auth/server/timeout
)

# =============================================================================
# DATABASE METRICS
# =============================================================================

DB_QUERY_DURATION_SECONDS = Histogram(
    "careplan_db_query_duration_seconds",
    "Database query duration",
    ["operation"],  # select/insert/update/delete
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5],
)

# =============================================================================
# BUSINESS SLI METRICS (Service Level Indicators)
# =============================================================================

# SLI: What percentage of orders get care plans generated successfully?
CARE_PLAN_SUCCESS_RATE = Gauge(
    "careplan_success_rate",
    "Rolling success rate of care plan generation (SLI)",
)

# SLI: p95 latency for care plan generation
CARE_PLAN_P95_LATENCY_SECONDS = Gauge(
    "careplan_p95_latency_seconds",
    "p95 latency for care plan generation (SLI)",
)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

# LLM pricing per 1K tokens (as of 2024)
LLM_PRICING = {
    "claude-sonnet-4-20250514": {"input": 0.003, "output": 0.015},
    "claude-3-5-sonnet-20241022": {"input": 0.003, "output": 0.015},
    "claude-3-opus-20240229": {"input": 0.015, "output": 0.075},
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
}


def record_llm_cost(provider: str, model: str, prompt_tokens: int, completion_tokens: int):
    """
    Record LLM cost based on token usage.

    Args:
        provider: LLM provider (claude/openai)
        model: Model name
        prompt_tokens: Number of input tokens
        completion_tokens: Number of output tokens
    """
    pricing = LLM_PRICING.get(model, {"input": 0.01, "output": 0.03})  # Default pricing

    cost = (prompt_tokens / 1000 * pricing["input"]) + (completion_tokens / 1000 * pricing["output"])

    LLM_COST_DOLLARS_TOTAL.labels(provider=provider, model=model).inc(cost)


def init_app_info(version: str, environment: str):
    """Initialize application info metric."""
    APP_INFO.info({
        "version": version,
        "environment": environment,
    })
