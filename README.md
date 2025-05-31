# Multi-Agent Document Processing System

A combined FastAPI backend and React frontend that allows users to upload documents (PDF, JSON, or Email), classifies them via Google Gemini, extracts relevant fields, and stores conversation memory in Redis.

---

## 📌 Features

* **Document Classification** via Google Gemini (format + intent).
* **JSON Extraction & Validation** (invoice\_id, amount, date).
* **Email Parsing & Extraction** (sender, subject, urgency, details).
* **Conversation Memory** stored in Redis (create/update/retrieve).
* **Responsive React Frontend** using plain CSS.

---

## 🛠 Prerequisites

* **Node.js & npm** (v14+)
* **Python 3.9+**
* **Docker Desktop** (for Redis)
* (Optional) **Git** for cloning/version control

---

## ⚙️ Backend Setup (FastAPI + Redis)

1. **Clone the repo (or create a folder)**

   ```bash
   git clone https://github.com/your-username/IngestIQ.git
   cd IngestIQ/app
   ```

2. **Create & activate a Python virtual environment**

   * Windows (PowerShell):

     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   * macOS/Linux:

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project root containing:

   ```
   GEMINI_API_KEY=<your-gemini-api-key>
   ```

5. **Start Redis via Docker**

   ```bash
   docker run -d --name redis-local -p 6379:6379 redis:7
   ```

6. **Verify Docker Redis is running**

   ```bash
   docker ps
   ```

7. **Start the FastAPI server**
   * From project root run :

   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

   * Check [http://localhost:8000/](http://localhost:8000/) → should return `{"message":"API Running!"}`.

---

## 🎨 Frontend Setup (React + Plain CSS)

1. **Open a new terminal** (not the one running FastAPI).

2. **Create the React app**

   ```bash
   cd IngestIQ
   npx create-react-app frontend
   cd frontend
   npm install
   ```

3. **Start the React app**

   ```bash
   npm start
   ```

   * The app will open at [http://localhost:3000](http://localhost:3000).

---

## 🔧 Environment Variables

* **.env** (placed at project root):

  ```
  GEMINI_API_KEY=<your-gemini-api-key>
  ```

---

## ▶️ Running the Backend

1. Activate Python virtual environment:

   * Windows:

     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   * macOS/Linux:

     ```bash
     source .venv/bin/activate
     ```

2. Start Uvicorn (FastAPI):

   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

3. Test with a browser or `curl`:

   ```
   http://localhost:8000/
   ```

   Should return:

   ```json
   {"message":"API Running!"}
   ```

---

## ▶️ Running the Frontend

1. Open a new terminal (don’t deactivate your Python venv).
2. Navigate to the React folder:

   ```bash
   cd frontend
   ```
3. Install dependencies (if not done):

   ```bash
   npm install
   ```
4. Start the React development server:

   ```bash
   npm start
   ```
5. Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📂 Project Structure

```
multi-agent-system/
├── app/                        # FastAPI backend
│   ├── agents/
│   │   ├── classifier_agent.py
│   │   ├── json_agent.py
│   │   └── email_agent.py
│   ├── memory/
│   │   ├── memory_manager.py
│   │   └── redis_client.py
│   ├── schemas.py
│   ├── utils.py
│   └── main.py
├── frontend/                   # React frontend
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── index.css
│   │   └── index.js
│   ├── package.json
│   └── README.md
├── .env                        # environment variables
└── README.md                   # this file
```

---

## 📖 Usage

1. **Backend** must be running on port 8000 (plus Redis on 6379).
2. **Frontend** runs on port 3000.
3. On the React UI:

   * Click “Choose File” → select a `.txt`, `.json`, or `.pdf`.
   * Click “Upload & Process.”
   * The right panel will display:

     * **Prediction Result** (format + intent or JSON extraction output).
     * **Memory Context** (Redis-stored entry).

---

## ⚠️ Troubleshooting

* **CORS Errors**
  Ensure FastAPI includes:

  ```python
  from fastapi.middleware.cors import CORSMiddleware

  app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )
  ```

* **Redis Connection Refused**

  * Verify Docker is running.
  * Run `docker ps` to confirm `redis-local` is up.
  * If not, start it:

    ```bash
    docker run -d --name redis-local -p 6379:6379 redis:7
    ```

* **Missing GEMINI\_API\_KEY**

  * Create a `.env` file at project root with:

    ```
    GEMINI_API_KEY=<your-key>
    ```
  * Restart Uvicorn.

* **Port Conflicts**

  * React: default 3000.
  * FastAPI: default 8000.
  * If needed, change with `npm start` (e.g. `PORT=4000 npm start`) or Uvicorn flags (`--port 9000`).

---

## 🤝 Contributing

1. Fork this repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add some feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

---

