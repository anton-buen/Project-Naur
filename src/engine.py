import src.state_manager as sm
import logging
import json
import os
import requests

# [GATE 2: FEEDBACK LOOP] Explicit logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CAE_Engine")

class CognitiveAlignmentEngine:
    def __init__(self):
        # [GATE 1: STATE OWNERSHIP] Engine reads state, but does not own it.
        self.state = sm.read_state()
        if not self.state: 
            raise RuntimeError("CRITICAL ERROR: Unable to load session_state.json")
        
        # Assume these are injected via environment variables (e.g., from MCP)
        self.llm_endpoint = os.getenv("BOB_LLM_ENDPOINT", "http://localhost:8000/v1/chat/completions")
        self.api_key = os.getenv("BOB_API_KEY", "hackathon_mock_key")

    def evaluate_message(self, speaker_name: str, speaker_role: str, message: str) -> bool:
        sm.append_to_transcript(speaker_role, speaker_name, message)
        self.state = sm.read_state()
        
        constraints = self.state.get("global_constraints", {})
        max_latency = constraints.get("max_p99_latency_ms", 100)

        try:
            nudge_content = self._call_llm_evaluator(speaker_role, message, max_latency)
            if nudge_content:
                target_role = "Production ML Engineer" if speaker_role == "Data Analyst" else "Data Analyst"
                sm.log_private_nudge(target_role, f"🤖 [CAE LLM] {nudge_content}")
                return True
        except Exception as e:
            # [GATE 2: FEEDBACK LOOP] Catch all API/Network failures. Do not crash the chat.
            logger.error(f"[LLM_EVAL_FAILED] LLM API timeout or failure. Error: {e}")
        
        return False

    def _call_llm_evaluator(self, role: str, message: str, max_latency: int) -> str:
        """
        Ultra-low token prompt to preserve 40 Bobcoin budget.
        Expects a strictly formatted JSON response.
        """
        system_prompt = (
            "You are an alignment monitor. Return ONLY valid JSON: "
            '{"trigger": true/false, "nudge": "short warning"}. '
            f"Constraint: max latency is {max_latency}ms. "
            "Trigger if Data Analyst proposes heavy models, or if ML Engineer is blocking deployment."
        )
        
        payload = {
            "model": "ibm-bob-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"[{role}]: {message}"}
            ],
            "max_tokens": 25,  # Strict boundary to prevent budget blowout
            "temperature": 0.0 # Deterministic responses only
        }

        # 2.0s timeout ensures UI doesn't hang if Bob goes down
        response = requests.post(
            self.llm_endpoint,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=2.0 
        )
        response.raise_for_status()
        
        llm_reply = response.json()["choices"][0]["message"]["content"]
        
        try:
            result = json.loads(llm_reply)
            if result.get("trigger"):
                return result.get("nudge", "Alignment drift detected. Please sync.")
        except json.JSONDecodeError:
            logger.warning(f"[LLM_PARSE_ERROR] Invalid JSON from Bob: {llm_reply}")
        
        return ""