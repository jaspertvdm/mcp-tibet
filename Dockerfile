# TIBET MCP Server - Docker Image
# Provenance tracking for AI decisions with cryptographic audit trails
#
# Build: docker build -t mcp-server-tibet .
# Run:   docker run -i mcp-server-tibet
#
# Part of HumoticaOS/SymbAIon - https://humotica.com

FROM python:3.11-slim

LABEL maintainer="Jasper van de Meent <info@humotica.com>"
LABEL org.opencontainers.image.source="https://github.com/jaspertvdm/mcp-server-tibet"
LABEL org.opencontainers.image.description="TIBET - Trust & Intent-Based Execution Tracking for AI provenance"
LABEL org.opencontainers.image.licenses="MIT"

# Install from PyPI
RUN pip install --no-cache-dir mcp-server-tibet

# Create data directory for audit logs
RUN mkdir -p /data
ENV TIBET_DATA_DIR=/data

# MCP servers communicate via stdio
ENTRYPOINT ["mcp-server-tibet"]
