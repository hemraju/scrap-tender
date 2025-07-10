# Tender Scraper Tool

## Features
- Scrapes tenders from Indian government sites (e.g., https://eprocure.gov.in)
- Categorizes tenders by user-defined categories (roads, canals, dams, PDN, etc.)
- Downloads and extracts content from tender documents (PDFs, ZIPs)
- Sends notifications (email, real-time via WebSocket)
- REST API for dashboard integration
- Web dashboard for visualization
- Easily extensible for new sites/categories

---

## Directory Structure
```
tender-scraper/
│
├── backend/
│   ├── main.py
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── eprocure.py
│   │   └── pdf_extractor.py
│   ├── categorizer.py
│   ├── notifier.py
│   ├── models.py
│   ├── database.py
│   └── config.py
│
├── frontend/
│   └── (React app for dashboard)
│
├── requirements.txt
└── README.md
```

---

## Backend Setup

1. **Install dependencies:**
    ```bash
    cd backend
    pip install -r ../requirements.txt
    ```
2. **Run FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
3. **API Docs:**
    - Visit [http://localhost:8000/docs](http://localhost:8000/docs)

4. **Scheduler Setup (Optional):**
    - To run the scraper periodically, add the following to `main.py`:
    ```python
    from apscheduler.schedulers.background import BackgroundScheduler
    from .main import scrape_and_store_tenders
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_and_store_tenders, 'interval', minutes=60)
    scheduler.start()
    ```
    - Or run as a cron job:
    ```bash
    0 * * * * cd /path/to/backend && /usr/bin/python3 main.py scrape
    ```

---

## Frontend Setup (React Dashboard)

1. **Create React app:**
    ```bash
    npx create-react-app frontend
    cd frontend
    npm install axios
    ```
2. **Configure API endpoint:**
    - Edit `src/api.js`:
    ```js
    import axios from 'axios';
    export const api = axios.create({ baseURL: 'http://localhost:8000' });
    ```
3. **Sample Dashboard Component:**
    - Create `src/TenderList.js`:
    ```jsx
    import React, { useEffect, useState } from 'react';
    import { api } from './api';
    export default function TenderList() {
      const [tenders, setTenders] = useState([]);
      useEffect(() => {
        api.get('/tenders').then(res => setTenders(res.data));
      }, []);
      return (
        <div>
          <h2>Tenders</h2>
          <ul>
            {tenders.map(t => (
              <li key={t.id}>
                <a href={t.url} target="_blank" rel="noopener noreferrer">{t.title}</a> [{t.category}]
                <br />{t.description.slice(0, 200)}...
                {t.document_path && <a href={`http://localhost:8000/files/${t.document_path}`} download>Download Doc</a>}
              </li>
            ))}
          </ul>
        </div>
      );
    }
    ```
4. **Add to App:**
    - Edit `src/App.js`:
    ```jsx
    import React from 'react';
    import TenderList from './TenderList';
    function App() {
      return <TenderList />;
    }
    export default App;
    ```
5. **Run React app:**
    ```bash
    npm start
    ```

---

## WebSocket Notifications (Optional)
- Add FastAPI WebSocket endpoint in backend for real-time updates.
- Use `socket.io-client` or native WebSocket in React to receive notifications.

---

## PDF/ZIP Extraction
- PDFs are parsed using `pdfplumber`.
- ZIPs can be extracted using Python's `zipfile` module (expand as needed).

---

## Extending
- Add new scrapers in `backend/scraper/` for other government sites.
- Update `config.py` for new categories.
- Enhance frontend for filtering, search, and visualization.

---

## License
MIT