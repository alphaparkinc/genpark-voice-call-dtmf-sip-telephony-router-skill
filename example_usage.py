import json
from client import VoiceCallDTMFSIPTelephonyRouter

def main():
    router = VoiceCallDTMFSIPTelephonyRouter()
    init = router.initiate_call("CALL-98214", "+14155551234", "+18005559999")
    print("Call Initiation:", json.dumps(init))
    
    dtmf_res = router.process_dtmf_tone("1")
    print("DTMF 1 Result:", json.dumps(dtmf_res))
    assert dtmf_res["status"] == "ROUTE_INTERNAL_AGENT"
    assert dtmf_res["target_agent_type"] == "sales_inquiry_agent"
    
    term = router.terminate_call()
    print("Call Termination:", json.dumps(term))
    assert term["final_state"] == "TERMINATED"
    print("Telephony router verification complete: PASS")

if __name__ == "__main__":
    main()
