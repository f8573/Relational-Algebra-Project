React + Vite starter for Relational Algebra frontend.

Security notes:
- API calls use relative paths (`/api/...`) to keep same-origin cookies.
- Avoid `dangerouslySetInnerHTML` and use text nodes (`textContent`) or React JSX escaping.
- Configure a strong CSP on the server and avoid inline scripts/styles.

Local vendor installation:
- Place MathQuill JS/CSS into `public/vendor/mathquill/` (already contains placeholders). Replace the placeholder files with upstream releases and pin them in your VCS.
- Using local vendor copies reduces CDN/supply-chain risk and lets you patch small rendering CSS issues locally.

SRI & CSP notes:
- For third-party scripts, prefer local copies or use Subresource Integrity (SRI) when including remote scripts.
- Always serve a strict `Content-Security-Policy` header from the backend; use nonces for allowed inline scripts if necessary.

To run locally (requires Node.js):

```bash
cd frontend/react-app
npm install
npm run dev
```
