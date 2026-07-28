# Government Service Tracker

An enterprise-ready civic governance portal designed to solve public infrastructure information fragmentation caused by political devolution. This platform bridges the transparency gap by aggregating distributed regional data streams, tracking application processes using a rigid Finite State Machine, and alerting citizens of critical milestones through automated SMS and email hooks.

## Key Features

- **Unified Civic Service Registry:** Replaces dozens of fragmented, slow-loading legacy county web landing pages with a clean, centralized web workspace.
- **Autonomous Scraper Engine:** Uses a robust background worker pipeline to extract dates, rules, application guidelines, and PDF announcements from un-indexed public notices.
- **Dynamic Application Tracker:** Visualizes live document statuses using transparent progress tracking states (e.g., `Submitted`, `Under Review`, `Action Required`, `Approved`).
- **Proactive Notification Matrix:** Delivers real-time SMS alerts (via Africa's Talking or Twilio gateways) when file changes or deadlines approach.
- **Civic Accountability Dashboard:** Ranks regional offices transparently using automated Efficiency Indexes, benchmarking public administrative processing speeds.

## Tech Stack

### Frontend
- **React.js** (Functional architecture using Hooks and Context API)
- **Tailwind CSS** (Utility-first styling optimized for high performance and clean UI)
- **Lucide Icons** (Consistent structural iconography system)

### Backend & Workers
- **Python / Django REST Framework** or **Node.js (Express)**
- **Celery** (Distributed task queue pipeline handling delayed automation routines)
- **BeautifulSoup4 & Requests** (Flexible data extraction layer)

### Storage & Cache
- **PostgreSQL** (ACID-compliant relational engine for reliable auditing trails)
- **Redis** (In-memory broker handling message distribution queues and rapid data cache hits)

---

## Architecture Layout

```text
  [ React SPA Client ] <---> [ JWT Secure API Gateway ] <---> [ PostgreSQL DB ]
                                      |
                               [ Redis Broker ]
                                      |
                              [ Celery Workers ] <---> [ Public Web Scrapers ]
                                      |
                             [ Local SMS Gateway ]
```

---

## How to Clone & Project Setup

### Prerequisites
Before configuration, ensure you have the following environments installed locally:
- Git
- Python 3.10+ or Node.js v18+
- PostgreSQL
- Redis Server

### 1. Repository Retrieval
Clone the system code tree locally using terminal configurations:
```bash
git clone https://github.com/your-organization/county-service-tracker.git
cd county-service-tracker
```

### 2. Backend Environment Construction
Navigate to the service engine directory, establish a protected environment container, and install all required modules:
```bash
cd backend
python -m venv venv
source venv/scripts/activate  # On Windows use: venv\Scripts\activate

# Install essential execution libraries
pip install -r requirements.txt
```

Set up your environment variables file:
```bash
cp .env.example .env
```
Open the newly created `.env` file and input your local PostgreSQL access configurations, database names, and API keys.

Execute the relational database schema migrations and start the server:
```bash
python manage.py migrate
python manage.py runserver
```

### 3. Asynchronous Worker Execution
In a separate terminal instance within the active backend virtual environment, start the background tasks worker:
```bash
celery -A core worker --loglevel=info
```

### 4. Frontend Compilation Setup
Open an additional separate terminal window, access the client architecture repository, install required dependencies, and launch the web interface:
```bash
cd ../frontend
npm install
npm run dev
```
The interface will compile instantly and serve locally on `http://localhost:5173`.

---

## License

Distributed under the MIT License. See the block text layout below for legal authorization details:

MIT License

Copyright (c) 2026 Derick

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.