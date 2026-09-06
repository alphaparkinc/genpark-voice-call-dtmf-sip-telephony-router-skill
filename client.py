from typing import Dict, Any, List, Optional

class VoiceCallDTMFSIPTelephonyRouter:
    """
    Finite state machine governing SIP/PSTN telephony lifecycle events,
    dual-tone multi-frequency (DTMF) digit recognition, and call transfer handoffs.
    """
    VALID_STATES = ["IDLE", "RINGING", "IN_CALL", "ON_HOLD", "WARM_TRANSFERRING", "TERMINATED"]

    def __init__(self, ivr_menu: Optional[Dict[str, str]] = None):
        self.current_state = "IDLE"
        self.call_metadata: Dict[str, Any] = {}
        self.ivr_menu = ivr_menu or {
            "1": "sales_inquiry_agent",
            "2": "billing_and_subscriptions",
            "3": "tier_2_technical_support",
            "9": "operator_live_escalation",
            "#": "repeat_menu"
        }

    def initiate_call(self, call_id: str, caller_number: str, destination_number: str) -> Dict[str, Any]:
        self.current_state = "RINGING"
        self.call_metadata = {
            "call_id": call_id,
            "caller": caller_number,
            "destination": destination_number,
            "dtmf_history": [],
            "transfer_target": None
        }
        self.current_state = "IN_CALL"
        return {"status": "CALL_CONNECTED", "call_id": call_id, "state": self.current_state}

    def process_dtmf_tone(self, digit: str) -> Dict[str, Any]:
        if self.current_state != "IN_CALL":
            return {"status": "ERROR", "message": f"Cannot process DTMF in state {self.current_state}"}
        
        self.call_metadata.setdefault("dtmf_history", []).append(digit)
        action = self.ivr_menu.get(digit)

        if action == "operator_live_escalation":
            self.current_state = "WARM_TRANSFERRING"
            self.call_metadata["transfer_target"] = "+1-800-555-0100"
            return {
                "status": "INITIATE_WARM_TRANSFER",
                "digit": digit,
                "target_department": action,
                "sip_refer_uri": "sip:operator@telephony.genpark.ai",
                "new_state": self.current_state
            }
        elif action:
            return {
                "status": "ROUTE_INTERNAL_AGENT",
                "digit": digit,
                "target_agent_type": action,
                "new_state": self.current_state
            }
        else:
            return {
                "status": "INVALID_OPTION",
                "digit": digit,
                "message": "Unrecognized option, repeating prompt.",
                "new_state": self.current_state
            }

    def terminate_call(self, reason: str = "caller_hangup") -> Dict[str, Any]:
        self.current_state = "TERMINATED"
        return {
            "status": "CALL_TERMINATED",
            "reason": reason,
            "dtmf_summary": self.call_metadata.get("dtmf_history", []),
            "final_state": self.current_state
        }
