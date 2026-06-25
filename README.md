# Smart Inventory Management System

## Project Overview

Smart Inventory Management System is a full-stack inventory tracking application developed using FastAPI, Angular, PostgreSQL, Docker, and AWS.

The application allows users to manage products, track stock movements, monitor inventory levels, and generate reports through a modern web interface.

---

## Features

### Authentication

* JWT-based authentication
* Secure login endpoint
* Protected APIs

### Product Management

* Add new products
* View product list
* Product SKU management
* Category management

### Inventory Movement

* Stock In
* Stock Out
* Quantity tracking
* Movement history

### Dashboard

* Total products overview
* Inventory summary
* Quick navigation

### Reports

* Inventory history
* Stock movement tracking
* Reorder monitoring

---

## Technology Stack

### Backend

* FastAPI
* Python
* PostgreSQL
* SQLAlchemy
* JWT Authentication

### Frontend

* Angular 20
* TypeScript
* HTML5
* CSS3

### DevOps & Cloud

* Docker
* AWS ECR
* AWS ECS (Fargate)
* GitHub

---

## Project Structure

```text
smart-inventory/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── dependencies/
│   │   ├── utils/
│   │   ├── database.py
│   │   ├── security.py
│   │   └── main.py
│   │
│   ├── scripts/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── angular.json
│   ├── package.json
│   └── tsconfig.json
│
└── README.md
```

---

## Backend Setup

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run FastAPI Server

```bash
python -m uvicorn app.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

## Frontend Setup

### Install Dependencies

```bash
npm install
```

### Run Angular Application

```bash
ng serve
```

Frontend URL:

```text
http://localhost:4200
```

---

## Docker

### Build Image

```bash
docker build -t smartinventory .
```

### Run Container

```bash
docker run -p 8000:8000 smartinventory
```

### Verify Running Containers

```bash
docker ps
```

---

## AWS Deployment

### Services Used

* Amazon Elastic Container Registry (ECR)
* Amazon Elastic Container Service (ECS)
* AWS Fargate
* Docker

### Deployment Steps

1. Build Docker image
2. Push image to ECR
3. Create ECS Cluster
4. Deploy ECS Service
5. Access application through ECS

---

## API Endpoints

### Authentication

```http
POST /api/auth/token
```

### Products

```http
GET /api/products
POST /api/products
```

### Movements

```http
GET /api/movements
POST /api/movements
```

### Reports

```http
GET /api/reports
```

---

## Screenshots Included

* Login Page
* Dashboard
* Product Management
* Swagger API Documentation
* Docker Container Running
* AWS ECR Repository
* AWS ECS Cluster

---

## GitHub Repository

Repository URL:

https://github.com/narayanadivya32-web/smart-inventory

---

## Author

Divya Narayana

Full Stack Inventory Management Assignment

Technologies Used:

* FastAPI
* Angular
* PostgreSQL
* Docker
* AWS ECR
* AWS ECS
* GitHub
