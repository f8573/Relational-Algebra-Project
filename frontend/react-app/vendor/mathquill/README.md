MathQuill fork (starter)

Goal
----
Provide a minimal fork/extension plan for MathQuill to support extended LaTeX macros (notably `\\mathcal`) and to make it easy to integrate with KaTeX rendering in our React app.

Scope of this starter
---------------------
- Document the approach to patching MathQuill parser/serializer for `\\mathcal`.
- Provide a small React wrapper component `MathQuillFork` (in `src/components`) which lets authors input LaTeX and shows a KaTeX preview that supports `\\mathcal` immediately (no core MathQuill change required yet).
- Outline a concrete patch (files and small diffs) to apply to MathQuill upstream to add `\\mathcal` token handling.

Why this approach
------------------
- Modifying the MathQuill core is higher-risk and requires forking, building, and publishing. The wrapper + KaTeX preview provides immediate UX value while the fork is prepared.
- The README below provides suggested code locations for changes in the MathQuill source and a small test plan.

Patch plan (high-level)
-----------------------
1. Clone upstream MathQuill (https://github.com/mathquill/mathquill) into `vendor/mathquill/upstream`.
2. Identify the LaTeX parser/serializer — typically `src/commands/` and `src/mathspeak/` or latex handling files.
3. Add a command definition for `\\mathcal` (similar to existing `\\mathbf`/`\\mathit` commands) that maps to an internal MathQuill node type (e.g. `mathcal`), with proper parse and toLatex handlers.
4. Update the LaTeX tokenizer to accept `\\mathcal{...}` and produce the `mathcal` node.
5. Add tests in upstream `tests/latex` to ensure round-trip serialization (`latex -> MQ -> latex` preserves `\\mathcal{...}`).
6. Build and test the fork locally; publish as private package or include as submodule in our project.

Quick example of the small token mapping (pseudocode)
---------------------------------------------------
- In command registry add:
  {
    name: 'mathcal',
    latex: '\\mathcal',
    create: function() { return MQ create markup node that renders with \mathcal style },
    toLatex: function(node){ return `\\mathcal{${node.innerLatex}}` }
  }

Integration notes
-----------------
- For security and consistent rendering, always render LaTeX with KaTeX in the preview and final renderer (`window.katex.renderToString`) using `throwOnError:false` and sanitized output.
- If the exam runner stores LaTeX answers, store raw LaTeX and re-render server-side with KaTeX for PDFs/exports.

Next steps (developer tasks)
---------------------------
- Task A: Add the `MathQuillFork` React component (done in this commit) to give immediate UX.
- Task B: Clone MathQuill upstream and prepare a branch with the minimal command addition for `\\mathcal`.
- Task C: Add CI tests for LaTeX round-trip and integration with KaTeX.

Contact
-------
If you want, I can proceed to clone MathQuill into `vendor/mathquill/upstream` and create the patch branches and tests. Say "fork upstream" and I'll continue.
