# TailorMyCV — Complete Setup Guide
### From Zero to Live in ~30 Minutes

---

## What You'll Have After This Guide

A live, publicly accessible web app at a URL like:
`https://tailormycv.streamlit.app`

Users can upload their CV, paste a job description, pick a mode, and pay ₹20 to download a tailored Word document — all on mobile.

---

## Prerequisites (all free)

| Tool | Where to get it |
|------|-----------------|
| Python 3.10+ | https://python.python.org/downloads |
| Git | https://git-scm.com |
| GitHub account | https://github.com |
| Streamlit Cloud account | https://share.streamlit.io (sign in with GitHub) |
| Anthropic account | https://console.anthropic.com |
| Razorpay account | https://dashboard.razorpay.com |

---

## Part 1 — Run Locally First

### Step 1.1 — Clone / create your project folder

```bash
mkdir tailormycv && cd tailormycv
# Copy app.py, requirements.txt, manifest.json into this folder
```

### Step 1.2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 1.3 — Create a local secrets file

Streamlit reads secrets from `.streamlit/secrets.toml`.

```bash
mkdir .streamlit
```

Create `.streamlit/secrets.toml` with this content:

```toml
# .streamlit/secrets.toml  ← NEVER commit this file to GitHub!

ANTHROPIC_API_KEY     = "sk-ant-api03-XXXXXXXXXXXXXXXXXXXX"
RAZORPAY_PAYMENT_LINK = "https://rzp.io/l/your-link-here"
```

> ⚠️ Add `.streamlit/secrets.toml` to your `.gitignore` immediately:
> ```
> echo ".streamlit/secrets.toml" >> .gitignore
> ```

### Step 1.4 — Run the app

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser. Test the full flow.

---

## Part 2 — Get Your Anthropic API Key

1. Go to https://console.anthropic.com
2. Sign up / log in
3. Click **API Keys** in the left sidebar
4. Click **Create Key** → name it `tailormycv-prod`
5. Copy the key (starts with `sk-ant-api03-…`) — you only see it once!
6. Paste it into your `secrets.toml` as `ANTHROPIC_API_KEY`

**Billing note:** Claude Sonnet costs ~$0.003 per CV generation.
At ₹20/user revenue, you're profitable after accounting for ~₹0.25 API cost.

---

## Part 3 — Set Up the ₹20 Razorpay Payment Link

### Step 3.1 — Create a Razorpay account

1. Go to https://dashboard.razorpay.com/signup
2. Complete KYC (takes 1–2 business days for full activation)
3. For testing, use **Test Mode** (toggle in top bar)

### Step 3.2 — Create a Payment Link

1. In the dashboard, go to **Payment Links** → **Create Payment Link**
2. Fill in:
   - **Amount:** ₹20
   - **Description:** "TailorMyCV — AI Tailored Resume Download"
   - **Reference ID:** (optional, for tracking)
3. Click **Create** → copy the short link (e.g., `https://rzp.io/l/tailormycv`)
4. Paste this URL into your `secrets.toml` as `RAZORPAY_PAYMENT_LINK`

### Step 3.3 — (Advanced) Webhook-based verification

For production-grade payment verification, replace the trust-based button with a webhook:

```python
# In a separate webhook handler (e.g., Flask or FastAPI sidecar):
import razorpay
import hmac, hashlib

client = razorpay.Client(auth=("YOUR_KEY_ID", "YOUR_KEY_SECRET"))

def verify_payment(order_id, payment_id, signature):
    body = f"{order_id}|{payment_id}"
    expected = hmac.new(
        b"YOUR_KEY_SECRET",
        body.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

For the ₹20 MVP, the trust-based "I've Paid" button is acceptable.
Add webhook verification before scaling to 100+ daily users.

---

## Part 4 — Deploy to Streamlit Cloud (Free)

### Step 4.1 — Push to GitHub

```bash
git init
git add app.py requirements.txt manifest.json
# Do NOT add .streamlit/secrets.toml
git commit -m "Initial TailorMyCV deployment"
git remote add origin https://github.com/YOUR_USERNAME/tailormycv.git
git push -u origin main
```

### Step 4.2 — Connect to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click **New app**
3. Select your GitHub repo → Branch: `main` → Main file: `app.py`
4. Click **Advanced settings**

### Step 4.3 — Add Secrets on Streamlit Cloud

In **Advanced settings → Secrets**, paste:

```toml
ANTHROPIC_API_KEY     = "sk-ant-api03-XXXXXXXXXXXXXXXXXXXX"
RAZORPAY_PAYMENT_LINK = "https://rzp.io/l/your-link-here"
```

5. Click **Deploy!** — Streamlit will install packages and launch your app.
6. Share your URL: `https://YOUR_APP_NAME.streamlit.app`

---

## Part 5 — PWA Setup (Add to Home Screen)

Streamlit doesn't natively serve a `manifest.json`, but you can enable PWA behavior:

### Option A — Quick: Inject via HTML (already in app.py)

The CSS in `app.py` already makes the app feel native on mobile (full-width, no browser chrome shown).

### Option B — Full PWA with custom domain (recommended for production)

1. Buy a `.in` domain (e.g., `tailormycv.in`) from GoDaddy or Namecheap (~₹800/yr)
2. Use **Cloudflare** (free) to proxy your Streamlit URL to your domain
3. Place `manifest.json` and icons at the root of a small static site (or use GitHub Pages)
4. Add this meta tag to your Streamlit HTML injection:

```python
st.markdown("""
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#4F46E5">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
""", unsafe_allow_html=True)
```

5. On Android Chrome: open your app URL → tap ⋮ → **Add to Home Screen**
6. On iOS Safari: tap Share → **Add to Home Screen**

### Icons needed for PWA

Create two square PNG icons:
- `icon-192.png` — 192×192 pixels
- `icon-512.png` — 512×512 pixels

Use Canva (free) to design a simple "TC✦" logo in Indigo (#4F46E5) on white.

---

## Part 6 — Marketing Your Micro-SaaS (Indian Market)

| Channel | What to post |
|---------|-------------|
| LinkedIn | "I built a ₹20 AI CV tool in a weekend" — founders love this |
| Naukri community forums | Share as a helpful resource |
| IIT/NIT WhatsApp alumni groups | "Free trial for 24 hours" |
| r/india, r/indianstartups | Show your revenue day 1 |
| Telegram job groups | Pin the link with a short demo GIF |

**Pricing tip:** Start at ₹20 to remove friction. Once you have 100+ users,
test ₹49 (still < coffee price). Many SaaS tools charge ₹499+ for similar features.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: PyPDF2` | Run `pip install PyPDF2` |
| `AuthenticationError` from Anthropic | Check your API key has no extra spaces |
| Razorpay link not opening | Make sure the link is live (not draft) in dashboard |
| App crashes on DOCX upload | Ensure `docx2txt` is installed: `pip install docx2txt` |
| Streamlit Cloud says "Resource limit" | Upgrade to Streamlit Team ($0 for open-source) or use lite mode |
| Blank page on mobile | Clear browser cache, disable ad-blockers |

---

## File Structure

```
tailormycv/
├── app.py                  ← Main Streamlit application
├── requirements.txt        ← Python dependencies
├── manifest.json           ← PWA manifest
├── .gitignore              ← Includes .streamlit/secrets.toml
├── .streamlit/
│   └── secrets.toml        ← API keys (NEVER commit this!)
└── README.md               ← Optional: describe your project
```

---

## Revenue Projection

| Users/day | Revenue/day | Revenue/month |
|-----------|-------------|---------------|
| 10 | ₹200 | ₹6,000 |
| 50 | ₹1,000 | ₹30,000 |
| 200 | ₹4,000 | ₹1,20,000 |

API costs at 200 users/day ≈ ₹1,500/month. Net margin: ~62% 🚀

---

*Built with Streamlit + Claude (Anthropic) · Setup guide v1.0*
