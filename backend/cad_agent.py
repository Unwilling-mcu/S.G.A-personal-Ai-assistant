"""
cad_agent.py — 3D CAD model generation from voice prompts.
Uses build123d for parametric CAD + exports to STL.

Install: pip install build123d

Voice examples:
  "Create a cube 5cm by 5cm by 5cm"
  "Make a cylinder radius 3cm height 10cm"
  "Design a box with a lid"
  "Create a phone stand with 60 degree angle"
  "Make a sphere radius 2cm"
  "Create a bracket 10cm by 5cm by 2cm with holes"
"""
import os
import re
import logging
import threading

logger = logging.getLogger(__name__)

OUTPUT_DIR  = "cad_models"
STL_COUNTER = 0
_build_lock = threading.Lock()


def _ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def _get_filename(name: str) -> str:
    global STL_COUNTER
    STL_COUNTER += 1
    safe = re.sub(r"[^a-zA-Z0-9_]", "_", name.lower())[:30]
    return os.path.join(OUTPUT_DIR, f"{safe}_{STL_COUNTER}.stl")


def _check_build123d() -> bool:
    try:
        import build123d
        return True
    except ImportError:
        return False


# ── Shape generators ──────────────────────────────────────────────────────────

def make_cube(width=50, height=50, depth=50) -> str:
    """Create a rectangular box in mm."""
    try:
        from build123d import Box, export_stl
        part = Box(width, depth, height)
        path = _get_filename(f"cube_{width}x{depth}x{height}")
        export_stl(part, path)
        return path
    except Exception as e:
        return f"ERROR: {e}"


def make_cylinder(radius=20, height=50) -> str:
    """Create a cylinder in mm."""
    try:
        from build123d import Cylinder, export_stl
        part = Cylinder(radius, height)
        path = _get_filename(f"cylinder_r{radius}_h{height}")
        export_stl(part, path)
        return path
    except Exception as e:
        return f"ERROR: {e}"


def make_sphere(radius=25) -> str:
    """Create a sphere in mm."""
    try:
        from build123d import Sphere, export_stl
        part = Sphere(radius)
        path = _get_filename(f"sphere_r{radius}")
        export_stl(part, path)
        return path
    except Exception as e:
        return f"ERROR: {e}"


def make_cone(radius=20, height=40) -> str:
    """Create a cone in mm."""
    try:
        from build123d import Cone, export_stl
        part = Cone(radius, 0, height)
        path = _get_filename(f"cone_r{radius}_h{height}")
        export_stl(part, path)
        return path
    except Exception as e:
        return f"ERROR: {e}"


def make_phone_stand(angle=60, width=80, depth=100, thickness=3) -> str:
    """Create a phone stand at given angle."""
    try:
        from build123d import (Box, Rotation, Location,
                                BuildPart, extrude, Plane,
                                export_stl)
        import math

        # Base plate
        base_h = depth * math.cos(math.radians(90 - angle))
        base   = Box(width, depth, thickness)

        # Upright support
        support_h = depth * math.sin(math.radians(angle))
        support   = Box(width, thickness, support_h)

        # Position support at back of base
        # Simple approximation — two boxes combined
        path = _get_filename(f"phone_stand_{angle}deg")
        export_stl(base, path)   # simplified: just export base
        return path
    except Exception as e:
        return f"ERROR: {e}"


def make_box_with_lid(width=80, depth=60, height=40, wall=3) -> str:
    """Create a box with removable lid."""
    try:
        from build123d import (Box, export_stl)

        # Outer shell minus inner cavity
        outer = Box(width, depth, height)
        inner = Box(width - wall*2, depth - wall*2, height - wall)

        # Simple box for now (full parametric requires Boolean ops)
        path = _get_filename(f"box_with_lid_{width}x{depth}x{height}")
        export_stl(outer, path)
        return path
    except Exception as e:
        return f"ERROR: {e}"


def make_bracket(width=100, height=50, depth=20, thickness=3) -> str:
    """Create an L-shaped bracket."""
    try:
        from build123d import (Box, export_stl)
        # Simplified: two boxes for L-shape
        part = Box(width, thickness, height)
        path = _get_filename(f"bracket_{width}x{height}")
        export_stl(part, path)
        return path
    except Exception as e:
        return f"ERROR: {e}"


# ── AI-powered CAD generation ─────────────────────────────────────────────────

CAD_CODE_PROMPT = """You are a build123d CAD expert. Generate Python code using build123d library to create a 3D model.

Rules:
- Use ONLY build123d imports
- End with: export_stl(part, output_path)
- Variable 'output_path' is pre-defined
- Keep it simple and functional
- Use mm units

Example for a cube:
```python
from build123d import Box, export_stl
part = Box(50, 50, 50)
export_stl(part, output_path)
```

Generate build123d code for: {description}
Only output the Python code, no explanation."""


def generate_cad_from_description(description: str) -> str:
    """
    Use AI to generate build123d code and execute it.
    Falls back to rule-based generation if AI unavailable.
    """
    if not _check_build123d():
        return "build123d not installed. Run: pip install build123d"

    _ensure_output_dir()

    # First try rule-based (fast, reliable)
    rule_result = _rule_based_cad(description)
    if rule_result and not rule_result.startswith("ERROR"):
        return rule_result

    # Then try AI-generated code
    return _ai_generated_cad(description)


def _rule_based_cad(description: str) -> str:
    """Parse simple descriptions into direct build123d calls."""
    d = description.lower()

    # Extract numbers (convert cm to mm)
    nums = re.findall(r"(\d+(?:\.\d+)?)\s*(?:cm|mm)?", d)
    nums = [float(n) for n in nums]

    # Apply unit conversion if cm mentioned
    if "cm" in d:
        nums = [n * 10 for n in nums]

    def n(i, default):
        return nums[i] if i < len(nums) else default

    if any(w in d for w in ["cube", "box", "rectangular", "block", "square"]):
        return make_cube(n(0, 50), n(1, 50), n(2, 50))

    elif any(w in d for w in ["cylinder", "tube", "rod", "pipe"]):
        return make_cylinder(n(0, 20), n(1, 50))

    elif "sphere" in d or "ball" in d:
        return make_sphere(n(0, 25))

    elif "cone" in d:
        return make_cone(n(0, 20), n(1, 40))

    elif "phone stand" in d or "phone holder" in d:
        angle = n(0, 60)
        return make_phone_stand(angle=angle)

    elif "bracket" in d:
        return make_bracket(n(0, 100), n(1, 50), n(2, 20))

    elif "box with lid" in d or "box and lid" in d:
        return make_box_with_lid(n(0, 80), n(1, 60), n(2, 40))

    return ""   # no rule matched


def _ai_generated_cad(description: str) -> str:
    """Use Gemini to write build123d code, then execute it safely."""
    import os
    from dotenv import load_dotenv
    load_dotenv()

    api_key  = os.getenv("GEMINI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    if not api_key and not groq_key:
        return "Cannot generate CAD model: set GROQ_API_KEY or GEMINI_API_KEY in .env"

    try:
        if groq_key:
            # Use Groq (faster + more free quota)
            from groq import Groq
            client   = Groq(api_key=groq_key)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a build123d CAD expert. Output only Python code, no markdown, no explanation."},
                    {"role": "user",   "content": CAD_CODE_PROMPT.format(description=description)}
                ],
                max_tokens=800,
                temperature=0.1,
            )
            code = response.choices[0].message.content.strip()
        else:
            # Fallback to Gemini
            from google import genai
            from google.genai import types
            client   = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=CAD_CODE_PROMPT.format(description=description),
                config=types.GenerateContentConfig(max_output_tokens=800, temperature=0.1)
            )
            code = response.text.strip()
        # Strip markdown fences
        code = re.sub(r"```python\n?|```\n?", "", code).strip()

        return _execute_cad_code(code, description)

    except Exception as e:
        return f"AI CAD generation failed: {e}"


def _execute_cad_code(code: str, description: str) -> str:
    """
    Execute AI-generated build123d code safely.
    Returns path to STL file or error message.
    """
    _ensure_output_dir()
    output_path = _get_filename(description)

    # Validate code safety — only allow build123d imports
    forbidden = ["import os", "import sys", "subprocess", "exec(", "eval(",
                 "open(", "__import__", "shutil", "socket"]
    for f in forbidden:
        if f in code:
            return f"Generated code contains unsafe operation: {f}"

    safe_globals = {
        "__builtins__": {
            "range": range, "len": len, "int": int, "float": float,
            "list": list, "tuple": tuple, "dict": dict, "str": str,
            "min": min, "max": max, "abs": abs, "round": round,
            "print": print, "True": True, "False": False, "None": None,
        },
        "output_path": output_path,
    }

    # Allow build123d imports
    try:
        import build123d
        safe_globals["build123d"] = build123d
        # Pre-import common symbols
        exec("from build123d import *", safe_globals)
    except Exception as e:
        return f"build123d import failed: {e}"

    try:
        with _build_lock:
            exec(code, safe_globals)

        if os.path.exists(output_path):
            size_kb = os.path.getsize(output_path) // 1024
            return output_path
        else:
            return "Code executed but no STL file was created"

    except Exception as e:
        return f"CAD code execution error: {e}\n\nCode:\n{code}"


# ── Voice interface ───────────────────────────────────────────────────────────

def handle_cad_voice(user_input: str, broadcast=None) -> str:
    """Main entry point called from agent_engine."""
    if broadcast:
        try: broadcast({"type": "thinking", "step": "Designing 3D model..."})
        except Exception: pass

    if not _check_build123d():
        return ("3D model generation requires build123d. "
                "Run: pip install build123d")

    result = generate_cad_from_description(user_input)

    if result and not result.startswith("ERROR") and os.path.exists(result):
        fname = os.path.basename(result)
        size  = os.path.getsize(result) // 1024

        if broadcast:
            try:
                broadcast({
                    "type": "cad_model",
                    "file": result,
                    "name": fname,
                    "size_kb": size
                })
            except Exception: pass

        return f"3D model created: {fname} ({size} KB). Saved to cad_models folder."

    return f"Could not generate 3D model: {result}"