# 🎫 Customer Ticket Management System (CTMS)

A full-stack customer support ticketing platform built with **Streamlit**, **MySQL**, and **Google Cloud SQL**. This system enables users to create, track, and manage support tickets with real-time updates and admin-level insights.

📺 **Demo Video**: [Watch on YouTube](https://youtu.be/ElCBT0TnTz8?si=HcIeqPa98MFmKaDz)

---

## 🚀 Features

- 🔐 Role-based login: Admin & User views
- 📝 Create, update, and delete tickets
- 📊 Filter tickets by type, status, priority, and user
- 📄 Paginated views for better performance
- ☁️ Cloud-hosted MySQL (GCP Cloud SQL)
- 🔔 Toast notifications and intuitive Streamlit UI
- 🔍 Search and analytics-ready design

---

## 🧱 Tech Stack

- **Frontend & App**: Streamlit
- **Backend**: Python, SQLAlchemy
- **Database**: MySQL (Cloud SQL on GCP)
- **Authentication**: Session-based login
- **Infrastructure**: Google Cloud Platform

---

## 🗃️ Database Design

Structured into 4 normalized tables (up to 3NF):

1. **Users Table** – User info: name, email, age, gender
2. **Products Table** – Product details
3. **Sales Table** – Purchase logs linking users and products
4. **Tickets Table** – Ticket metadata, priority, type, timestamps, resolution

📄 [View full database design document](./database/CTMS%20-%20Database%20Design.pdf)

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/SandeepBatta/Customer-Ticket-management-System.git
cd Customer-Ticket-management-System/src
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Database Secrets
Create a `.streamlit/secrets.toml` file

```bash
[general]
hostname = "YOUR_DB_HOST"
user = "YOUR_DB_USER"
password = "YOUR_DB_PASSWORD"
database = "ctms"
```

### 4. Run the app

```bash
streamlit run app.py
```
