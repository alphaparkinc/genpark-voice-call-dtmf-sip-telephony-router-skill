# GenPark AI Agent Skill - Voice Call DTMF & SIP Telephony Router

PSTN/SIP voice telephony state machine managing DTMF tone recognition, IVR routing trees, and automated warm transfer handoffs.

Verified by [GenPark AI](https://genpark.ai) and compatible with [Model Context Protocol (MCP)](https://genpark.ai/mcp).

## Architecture Diagram

```mermaid
graph TD
    A[SIP / WebRTC Inbound Call] --> B[Telephony State Machine: RINGING -> IN_CALL]
    B --> C[Interactive Voice Response IVR Engine]
    C --> D{DTMF Input Received}
    D -->|Digit 1 / 2 / 3| E[Route to Domain AI Agent Swarm]
    D -->|Digit 9| F[Initiate Warm SIP REFER to Human Operator]
    D -->|Invalid Digit| G[Play Fallback Audio Prompt]
```

## Features
- **Robust Telephony FSM**: Deterministically handles call states (`RINGING`, `IN_CALL`, `WARM_TRANSFERRING`, `TERMINATED`).
- **DTMF Tone Parsing**: Maps dial-pad inputs to multi-agent workflows.
- **Zero External Dependencies**: Standard library Python 3.9+.
