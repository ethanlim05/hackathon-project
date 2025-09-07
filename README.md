# Smart Vehicle Data Validation & Error Detection

> **One platform, two tools, one flow.**
>
> * A **customer-facing web onboarding** that validates inputs in real time and guides users through a clean, multi‑step flow.
> * A **Python validation engine** used by both the web backend and an **employee CLI** for operations.

---

## Table of contents

* [Overview](#overview)
* [Why it matters](#why-it-matters)
* [Architecture](#architecture)
* [Live Demo (local)](#live-demo-local)
* [Quick Start](#quick-start)

  * [Prerequisites](#prerequisites)
  * [1) Clone](#1-clone)
  * [2) Frontend (Vite + React)](#2-frontend-vite--react)
  * [3) Python Engine & Employee CLI](#3-python-engine--employee-cli)
* [Project Layout](#project-layout)
* [Frontend: Smart Onboarding](#frontend-smart-onboarding)

  * [Features](#features)
  * [How the plate check works](#how-the-plate-check-works)
  * [Local configuration](#local-configuration)
  * [i18n (EN/BM/中文)](#i18n-enbm中文)
* [Python Validation Engine](#python-validation-engine)

  * [Capabilities](#capabilities)
  * [Run modes](#run-modes)
* [Employee CLI](#employee-cli)
* [Data Files](#data-files)
* [Testing](#testing)
* [Troubleshooting](#troubleshooting)
* [FAQ](#faq)
* [License](#license)

---

## Overview

This project ships a **real‑time vehicle data validator** and a **streamlined insurance onboarding UI** that together reduce bad inputs (plate, brand, model, year), shrink time‑to‑quote, and lower back‑office correction effort.

### Components

1. **Frontend (Vite + React)**

   * Single‑page, expandable sections (Car Plate → Personal → Car → Funding)
   * Real‑time hints, soft validations, and modal confirmations (e.g., last 4 NRIC)
   * Language toggle: **EN / BM / 中文**
2. **Python Validation Engine (customer tool)**

   * Fuzzy matching (brand/model), plate regex checks, year windows
   * Batch processing + JSON results + auto‑correction pass
3. **Employee CLI (operations tool)**

   * Search, validate, and manage grants
   * Zero third‑party deps; standard library only

## Why it matters

Typos and loose validation push errors downstream: wrong quotes, delayed policies, avoidable support pings. We shift quality **left** with inline validation and guided confirmation steps.

---

## Architecture

```
Frontend (React) ──calls──> Backend API (stubbed/local for demo)
        │                         │
        └─────────────────────────┴──> Python Validation Engine
                                        └─ shared logic for CLI & batch
```

> In hackathon mode the frontend talks to mocked/stubbed endpoints that call directly into the Python engine or use local sample data. Swap the stubs with real API URLs later.

---

## Live Demo (local)

* **Frontend:** [http://localhost:5173](http://localhost:5173)
* **Employee CLI:** runs in terminal

---

## Quick Start

### Prerequisites

* **Git**
* **Python ≥ 3.8**
* **Node.js ≥ 18** and **npm**

  * Recommended: install via **nvm** (Node Version Manager)
  * macOS/Linux

    ```bash
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    # reload your shell then
    nvm install --lts
    nvm use --lts
    ```
  * Windows: use **nvm-windows** or install Node.js LTS from [https://nodejs.org](https://nodejs.org)

---

### 1) Clone

```bash
git clone https://github.com/ethanlim05/hackathon-project.git
cd hackathon-project
```

### 2) Frontend (Vite + React)

```bash
cd smart-onboarding
npm install
npm run dev    # starts Vite dev server on :5173
```

You should see the **BJAK** header, stepper (Car Plate → Personal → Car → Funding), and the benefits + footer sections.

**Common scripts**

```bash
npm run dev       # local dev
npm run build     # production build (dist/)
npm run preview   # preview the prod build
```

### 3) Python Engine & Employee CLI

Open a second terminal in the project root.

```bash
# Create a virtual environment
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

# Move to the customer tool
cd customer_tool
python -m pip install -r requirements.txt  # (if provided; otherwise stdlib only)

# Try the validator
python src/main.py --mode validate
python src/main.py --mode workflow

# Run the Employee CLI
cd ../../employee_tool
python main.py --mode init   # one-time data bootstrap
python main.py --mode cli    # interactive menu
```

---

## Project Layout

```
project-root/
├─ smart-onboarding/            # React app (frontend)
│  ├─ src/
│  │  ├─ components/            # Stepper, Accordion, Sections, Modals, Header, Footer
│  │  ├─ assets/                # Logo, icons
│  │  ├─ api.js                 # stubbed API hooks to Python logic/mock
│  │  ├─ i18n.js                # EN/BM/中文 translations
│  │  ├─ App.jsx / main.jsx
│  │  └─ styles.css
│  └─ vite.config.js
│
├─ customer_tool/               # Python validation engine
│  └─ src/ (core, utils, processing, workflows, tests)
│
└─ employee_tool/               # Python CLI for ops
   └─ src/ (core, utils, cli, config, tests)
```

---

## Frontend: Smart Onboarding

### Features

* **Single‑page flow** with expandable sections and a **top progress stepper**
* **Realtime plate check** → if matched, prompts for **last 4 NRIC** in a modal and **prefills personal info**
* **Context chips** under the plate field:

  * *No plate yet? Register new car*
  * *Use Passport instead of NRIC*
  * *Company car (SSM/BRN)*
* **Personal Info** supports **ID type** switch (NRIC / Passport / Business Reg No.)
* **Car Info** with brand/model/year validation hooks and auto‑correction suggestions (via engine)
* **Funding/Confirmation** with final summary
* **Benefits (6 cards)** and **full‑width footer** styled to match the brand
* **Language toggle** (EN/BM/中文) across the header and UI labels

### How the plate check works

1. User enters a plate → click **Verify**.
2. Frontend calls a local stub (`api.verifyPlate`) which consults sample data (or your API).
3. If found, show modal **“We found this vehicle”** → ask for **last 4 NRIC** → on success, prefill *Personal Info*.
4. If not found, continue as **new registration**.

### Local configuration

`smart-onboarding/src/api.js` contains stubbed functions. Replace with real endpoints when your backend is ready.

### i18n (EN/BM/中文)

* Language toggle component updates `lang` context.
* Labels are mapped via `i18n.js`. To add/rename keys, edit the dictionary once and use `t('key')` in components.

---

## Python Validation Engine

### Capabilities

* Plate regex validation (MY formats)
* Fuzzy matching for **brand** and **model** (custom Levenshtein + early exit)
* Year window checks (per model: `year_start`–`year_end`)
* Error typing: `typo_brand`, `typo_model`, `invalid_year`, `plate_format_error`, `invalid_brand`, `invalid_model`
* Auto‑suggest & auto‑correct modes

### Run modes

```bash
# From customer_tool/src
python main.py --mode validate    # run validator on sample dataset
python main.py --mode batch       # batch → JSON
python main.py --mode correct     # apply corrections
python main.py --mode workflow    # validate → correct → revalidate → compare
python main.py --mode test        # unit tests
```

---

## Employee CLI

**Menu:** View Car Models • Validate Vehicle Grant • Search Grants • Generate Report • Exit

```bash
# From employee_tool
python main.py --mode init   # seeds CSVs
python main.py --mode cli    # start TUI/CLI
```

---

## Data Files

* `car_dataset.csv` — canonical brand/model/year ranges
* `validation_dataset.csv` — noisy input samples for testing
* `car_models_list.csv` — (CLI) reference list
* `employee_credentials.csv`, `customer_data.csv`, `vehicle_grants.csv` — (CLI) operational data

> All CSVs are human‑readable; adjust or extend as needed for your demos.

---

## Testing

* **Frontend:** add React tests with Vitest/Jest as needed
* **Engine:** `python src/main.py --mode test`
* **CLI:** `python -m unittest tests.test_employee_tool`

---

## Troubleshooting

* **Vite shows a blank page**

  * Check the console for import errors
  * Ensure Node ≥ 18: `node -v`
* **Modal not closing / keyboard focus issues**

  * Verify component state and that only one modal is mounted
* **Python cannot import modules**

  * Activate venv and run from the correct folder (`customer_tool/src` or `employee_tool`)
* **Unicode paths on Windows**

  * Use absolute paths or run PowerShell as Admin

---

## FAQ

**Can I plug a real API instead of stubs?**
Yes. Replace `api.js` calls with your endpoints; keep the response shape.

**Do I need external ML/AI?**
No. The engine uses custom fuzzy matching and standard Python.

**How do I add another language?**
Add a new key (e.g., `id`) in `i18n.js`, translate the labels, and expose a toggle chip.

---

## License

MIT for hackathon/demo purposes unless superseded by sponsor requirements.
