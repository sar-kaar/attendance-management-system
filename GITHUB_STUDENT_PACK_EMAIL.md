# GitHub Student Pack — Email/OTP Relevant Offers (From Current Page)

> Source: GitHub Education page you pasted. Only includes services relevant to email, OTP, auth, domains, secrets.

---

## ✅ Directly Useful for Email/OTP

| Service | Offer | Use For | Claim |
|---------|-------|---------|-------|
| **Testmail** | Free Essential plan while student | **Email testing** — unlimited addresses/mailboxes, API for automated tests | [Claim](https://education.github.com/pack/offers/testmail) |
| **Namecheap** | 1 yr `.me` domain + 1 yr SSL | **Custom domain** for sending email (e.g., `mg.yourname.me`) | [Claim](https://education.github.com/pack/offers/namecheap) |
| **Name.com** | Free domain (25+ TLDs: .live, .studio, .dev, .app) | Alternative custom domain | [Claim](https://education.github.com/pack/offers/name.com) |
| **1Password** | Free 1 yr + Developer Tools | **Store SMTP credentials, API keys** securely | [Claim](https://education.github.com/pack/offers/1password) |
| **Clerk** | Free Pro plan while student | **Auth alternative** — includes email/password, MFA, but NOT transactional email sending | [Claim](https://education.github.com/pack/offers/clerk) |

---

## 🔧 Infrastructure & Supporting Services

| Service | Offer | Use For |
|---------|-------|---------|
| **Microsoft Azure** | $100 credit + 25+ free services | Already have — App Service, Key Vault, PostgreSQL |
| **DigitalOcean** | $200 credit (expires 7/31/26) | Backup hosting, managed DBs, Spaces (S3-compatible) |
| **Heroku** | $13/mo × 24 months | Alternative deployment (but needs credit card) |
| **MongoDB Atlas** | $50 credit + free M0 cluster | Alternative database |
| **GitHub Pro** | Free while student | Private repos, Codespaces (60 hrs/mo), Actions (2000 min/mo) |

---

## 📊 Monitoring & Error Tracking (Free for Students)

| Service | Offer | Use For |
|---------|-------|---------|
| **Sentry** | 50K errors, 100K txns, 1GB attachments, 1 yr | **Error tracking** for email/OTP failures |
| **Datadog** | Pro (10 servers) free 2 yrs | Infrastructure monitoring |
| **New Relic** | Free while student ($300/mo value) | APM, logs, alerts |
| **Honeybadger** | Small account free 1 yr | Exception + uptime monitoring |
| **Codecov** | Free public + private repos | Code coverage |

---

## 🛠️ Developer Tools

| Service | Offer | Use For |
|---------|-------|---------|
| **GitHub Codespaces** | Pro free | Cloud dev environment |
| **JetBrains** | Free student license (renew annually) | PyCharm Pro, IntelliJ |
| **GitKraken** | Student plan free 6 mo, then 80% off | Git GUI |
| **Postman** | Pro free | API testing (test email/OTP endpoints) |
| **Requestly** | Pro free 1 yr ($270 value) | Intercept/modify HTTP (debug email APIs) |

---

## ❌ NOT in Current List (Check Separately)

These were previously in Student Pack but **not visible in your pasted page**:

| Service | Status | Alternative |
|---------|--------|-------------|
| **Mailgun** | Not shown | Claim via [education.github.com/pack](https://education.github.com/pack) search |
| **SendGrid** | Not shown | Same — search pack offers |
| **Stripe** | **IS listed** — waived fees on first $1K | Payments if needed |

> **Action**: Go to https://education.github.com/pack → search "Mailgun" and "SendGrid" — they may still be available but not rendered in your view.

---

## 🎯 Recommended Setup for AMS (Free)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Claim Namecheap → get yourname.me domain                │
│ 2. Claim Testmail → test email flows in CI/CD              │
│ 3. Claim 1Password → store SMTP creds securely             │
│ 4. Search Pack for Mailgun/SendGrid → claim if available   │
│ 5. If no Mailgun/SendGrid → use Brevo/Resend (free forever)│
└─────────────────────────────────────────────────────────────┘
```

---

## 🔗 Quick Claim Links

| Service | Direct Claim URL |
|---------|------------------|
| Testmail | https://education.github.com/pack/offers/testmail |
| Namecheap | https://education.github.com/pack/offers/namecheap |
| Name.com | https://education.github.com/pack/offers/name.com |
| 1Password | https://education.github.com/pack/offers/1password |
| Clerk | https://education.github.com/pack/offers/clerk |
| Sentry | https://education.github.com/pack/offers/sentry |
| Datadog | https://education.github.com/pack/offers/datadog |
| DigitalOcean | https://education.github.com/pack/offers/digitalocean |
| MongoDB | https://education.github.com/pack/offers/mongodb |
| JetBrains | https://education.github.com/pack/offers/jetbrains |
| Postman | https://education.github.com/pack/offers/postman |

---

## 📝 Next Steps for You

1. **Open each link above** → Click "Get this offer" → Follow verification
2. **Fill in `EMAIL_OTP_SERVICES.md`** with your actual credentials
3. **Add to Azure Key Vault** + **GitLab CI/CD Variables**
4. **Tell me when done** → I'll wire Django settings (Phase 1)