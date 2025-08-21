# Inbound Sales AI Agent - Architecture Diagram

## System Overview

```mermaid
graph TB
    subgraph "External Services"
        FMCSA[FMCSA API<br/>Carrier Verification]
        HR[HappyRobot AI<br/>Voice Platform]
        EL[External Loadboards<br/>Load Sources]
    end

    subgraph "Load Balancer & Proxy"
        NGINX[NGINX<br/>Reverse Proxy<br/>SSL Termination]
    end

    subgraph "Application Layer"
        FAST[FastAPI<br/>Main Application<br/>REST API]
        DASH[Dash Dashboard<br/>Analytics UI<br/>Port 8050]
    end

    subgraph "Service Layer"
        CS[Call Service<br/>call_service.py]
        LS[Load Service<br/>load_service.py]
        FS[FMCSA Service<br/>fmcsa_service.py]
        HRS[HappyRobot Service<br/>happyrobot_service.py]
        SEC[Security Service<br/>security.py]
    end

    subgraph "Data Layer"
        DB[(SQLite Database<br/>loads.db)]
        REDIS[(Redis Cache<br/>Session Storage)]
        MODELS[SQLAlchemy Models<br/>Load, Carrier, Call]
    end

    subgraph "Configuration & Utils"
        CONFIG[Configuration<br/>settings.py]
        SCHEMAS[Pydantic Schemas<br/>Request/Response Models]
    end

    %% External connections
    HR -.->|Webhooks| FAST
    FMCSA -.->|API Calls| FS
    EL -.->|Load Data| LS

    %% Load balancer
    NGINX --> FAST
    NGINX --> DASH

    %% Service interactions
    FAST --> CS
    FAST --> LS
    FAST --> FS
    FAST --> HRS
    FAST --> SEC

    CS --> FS
    CS --> LS
    CS --> HRS

    %% Data access
    CS --> DB
    LS --> DB
    FS --> DB
    HRS --> DB

    FAST --> REDIS
    CS --> REDIS

    %% Configuration
    FAST --> CONFIG
    FAST --> SCHEMAS
    CS --> SCHEMAS
    LS --> SCHEMAS
    FS --> SCHEMAS

    %% Models
    DB --> MODELS

    classDef external fill:#ffcccc
    classDef app fill:#ccffcc
    classDef service fill:#ccccff
    classDef data fill:#ffffcc
    classDef config fill:#ffccff

    class FMCSA,HR,EL external
    class NGINX,FAST,DASH app
    class CS,LS,FS,HRS,SEC service
    class DB,REDIS,MODELS data
    class CONFIG,SCHEMAS config
```

## Detailed Component Architecture

### 1. API Gateway & Load Balancing
- **NGINX**: Reverse proxy, SSL termination, static file serving
- **FastAPI**: Main application server with automatic OpenAPI documentation
- **CORS Middleware**: Cross-origin request handling

### 2. Core Services Architecture

```mermaid
graph LR
    subgraph "FastAPI Endpoints"
        LOAD_EP[Load Management<br/>/api/loads/*]
        CALL_EP[Call Handling<br/>/api/calls/*]
        CARR_EP[Carrier Management<br/>/api/carriers/*]
        METR_EP[Metrics<br/>/api/metrics/*]
        HOOK_EP[Webhooks<br/>/api/webhook/*]
    end

    subgraph "Business Logic Services"
        CALL_SVC[CallHandlingService<br/>• start_call()<br/>• find_and_pitch_loads()<br/>• handle_negotiation()<br/>• end_call()]
        LOAD_SVC[LoadService<br/>• create_load()<br/>• get_available_loads()<br/>• search_loads()<br/>• match_criteria()]
        FMCSA_SVC[FMCSAService<br/>• verify_carrier()<br/>• check_eligibility()<br/>• parse_response()]
        HR_SVC[HappyRobotService<br/>• initiate_call()<br/>• handle_webhook()<br/>• process_transcript()]
    end

    LOAD_EP --> LOAD_SVC
    CALL_EP --> CALL_SVC
    CARR_EP --> FMCSA_SVC
    METR_EP --> CALL_SVC
    METR_EP --> LOAD_SVC
    HOOK_EP --> HR_SVC

    CALL_SVC --> LOAD_SVC
    CALL_SVC --> FMCSA_SVC
    CALL_SVC --> HR_SVC
```

### 3. Data Model Architecture

```mermaid
erDiagram
    Load {
        string load_id PK
        string origin
        string destination
        datetime pickup_datetime
        datetime delivery_datetime
        string equipment_type
        float loadboard_rate
        enum status
        string notes
        int weight
        string commodity_type
        int num_of_pieces
        int miles
        string dimensions
        datetime created_at
        datetime updated_at
    }

    Carrier {
        string mc_number PK
        string legal_name
        string dba_name
        string entity_type
        string operating_status
        string out_of_service_date
        string phone
        string address
        datetime verified_at
        datetime created_at
        datetime updated_at
    }

    Call {
        int id PK
        string mc_number FK
        string load_id FK
        enum status
        enum outcome
        enum sentiment
        int negotiation_rounds
        float final_rate
        string notes
        datetime started_at
        datetime ended_at
        datetime created_at
        datetime updated_at
    }

    Negotiation {
        int id PK
        int call_id FK
        int round_number
        float carrier_offer
        float broker_counter
        boolean accepted
        string notes
        datetime created_at
    }

    Load ||--o{ Call : "matched_to"
    Carrier ||--o{ Call : "makes"
    Call ||--o{ Negotiation : "has"
```

### 4. Security Architecture

```mermaid
graph TD
    CLIENT[Client Request]
    
    subgraph "Security Layer"
        API_KEY[API Key Validation<br/>X-API-Key Header]
        CORS[CORS Middleware<br/>Cross-Origin Handling]
        RATE[Rate Limiting<br/>Request Throttling]
    end

    subgraph "Authentication Flow"
        HEADER[Extract API Key<br/>from Header]
        VALIDATE[Validate Against<br/>Settings]
        AUTHORIZE[Authorize Request<br/>or Reject]
    end

    CLIENT --> API_KEY
    API_KEY --> CORS
    CORS --> RATE
    RATE --> HEADER
    HEADER --> VALIDATE
    VALIDATE --> AUTHORIZE
    
    AUTHORIZE -->|Valid| APP[Application Logic]
    AUTHORIZE -->|Invalid| REJECT[HTTP 401 Unauthorized]
```

### 5. Dashboard Architecture

```mermaid
graph TB
    subgraph "Dashboard Components"
        DASH_APP[Dash Application<br/>Port 8050]
        
        subgraph "UI Components"
            METRICS_UI[Metrics Cards<br/>Call & Load Stats]
            CHARTS[Interactive Charts<br/>Plotly Graphs]
            TABLES[Data Tables<br/>Recent Activity]
            FILTERS[Filter Controls<br/>Date/Status Filters]
        end
        
        subgraph "Data Sources"
            API_CALLS[FastAPI Endpoints<br/>/api/metrics/*]
            DB_DIRECT[Direct Database<br/>Real-time Queries]
        end
    end

    DASH_APP --> METRICS_UI
    DASH_APP --> CHARTS
    DASH_APP --> TABLES
    DASH_APP --> FILTERS

    METRICS_UI --> API_CALLS
    CHARTS --> DB_DIRECT
    TABLES --> DB_DIRECT
    FILTERS --> DB_DIRECT
```

### 6. External Integration Flow

```mermaid
sequenceDiagram
    participant C as Carrier
    participant HR as HappyRobot
    participant API as FastAPI App
    participant FMCSA as FMCSA API
    participant DB as Database

    C->>HR: Incoming Call
    HR->>API: Webhook /api/webhook/happyrobot
    API->>FMCSA: Verify MC Number
    FMCSA-->>API: Carrier Data
    API->>DB: Store Carrier Info
    API->>DB: Query Available Loads
    DB-->>API: Matching Loads
    API->>HR: Send Load Options
    HR->>C: Present Loads
    C->>HR: Rate Negotiation
    HR->>API: POST /api/calls/{id}/negotiate
    API->>DB: Store Negotiation
    API-->>HR: Counter Offer
    HR->>C: Present Counter
    C->>HR: Accept/Reject
    HR->>API: Final Decision
    API->>DB: Update Call Status
```

## Technology Stack

### Backend Technologies
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **SQLite**: Lightweight database for development
- **Redis**: In-memory data structure store for caching

### Frontend Technologies
- **Dash**: Python web application framework
- **Plotly**: Interactive graphing library
- **HTML/CSS**: Static templates and styling

### External Services
- **FMCSA API**: Federal Motor Carrier Safety Administration
- **HappyRobot**: AI voice platform for call handling

### DevOps & Deployment
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **NGINX**: Web server and reverse proxy
- **pytest**: Testing framework

## Key Features

### 1. Automated Call Handling
- Inbound carrier call processing
- Real-time carrier verification via FMCSA
- Intelligent load matching based on equipment and routes
- Automated price negotiation with fallback to human transfer

### 2. Load Management
- RESTful API for load operations (CRUD)
- Advanced search and filtering capabilities
- Status tracking throughout load lifecycle
- Integration with external loadboards

### 3. Real-time Analytics
- Interactive dashboard with live metrics
- Call conversion tracking
- Load performance analysis
- Carrier sentiment monitoring

### 4. Security & Compliance
- API key authentication
- Request rate limiting
- CORS handling for web clients
- FMCSA compliance for carrier verification

### 5. Scalable Architecture
- Microservices-oriented design
- Containerized deployment
- Horizontal scaling capabilities
- Redis caching for performance

This architecture provides a robust, scalable solution for automating inbound carrier sales while maintaining compliance and providing comprehensive analytics.
