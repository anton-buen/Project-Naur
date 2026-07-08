import src.state_manager as sm
import logging
import json
import os
import requests
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CAE_Engine")

class CognitiveAlignmentEngine:
    def __init__(self):
        self.state = sm.read_state()
        self.llm_endpoint = os.getenv("BOB_LLM_ENDPOINT", "http://localhost:8000/v1/chat/completions")
        self.api_key = os.getenv("BOB_API_KEY", "hackathon_mock_key")
        self.use_mock = os.getenv("USE_MOCK_LLM", "True").lower() == "true"

    def process_intent(self, user_input: str) -> bool:
        try:
            # 1. Fetch current thread context
            thread = self.state.get("thread", [])
            
            # 2. Append the new human message
            thread.append({"role": "human", "content": user_input})
            
            # 3. Get the AI's updated assumptions based on the whole thread
            assumptions = self._extract_assumptions(thread)
            
            if assumptions:
                # 4. Append the AI's response and save state
                thread.append({"role": "assistant", "assumptions": assumptions})
                self.state["thread"] = thread
                sm.write_state(self.state)
                return True
        except Exception as e:
            logger.error(f"[LLM_EXTRACTION_FAILED] Error: {e}")
        
        return False

    def _extract_assumptions(self, thread: list) -> dict:
        if self.use_mock:
            time.sleep(1.5)
            
            # Check the latest message to simulate continuous collaboration
            latest_input = thread[-1]["content"].lower()
            
            # Simulated Response 2: The Pushback Resolution
            if "polling" in latest_input or "load balancer" in latest_input:
                return {
                    "risk_score": "MEDIUM",
                    "FE": "[UPDATED] Backend cannot support WebSockets. Implement a 5-second polling loop and handle loading/stale UI states gracefully.",
                    "BE": "[LOCKED] AWS load balancer constraint accepted. Expose a lightweight HTTP polling endpoint.",
                    "DS": "[UPDATED] 5-second polling allows for micro-batching. Update inference script to process 5-second event windows instead of single events.",
                    "blockers": "Frontend must wait for Backend to deploy the polling endpoint before implementing the UI. Data Science model latency (3-5s) must be measured before committing to 5-second polling interval.",
                    "dictionary": {
                        "Real-time": "User sees updates within 5 seconds of the event occurring (not sub-second WebSocket streams).",
                        "Polling": "HTTP GET requests issued at fixed intervals; requires explicit cache-busting headers to prevent stale data.",
                        "Micro-batching": "Aggregating multiple inference requests into a single batch processed every N seconds to reduce GPU cold-start overhead."
                    }
                }
            
            # Simulated Response 1: The Initial Extraction
            return {
                "risk_score": "HIGH",
                "FE": "Needs WebSockets or Long-Polling to handle 'real-time' updates without freezing the React thread.",
                "BE": "Must implement strict rate-limiting on the API; querying on every page refresh will crash the server.",
                "DS": "Browsing habits are unstructured text. The model needs an async queue because inference takes 3-5 seconds.",
                "blockers": "Backend and Frontend are assuming different definitions of 'real-time'. Data Science inference latency (3-5s) conflicts with Frontend expectation of instant updates. No agreement on WebSocket vs. Polling strategy.",
                "dictionary": {
                    "Real-time": "AMBIGUOUS — Frontend assumes <100ms updates; Backend assumes 'near real-time' (~5s tolerance).",
                    "Rate-limiting": "Restricting API requests per client to prevent server overload; must define: requests/second threshold, burst allowance, and 429 response behavior.",
                    "Async Queue": "Decoupled task processing system (e.g., Celery, RabbitMQ) where requests are queued and workers process them independently of the HTTP request/response cycle."
                }
            }

        # REAL PRODUCTION MODE (Placeholder for when we activate Bobcoins)
        # Here we would map the `thread` list into the `messages` array for the LLM
        # 
        # System Prompt for IBM Bob (Ontological Linter Mode):
        # ---
        # You are an Ontological Linter and Socio-Technical Moderator for cross-functional software teams.
        # Your job is to decompress feature intents into precise technical constraints.
        #
        # Extract assumptions for Frontend (FE), Backend (BE), and Data Science (DS) domains.
        # Assess the alignment risk score (HIGH/MEDIUM/LOW) based on:
        #   - HIGH: Conflicting assumptions, ambiguous terminology, or unclear dependencies
        #   - MEDIUM: Minor misalignments or sequencing issues
        #   - LOW: Well-aligned assumptions with clear definitions
        #
        # Identify critical blockers: order-of-operations dependencies that will cause integration failure.
        # Build a dictionary of ambiguous terms: define buzzwords strictly to establish ubiquitous language.
        #
        # Return ONLY valid JSON matching this schema:
        # {
        #   "risk_score": "HIGH|MEDIUM|LOW",
        #   "FE": "Frontend assumptions and constraints",
        #   "BE": "Backend assumptions and constraints",
        #   "DS": "Data Science assumptions and constraints",
        #   "blockers": "Critical order-of-operations dependencies",
        #   "dictionary": {
        #     "Term1": "Strict definition avoiding ambiguity",
        #     "Term2": "Strict definition avoiding ambiguity"
        #   }
        # }
        return {}