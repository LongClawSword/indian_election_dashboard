# Indian Election Dashboard

## Project Overview
The Indian Election Dashboard is a full-stack application designed to provide insights and visualizations of Indian election data. It consists of a backend and a frontend, with a PostgreSQL database for data storage.

## Features
- **Backend**: Handles CRUD operations, data processing, and API endpoints.
- **Frontend**: Displays interactive dashboards and visualizations of election data.
- **Database**: Stores election data in a PostgreSQL database.

## Prerequisites
- Docker
- Docker Compose
- Python 3.8+

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/LongClawSword/indian_election_dashboard.git
cd indian_election_dashboard
```

### 2. Start the Application
Use Docker Compose to build and start the application:
```bash
docker-compose up --build
```

### 3. Access the Dashboard
Once the application is running, open your browser and navigate to:
```
http://localhost:8501/
```
## Backend
The backend is built with Python and uses FastAPI for creating RESTful APIs. It connects to a PostgreSQL database to store and retrieve election data.

### Key Files
- `main.py`: Entry point for the backend server.
- `crud.py`: Contains CRUD operations for the database.
- `models.py`: Defines the database schema.

## Frontend
The frontend is built with Python and uses libraries like Plotly and Dash to create interactive visualizations.

### Key Files
- `election_dashboard.py`: Main file for the frontend application.
- `india_states.geojson`: GeoJSON file for mapping state boundaries.

## Database
The PostgreSQL database stores the election data. Configuration files for the database are located in the `postgres_data/` directory.
