##README.py
# TyTUX Token Management System

## Project Description

### Problem Statement
Supply chain issues like damaged products, incorrect deliveries, or delays require efficient token generation for tracking and resolution (e.g., refunds). Manual processes are error-prone, leading to inefficiencies.

### Domain Relevance (Logistics)
Automates complaint handling in logistics, improving trust and traceability—similar to e-commerce platforms like Amazon or FedEx.

### High-Level Architecture
- **Frontend**: HTML forms for role selection, login, and token creation (welcome, input, error, success pages).
- **Backend**: Flask app for routing, supplier authentication (encrypted CSV), and ticket generation.
- **Docker and Docker Compose** (for containerized runs): Download from [docker.com](https://www.docker.com/get-started). Verify with `docker --version` and `docker-compose --version`.
- **Data Layer**: CSV files (`suppliers.csv` for credentials, `tokens.csv` for issues); basic ASCII-shift encryption.
- **Workflow**: Users select roles, input details, and submit; data validates and stores.

### Assumptions and Limitations
- **Assumptions**: Basic web access; pre-stored supplier credentials; unique sequential tickets.
- **Limitations**: CSV-based (not scalable); basic encryption (use bcrypt for production); no sessions/auth; local-only; single-threaded. Integrate database for scalability.

## Features
- Customer token creation (email input).
- Supplier login (encrypted passwords).
- Token generation for damaged/incorrect/pending issues.
- Resolution options (cancellation, refund, replacement, date change).
- CSV storage for suppliers and tokens.

## Technologies Used
- **Backend**: Python, Flask
- **Frontend**: HTML
- **Data Storage**: CSV files

## Setup and Execution Instructions

### Prerequisites
- Python 3.6+ (for local runs)
- Git (to clone repo)

### Option 1: Run Locally
1. Clone: `git clone https://github.com/yourusername/TyTUX-Token-Management-System.git`
2. Navigate: `cd TyTUX-Token-Management-System`
3. Install: `pip install -r requirements.txt`
4. Run: `python TyTUX.py`
5. Open browser to `http://127.0.0.1:5000`

#### Option 2: Run with Docker Compose (Containerized)
Best for portability and production-like environments. Docker handles everything in an isolated container.
1. Ensure Docker and Docker Compose are installed and running.
2. Build and start the services: `docker-compose up --build`.
   - `--build` rebuilds the image if you've made code changes.
   - First run may take a few minutes to download the Python base image.
3. Check the terminal output: Look for "Running on http://0.0.0.0:5000/" inside the container logs.
4. Access the app in your browser at `http://localhost:5000`.
5. To stop: Press `Ctrl + C` or run `docker-compose down` in another terminal.
6. **Rebuilding After Changes**: If you edit code, run `docker-compose up --build` again to apply updates. Volumes ensure file changes are reflected.

**Note**: Docker runs the app in a container, so no local Python installation is needed. Data (e.g., CSV files) persists via mounted volumes.

### Usage
- Start at welcome page; choose customer/supplier; follow prompts to create tokens.
- Data stores in `tokens.csv` and `suppliers.csv`.

#### Navigating the Website
Open `http://127.0.0.1:5000` in browser. Site uses HTML forms.

**General Tips**
- Required inputs; errors redirect.
- Tokens save to `tokens.csv`; refresh for issues.

**Customer Token Creation (No Login)**
1. Click "Create Token".
2. Select "Customer".
3. Enter email.
4. Choose issue (Damaged/Incorrect/Pending).
5. Add sub-details.
6. Select resolution.
7. Submit; view ticket (e.g., "CM|DAM|REF").
8. Check `tokens.csv`; return home.

**Supplier Token Creation (Login Required)**
1. Click "Create Token".
2. Select "Supplier".
3. Log in (name/password from `suppliers.csv`); invalid shows error.
4. Choose issue, sub-details, resolution.
5. Submit; view ticket (e.g., "SP|PEN|REP").
6. Check `tokens.csv`; return home.

**Testing Tips**
- Create one customer/supplier token; verify in CSV.
- Test errors (wrong login/missing fields).
- Data persists; browser-compatible.

## Contributing
Fork and submit PRs. Use GitHub Issues for problems.

## License
MIT License.