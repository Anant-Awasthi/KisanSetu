import os
import json
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from database import query_farmer_by_token, init_db

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

init_db()
app = FastAPI(title="KisanSetu API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "check_pm_kisan_status",
            "description": "Extracts mock identification tokens or phone numbers to query PM-Kisan status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "identifier": {
                        "type": "string",
                        "description": "The mock identification token (e.g., MOCK-AADHAAR-1001) or phone number extracted from the query."
                    }
                },
                "required": ["identifier"]
            }
        }
    }
]

class QueryRequest(BaseModel):
    prompt: str

@app.post("/api/assistant")
async def handle_assistant_query(req: QueryRequest):
    system_prompt = (
        "You are KisanSetu, an AI public service assistant for Indian farmers. "
        "Extract mock identification tokens or phone numbers from the user's input. "
        "If the user asks a general question without an ID, default to using 'MOCK-AADHAAR-1001'."
    )
    
    try:
        if not client:
            raise Exception("API key missing")
            
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.prompt}
            ],
            tools=tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            args = json.loads(tool_call.function.arguments)
            identifier = args.get("identifier", "MOCK-AADHAAR-1001")
            
            db_result = query_farmer_by_token(identifier)
            if db_result:
                return {
                    "success": True,
                    "parsed_intent": "check_pm_kisan_status",
                    "data": db_result,
                    "message": f"Status record retrieved successfully for {db_result['name']}."
                }
    except Exception as e:
        # Fallback handling for Quota Error / No Billing
        match = re.search(r'MOCK-[A-Z0-9-]+', req.prompt)
        identifier = match.group(0) if match else "MOCK-AADHAAR-1001"
        
        db_result = query_farmer_by_token(identifier)
        if db_result:
            return {
                "success": True,
                "parsed_intent": "check_pm_kisan_status (Agentic Fallback)",
                "data": db_result,
                "message": f"Status record retrieved successfully for {db_result['name']}."
            }

    return {
        "success": False,
        "message": "No matching synthetic record found. Try demo token: MOCK-AADHAAR-1001 or MOCK-AADHAAR-1002"
    }

app.mount("/", StaticFiles(directory="static", html=True), name="static")