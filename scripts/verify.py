"""Serial, bounded package, compiler, axiom, and exact-type verification.

Use --lake-build for a normal pinned Lake dependency installation and build.
No project olean is used to compile the isolated renamed Challenge.
"""
from __future__ import annotations
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import uuid

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--lean-bin", default=shutil.which("lean"))
parser.add_argument("--lake-build", action="store_true", help="Fetch the pinned cache and run lake build first")
parser.add_argument("--check-package-only", action="store_true", help="Check headers, sizes, and pins without Lean")
parser.add_argument("--output", type=Path, default=ROOT / "verification.json", help="Receipt path")
args = parser.parse_args()
manifest = json.loads((ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
report = {"scope": "Compiler, transitive axiom, and exact type checks; not hosted Comparator",
          "stages": [], "sources": {}}
for name in ["Solution.lean", "Challenge.lean", "comparator.json", "lake-manifest.json",
             "scripts/CompareTypes.lean", "scripts/verify.py", "formalization.yaml", "lean-toolchain"]:
    data = (ROOT / name).read_bytes()
    report["sources"][name] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
for name in ["Solution.lean", "Challenge.lean", "scripts/CompareTypes.lean"]:
    text = (ROOT / name).read_text(encoding="utf-8")
    header = re.sub(r"\A\s*/-.*?-/\s*", "", text, count=1, flags=re.S)
    if not header.startswith("module\n") or len(text.splitlines()) >= 2000:
        raise SystemExit("Missing module header or oversized Lean source: " + name)
solution_text = (ROOT / "Solution.lean").read_text(encoding="utf-8")
if re.search(r"\b(sorry|admit|axiom|unsafe|native_decide)\b", solution_text):
    raise SystemExit("Forbidden proof admission or trust escape in Solution")
if report["sources"]["Challenge.lean"]["bytes"] >= 5 * 1024:
    raise SystemExit("Challenge exceeds configured 5 KiB limit")
challenge_text = (ROOT / "Challenge.lean").read_text(encoding="utf-8")
imports = re.findall(r"^(?:(?:public|private|meta) )*import (.+)$", challenge_text, re.M)
if imports != ["Mathlib.Topology.Separation.Hausdorff", "Mathlib.Topology.Connected.Clopen", "Mathlib.Order.Zorn"]:
    raise SystemExit("Challenge must import Mathlib alone")
selected_names = ['NonCutPoints.exists_two_noncut_points', 'NonCutPoints.eq_of_contains_noncut_points']
config = json.loads((ROOT / "comparator.json").read_text(encoding="utf-8"))
if config["theorem_names"] != selected_names or config["definition_names"]:
    raise SystemExit("Comparator selected declarations do not match the audited contract")
if (ROOT / "lean-toolchain").read_text(encoding="utf-8").strip() != "leanprover/lean4:v4.35.0-rc2":
    raise SystemExit("Lean toolchain file does not match exact pin")
mathlib = next(p for p in manifest["packages"] if p["name"] == "mathlib")
if mathlib["rev"] != "065356127b1dc0016f66b7283ce0ce2c4055aa55":
    raise SystemExit("Mathlib manifest does not match exact pin")
print("PACKAGE CHECKS PASS", flush=True)
if args.check_package_only:
    raise SystemExit(0)
if not args.lean_bin:
    parser.error("Install elan or supply --lean-bin")
if os.name == "nt":
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    handle = ctypes.c_void_p(kernel.GetCurrentProcess())
    process_mask, system_mask = ctypes.c_size_t(), ctypes.c_size_t()
    if not kernel.GetProcessAffinityMask(handle, ctypes.byref(process_mask), ctypes.byref(system_mask)):
        raise ctypes.WinError(ctypes.get_last_error())
    bits = [1 << i for i in range(64) if process_mask.value & (1 << i)]
    if not kernel.SetProcessAffinityMask(handle, ctypes.c_size_t(sum(bits[:1]))):
        raise ctypes.WinError(ctypes.get_last_error())
elif hasattr(os, "sched_getaffinity"):
    os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:1])
launcher = str(Path(args.lean_bin).absolute())
prefix = subprocess.check_output([launcher, "--print-prefix"], cwd=ROOT, text=True).strip()
lean = Path(prefix) / "bin" / ("lean.exe" if os.name == "nt" else "lean")
env = dict(os.environ)
env["PATH"] = str(lean.parent) + os.pathsep + env.get("PATH", "")
env["LEAN_NUM_THREADS"] = "1"
env["LEAN_PATH"] = ""
env.pop("LEAN_SRC_PATH", None)
version = subprocess.check_output([str(lean), "--version"], env=env, text=True).strip()
if "version 4.35.0-rc2," not in version or "11acb17ec6b07a8f9e9173e6845197929540936b" not in version:
    raise SystemExit("Compiler does not match exact pin")
report["lean_version"] = version
report["lean_binary_sha256"] = hashlib.sha256(lean.read_bytes()).hexdigest()

def run_command(stage, command, cwd, environment):
    result = subprocess.run(command, cwd=cwd, env=environment, encoding="utf-8",
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=3600)
    report["stages"].append({"stage": stage, "argv": command, "cwd": str(cwd),
                             "LEAN_PATH": environment["LEAN_PATH"], "exit_code": result.returncode,
                             "output": result.stdout})
    print(result.stdout, end="", flush=True)
    if result.returncode:
        raise RuntimeError(stage + " failed")
    return result.stdout

def run(stage, extra, cwd, environment):
    return run_command(stage, [str(lean), "-j1", "-M3072", *map(str, extra)], cwd, environment)

try:
    if args.lake_build:
        lake = lean.parent / ("lake.exe" if os.name == "nt" else "lake")
        run_command("pinned Mathlib cache", [str(lake), "exe", "cache", "get"], ROOT, env)
        run_command("ordinary Lake build", [str(lake), "build", "--wfail"], ROOT, env)
        if hashlib.sha256((ROOT / "lake-manifest.json").read_bytes()).hexdigest() != report["sources"]["lake-manifest.json"]["sha256"]:
            raise RuntimeError("Lake changed the pinned manifest")
    dep_paths = [ROOT / manifest.get("packagesDir", ".lake/packages") / p["name"] /
                 ".lake/build/lib/lean" for p in manifest["packages"]]
    dep_paths = [p.resolve() for p in dep_paths if p.is_dir()]
    if not dep_paths:
        raise RuntimeError("No dependency build paths; use --lake-build")
    for p in dep_paths:
        for name in ["Solution", "Challenge", "NonCutPoints"]:
            if (p / (name + ".olean")).exists() or (p / name).exists():
                raise RuntimeError("Project artifact contaminates dependency path")
    env["LEAN_PATH"] = os.pathsep.join(map(str, dep_paths))
    report["dependency_paths"] = list(map(str, dep_paths))
    with tempfile.TemporaryDirectory(prefix="noncut-check-") as temp:
        folder = Path(temp)
        run("fresh solution compilation", ["-DwarningAsError=true", "-o", folder / "Solution.olean",
            ROOT / "Solution.lean"], ROOT, env)
        canonical = "CanonicalChallenge_" + uuid.uuid4().hex
        (folder / (canonical + ".lean")).write_bytes((ROOT / "Challenge.lean").read_bytes())
        challenge_output = run("renamed dependency-only challenge",
            ["-o", canonical + ".olean", canonical + ".lean"], folder, env)
        if challenge_output.count("declaration uses `sorry`") != 2:
            raise RuntimeError("Expected exactly two Challenge hole warnings")
        project_env = dict(env)
        project_env["LEAN_PATH"] = str(folder) + os.pathsep + env["LEAN_PATH"]
        challenge_types = run("raw Challenge types", ["--run", ROOT / "scripts/CompareTypes.lean", canonical],
            folder, project_env)
        solution_types = run("raw Solution types", ["--run", ROOT / "scripts/CompareTypes.lean", "Solution"],
            folder, project_env)
        if challenge_types != solution_types:
            raise RuntimeError("Exact raw declaration type representations differ")
        report["exact_selected_types"] = {
            "method": "Byte equality of universe parameter lists and complete derived Repr Lean.Expr output in separate processes, including explicit predicate value",
            "sha256": hashlib.sha256(solution_types.encode()).hexdigest(), "selected_count": 2,
            "predicate_type_and_value_matched": "NonCutPoints.IsNonCutPoint"}
        print("EXACT SELECTED TYPE MATCH: both theorem raw Expr representations and universe lists, plus explicit predicate type and value", flush=True)
        names = selected_names + ["NonCutPoints.IsNonCutPoint"]
        (folder / "AxiomAudit.lean").write_text("module\npublic import Solution\npublic section\n" +
            "\n".join("#print axioms " + name for name in names) + "\n", encoding="utf-8")
        output = run("transitive axiom audit", [folder / "AxiomAudit.lean"], folder, project_env)
        audits = re.findall(r"(?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", output)
        if len(audits) != len(names):
            raise RuntimeError("Incomplete axiom audit")
        permitted = {"propext", "Classical.choice", "Quot.sound"}
        if any({item.strip() for item in a.split(",") if item.strip()} - permitted for a in audits):
            raise RuntimeError("Unexpected transitive axiom")
        report["status"] = "pass"
finally:
    report.setdefault("status", "fail")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print("ALL LOCAL GATES PASS", flush=True)
