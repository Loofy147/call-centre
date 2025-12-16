# Algerian Voice Agent System - Complete Deployment Guide

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Deployment](#deployment)
6. [WhatsApp Integration](#whatsapp-integration)
7. [Monitoring & Scaling](#monitoring--scaling)
8. [Testing](#testing)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT CHANNELS                          │
│   WhatsApp │ Web Chat │ Phone Calls │ SMS │ Telegram        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    NGINX LOAD BALANCER                       │
│                     (SSL Termination)                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      FASTAPI SERVER                          │
│            (src/deployment_api.py - Multiple Instances)      │
└─────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┴───────────────────┐
        ↓                                         ↓
┌──────────────────┐                   ┌──────────────────┐
│  ASR PIPELINE    │                   │ AGENT CORE       │
│  (Whisper Model) │                   │ (LLM + NLU)      │
└──────────────────┘                   └──────────────────┘
        ↓                                         ↓
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│   Redis (Sessions) │ PostgreSQL (Logs) │ S3 (Audio Files)  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Prerequisites

### Software Requirements
- **Python 3.9+**
- **Docker & Docker Compose**
- **Redis 6.0+**
- **PostgreSQL 13+** (optional, for persistent storage)
- **NVIDIA GPU** (optional, for faster ASR)

### API Keys & Services
- **WhatsApp Business API** credentials
- **Twilio** (optional, for SMS)
- **Cloud storage** (AWS S3, Google Cloud Storage, or local)

---

## 🚀 Installation

### Step 1: Clone and Setup Repository

```bash
# Clone your existing repo
cd algerian-call-center-asr

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install additional dependencies for agent system
pip install fastapi uvicorn aioredis pydantic python-multipart
```

### Step 2: Download ASR Models

```bash
# Download Whisper models
python -c "
from transformers import WhisperProcessor, WhisperForConditionalGeneration
WhisperProcessor.from_pretrained('openai/whisper-small')
WhisperForConditionalGeneration.from_pretrained('openai/whisper-small')
"
```

### Step 3: Setup Redis

```bash
# Using Docker
docker run -d --name redis-agent -p 6379:6379 redis:latest

# Or install locally (Ubuntu/Debian)
sudo apt-get install redis-server
sudo systemctl start redis
```

---

## ⚙️ Configuration


### Environment Variables

Create `.env`:

```bash
# Environment
ENVIRONMENT=production

# Redis
REDIS_URL=redis://localhost:6379/0

# PostgreSQL (optional)
DATABASE_URL=postgresql://user:password@localhost:5432/agent_db

# WhatsApp
WHATSAPP_ACCESS_TOKEN=your_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_verify_token

# AWS S3 (for audio storage)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_S3_BUCKET=algerian-agent-audio

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret

# Monitoring
SENTRY_DSN=your_sentry_dsn  # optional
```

---

## 🐳 Docker Deployment

### Dockerfile

The `Dockerfile.agent` file defines the container image for the agent's API server. See the file for implementation details.

### Docker Compose

The `docker-compose.yml` file orchestrates the deployment of the entire system, including the API server, Redis, PostgreSQL, and NGINX. See the file for implementation details.

### NGINX Configuration

The `nginx.conf` file configures the NGINX load balancer. See the file for implementation details.

### Launch Services

```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f agent_api_1

# Scale API servers
docker-compose up -d --scale agent_api=4
```

---

## 📱 WhatsApp Integration

### Step 1: Setup WhatsApp Business API

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create a Business App
3. Add WhatsApp product
4. Get your credentials:
   - Phone Number ID
   - Business Account ID
   - Access Token

### Step 2: Configure Webhook

```bash
# Set webhook URL
curl -X POST "https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/webhook" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d "callback_url=https://your-domain.com/webhooks/whatsapp" \
  -d "verify_token=YOUR_VERIFY_TOKEN"
```

### Step 3: Test Integration

```python
# test_whatsapp.py
import requests

def send_test_message(phone_number, message):
    url = f"https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages"

    headers = {
        "Authorization": f"Bearer YOUR_ACCESS_TOKEN",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Test
result = send_test_message("+213XXXXXXXXX", "مرحبا! كيفاش نقدر نعاونك؟")
print(result)
```

---

## 📊 Monitoring & Scaling


### Health Checks

```bash
# Check API health
curl http://localhost:8000/health

# Check Redis
redis-cli ping

# Check database
psql -U agent_user -d agent_db -c "SELECT 1;"
```

### Log Aggregation

```yaml
# docker-compose.yml - add logging driver
services:
  agent_api_1:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 🧪 Testing

### Unit Tests

```python
# tests/test_agent.py
import pytest
from src.classifiers import AlgerianLanguageDetector, IntentClassifier

def test_language_detection():
    detector = AlgerianLanguageDetector()

    # Test Darija detection
    result = detector.detect("نحب ندير réservation غدوة")
    assert result.primary.value == "mixed"
    assert result.contains_darija == True
    assert result.contains_french == True

def test_intent_classification():
    classifier = IntentClassifier()

    # Test reservation intent
    intent = classifier.classify("نحب نحجز طاولة غدوة")
    assert intent.type.value == "reservation"
    assert intent.confidence > 0.5

# Run tests
pytest tests/ -v
```

### Integration Tests

```bash
# Test text message endpoint
curl -X POST http://localhost:8000/api/v1/message/text \
  -H "Content-Type: application/json" \
  -d '{
    "message": "نحب ندير réservation",
    "customer_id": "test_001",
    "tenant_id": "restaurant_001"
  }'

# Test voice message endpoint
curl -X POST http://localhost:8000/api/v1/message/voice \
  -F "audio=@sample_audio.wav" \
  -F "customer_id=test_001" \
  -F "tenant_id=restaurant_001"
```

### Load Testing

```python
# load_test.py
from locust import HttpUser, task, between

class AgentUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def send_message(self):
        self.client.post("/api/v1/message/text", json={
            "message": "نحب معلومات",
            "customer_id": f"test_{self.environment.runner.user_count}",
            "tenant_id": "restaurant_001"
        })

# Run: locust -f load_test.py --host=http://localhost:8000
```

---

## 🚀 Production Checklist

- [ ] SSL certificates configured
- [ ] Environment variables secured
- [ ] Database backups configured
- [ ] Redis persistence enabled
- [ ] Log rotation setup
- [ ] Monitoring dashboards created
- [ ] WhatsApp webhook verified
- [ ] Rate limiting implemented
- [ ] Load testing completed
- [ ] Documentation updated

---

## 📈 Scaling Strategies

### Horizontal Scaling

```bash
# Scale API servers
docker-compose up -d --scale agent_api=8

# Use Kubernetes for auto-scaling
kubectl autoscale deployment agent-api --min=2 --max=10 --cpu-percent=70
```

### Vertical Scaling

- Increase RAM for ASR models (4GB+ recommended)
- Use GPU instances for faster inference
- Optimize model quantization

### Caching Strategy

```python
# Implement response caching
@lru_cache(maxsize=1000)
def get_common_response(intent: str, language: str):
    # Cache frequently used responses
    pass
```

---

## 🔧 Troubleshooting

### Common Issues

**Issue**: High latency on voice processing
```bash
# Solution: Use GPU or optimize model
export CUDA_VISIBLE_DEVICES=0  # Use GPU
# Or switch to whisper-tiny for faster inference
```

**Issue**: Redis connection errors
```bash
# Check Redis status
docker-compose logs redis
# Restart Redis
docker-compose restart redis
```

**Issue**: WhatsApp webhook not receiving messages
```bash
# Verify webhook
curl -X GET "https://your-domain.com/webhooks/whatsapp?hub.verify_token=YOUR_TOKEN"
```

---

## 📚 Additional Resources

- [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp)
- [Whisper Model Documentation](https://github.com/openai/whisper)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Algerian Darija Resources](https://github.com/yourusername/algerian-darija-nlp)

---

## 📞 Support

For issues and questions:
- GitHub Issues: [your-repo]/issues
- Email: support@your-domain.com
- Slack: #algerian-agent-support
