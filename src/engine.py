import src.state_manager as sm
import logging
import json
import os
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CAE_Engine")

class CognitiveAlignmentEngine:
    def __init__(self):
        self.state = sm.read_state()
        self.llm_endpoint = os.getenv("BOB_LLM_ENDPOINT", "http://localhost:8000/v1/chat/completions")
        self.api_key = os.getenv("BOB_API_KEY", "hackathon_mock_key")

    def process_intent(self, intent: str) -> bool:
        try:
            assumptions = self._extract_assumptions(intent)
            if assumptions:
                sm.save_extraction(intent, assumptions)
                return True
        except Exception as e:
            logger.error(f"[LLM_EXTRACTION_FAILED] API timeout or failure. Error: {e}")
        
        return False

    def _extract_assumptions(self, intent: str) -> dict:
        """
        Forces the LLM to decompress a single intent into strict technical constraints.
        """
        system_prompt = (
            "Extract 1 hidden constraint for Frontend(FE), Backend(BE), and DataScience(DS) "
            "from the user intent. Return ONLY valid JSON: {\"FE\":\"\",\"BE\":\"\",\"DS\":\"\"}. Keep short."
        )
        
        payload = {
            "model": "ibm-bob-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": intent}
            ],
            "max_tokens": 50,
            "temperature": 0.0
        }

        response = requests.post(
            self.llm_endpoint,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=3.0 
        )
        response.raise_for_status()
        
        llm_reply = response.json()["choices"][0]["message"]["content"]
        
        try:
            return json.loads(llm_reply)
        except json.JSONDecodeError:
            logger.warning(f"[LLM_PARSE_ERROR] Invalid JSON from Bob: {llm_reply}")
            return {}