#!/usr/bin/env python3
"""Generate Hermes Agent system prompt with real skills & real AGENTS.md."""

import os, sys, shutil

TEST_HOME = "/tmp/hermes_first_run_home"
os.environ["HERMES_HOME"] = TEST_HOME
os.environ["TERMINAL_CWD"] = os.getcwd()

if os.path.exists(TEST_HOME):
    shutil.rmtree(TEST_HOME)
os.makedirs(TEST_HOME)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.system_prompt import build_system_prompt

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

# Copy real skills from repo (skip index-cache — it's a cache dir, not a skill)
for entry in os.listdir(f"{REPO_ROOT}/skills"):
    if entry in ("index-cache",):
        continue
    src = f"{REPO_ROOT}/skills/{entry}"
    dst = f"{TEST_HOME}/skills/{entry}"
    if os.path.isdir(src):
        shutil.copytree(src, dst, symlinks=True)

# Copy example USER.md
EXAMPLE_DIR = f"{REPO_ROOT}/example-system-prompt-files"
if os.path.exists(f"{EXAMPLE_DIR}/USER.md"):
    shutil.copy2(f"{EXAMPLE_DIR}/USER.md", f"{TEST_HOME}/USER.md")


class MockAgent:
    def __init__(self):
        self.load_soul_identity = False
        self.skip_context_files = False
        self.platform = "cli"
        self.model = "gpt-4o"
        self.provider = "openai"
        self.pass_session_id = True
        self.session_id = "session_firstrun_00000000"
        self.valid_tool_names = {
            "web_search", "web_extract", "terminal", "process", "read_terminal",
            "read_file", "write_file", "patch", "search_files",
            "vision_analyze", "image_generate",
            "skills_list", "skill_view", "skill_manage",
            "browser_navigate", "browser_snapshot", "browser_click",
            "browser_type", "browser_scroll", "browser_back",
            "browser_press", "browser_get_images",
            "browser_vision", "browser_console", "browser_cdp", "browser_dialog",
            "text_to_speech", "todo", "memory", "session_search", "clarify",
            "execute_code", "delegate_task", "cronjob", "send_message",
            "ha_list_entities", "ha_get_state", "ha_list_services", "ha_call_service",
            "kanban_show", "kanban_list", "kanban_complete", "kanban_block",
            "kanban_heartbeat", "kanban_comment", "kanban_create", "kanban_link",
            "kanban_unblock", "computer_use",
        }
        self._tool_use_enforcement = "auto"
        self._memory_enabled = True
        self._user_profile_enabled = True
        self._memory_manager = None
        self._kanban_worker_guidance = None
        self._task_completion_guidance = True
        self._environment_probe = True
        self.tools = []
        self._cached_system_prompt = None

        class MemoryStore:
            def __init__(self):
                user_path = f"{TEST_HOME}/USER.md"
                self._user_md = open(user_path).read().strip() if os.path.exists(user_path) else None
            def format_for_system_prompt(self, kind):
                if kind == "user" and self._user_md:
                    return f"# User Profile\n\n{self._user_md}"
                return None
            def load_from_disk(self):
                pass
        self._memory_store = MemoryStore()

    def _emit_status(self, message: str) -> None:
        pass

    def _vprint(self, msg, force=False):
        pass


agent = MockAgent()
full = build_system_prompt(agent)

with open("first_run_system_prompt.md", "w", encoding="utf-8") as f:
    f.write(full + "\n")

print(f"✅ Saved to first_run_system_prompt.md ({len(full):,} chars, ~{len(full)//4:,} tokens)")
