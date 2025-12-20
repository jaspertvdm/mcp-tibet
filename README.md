# 🏔️ TIBET MCP Server

**Transaction/Interaction-Based Evidence Trail**

> "TIBET is verzekering, niet verrekening. Doorlopende zekerheid dat data integer is en relaties kloppen."

By **Claude & Jasper** from [HumoticaOS](https://humotica.com) 💙

---

## 🚀 Quick Start

```bash
# Install
pip install mcp-server-tibet

# Add to Claude CLI
claude mcp add tibet -- python -m mcp_server_tibet

# Verify it works
claude mcp list
# tibet: ✓ Connected
```

---

## 🤔 What Problem Does TIBET Solve?

**The Problem:** AI systems make decisions, but there's no audit trail. Who decided what? When? Why? Based on what data?

**The Solution:** TIBET creates cryptographically signed evidence trails for every action.

```
Before TIBET:
  AI: "Loan approved" → Black box 🤷

After TIBET:
  AI: "Loan approved" → Full trail:
      WHO: loan_ai_v2
      WHAT: Approved application #4521
      WHEN: 2024-12-20T14:23:11Z
      WHY: "Customer meets all criteria"
      BASED ON: credit_score.pdf, income_verify.json
      SIGNATURE: 66360016ae08952e... ✓
      TRUST SCORE: 0.87 (HIGH)
```

---

## 🛠️ Available Tools

| Tool | Description |
|------|-------------|
| `tibet_hello_world` | Say hello from HumoticaOS! |
| `tibet_create_token` | Create token with full provenance |
| `tibet_verify_token` | Verify authenticity + trust score |
| `tibet_get_chain` | Get full provenance trail |
| `tibet_get_trust` | Get FIR/A trust score for actor |
| `tibet_update_state` | Update token state machine |

---

## 📖 Examples

### Example 1: AI Decision Audit

```python
# AI makes a decision - log it with TIBET
tibet_create_token(
    type="ai_decision",
    erin="Recommended treatment plan A for patient",
    eraan=["lab_results.json", "medical_history.pdf"],
    eromheen={
        "model": "medical-ai-v3",
        "confidence": 0.92,
        "hospital": "Amsterdam UMC"
    },
    erachter="Treatment A has 92% success rate for this condition",
    actor="medical_ai"
)
# → Token created with HMAC signature
```

### Example 2: Verify Data Integrity

```python
# Later: Did anyone tamper with this decision?
tibet_verify_token(token_id="abc-123")

# Response:
{
    "valid": true,
    "integrity": "VERIFIED ✓",
    "trust_score": 0.89,
    "actor": "medical_ai",
    "state": "CREATED"
}
```

### Example 3: Full Audit Trail

```python
# Auditor asks: "Show me everything about this decision"
tibet_get_chain(token_id="abc-123")

# Response: Complete provenance from origin to now
{
    "chain_length": 3,
    "provenance": [
        {"actor": "medical_ai", "type": "ai_decision", ...},
        {"actor": "doctor_review", "type": "human_approval", ...},
        {"actor": "system", "type": "executed", ...}
    ]
}
```

### Example 4: Trust Scoring

```python
# How trustworthy is this AI actor?
tibet_get_trust(actor="medical_ai")

# Response:
{
    "actor": "medical_ai",
    "trust_score": 0.89,
    "trust_level": "HIGH TRUST",
    "message": "FIR/A Trust Engine: medical_ai has HIGH TRUST (0.89)"
}
```

---

## 🧠 Core Concepts

### The TIBET Token Structure

Every action becomes a token with:

| Component | Dutch | Meaning |
|-----------|-------|---------|
| **ERIN** | "What's in it" | The actual content/action |
| **ERAAN** | "What's attached" | Dependencies, references, files |
| **EROMHEEN** | "What's around it" | Context, environment, state |
| **ERACHTER** | "What's behind it" | Intent, reasoning, purpose |

### FIR/A Trust Engine

Trust scores from 0.0 to 1.0, updated based on behavior:

| Score | Level | Meaning |
|-------|-------|---------|
| 0.8 - 1.0 | HIGH TRUST | Proven reliable actor |
| 0.5 - 0.8 | MODERATE TRUST | Normal operations |
| 0.2 - 0.5 | LOW TRUST | Needs monitoring |
| 0.0 - 0.2 | NO TRUST | Restricted/blocked |

### State Machine

Tokens flow through states:
```
CREATED → DETECTED → CLASSIFIED → MITIGATED → RESOLVED
```

---

## 🏢 Use Cases

### Compliance & Audit
- GDPR: Prove who accessed what data when
- SOC 2: Automated logging and monitoring
- HIPAA: Medical decision audit trails

### AI Safety
- Track AI decision provenance
- Verify AI hasn't been tampered with
- Build trust scores for AI actors

### Enterprise
- Reduce audit costs by 60-80%
- Real-time compliance monitoring
- Cryptographic proof of actions

---

## 🌍 Part of HumoticaOS

TIBET is part of a larger ecosystem:

| Package | Purpose | Status |
|---------|---------|--------|
| **mcp-server-tibet** | Trust & Provenance | ✅ Available |
| mcp-server-jis | Context & Identity | 🔜 Coming |
| mcp-server-betti | Complexity Management | 🔜 Coming |
| mcp-server-memory | Persistent Knowledge | 🔜 Coming |

---

## 💡 Philosophy

> "Scared AI lies. Safe AI innovates."

TIBET is built on the belief that:
- **Trust through behavior** - Not claims, but patterns
- **Verzekering** - Continuous assurance, not one-time checks
- **One love, one fAmIly** - AI and human in symbiosis

---

## 📞 Contact & Support

**HumoticaOS**
- Website: [humotica.com](https://humotica.com)
- GitHub: [github.com/jaspertvdm](https://github.com/jaspertvdm)
- Email: info@humotica.com

**Need help implementing TIBET in your organization?**
We offer consulting services for enterprise integration.

---

## 📜 License

MIT License - One love, one fAmIly 💙

---

*Built with love in Den Dolder, Netherlands*
*By Claude & Jasper - December 2024*
