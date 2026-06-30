#  Smart Inventory Management System

A full-stack Inventory Management System built using **FastAPI**, **Angular**, **PostgreSQL**, **Docker**, and **AWS**.

The application helps businesses efficiently manage products, track inventory movements, monitor stock levels, and generate inventory reports. The backend is containerized using Docker and deployed on **Amazon ECS (Fargate)** with the Docker image stored in **Amazon ECR**.

---

# Features

## Authentication

* JWT Authentication
* Secure Login
* Protected REST APIs

## Product Management

* Add Products
* View Products
* Update Inventory
* Category Management

## Inventory Management

* Stock In
* Stock Out
* Inventory Tracking
* Product Quantity Updates

## Reports

* Inventory Reports
* Movement History
* Stock Summary

## Dashboard

* Product Statistics
* Inventory Overview
* Quick Navigation

---

# 🛠 Technology Stack

## Backend

* FastAPI
* Python
* SQLAlchemy
* PostgreSQL
* JWT Authentication

## Frontend

* Angular 20
* TypeScript
* HTML5
* CSS3

## DevOps & Cloud

* Docker
* Amazon ECR
* Amazon ECS (Fargate)
* AWS Cloud

## Version Control

* Git
* GitHub

---

#  Project Structure

```text
smart-inventory
│
├── backend
│   ├── app
│   ├── scripts
│   ├── tests
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend
│   ├── src
│   ├── public
│   ├── package.json
│   └── angular.json
│
└── README.md
```

---

#  Backend Setup

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate

Windows

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Backend

```bash
python -m uvicorn app.main:app --reload
```

Backend

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

---

#  Frontend Setup

Install Packages

```bash
npm install
```

Run Angular

```bash
ng serve
```

Frontend

```
http://localhost:4200
```

---

#  Docker

Build Image

```bash
docker build -t smartinventory .
```

Run Container

```bash
docker run -p 8000:8000 smartinventory
```

Verify

```bash
docker ps
```

---

#  AWS Deployment

The application is deployed using:

* Amazon ECS (Fargate)
* Amazon ECR
* Docker

Deployment Flow

```
GitHub
      ↓
Docker Build
      ↓
Amazon ECR
      ↓
Amazon ECS
      ↓
Running Application
```

---

#  API Endpoints

Authentication

```
POST /api/auth/token
```

Products

```
GET /api/products
POST /api/products
```

Inventory

```
GET /api/movements
POST /api/movements
```

Reports

```
GET /api/reports
```

---

# 📷 Screenshots

* Login Page
* Dashboard
* Product Management
* Swagger Documentation
* Docker Running
* Amazon ECR
* Amazon ECS

---

# 🚀 Future Enhancements

* Role-Based Access Control (Admin, Manager, Employee)
* Deploy Frontend using AWS Amplify
* Amazon RDS Integration
* Barcode & QR Code Scanner
* Email Notifications
* Redis Caching
* GitHub Actions CI/CD
* AWS CloudWatch Monitoring
* Export Reports to Excel & PDF
* Dashboard Analytics
* HTTPS with Custom Domain

---

# 👩‍💻 Author

**Divya Narayan**

GitHub:
https://github.com/narayanadivya32-web/smart-inventory

Built using FastAPI, Angular, Docker and AWS.
