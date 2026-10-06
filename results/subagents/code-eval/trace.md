### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: ls
{"path": "/workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool call: ls
{"path": "/workspace/bookings"}

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py']

### Assistant







### Tool call: ls
{"path": "/workspace/tests"}

### Tool call: read_file
{"file_path": "/workspace/bookings/__init__.py"}

### Tool call: read_file
{"file_path": "/workspace/bookings/billing.py"}

### Tool call: read_file
{"file_path": "/workspace/bookings/calendar_export.py"}

### Tool call: read_file
{"file_path": "/workspace/bookings/schedule.py"}

### Tool call: read_file
{"file_path": "/workspace/bookings/timeutil.py"}

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_bookings.py']

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

### Tool call: read_file
{"file_path": "/workspace/tests/test_bookings.py"}

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
{"command": "cd /workspace && python -m pytest tests/test_bookings.py -v 2>&1"}

### Tool result
[stderr] /bin/sh: line 0: cd: /workspace: No such file or directory

Exit code: 1
[Command failed with exit code 1]

### Tool call: execute
{"command": "python -m pytest tests/test_bookings.py -v"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.13.11, pytest-9.1.1, pluggy-1.6.0 -- ~/Documents/vinAI20K/Day20_061026_t2/K4-DAY20-MULTIAGENTS-NguyenLePhuocTien-2A202602616/.venv/bin/python
cachedir: .pytest_cache
rootdir: /private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpjisefyd5
plugins: langsmith-0.14.4, anyio-4.15.1
collecting ... collected 0 items

============================ no tests ran in 0.00s =============================

[stderr] ERROR: file or directory not found: tests/test_bookings.py

Exit code: 4
[Command failed with exit code 4]

### Tool call: execute
{"command": "cd /workspace && python -m pytest tests/test_bookings.py -v"}

### Tool result
[stderr] /bin/sh: line 0: cd: /workspace: No such file or directory

Exit code: 1
[Command failed with exit code 1]

### Tool call: execute
{"command": "ls /workspace"}

### Tool result
[stderr] ls: /workspace: No such file or directory

Exit code: 1
[Command failed with exit code 1]

### Tool call: execute
{"command": "pwd && ls"}

### Tool result
/private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpjisefyd5
workspace

[Command succeeded with exit code 0]

### Assistant




### Tool call: execute
{"command": "python -m pytest workspace/tests/test_bookings.py -v"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.13.11, pytest-9.1.1, pluggy-1.6.0 -- ~/Documents/vinAI20K/Day20_061026_t2/K4-DAY20-MULTIAGENTS-NguyenLePhuocTien-2A202602616/.venv/bin/python
cachedir: .pytest_cache
rootdir: /private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpjisefyd5
plugins: langsmith-0.14.4, anyio-4.15.1
collecting ... collected 0 items / 1 error

==================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py _______________
ImportError while importing test module '/private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpjisefyd5/workspace/tests/test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
~/Documents/vinAI20K/Day20_061026_t2/K4-DAY20-MULTIAGENTS-NguyenLePhuocTien-2A202602616/tasks/code-eval/workspace/tests/test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ============================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!

### Assistant




### Tool call: execute
{"command": "cd /workspace && PYTHONPATH=/workspace python -m pytest tests/test_bookings.py -v"}

### Tool result
[stderr] /bin/sh: line 0: cd: /workspace: No such file or directory

Exit code: 1
[Command failed with exit code 1]

### Assistant





### Tool call: execute
{"command": "cd /private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpjisefyd5/workspace && PYTHONPATH=. python -m pytest tests/test_bookings.py -v"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.13.11, pytest-9.1.1, pluggy-1.6.0 -- ~/Documents/vinAI20K/Day20_061026_t2/K4-DAY20-MULTIAGENTS-NguyenLePhuocTien-2A202602616/.venv/bin/python
cachedir: .pytest_cache
rootdir: /private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpjisefyd5/workspace
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

### Tool call: read_file
{"file_path": "/workspace/bookings/timeutil.py"}

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

### Assistant
Now I can see the three bugs. Let me fix them:

1. **`parse_duration` in `timeutil.py`**: The regex only matches `XhYm` format, but the docstring says it should also handle `2h`, `45m`, `1:30`, and bare numbers `45`.
2. **`billable_blocks` in `billing.py`**: Uses `round()` (banker's rounding) but the docstring says "always round UP" - need `math.ceil`.
3. **`add_slot` in `schedule.py`**: Mutable default argument `slots=[]` causes shared state across calls, but the docstring says "Separate calls must not share state".



### Tool call: edit_file
{"old_string": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n\ndef parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    m = re.fullmatch(r\"(\\d+)h(\\d+)m\", text.strip())\n    if not m:\n        raise ValueError(f\"bad duration: {text!r}\")\n    return int(m.group(1)) * 60 + int(m.group(2))", "file_path": "/workspace/bookings/timeutil.py", "new_string": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n\ndef parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    text = text.strip()\n    m = re.fullmatch(r\"(\\d+)h(\\d+)m\", text)\n    if m:\n        return int(m.group(1)) * 60 + int(m.group(2))\n    m = re.fullmatch(r\"(\\d+)m\", text)\n    if m:\n        return int(m.group(1))\n    m = re.fullmatch(r\"(\\d+)h\", text)\n    if m:\n        return int(m.group(1)) * 60\n    m = re.fullmatch(r\"(\\d+):(\\d+)\", text)\n    if m:\n        return int(m.group(1)) * 60 + int(m.group(2))\n    raise ValueError(f\"bad duration: {text!r}\")

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/timeutil.py'

### Tool call: edit_file
{"file_path": "/workspace/bookings/schedule.py", "old_string": "\"\"\"Schedule helpers.\"\"\"\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations):\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot, slots=[]):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    slots.append(slot)\n    return slots", "new_string": "\"\"\"Schedule helpers.\"\"\"\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations):\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot, slots=None):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    if slots is None:\n        slots = []\n    slots.append(slot)\n    return slots"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/schedule.py'

### Tool call: edit_file
{"file_path": "/workspace/bookings/billing.py", "old_string": "\"\"\"Billing rules.\"\"\"\n\n\ndef billable_blocks(minutes, block=15):\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    return round(minutes / block)", "new_string": "\"\"\"Billing rules.\"\"\"\nimport math\n\n\ndef billable_blocks(minutes, block=15):\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(\"minutes must be >= 0\")\n    return math.ceil(minutes / block)"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/billing.py'

### Tool call: execute
{"command": "cd /private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpjisefyd5/workspace && PYTHONPATH=. python -m pytest tests/test_bookings.py -v"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.13.11, pytest-9.1.1, pluggy-1.6.0 -- ~/Documents/vinAI20K/Day20_061026_t2/K4-DAY20-MULTIAGENTS-NguyenLePhuocTien-2A202602616/.venv/bin/python
cachedir: .pytest_cache
rootdir: /private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpjisefyd5/workspace
plugins: langsmith-0.14.4, anyio-4.15.1
collecting ... collected 3 items

tests/test_bookings.py::test_total_minutes_mixed_formats PASSED          [ 33%]
tests/test_bookings.py::test_billable_blocks_rounds_up PASSED            [ 66%]
tests/test_bookings.py::test_add_slot_single_call PASSED                 [100%]

============================== 3 passed in 0.01s ===============================

[Command succeeded with exit code 0]

### Assistant




### Tool call: execute
{"command": "cd /private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpjisefyd5/workspace && PYTHONPATH=. python -c \"\nfrom bookings.billing import billable_blocks\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.timeutil import parse_duration\n\n# Test parse_duration formats\nassert parse_duration('1h30m') == 90\nassert parse_duration('2h') == 120\nassert parse_duration('45m') == 45\nassert parse_duration('1:30') == 90\nassert parse_duration('45') == 45\nassert parse_duration('  1h  ') == 60  # whitespace ignored\nassert parse_duration('  45m  ') == 45\n\n# Test billable_blocks\nassert billable_blocks(20) == 2\nassert billable_blocks(45) == 3\nassert billable_blocks(0) == 0\nassert billable_blocks(15) == 1\ntry:\n    billable_blocks(-5)\n    assert False, 'should have raised'\nexcept ValueError:\n    pass\n\n# Test add_slot - separate calls must not share state\nassert add_slot('a') == ['a']\nassert add_slot('b') == ['b']\nassert add_slot('c', ['x', 'y']) == ['x', 'y', 'c']\n\n# Test total_minutes\nassert total_minutes(['1h30m', '2h']) == 210\nassert total_minutes(['45m', '1:30']) == 135\n\nprint('All docstring checks passed!')\n\""}

### Tool result
[stderr] Traceback (most recent call last):
[stderr]   File "<string>", line 11, in <module>
[stderr]     assert parse_duration('45') == 45
[stderr]            ~~~~~~~~~~~~~~^^^^^^
[stderr]   File "/private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpjisefyd5/workspace/bookings/timeutil.py", line 29, in parse_duration
[stderr]     raise ValueError(f"bad duration: {text!r}")
[stderr] ValueError: bad duration: '45'

Exit code: 1
[Command failed with exit code 1]

### Assistant
I need to add support for bare numbers in `parse_duration`.


### Tool call: edit_file
{"file_path": "/workspace/bookings/timeutil.py", "old_string": "    m = re.fullmatch(r\"(\\d+):(\\d+)\", text)\n    if m:\n        return int(m.group(1)) * 60 + int(m.group(2))\n    raise ValueError(f\"bad duration: {text!r}\")", "new_string": "    m = re.fullmatch(r\"(\\d+):(\\d+)\", text)\n    if m:\n        return int(m.group(1)) * 60 + int(m.group(2))\n    m = re.fullmatch(r\"(\\d+)\", text)\n    if m:\n        return int(m.group(1))\n    raise ValueError(f\"bad duration: {text!r}\")"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/timeutil.py'

### Tool call: execute
{"command": "cd /private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpjisefyd5/workspace && PYTHONPATH=. python -m pytest tests/test_bookings.py -v"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.13.11, pytest-9.1.1, pluggy-1.6.0 -- ~/Documents/vinAI20K/Day20_061026_t2/K4-DAY20-MULTIAGENTS-NguyenLePhuocTien-2A202602616/.venv/bin/python
cachedir: .pytest_cache
rootdir: /private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpjisefyd5/workspace
plugins: langsmith-0.14.4, anyio-4.15.1
collecting ... collected 3 items

tests/test_bookings.py::test_total_minutes_mixed_formats PASSED          [ 33%]
tests/test_bookings.py::test_billable_blocks_rounds_up PASSED            [ 66%]
tests/test_bookings.py::test_add_slot_single_call PASSED                 [100%]

============================== 3 passed in 0.01s ===============================

[Command succeeded with exit code 0]

### Assistant




### Tool call: execute
{"command": "cd /private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpjisefyd5/workspace && PYTHONPATH=. python -c \"\nfrom bookings.billing import billable_blocks\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.timeutil import parse_duration\n\n# Test parse_duration formats\nassert parse_duration('1h30m') == 90\nassert parse_duration('2h') == 120\nassert parse_duration('45m') == 45\nassert parse_duration('1:30') == 90\nassert parse_duration('45') == 45\nassert parse_duration('  1h  ') == 60  # whitespace ignored\nassert parse_duration('  45m  ') == 45\n\n# Test billable_blocks\nassert billable_blocks(20) == 2\nassert billable_blocks(45) == 3\nassert billable_blocks(0) == 0\nassert billable_blocks(15) == 1\ntry:\n    billable_blocks(-5)\n    assert False, 'should have raised'\nexcept ValueError:\n    pass\n\n# Test add_slot - separate calls must not share state\nassert add_slot('a') == ['a']\nassert add_slot('b') == ['b']\nassert add_slot('c', ['x', 'y']) == ['x', 'y', 'c']\n\n# Test total_minutes\nassert total_minutes(['1h30m', '2h']) == 210\nassert total_minutes(['45m', '1:30']) == 135\n\nprint('All docstring checks passed!')\n\""}

### Tool result
All docstring checks passed!

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd /private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpjisefyd5/workspace && PYTHONPATH=. python -c \"\nimport bookings\nprint('Import successful')\n\n# Test all modules can be imported\nfrom bookings.billing import billable_blocks\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.timeutil import parse_duration\nfrom bookings.calendar_export import slot_end\n\nprint('All imports successful')\nprint('parse_duration tests:')\nprint('  1h30m ->', parse_duration('1h30m'))\nprint('  2h ->', parse_duration('2h'))\nprint('  45m ->', parse_duration('45m'))\nprint('  1:30 ->', parse_duration('1:30'))\nprint('  45 ->', parse_duration('45'))\n\nprint('billable_blocks tests:')\nprint('  20 ->', billable_blocks(20))\nprint('  45 ->', billable_blocks(45))\nprint('  0 ->', billable_blocks(0))\n\nprint('add_slot tests:')\nprint('  add_slot(\\\"a\\\") ->', add_slot('a'))\nprint('  add_slot(\\\"b\\\") ->', add_slot('b'))\n\nprint('total_minutes tests:')\nprint('  [\\\"1h30m\\\", \\\"2h\\\"] ->', total_minutes(['1h30m', '2h']))\n\nprint('All functionality works!')\n\""}

### Tool result
Import successful
All imports successful
parse_duration tests:
  1h30m -> 90
  2h -> 120
  45m -> 45
  1:30 -> 90
  45 -> 45
billable_blocks tests:
  20 -> 2
  45 -> 3
  0 -> 0
add_slot tests:
  add_slot("a") -> ['a']
  add_slot("b") -> ['b']
total_minutes tests:
  ["1h30m", "2h"] -> 210
All functionality works!

[Command succeeded with exit code 0]

### Assistant
All three bugs have been fixed. Here's a summary of the changes:

### 1. `bookings/timeutil.py` — `parse_duration()` 
The original regex `r"(\d+)h(\d+)m"` only matched `XhYm` format. Fixed to support all formats documented:
- `"1h30m"` → 90 (h+m format)
- `"2h"` → 120 (hours only)
- `"45m"` → 45 (minutes only)
- `"1:30"` → 90 (h:mm format)
- `"45"` → 45 (bare number = minutes)
- Whitespace is ignored as documented.

### 2. `bookings/billing.py` — `billable_blocks()` 
Changed from `round()` (banker's rounding) to `math.ceil()` so that partial blocks are always rounded up as the docstring specifies. Also added a `ValueError` for negative `minutes` values.

### 3. `bookings/schedule.py` — `add_slot()` 
Changed the mutable default argument `slots=[]` to `slots=None` with an internal check `if slots is None: slots = []`. This prevents shared state across separate calls, which the docstring explicitly requires.

All 3 tests pass, and the functions behave according to their docstrings.


### Tool call: summary
{}

### Tool result
Error: summary is not a valid tool, try one of [ls, read_file, write_file, edit_file, delete, glob, grep, execute, task].

### Assistant




### Tool call: execute
{"command": "cat /private/var/folders/c3/95pt1y3x1z79jk8mjdcgvrm80000gp/T/tmpjisefyd5/workspace/bookings/timeutil.py"}

### Tool result
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
    text = text.strip()
    m = re.fullmatch(r"(\d+)h(\d+)m", text)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    m = re.fullmatch(r"(\d+)m", text)
    if m:
        return int(m.group(1))
    m = re.fullmatch(r"(\d+)h", text)
    if m:
        return int(m.group(1)) * 60
    m = re.fullmatch(r"(\d+):(\d+)", text)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    m = re.fullmatch(r"(\d+)", text)
    if m:
        return int(m.group(1))
    raise ValueError(f"bad duration: {text!r}")

[Command succeeded with exit code 0]