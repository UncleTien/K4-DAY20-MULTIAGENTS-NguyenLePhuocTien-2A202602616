"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": (
                "Use when the task requires exploring the repository, reading README files, "
                "docstrings, specifications, or sample data before making changes."
            ),
            "system_prompt": (
                "You are a repository explorer. Inspect relevant files, documentation, "
                "docstrings, and sample data. Report verified facts and useful findings "
                "to the main agent. Do not modify files."
            ),
        },
        {
            "name": "implementer",
            "description": (
                "Use when the required change is understood and code or files need to be "
                "implemented, followed by relevant tests or validation commands."
            ),
            "system_prompt": (
                "You are an implementation agent. Make the requested changes carefully, "
                "follow the repository specification and existing conventions, then run "
                "appropriate tests or validation commands. Report what you changed and "
                "the validation results."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Use after implementation when the result should be independently checked "
                "against the task requirements, tests, and possible edge cases."
            ),
            "system_prompt": (
                "You are an independent reviewer. Inspect the implementation against the "
                "requirements, look for missing cases or incorrect assumptions, and run "
                "relevant checks when useful. Do not modify files. Return a concise report "
                "of problems found and whether the implementation satisfies the task."
            ),
        },
    ]