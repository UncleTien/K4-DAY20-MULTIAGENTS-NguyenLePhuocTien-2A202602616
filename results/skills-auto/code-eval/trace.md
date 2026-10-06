### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Assistant


I'll start by exploring the workspace structure and reading the relevant skill guidelines.





### Tool call: ls
{"path": "workspace"}

### Tool call: read_file
{"file_path": "skills/avoid-unbounded-find/SKILL.md", "limit": 1000}

### Tool call: read_file
{"file_path": "skills/verify-workspace-path/SKILL.md", "limit": 1000}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool result
@@ lines 1-8 of 8 @@
---
name: avoid-unbounded-find
description: Use this skill when searching for files to prevent overly broad or long-running commands.
---
- Limit search scope to relevant directories (e.g., current directory or known subdirectories)
- Use `-maxdepth` to restrict search depth
- Add timeout (e.g., `timeout 30s find ...`) to prevent hanging
- Target specific file patterns instead of scanning entire filesystem

### Tool result
@@ lines 1-7 of 7 @@
---
name: verify-workspace-path
description: Use this skill when starting a task to confirm the workspace location and avoid hardcoded paths.
---
- Check current directory with `pwd`
- List directory contents to locate workspace files
- Use relative paths (e.g., `./file.csv`) instead of assuming fixed paths like `/workspace/file.csv`

### Tool call: ls
{"path": "workspace/bookings"}

### Tool call: ls
{"path": "workspace/tests"}

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py']

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_bookings.py']

### Tool call: read_file
{"file_path": "workspace/bookings/__init__.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py"}

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py"}

### Tool result
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Tool call: execute
{"command": "cd workspace && python -m pytest tests/test_bookings.py -v 2>&1"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.13.11, pytest-9.1.1, pluggy-1.6.0 -- ~/Documents/vinAI20K/Day20_061026_t2/K4-DAY20-MULTIAGENTS-NguyenLePhuocTien-2A202602616/.venv/bin/python
cachedir: .pytest_cache
rootdir: /private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpp_q5dhxn/workspace
plugins: langsmith-0.14.4, anyio-4.15.1
collecting ... collected 3 items

tests/test_bookings.py::test_total_minutes_mixed_formats FAILED          [ 33%]
tests/test_bookings.py::test_billable_blocks_rounds_up FAILED            [ 66%]
tests/test_bookings.py::test_add_slot_single_call PASSED                 [100%]

=================================== FAILURES ===================================
_______________________ test_total_minutes_mixed_formats _______________________

    def test_total_minutes_mixed_formats():
>       assert total_minutes(["1h30m", "2h"]) == 210
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

~/Documents/vinAI20K/Day20_061026_t2/K4-DAY20-MULTIAGENTS-NguyenLePhuocTien-2A202602616/tasks/code-eval/workspace/tests/test_bookings.py:6: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
bookings/schedule.py:7: in total_minutes
    return sum(parse_duration(d) for d in durations)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
bookings/schedule.py:7: in <genexpr>
    return sum(parse_duration(d) for d in durations)
               ^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _

### Assistant


Now I can see the issues. Let me fix all three modules according to their docstrings:

**Issues found:**
1. `parse_duration` only handles `NhNm` format — needs to support `Nh`, `Nm`, `M:SS`, bare numbers
2. `billable_blocks` uses `round()` instead of ceiling — must round UP
3. `add_slot` uses a mutable default argument, causing state sharing between calls




### Tool call: write_file
{"file_path": "workspace/bookings/timeutil.py", "content": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n\ndef parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    text = text.strip()\n    # \"1:30\" format (MM:SS or H:MM)\n    if \":\" in text:\n        parts = text.split(\":\")\n        if len(parts) == 2:\n            h, m = parts\n            return int(h) * 60 + int(m)\n        elif len(parts) == 3:\n            h, m, s = parts\n            return int(h) * 60 + int(m) + int(s)\n        else:\n            raise ValueError(f\"bad duration: {text!r}\")\n    # \"1h30m\", \"2h\", \"45m\", \"45\" formats\n    m = re.fullmatch(r\"(?:(\\d+)h)?(?:(\\d+)m)?\", text)\n    if not m or not any(m.groups()):\n        raise ValueError(f\"bad duration: {text!r}\")\n    hours = int(m.group(1) or 0)\n    minutes = int(m.group(2) or 0)\n    return hours * 60 + minutes"}

### Tool call: write_file
{"file_path": "workspace/bookings/billing.py", "content": "\"\"\"Billing rules.\"\"\"\nimport math\n\n\ndef billable_blocks(minutes, block=15):\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(\"minutes must be >= 0\")\n    if block <= 0:\n        raise ValueError(\"block must be positive\")\n    return math.ceil(minutes / block)"}

### Tool call: write_file
{"file_path": "workspace/bookings/schedule.py", "content": "\"\"\"Schedule helpers.\"\"\"\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations):\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot, slots=None):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    if slots is None:\n        slots = []\n    slots = slots + [slot]\n    return slots"}

### Tool result
Updated file /workspace/bookings/timeutil.py

### Tool result
Updated file /workspace/bookings/billing.py

### Tool result
Updated file /workspace/bookings/schedule.py

### Tool call: execute
{"command": "cd workspace && python -m pytest tests/test_bookings.py -v 2>&1"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.13.11, pytest-9.1.1, pluggy-1.6.0 -- ~/Documents/vinAI20K/Day20_061026_t2/K4-DAY20-MULTIAGENTS-NguyenLePhuocTien-2A202602616/.venv/bin/python
cachedir: .pytest_cache
rootdir: /private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpp_q5dhxn/workspace
plugins: langsmith-0.14.4, anyio-4.15.1
collecting ... collected 3 items

tests/test_bookings.py::test_total_minutes_mixed_formats PASSED          [ 33%]
tests/test_bookings.py::test_billable_blocks_rounds_up PASSED            [ 66%]
tests/test_bookings.py::test_add_slot_single_call PASSED                 [100%]

============================== 3 passed in 0.01s ===============================

[Command succeeded with exit code 0]

### Assistant


All tests pass. Let me run a final sanity check against every docstring example to be thorough:



### Tool call: execute
{"command": "cd workspace && python -c \"\nfrom bookings.timeutil import parse_duration as p\nfrom bookings.billing import billable_blocks as b\nfrom bookings.schedule import add_slot as a, total_minutes as t\n\n# parse_duration docstring examples\nassert p('1h30m') == 90 and p('2h') == 120 and p('45m') == 45 and p('1:30') == 90 and p('45') == 45\nassert p('  2h  ') == 120\nassert p(':30') is not None\n# negative minutes\ntry:\n    p('45'); b(-1); \nexcept ValueError:\n    pass\nassert b(-1) == 0 or True  # will raise, handled below\n\n# billable_blocks: round up\nassert b(0) == 0\nassert b(15) == 1\nassert b(16) == 2\nassert b(20) == 2\nassert b(45) == 3\nassert b(29) == 2\ntry:\n    b(-5)\nexcept ValueError:\n    pass\ntry:\n    b(15, 0)\nexcept ValueError:\n    pass\n\n# add_slot: no shared state\nassert a('a') == ['a']\nassert a('b') == ['b']\ns = []\nassert a('x', s) == ['x'] and s == []\nassert a('y', s) == ['x', 'y'] and s == ['x']\n\n# total_minutes\nassert t(['1h30m', '2h']) == 210\nassert t(['1h', '30m', '45', '1:30']) == 225\nprint('All docstring checks passed!')\n\" 2>&1"}

### Tool result
Traceback (most recent call last):
  File "<string>", line 7, in <module>
    assert p('1h30m') == 90 and p('2h') == 120 and p('45m') == 45 and p('1:30') == 90 and p('45') == 45
                                                                                          ~^^^^^^
  File "/private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpp_q5dhxn/workspace/bookings/timeutil.py", line 31, in parse_duration
    raise ValueError(f"bad duration: {text!r}")
ValueError: bad duration: '45'

Exit code: 1
[Command failed with exit code 1]

### Tool call: execute
{"command": "cd workspace && python -c \"\nimport re\ntext = '45'\nm = re.fullmatch(r'(?:(\\d+)h)?(?:(\\d+)m)?', text)\nprint('m:', m)\nprint('groups:', m.groups() if m else None)\n\" 2>&1"}

### Tool result
m: None
groups: None

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python -c \"\nimport re\ntext = '45'\nm = re.fullmatch(r'(?:(\\d+)h)?(?:(\\d+)m)?', text)\nprint('m:', m)\n\" 2>&1"}

### Tool result
m: None

[Command succeeded with exit code 0]

### Assistant





### Tool call: write_file
{"file_path": "workspace/bookings/timeutil.py", "content": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n\ndef parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    text = text.strip()\n    # \"1:30\" format (H:MM or MM:SS)\n    if \":\" in text:\n        parts = text.split(\":\")\n        if len(parts) == 2:\n            return int(parts[0]) * 60 + int(parts[1])\n        elif len(parts) == 3:\n            return int(parts[0]) * 60 + int(parts[1]) + int(parts[2])\n        else:\n            raise ValueError(f\"bad duration: {text!r}\")\n    # Bare number means minutes\n    if re.fullmatch(r\"\\d+\", text):\n        return int(text)\n    # \"1h30m\", \"2h\", \"45m\" formats\n    m = re.fullmatch(r\"(\\d+)h(\\d+)m\", text)\n    if m:\n        return int(m.group(1)) * 60 + int(m.group(2))\n    m = re.fullmatch(r\"(\\d+)h\", text)\n    if m:\n        return int(m.group(1)) * 60\n    m = re.fullmatch(r\"(\\d+)m\", text)\n    if m:\n        return int(m.group(1))\n    raise ValueError(f\"bad duration: {text!r}\")"}

### Tool result
Updated file /workspace/bookings/timeutil.py

### Tool call: execute
{"command": "cd workspace && python -c \"\nfrom bookings.timeutil import parse_duration as p\nfrom bookings.billing import billable_blocks as b\nfrom bookings.schedule import add_slot as a, total_minutes as t\n\n# parse_duration docstring examples\nassert p('1h30m') == 90, f'got {p(\\\"1h30m\\\")}'\nassert p('2h') == 120, f'got {p(\\\"2h\\\")}'\nassert p('45m') == 45, f'got {p(\\\"45m\\\")}'\nassert p('1:30') == 90, f'got {p(\\\"1:30\\\")}'\nassert p('45') == 45, f'got {p(\\\"45\\\")}'\nassert p('  2h  ') == 120, f'got {p(\\\"  2h  \\\")}'\nassert p('0') == 0, f'got {p(\\\"0\\\")}'\nassert p('1:30:15') == 105, f'got {p(\\\"1:30:15\\\")}'\nassert p('30:15') == 1815, f'got {p(\\\"30:15\\\")}'\n\n# billable_blocks: round up\nassert b(0) == 0, f'got {b(0)}'\nassert b(15) == 1, f'got {b(15)}'\nassert b(16) == 2, f'got {b(16)}'\nassert b(20) == 2, f'got {b(20)}'\nassert b(45) == 3, f'got {b(45)}'\nassert b(29) == 2, f'got {b(29)}'\nassert b(1) == 1, f'got {b(1)}'\nassert b(14) == 1, f'got {b(14)}'\nassert b(15, 30) == 1, f'got {b(15, 30)}'\nassert b(31, 30) == 2, f'got {b(31, 30)}'\n\n# add_slot: no shared state\nassert a('a') == ['a'], f'got {a(\\\"a\\\")}'\nassert a('b') == ['b'], f'got {a(\\\"b\\\")}'\ns = []\nassert a('x', s) == ['x'], f'got {a(\\\"x\\\", s)}'\nassert s == [], f'shared state: {s}'\nassert a('y', s) == ['x', 'y'], f'got {a(\\\"y\\\", s)}'\nassert s == ['x'], f'shared state: {s}'\n\n# total_minutes\nassert t(['1h30m', '2h']) == 210, f'got {t([\\\"1h30m\\\", \\\"2

### Tool result
Traceback (most recent call last):
  File "<string>", line 35, in <module>
    assert a('y', s) == ['x', 'y'], f'got {a("y", s)}'
           ^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: got ['y']

Exit code: 1
[Command failed with exit code 1]

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py"}

### Tool result
@@ lines 1-19 of 19 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=None):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    if slots is None:
        slots = []
    slots = slots + [slot]
    return slots

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py"}

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Tool call: execute
{"command": "cd workspace && python -m pytest tests/test_bookings.py -v 2>&1"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.13.11, pytest-9.1.1, pluggy-1.6.0 -- ~/Documents/vinAI20K/Day20_061026_t2/K4-DAY20-MULTIAGENTS-NguyenLePhuocTien-2A202602616/.venv/bin/python
cachedir: .pytest_cache
rootdir: /private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpp_q5dhxn/workspace
plugins: langsmith-0.14.4, anyio-4.15.1
collecting ... collected 3 items

tests/test_bookings.py::test_total_minutes_mixed_formats PASSED          [ 33%]
tests/test_bookings.py::test_billable_blocks_rounds_up PASSED            [ 66%]
tests/test_bookings.py::test_add_slot_single_call PASSED                 [100%]

============================== 3 passed in 0.01s ===============================

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python -c \"\nfrom bookings.schedule import add_slot\nprint('add_slot(\\\"a\\\"):', add_slot('a'))\nprint('add_slot(\\\"b\\\"):', add_slot('b'))\ns = []\nprint('add_slot(\\\"x\\\", s):', add_slot('x', s))\nprint('s after first call:', s)\nprint('add_slot(\\\"y\\\", s):', add_slot('y', s))\nprint('s after second call:', s)\n\""}

### Tool result
add_slot("a"): ['a']
add_slot("b"): ['b']
add_slot("x", s): ['x']
s after first call: []
add_slot("y", s): ['y']
s after second call: []

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python -c \"\nfrom bookings.timeutil import parse_duration as p\nfrom bookings.billing import billable_blocks as b\nfrom bookings.schedule import add_slot as a, total_minutes as t\n\n# parse_duration docstring examples\nassert p('1h30m') == 90, f'got {p(\\\"1h30m\\\")}'\nassert p('2h') == 120, f'got {p(\\\"2h\\\")}'\nassert p('45m') == 45, f'got {p(\\\"45m\\\")}'\nassert p('1:30') == 90, f'got {p(\\\"1:30\\\")}'\nassert p('45') == 45, f'got {p(\\\"45\\\")}'\nassert p('  2h  ') == 120, f'got {p(\\\"  2h  \\\")}'\nassert p('0') == 0, f'got {p(\\\"0\\\")}'\nassert p('1:30:15') == 105, f'got {p(\\\"1:30:15\\\")}'\nassert p('30:15') == 1815, f'got {p(\\\"30:15\\\")}'\n\n# billable_blocks: round up\nassert b(0) == 0, f'got {b(0)}'\nassert b(15) == 1, f'got {b(15)}'\nassert b(16) == 2, f'got {b(16)}'\nassert b(20) == 2, f'got {b(20)}'\nassert b(45) == 3, f'got {b(45)}'\nassert b(29) == 2, f'got {b(29)}'\nassert b(1) == 1, f'got {b(1)}'\nassert b(14) == 1, f'got {b(14)}'\nassert b(15, 30) == 1, f'got {b(15, 30)}'\nassert b(31, 30) == 2, f'got {b(31, 30)}'\n\n# add_slot: no shared state\nassert a('a') == ['a'], f'got {a(\\\"a\\\")}'\nassert a('b') == ['b'], f'got {a(\\\"b\\\")}'\n\n# total_minutes\nassert t(['1h30m', '2h']) == 210, f'got {t([\\\"1h30m\\\", \\\"2h\\\"])}'\nassert t(['1h', '30m', '45', '1:30']) == 225, f'got {t([\\\"1h\\\", \\\"30m\\\", \\\"45\\\", \\\"1:30\\\"])}'\nprint('All docstring checks passed!')\n\" 2>&1"}

### Tool result
All docstring checks passed!

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python -m pytest tests/test_bookings.py -v 2>&1"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.13.11, pytest-9.1.1, pluggy-1.6.0 -- ~/Documents/vinAI20K/Day20_061026_t2/K4-DAY20-MULTIAGENTS-NguyenLePhuocTien-2A202602616/.venv/bin/python
cachedir: .pytest_cache
rootdir: /private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpp_q5dhxn/workspace
plugins: langsmith-0.14.4, anyio-4.15.1
collecting ... collected 3 items

tests/test_bookings.py::test_total_minutes_mixed_formats PASSED          [ 33%]
tests/test_bookings.py::test_billable_blocks_rounds_up PASSED            [ 66%]
tests/test_bookings.py::test_add_slot_single_call PASSED                 [100%]

============================== 3 passed in 0.01s ===============================

[Command succeeded with exit code 0]

### Assistant
All 3 tests pass and every docstring example is verified. Here's what I changed:

**`bookings/timeutil.py` — `parse_duration`**: Only handled `"1h30m"` format. Rewrote to support all documented formats: bare numbers (`"45"` → 45), hours-only (`"2h"` → 120), minutes-only (`"45m"` → 45), colon-separated (`"1:30"` → 90), and combined (`"1h30m"` → 90).

**`bookings/billing.py` — `billable_blocks`**: Used `round()` (rounds to nearest), but docstring says "always round UP". Changed to `math.ceil()` and added input validation for negative minutes and non-positive block size.

**`bookings/schedule.py` — `add_slot`**: Had a mutable default argument `slots=[]` causing state sharing between calls. Changed to `slots=None` with a fresh list each call, and used `slots + [slot]` (concatenation) instead of `slots.append(slot)` (mutation) so the original list is never modified.