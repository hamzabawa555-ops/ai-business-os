# Deployment Guide for AI Business OS

## Prerequisites

- Docker & Docker Compose
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+

## Quick Start

### Backend Setup

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Set environment variables
cp .env.example .env

# Run migrations
alembic upgrade head

# Start server
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm start
```

## Docker Deployment

```bash
# Start services
docker-compose -f docker/docker-compose.dev.yml up -d

# Run migrations
docker-compose -f docker/docker-compose.dev.yml exec backend alembic upgrade head

# Check logs
docker-compose -f docker/docker-compose.dev.yml logs -f
```

## Production Deployment

See docs/DEPLOYMENT.md for comprehensive production deployment guide.

## Security Best Practices

See SECURITY.md for security guidelines and best practices.

## Troubleshooting

### Database Connection Issues
```bash
echo $DATABASE_URL
psql $DATABASE_URL
```

### Migration Issues
```bash
alembic current
alembic history
```

### Service Health Check
```bash
curl http://localhost:8000/health
```

## Support

- GitHub Issues: https://github.com/hamzabawa555-ops/ai-business-os/issues
- Community: https://github.com/hamzabawa555-ops/ai-business-os/discussions
- Email: support@aibusinessos.com
