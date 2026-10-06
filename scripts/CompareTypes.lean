module

public import Lean.Environment

/-! Export the complete raw expression representation of selected theorem types.
The verifier compares the two outputs byte for byte in separate processes. -/

@[expose] public section

open Lean

def main (args : List String) : IO Unit := do
  let [moduleName] := args | throw <| IO.userError "Expected one module name"
  initSearchPath (← findSysroot)
  let env ← importModules #[{ module := moduleName.toName }] {}
    (level := .exported)
  for name in #[`NonCutPoints.exists_two_noncut_points,`NonCutPoints.eq_of_contains_noncut_points,`NonCutPoints.IsNonCutPoint] do
    let some info := env.find? name | throw <| IO.userError s!"Missing declaration: {name}"
    IO.println s!"RAW TYPE {name}"
    IO.println (reprStr info.levelParams)
    IO.println (reprStr info.type)
    if name == `NonCutPoints.IsNonCutPoint then
      IO.println (reprStr info.value?)
