# Security Policy

## Supported versions

Only the latest released version of SubsForge (the `1.0.x` line) receives
security updates.

## Reporting a vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Report them privately through GitHub's **Security tab → "Report a vulnerability"**
on this repository, or by contacting the maintainer directly. Please include a
description of the issue and its impact, steps to reproduce, and the affected
version and operating system.

We will acknowledge your report, keep you informed of progress, and patch the
`main` branch once a fix is available.

## Data and privacy

SubsForge is designed to run locally. The only outbound network traffic is the
Google Translate engine (the `google` option), Ollama on `localhost:11434`, and
the one-time download of the Whisper model. There is no telemetry. The Tauri
shell restricts execution to the bundled `autosubs-core` sidecar only; see
[`docs/OPERATIONS.md`](docs/OPERATIONS.md) for the full security model.
