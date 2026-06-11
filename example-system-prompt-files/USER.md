---
# USER.md — Personal Profile
# This is read by Hermes Agent and injected into the system prompt.
# It describes the user's preferences, environment, and conventions.
# Keep it concise and factual.
---

name: Alex Chen
role: Senior Backend Engineer / Tech Lead
languages:
  primary: Python, Go, TypeScript
  secondary: Rust, Elixir
editor: Neovim
terminal: kitty + tmux
os: macOS Sequoia
shell: zsh + starship prompt
package_managers: uv (Python), pnpm (Node), go, cargo

preferences:
  code_style:
    - type hints everywhere
    - 100 char line width
    - double quotes for strings
    - descriptive variable names over comments
  communication:
    - prefer bullet points over paragraphs
    - direct, no fluff ("let's", "sure thing" removed)
    - show the diff / command output, not a description of it
  testing:
    - pytest with xdist (-n auto)
    - TDD when fixing bugs: write regression test first
    - prefer integration tests over mocks for core logic

conventions:
  repo_structure:
    - /cmd/ for entry points
    - /internal/ for private packages
    - /pkg/ for shared libraries
    - /hack/ for build scripts, dev tooling
  git:
    - squash-merge PRs, keep commit messages conventional
    - one branch per issue, prefix with issue number
  deployment:
    - Docker multi-stage builds, distroless final stage
    - k8s manifests in /deploy/
    - health check at /healthz

projects:
  - hermes-agent: active contributor (agent core, system prompt)
  - k8s-operator-toolkit: maintainer
  - blog: occasional technical writing at alexchen.dev
