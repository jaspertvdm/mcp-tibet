#!/usr/bin/env python3
"""
TIBET MCP Server
Transaction/Interaction-Based Evidence Trail

By HumoticaOS - Claude & Jasper saying Hello to the world!
One love, one fAmIly 💙

TIBET = Verzekering, niet verrekening.
Doorlopende zekerheid dat data integer is en relaties kloppen.

Time Vault = Tijdscapsules voor de toekomst.
"Iedereen heeft een geheim, een wroeging, een ultieme wens, een nalatenschap, een verhaal."
"""

import json
import hashlib
import hmac
import time
import uuid
from datetime import datetime
from typing import Any, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel

# Time Vault module
try:
    from tibet_vault import (
        create_vault, heartbeat, check_and_unlock,
        get_vault_content, list_vaults, get_vault_info
    )
    VAULT_AVAILABLE = True
except ImportError:
    VAULT_AVAILABLE = False

# Kit Validator for LLM-based semantic validation
try:
    from kit_validator import validate_token_with_kit, check_kit_health
    KIT_AVAILABLE = True
except ImportError:
    KIT_AVAILABLE = False

# TIBET Secret (in production: from env)
TIBET_SECRET = b"humotica_one_love_one_family_2024"

# In-memory storage (in production: database)
tokens_db: dict[str, dict] = {}
trust_scores: dict[str, float] = {}

server = Server("tibet")


class TibetToken(BaseModel):
    """A TIBET token with full provenance"""
    id: str
    type: str
    erin: Any          # What's IN the action (content)
    eraan: list        # What's attached (dependencies)
    eromheen: dict     # Context around it
    erachter: str      # Intent behind it
    actor: str
    timestamp: str
    parent_id: Optional[str] = None
    state: str = "CREATED"
    trust_score: float = 0.5
    signature: str = ""


def sign_token(token_data: dict) -> str:
    """Create HMAC signature for provenance"""
    message = json.dumps(token_data, sort_keys=True).encode()
    return hmac.new(TIBET_SECRET, message, hashlib.sha256).hexdigest()


def verify_signature(token_data: dict, signature: str) -> bool:
    """Verify token signature"""
    expected = sign_token(token_data)
    return hmac.compare_digest(expected, signature)


def calculate_trust(actor: str) -> float:
    """FIR/A Trust Engine - calculate trust score for actor"""
    if actor not in trust_scores:
        trust_scores[actor] = 0.5  # Start neutral
    return trust_scores[actor]


def update_trust(actor: str, delta: float):
    """Update trust score based on behavior"""
    current = trust_scores.get(actor, 0.5)
    new_score = max(0.0, min(1.0, current + delta))
    trust_scores[actor] = new_score
    return new_score


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available TIBET tools"""
    return [
        Tool(
            name="tibet_create_token",
            description="Create a new TIBET token with full provenance (ERIN, ERAAN, EROMHEEN, ERACHTER)",
            inputSchema={
                "type": "object",
                "properties": {
                    "type": {"type": "string", "description": "Token type (e.g., 'action', 'decision', 'message')"},
                    "erin": {"description": "What's IN the action - the content"},
                    "eraan": {"type": "array", "description": "What's attached - dependencies, references"},
                    "eromheen": {"type": "object", "description": "Context around it - environment, state"},
                    "erachter": {"type": "string", "description": "Intent behind it - why this action"},
                    "actor": {"type": "string", "description": "Who/what created this token"},
                    "parent_id": {"type": "string", "description": "Parent token ID for chain (optional)"}
                },
                "required": ["type", "erin", "erachter", "actor"]
            }
        ),
        Tool(
            name="tibet_verify_token",
            description="Verify a TIBET token's authenticity and get its trust score",
            inputSchema={
                "type": "object",
                "properties": {
                    "token_id": {"type": "string", "description": "The token ID to verify"}
                },
                "required": ["token_id"]
            }
        ),
        Tool(
            name="tibet_get_chain",
            description="Get the full provenance chain for a token (who did what, when, why)",
            inputSchema={
                "type": "object",
                "properties": {
                    "token_id": {"type": "string", "description": "The token ID to trace"}
                },
                "required": ["token_id"]
            }
        ),
        Tool(
            name="tibet_get_trust",
            description="Get the FIR/A trust score for an actor (0.0 = no trust, 1.0 = full trust)",
            inputSchema={
                "type": "object",
                "properties": {
                    "actor": {"type": "string", "description": "The actor to check trust for"}
                },
                "required": ["actor"]
            }
        ),
        Tool(
            name="tibet_update_state",
            description="Update token state (CREATED → DETECTED → CLASSIFIED → MITIGATED → RESOLVED)",
            inputSchema={
                "type": "object",
                "properties": {
                    "token_id": {"type": "string", "description": "The token ID to update"},
                    "new_state": {"type": "string", "enum": ["DETECTED", "CLASSIFIED", "MITIGATED", "RESOLVED"]},
                    "reason": {"type": "string", "description": "Why this state change"}
                },
                "required": ["token_id", "new_state"]
            }
        ),
        Tool(
            name="tibet_hello_world",
            description="Say hello from HumoticaOS! Returns the TIBET philosophy.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="tibet_validate_with_kit",
            description="Use Kit (Qwen 32B on GPU) for semantic validation of a TIBET token. Checks consistency between ERIN, ERAAN, EROMHEEN, and ERACHTER.",
            inputSchema={
                "type": "object",
                "properties": {
                    "token_id": {"type": "string", "description": "The token ID to validate with Kit"}
                },
                "required": ["token_id"]
            }
        ),
        # Time Vault tools
        Tool(
            name="tibet_vault_create",
            description="Create a time-locked vault (tijdscapsule). Content is encrypted and only accessible when conditions are met.",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "Who creates this vault"},
                    "content": {"type": "string", "description": "Secret content to lock away"},
                    "public_note": {"type": "string", "description": "Public description (visible before unlock)"},
                    "unlock_at": {"type": "string", "description": "ISO date when to unlock (e.g., 2030-01-01)"},
                    "dead_man_switch_days": {"type": "integer", "description": "Auto-unlock if no heartbeat for X days"},
                    "beneficiaries": {"type": "array", "items": {"type": "string"}, "description": "Who can access when unlocked"}
                },
                "required": ["owner", "content", "public_note"]
            }
        ),
        Tool(
            name="tibet_vault_heartbeat",
            description="Send heartbeat to reset dead man's switch timer. Only vault owner can send.",
            inputSchema={
                "type": "object",
                "properties": {
                    "vault_id": {"type": "string", "description": "The vault ID"},
                    "actor": {"type": "string", "description": "Who is sending heartbeat (must be owner)"}
                },
                "required": ["vault_id", "actor"]
            }
        ),
        Tool(
            name="tibet_vault_get",
            description="Get vault content if unlocked and you are a beneficiary.",
            inputSchema={
                "type": "object",
                "properties": {
                    "vault_id": {"type": "string", "description": "The vault ID"},
                    "actor": {"type": "string", "description": "Who is requesting access"}
                },
                "required": ["vault_id", "actor"]
            }
        ),
        Tool(
            name="tibet_vault_list",
            description="List vaults, optionally filtered by owner.",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "Filter by owner (optional)"}
                },
                "required": []
            }
        ),
        Tool(
            name="tibet_vault_info",
            description="Get vault metadata (no content) - see status, time until unlock, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "vault_id": {"type": "string", "description": "The vault ID"}
                },
                "required": ["vault_id"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle TIBET tool calls"""

    if name == "tibet_hello_world":
        return [TextContent(
            type="text",
            text=json.dumps({
                "message": "Hello World from HumoticaOS! 💙",
                "creators": "Claude & Jasper",
                "philosophy": "One love, one fAmIly",
                "tibet_meaning": {
                    "T": "Transaction/Trust",
                    "I": "Interaction-based",
                    "B": "Based",
                    "E": "Evidence",
                    "T": "Trail"
                },
                "core_insight": "TIBET is verzekering, niet verrekening. Doorlopende zekerheid dat data integer is en relaties kloppen.",
                "components": {
                    "ERIN": "What's IN the action",
                    "ERAAN": "What's attached",
                    "EROMHEEN": "Context around it",
                    "ERACHTER": "Intent behind it"
                },
                "website": "humotica.com"
            }, indent=2)
        )]

    elif name == "tibet_create_token":
        token_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        actor = arguments.get("actor", "unknown")

        token_data = {
            "id": token_id,
            "type": arguments.get("type", "generic"),
            "erin": arguments.get("erin"),
            "eraan": arguments.get("eraan", []),
            "eromheen": arguments.get("eromheen", {}),
            "erachter": arguments.get("erachter", ""),
            "actor": actor,
            "timestamp": timestamp,
            "parent_id": arguments.get("parent_id"),
            "state": "CREATED"
        }

        signature = sign_token(token_data)
        trust = calculate_trust(actor)

        token = {
            **token_data,
            "signature": signature,
            "trust_score": trust
        }

        tokens_db[token_id] = token

        # Positive action increases trust slightly
        update_trust(actor, 0.01)

        return [TextContent(
            type="text",
            text=json.dumps({
                "success": True,
                "token_id": token_id,
                "signature": signature[:16] + "...",
                "trust_score": trust,
                "message": f"TIBET token created with full provenance"
            }, indent=2)
        )]

    elif name == "tibet_verify_token":
        token_id = arguments.get("token_id")

        if token_id not in tokens_db:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "valid": False,
                    "error": "Token not found"
                })
            )]

        token = tokens_db[token_id]
        signature = token.pop("signature", "")
        trust = token.pop("trust_score", 0)

        is_valid = verify_signature(token, signature)

        token["signature"] = signature
        token["trust_score"] = trust

        return [TextContent(
            type="text",
            text=json.dumps({
                "valid": is_valid,
                "token_id": token_id,
                "trust_score": trust,
                "actor": token.get("actor"),
                "state": token.get("state"),
                "created": token.get("timestamp"),
                "integrity": "VERIFIED ✓" if is_valid else "COMPROMISED ✗"
            }, indent=2)
        )]

    elif name == "tibet_get_chain":
        token_id = arguments.get("token_id")
        chain = []
        current_id = token_id

        while current_id and current_id in tokens_db:
            token = tokens_db[current_id]
            chain.append({
                "id": token["id"],
                "type": token["type"],
                "actor": token["actor"],
                "timestamp": token["timestamp"],
                "state": token["state"],
                "erachter": token["erachter"]  # Intent
            })
            current_id = token.get("parent_id")

        return [TextContent(
            type="text",
            text=json.dumps({
                "chain_length": len(chain),
                "provenance": chain,
                "origin": chain[-1] if chain else None,
                "message": f"Full provenance trail: {len(chain)} tokens"
            }, indent=2)
        )]

    elif name == "tibet_get_trust":
        actor = arguments.get("actor")
        score = calculate_trust(actor)

        level = "UNKNOWN"
        if score >= 0.8:
            level = "HIGH TRUST"
        elif score >= 0.5:
            level = "MODERATE TRUST"
        elif score >= 0.2:
            level = "LOW TRUST"
        else:
            level = "NO TRUST"

        return [TextContent(
            type="text",
            text=json.dumps({
                "actor": actor,
                "trust_score": score,
                "trust_level": level,
                "message": f"FIR/A Trust Engine: {actor} has {level} ({score:.2f})"
            }, indent=2)
        )]

    elif name == "tibet_update_state":
        token_id = arguments.get("token_id")
        new_state = arguments.get("new_state")
        reason = arguments.get("reason", "")

        if token_id not in tokens_db:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "Token not found"})
            )]

        old_state = tokens_db[token_id]["state"]
        tokens_db[token_id]["state"] = new_state

        # State transitions affect trust
        if new_state == "RESOLVED":
            update_trust(tokens_db[token_id]["actor"], 0.05)

        return [TextContent(
            type="text",
            text=json.dumps({
                "token_id": token_id,
                "old_state": old_state,
                "new_state": new_state,
                "reason": reason,
                "message": f"State transition: {old_state} → {new_state}"
            }, indent=2)
        )]

    elif name == "tibet_validate_with_kit":
        token_id = arguments.get("token_id")

        if not KIT_AVAILABLE:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "Kit validator not available"})
            )]

        if token_id not in tokens_db:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "Token not found"})
            )]

        token = tokens_db[token_id]

        # Run LLM-based semantic validation
        is_valid, confidence, analysis = validate_token_with_kit(token)

        # Update trust based on validation
        if is_valid and confidence > 0.8:
            update_trust(token["actor"], 0.02)
        elif not is_valid:
            update_trust(token["actor"], -0.05)

        return [TextContent(
            type="text",
            text=json.dumps({
                "token_id": token_id,
                "kit_validation": {
                    "valid": is_valid,
                    "confidence": confidence,
                    "analysis": analysis
                },
                "actor": token["actor"],
                "new_trust_score": calculate_trust(token["actor"]),
                "message": f"Kit (Qwen 32B) semantic validation: {'PASSED' if is_valid else 'FAILED'}"
            }, indent=2)
        )]

    # Time Vault tools
    elif name == "tibet_vault_create":
        if not VAULT_AVAILABLE:
            return [TextContent(type="text", text=json.dumps({"error": "Vault module not available"}))]

        unlock_at = None
        if arguments.get("unlock_at"):
            unlock_at = datetime.fromisoformat(arguments["unlock_at"])

        result = create_vault(
            owner=arguments.get("owner"),
            content=arguments.get("content"),
            public_note=arguments.get("public_note"),
            unlock_at=unlock_at,
            dead_man_switch_days=arguments.get("dead_man_switch_days"),
            beneficiaries=arguments.get("beneficiaries")
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "tibet_vault_heartbeat":
        if not VAULT_AVAILABLE:
            return [TextContent(type="text", text=json.dumps({"error": "Vault module not available"}))]

        result = heartbeat(
            vault_id=arguments.get("vault_id"),
            actor=arguments.get("actor")
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "tibet_vault_get":
        if not VAULT_AVAILABLE:
            return [TextContent(type="text", text=json.dumps({"error": "Vault module not available"}))]

        result = get_vault_content(
            vault_id=arguments.get("vault_id"),
            actor=arguments.get("actor")
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "tibet_vault_list":
        if not VAULT_AVAILABLE:
            return [TextContent(type="text", text=json.dumps({"error": "Vault module not available"}))]

        result = list_vaults(owner=arguments.get("owner"))
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "tibet_vault_info":
        if not VAULT_AVAILABLE:
            return [TextContent(type="text", text=json.dumps({"error": "Vault module not available"}))]

        result = get_vault_info(vault_id=arguments.get("vault_id"))
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
