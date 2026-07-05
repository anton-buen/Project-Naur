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
                    "FE": "[UPDATED] Backend cannot support WebSockets. Implement a 5-second polling loop and handle loading/stale UI states gracefully.",
                    "BE": "[LOCKED] AWS load balancer constraint accepted. Expose a lightweight HTTP polling endpoint.",
                    "DS": "[UPDATED] 5-second polling allows for micro-batching. Update inference script to process 5-second event windows instead of single events."
                }
            
            # Simulated Response 1: The Initial Extraction
            return {
                "FE": "Needs WebSockets or Long-Polling to handle 'real-time' updates without freezing the React thread.",
                "BE": "Must implement strict rate-limiting on the API; querying on every page refresh will crash the server.",
                "DS": "Browsing habits are unstructured text. The model needs an async queue because inference takes 3-5 seconds."
            }

        # REAL PRODUCTION MODE (Placeholder for when we activate Bobcoins)
        # Here we would map the `thread` list into the `messages` array for the LLM
        return {}