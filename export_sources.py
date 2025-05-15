import ast
from pathlib import Path

INCLUDE_DIRS = [
    "qa-testing-utils",
    "qa-pytest-rest",
    "qa-pytest-webdriver",
    "qa-pytest-commons",
    "qa-pytest-examples",
]

EXCLUDE_PATTERNS = {"__pycache__",
                    "venv", "build", "dist", ".hatch", ".tox"}


def should_include(path: Path) -> bool:
    return (
        any(path.parts[0].startswith(d) for d in INCLUDE_DIRS)
        and not any(part in EXCLUDE_PATTERNS for part in path.parts)
        and path.suffix == ".py"
    )


def strip_docstrings_and_comments(source: str) -> str:
    """
    Removes docstrings (via AST) and comments (via line filtering).
    """
    try:
        parsed = ast.parse(source)
        for node in ast.walk(parsed):
            if isinstance(node,
                          (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
                           ast.Module)):
                if (doc := ast.get_docstring(node)) is not None:
                    if isinstance(
                            node.body[0],
                            ast.Expr) and isinstance(
                            node.body[0].value, ast.Str):
                        # Replace docstring with pass to keep structure
                        node.body[0] = ast.Pass()
        source = ast.unparse(parsed)
    except Exception as e:
        print(f"# Warning: AST parse failed: {e}")
        return ""

    # Now strip comments and empty lines
    stripped_lines = []
    for line in source.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "#" in line:
            line = line.split("#", 1)[0].rstrip()
        if line:
            stripped_lines.append(line)

    return "\n".join(stripped_lines)


def main():
    root = Path(".")
    output_path = Path("framework_stripped.txt")
    output_path.write_text("", encoding="utf-8")  # Truncate output

    for file in sorted(root.rglob("*.py")):
        if not should_include(file):
            continue
        try:
            raw = file.read_text(encoding="utf-8")
            clean = strip_docstrings_and_comments(raw)
            if clean:
                with output_path.open("a", encoding="utf-8") as out:
                    out.write(f"{file.relative_to(root)}:\n")
                    out.write(clean + "\n")
                    out.write("\n" + "=" * 80 + "\n")
        except Exception as e:
            print(f"# Failed to process {file}: {e}")

    print(f"✅ Done. Output written to {output_path}")


if __name__ == "__main__":
    main()
