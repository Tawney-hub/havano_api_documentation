# Havano POS - Frappe & SaaS Swagger Documentation

This repository contains the interactive Swagger UI and complete OpenAPI 3.0.3 specification for all **121 Frappe RPC, REST DocType resources, SaaS multi-tenant, and ZIMRA fiscalization endpoints** used by the Havano POS system.

Production Base URL: `https://backoffice.havano.pro`

---

## 🚀 How to Host on Vercel Immediately

### Option 1: Deploy with Vercel CLI (Fastest - 30 seconds)
Open your terminal in this folder (`havano-frappe-swagger-docs`) and run:

```bash
# 1. Install or run vercel directly
npx vercel

# 2. Follow the 3 prompts (hit Enter to accept defaults)
# 3. For immediate production deployment:
npx vercel --prod
```

Your live Swagger website URL (e.g. `https://havano-pos-frappe-swagger.vercel.app`) will be printed immediately!

---

### Option 2: Deploy via Vercel Web Dashboard (Drag & Drop or Git)
1. Go to **[vercel.com/new](https://vercel.com/new)**.
2. Either:
   - **Import Git Repository**: Push this directory or branch to GitHub, select it, and click **Deploy** (zero configuration needed).
   - **Upload Directory**: Drag and drop the `havano-frappe-swagger-docs` folder directly into Vercel.
3. Click **Deploy**. Vercel will auto-detect the static site with `vercel.json` and deploy it instantly.

---

### Option 3: Test Locally First
To preview the Swagger site on your machine right now:

```bash
# Using Python
python -m http.server 8080

# Or using Node
npx serve .
```

Open `http://localhost:8080` in your web browser.

---

## 📑 File Structure

```text
havano-frappe-swagger-docs/
├── index.html        # Modern Swagger UI site with Havano POS theme, category filter & Auth Helper
├── openapi.json      # Full OpenAPI 3.0.3 specification (121 endpoints, 16 categories)
├── vercel.json       # Vercel deployment configuration (CORS, cache headers, clean URLs)
├── package.json      # Node/Vercel package configuration
├── generate_spec.py  # Python script to regenerate openapi.json if needed
└── README.md         # Deployment and usage guide
```

---

## 📌 Endpoint Categories Covered (121 Endpoints)

1. **Auth & Multi-Tenant Terminals**: SaaS login, terminal selection & takeover, user shops, session info, and server versions.
2. **Products, Catalog & Bundles**: Product catalog sync, delta modified sync, barcodes, prices, combo bundles, item groups, and UOMs.
3. **Customers & Loyalty**: Customer sync, create customer, account balance queries, loyalty point redemption, and tenant user permissions.
4. **Sales Invoices & POS Upload**: POS sales submission, return credit notes, RPC `make_sale`, and ERP invoice retrieval.
5. **Sales Orders & Quotations**: Sales order pulling and upload, quotation sync, creation, and cancellation.
6. **Payments, MOPs & Shifts**: Payment entries, Modes of Payment, multi-currency rates, cash transfers, cashbook, and shift management.
7. **Expenses Management**: Petty cash claims, expense categories, approvals, and expense synchronization.
8. **Medical & Pharmacy**: Doctors directory, doctor push, prescription dosage directions push and sync.
9. **Inventory & Stock**: Real-time stock balance queries, stock entries, warehouse locations, and stock reconciliations.
10. **Suppliers & Purchasing**: Supplier registration, purchase invoices, and procurement sync.
11. **Master Data & Setup**: Currencies, exchange rates, chart of accounts, tax categories, countries, and company registration.
12. **ZIMRA Fiscalization**: Havano ZIMRA cloud gateway: tokens, day open/close (Z-Report), status, and fiscal invoice transmission.
13. **Restaurant & Hospitality**: Dining areas, table statuses, Kitchen Order Tickets (KOT), and table order closures.
14. **Subscriptions & Billing**: SaaS subscription plans, status, balance top-ups, and subscription renewal payments.
15. **Reports & Analytics**: Daily sales, gross margin analysis, cashier performance, and Frappe Query Reports.
16. **Support & Helpdesk**: Support ticket creation and issue reporting directly from POS.

---

## 🔐 Authentication in Swagger UI

Click the **Auth Helper** button or the green **Authorize** button in Swagger UI:
- **Token Auth**: Header format `Authorization: token <api_key>:<api_secret>` (e.g. `token cashier@havano.pro:MyPassword123`)
- **Bearer Auth**: Header format `Authorization: Bearer <jwt_token>`

