# 🌾 KisanSetu (किसान सेतु)
> **AI Public Service Portal • Independent Prototype**
> *Built for the "Build What Moves India" Hackathon by Varun Mayya x OpenAI*

KisanSetu replaces multi-step forms, dense drop-down menus, and technical jargon on Indian government public agricultural portals (like PM-Kisan) with a direct, natural-language interface.

Citizens can query their welfare installment status or pending action items via voice/text prompts and receive instant, visual status cards.

---

## ✨ Key Features
* **Conversational Query Processing:** Parses unstructured Hindi/English citizen inputs into actionable intent.
* **OpenAI Function Calling Agent:** Autonomously extracts identifiers (e.g., mock Aadhaar tokens or phone numbers) and triggers backend tools.
* **Instant Citizen Status Cards:** Generates human-readable visual status cards highlighting active payments or pending e-KYC/Aadhaar-bank linking requirements.
* **Privacy-First & Isolated:** Runs on a local SQLite database with 100% synthetic mock data, ensuring zero reliance on live production infrastructure or exposure of real PII.

---

## 🛠️ Tech Stack
* **AI Engine:** OpenAI API (`gpt-4o` / `gpt-4o-mini`) via Function Calling
* **Backend:** Python, FastAPI, Uvicorn
* **Database:** SQLite (Synthetic Mock Data)
* **Frontend:** HTML5, Tailwind CSS, JavaScript
* **Tunneling/Hosting:** ngrok

---

## 🏗️ Architecture & Data Flow

```text
[ Citizen Query / Voice Prompt ]
               │
               ▼
   [ FastAPI Backend Handler ]
               │
               ▼
 [ OpenAI Function Calling Agent ] ──(Extracts Intent & Token)
               │
               ▼
  [ Local SQLite Database Tool ]  ──(Executes Parameterized Query)
               │
               ▼
[ Dynamic Visual Status Card Rendered ]