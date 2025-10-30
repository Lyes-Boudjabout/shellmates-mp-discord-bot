# Task Manager Discord Bot

A modular task management system integrating a RESTful backend API with a Discord bot interface. This project was developed as part of the **Shellmates Integration Program**, showcasing team collaboration, containerized services, and API-bot communication.

---

## Overview

The **Task Manager Bot** combines:

* A **FastAPI backend** handling task CRUD operations and MongoDB persistence.
* A **Discord bot** enabling users to manage and interact with their tasks directly from Discord.

---

## Project Structure

```
task-manager-bot/
├── backend/         # FastAPI backend service
│   ├── api/
│   ├── database/
│   ├── main.py
│   ├── .env
│   └── requirements.txt
│
├── bot/             # Discord bot service
│   ├── cogs/
│   ├── utils/
│   ├── bot.py
│   ├── .env
│   └── requirements.txt
│
├── docs/            # Documentation resources
├── docker-compose.yml
├── .env.example
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

## Quick Start

### Clone the Repository

```bash
git clone https://github.com/Lyes-Boudjabout/shellmates-mp-discord-bot.git
cd shellmates-mp-discord-bot
```

### Run with Docker (Optional)

```bash
docker-compose up --build
```

---

## 👥 Team Members
- **Baghdadi Abderrahim Wael**
- **Lyes Boudjabout**
- **Bel Mohammed Wassim**   
- **Maaziz Adel Ayoub**
- **Takouk Abla**
- **Wail**

---

## 📜 License

Licensed under the **MIT License**.
© 2025 Shellmates Integration Program.
