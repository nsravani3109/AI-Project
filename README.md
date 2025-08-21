# Inbound Sales AI Agent

An AI-powered system for automating inbound carrier calls and load booking for freight brokerages.

## 🎯 Overview

This system handles inbound calls from carriers looking to book loads by:
- Verifying carrier credentials via FMCSA API
- Matching carriers to suitable loads
- Negotiating pricing automatically
- Transferring successful negotiations to sales representatives
- Providing comprehensive metrics and dashboards

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   HappyRobot    │    │   FastAPI        │    │   Dashboard     │
│   Platform      │◄───┤   Application    │◄───┤   (Dash)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                       ┌────────┴────────┐
                       │                 │
                ┌──────▼─────┐    ┌──────▼─────┐
                │  FMCSA     │    │  SQLite    │
                │  API       │    │  Database  │
                └────────────┘    └────────────┘
```

## 🚀 Features

### Core Functionality
- **Carrier Verification**: Real-time FMCSA MC number validation
- **Load Matching**: AI-powered load recommendation engine
- **Price Negotiation**: Automated negotiation with configurable parameters
- **Call Management**: Complete call lifecycle tracking
- **Sales Transfer**: Seamless handoff to human representatives

### Technical Features
- **RESTful API**: Comprehensive API with OpenAPI documentation
- **Real-time Dashboard**: Live metrics and call monitoring
- **Docker Support**: Full containerization for easy deployment
- **Security**: API key authentication and HTTPS support
- **Metrics & Analytics**: Detailed reporting on call outcomes and performance

## 📁 Project Structure

```
InboundSalesAiAgent/
├── src/                     # Core application code
│   ├── models.py           # Database models
│   ├── schemas.py          # Pydantic schemas
│   ├── database.py         # Database connection
│   ├── call_service.py     # Call handling logic
│   ├── load_service.py     # Load management
│   ├── fmcsa_service.py    # FMCSA API integration
│   ├── happyrobot_service.py # HappyRobot integration
│   └── security.py         # Authentication & security
├── config/                  # Configuration
│   └── settings.py         # Application settings
├── data/                   # Data files
│   └── sample_loads.json   # Sample load data
├── templates/              # HTML templates
├── static/                 # Static files
├── tests/                  # Test suite
├── main.py                 # FastAPI application
├── dashboard.py            # Dashboard application
├── init_data.py           # Database initialization
├── docker-compose.yml      # Docker composition
├── Dockerfile             # Container definition
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional)
- HappyRobot API account

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd InboundSalesAiAgent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   python init_data.py
   ```

6. **Run the application**
   ```bash
   # Start API server
   uvicorn main:app --reload --port 8000
   
   # Start dashboard (in another terminal)
   python dashboard.py
   ```

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the applications**
   - API: http://localhost:8000
   - Dashboard: http://localhost:8050
   - API Documentation: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | API authentication key | `default-api-key` |
| `SECRET_KEY` | JWT signing secret | `your-secret-key-here` |
| `DATABASE_URL` | Database connection string | `sqlite:///./loads.db` |
| `HAPPYROBOT_API_KEY` | HappyRobot API key | `None` |
| `FMCSA_API_BASE_URL` | FMCSA API endpoint | `https://mobile.fmcsa.dot.gov/qc/services/carriers` |
| `DEBUG` | Enable debug mode | `True` |

### HappyRobot Integration

1. **Set up your HappyRobot account**
2. **Configure webhook endpoint**: `http://your-domain/api/webhook/happyrobot`
3. **Update API key in environment variables**
4. **Initialize agent configuration**:
   ```bash
   python src/happyrobot_service.py
   ```

## 📊 API Documentation

### Authentication
All API endpoints require an API key in the header:
```
X-API-Key: your-api-key-here
```

### Key Endpoints

#### Load Management
- `POST /api/loads` - Create new load
- `GET /api/loads` - List available loads
- `GET /api/loads/search` - Search loads by criteria
- `GET /api/loads/{load_id}` - Get specific load

#### Call Handling
- `POST /api/calls/start` - Start new carrier call
- `GET /api/calls/{call_id}/loads` - Get suitable loads
- `POST /api/calls/{call_id}/negotiate` - Handle negotiation
- `POST /api/calls/{call_id}/end` - End call

#### Metrics
- `GET /api/metrics/calls` - Call performance metrics
- `GET /api/metrics/loads` - Load statistics

Full API documentation available at `/docs` when running the application.

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_main.py
```

## 📈 Metrics & Dashboard

The dashboard provides real-time insights into:

- **Call Performance**: Total calls, conversion rates, negotiation rounds
- **Sentiment Analysis**: Carrier satisfaction tracking
- **Load Management**: Available loads, booking rates, average pricing
- **System Health**: API status, response times, error rates

Access the dashboard at `http://localhost:8050`

## 🔒 Security Features

- **API Key Authentication**: Secure endpoint access
- **HTTPS Support**: SSL/TLS encryption (configure with valid certificates)
- **Input Validation**: Comprehensive request validation
- **Rate Limiting**: Protection against abuse (implement with Redis)
- **Audit Logging**: Complete call and transaction logging

## 🚀 Deployment

### Cloud Deployment Options

#### AWS Deployment
1. Use ECS or EKS for container orchestration
2. RDS for production database
3. ElastiCache for Redis
4. Application Load Balancer for traffic distribution
5. Route 53 for DNS management

#### Google Cloud Deployment
1. Cloud Run for serverless containers
2. Cloud SQL for database
3. Memorystore for Redis
4. Cloud Load Balancing

#### Azure Deployment
1. Container Instances or AKS
2. Azure Database for PostgreSQL
3. Azure Cache for Redis
4. Application Gateway

### Production Checklist
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set up SSL certificates
- [ ] Configure proper logging
- [ ] Set up monitoring and alerting
- [ ] Configure backup strategy
- [ ] Update security settings
- [ ] Set up CI/CD pipeline

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the API documentation at `/docs`

## 🔄 Changelog

### Version 1.0.0
- Initial release with core functionality
- FMCSA integration
- Basic negotiation engine
- Dashboard implementation
- Docker support
