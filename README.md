# Shellmates Discord Bot — Events & CyberFacts

A modular Discord bot integrating a RESTful backend API for managing club events and sharing cybersecurity facts. Developed as part of the **Shellmates Integration Program**, this project demonstrates team collaboration, containerized services, and seamless API-bot communication.

---

## Overview

The **Shellmates Discord Bot** combines:

* A **FastAPI backend** handling CRUD operations for events and cybersecurity facts with MongoDB persistence.
* A **Discord bot** enabling users to view and manage events, retrieve cyber facts, and interact with the backend through slash commands.

---

## Project Structure

```
shellmates-discord-bot/
├── backend/         
│   ├── api/             # Event, Fact and Joke endpoints
│   ├── database/        # MongoDB configuration
│   ├── main.py          # Backend entrypoint
│   ├── app.py           # FastAPI app configuration
│   ├── Dockerfile
│   ├── .env.example
│   └── requirements.txt
│
├── bot/               
│   ├── bot.py           # Main bot with slash commands
│   ├── api_client.py    # Async API client for backend communication
│   ├── Dockerfile
│   ├── .env.example
│   └── requirements.txt
│
├── docs/                
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## Tech Stack

| Component            | Technology             |
| -------------------- | ---------------------- |
| **Backend**          | FastAPI, PyMongo       |
| **Bot**              | Discord.py             |
| **Database**         | MongoDB                |
| **Containerization** | Docker, Docker Compose |

---

## Features

* Display upcoming club events (`/events`).
* Add, Update or remove events (Admin only: `/add_event`, `/update_event`, `/remove_event`).
* Fetch random cybersecurity facts (`/cyberfact`).
* Add new facts (Admin only: `/add_fact`).
* Fetch random cybersecurity jokes (`/cyberjoke`).
* Add new jokes (Admin only: `/add_joke`).
* Fully async, API-driven architecture using `APIClient`.
* Slash commands only (no prefix commands).
* Logging, error handling, and permission checks for reliable operation.

---

## Shellmates Discord Bot Quick Start Guide

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Lyes-Boudjabout/shellmates-mp-discord-bot.git
cd shellmates-mp-discord-bot
```

---

### 2️⃣ Set Environment Variables

**Bot `.env` (`bot/.env`):**

```env
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
API_BASE_URL=YOUR_API_BASE_URL
```

**Backend `.env` (`backend/.env`):**

```env
MONGO_URI=YOUR_MONGO_URI
DB_NAME=YOUR_DB_NAME
PORT=YOUR_PORT
```

> ⚠️ Ensure that MongoDB is running locally or that your `MONGO_URI` points to a reachable MongoDB instance.

---

### 3️⃣ Install Python Dependencies And Run

**Bot:**

```bash
cd bot
python3 -m venv venv_bot
source venv_bot/bin/activate
pip install -r requirements.txt
python3 -m bot
```

**Backend:**

```bash
cd backend
python3 -m venv venv_backend
source venv_backend/bin/activate
pip install -r requirements.txt
uvicorn main:app
```

> 💡 Use separate virtual environments (which means 2 separate terminals) for bot and backend to avoid dependency conflicts.

---

* The bot will connect to Discord using your `DISCORD_TOKEN`.
* Slash commands (`/events`, `/add_event`, `/update_event`, `/remove_event`, `/cyberfact`, `/add_fact`, `/cyberjoke`, `/add_joke`) will be available in your server.

---

### 4️⃣ Optional: Using Docker

If you prefer a containerized setup, ensure Docker and Docker Compose are installed:

### Build Docker Images

```bash
docker-compose build
```

### Run All Services

```bash
docker-compose up
```

### Run in Detached Mode

```bash
docker-compose up -d
```

### Stop and Remove Containers

```bash
docker-compose down
```

### Check Logs

```bash
docker-compose logs -f backend
docker-compose logs -f bot
```

## Notes

* The bot communicates with the backend via the `API_BASE_URL`.
* MongoDB data is persisted via Docker volume `mongo_data`.
* `restart: unless-stopped` ensures auto-restart of containers.
* Logs are limited in size to avoid filling up disk space.

---

## Slash Commands

| Command         | Description                         | Permissions |
| --------------- | ----------------------------------- | ----------- |
| `/events`       | List all upcoming events            | Everyone    |
| `/add_event`    | Add a new event                     | Admin only  |
| `/update_event` | Update a new event                  | Admin only  |
| `/remove_event` | Remove an event                     | Admin only  |
| `/cyberfact`    | Display a random cybersecurity fact | Everyone    |
| `/add_fact`     | Add a new fact                      | Admin only  |
| `/cyberjoke`    | Display a random cybersecurity joke | Everyone    |
| `/add_joke`     | add a new joke                      | Admin only  |
| `/cyberquiz`    | Play a random cybersecurity quiz    | Everyone    |
| `/add_quiz`     | add a new quizz                     | Admin only  |
| `/help`         | Show all available commands         | Everyone    |

---

## Team Members

* **Baghdadi Abderrahim Wael**
* **Lyes Boudjabout**
* **Bel Mohammed Wassim**
* **Maaziz Adel Ayoub**
* **Takouk Abla**
* **Wail**

---

## License

Licensed under the **MIT License**.
© 2025 Shellmates Integration Program
