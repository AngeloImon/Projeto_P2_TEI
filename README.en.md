> 📘 Este README está disponível em: [🇧🇷 Português](README.md) | [🇺🇸 English](README.en.md)

# 📘 Special Topics in Computer Science — Study Planner Web App

Web application developed in Python using the **NiceGUI** library. It helps users organize their study plans through weekly scheduling, calendar-based planning, and data export functionality. The system is responsive, intuitive, and packed with integrated features.

---

## 🎯 Purpose

- Build an accessible interface for user registration and login.
- Enable study planning via calendar and day-of-week configurations.
- Manage multiple study plans in a visually interactive way.
- Import and export data for recorded plans.
- Display a dashboard showing plan summaries and usage metrics.

---

## 🧱 Project Structure

The project follows a modular design with components organized in the `Telas` folder, using a routing system for page navigation.

### Key Modules:

- `main.py` — Main file that initializes the interface and route system.
- `login.py` / `signup.py` — Authentication screens.
- `dashboard.py` — Overview of active study plans.
- `meus_planos.py` — Page listing user-created plans.
- `novo_plano.py` — Form for creating new study plans.
- `novo_plano_dias_semana.py` — Weekly-based plan configuration.
- `novo_plano_calendario.py` — Calendar-based plan setup.
- `sobre.py` — Institutional info and app details.
- `importar_exportar_dados_geral.py` — Full import/export handling.
- `importar_exportar_dados_individual.py` — Plan-specific data management.

Other helper files include utility functions and Firebase integration via `firebase_firestore.py`.

---

## 💻 Technologies Used

- 🐍 **Python**
- 🌐 **NiceGUI** (declarative web interface)
- 🧪 **dotenv** (environment variable handling)
- ☁️ **Firebase Firestore** (cloud data storage)
- 📦 Modular structure with routes and dynamic page loading

---

## 🧠 Features

- Authentication via login and signup screens
- Study plan creation with multiple configuration options:
  - Calendar-based
  - Day-of-week based
- Clean visualization using cards and stylized buttons
- Data export in structured format
- Responsive and intuitive UI with animations and gradients
- Standardized headers across all pages with fixed navigation links

---

## 📱 Landing Page Layout

- Header with title and quick access links
- Central card with system overview
- Login and signup buttons
- Explanatory Markdown text

