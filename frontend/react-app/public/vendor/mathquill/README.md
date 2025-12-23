MathQuill vendor directory

This folder is intended to contain a local copy of the MathQuill distribution
so the project doesn't rely on remote CDNs for MathQuill JS/CSS.

Recommended steps to populate this directory:

1. Run the provided PowerShell script from the project root:

   ```powershell
   cd frontend/react-app
   ./scripts/fetch_mathquill.ps1
   ```

2. Inspect the cloned repository. If it provides a `dist` or `build` folder, copy
   `mathquill.min.js` and `mathquill.css` into this directory. Commit them to your
   repository so they are versioned.

3. If you need to tweak font rendering for specific symbols (e.g., `\mathcal{}`),
   edit `mathquill.css` locally or add additional font files under `public/fonts/`
   and update the CSS to load them.

Notes on fonts:
- Math symbol coverage depends on the fonts you include. Consider bundling
  STIX Two Math or Symbola fonts locally if you need broader Unicode math glyphs.
- For extreme cases (missing glyphs), you may need to modify how MathQuill maps
  commands to glyphs or patch its rendering CSS.

Security note:
- After adding vendor files, run audits on the code and pin the vendor commit or
  include the minified files directly to reduce supply-chain risks.
