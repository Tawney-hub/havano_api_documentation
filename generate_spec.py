import json
import os

out_dir = r"c:\Users\user\Desktop\Havano_POS_2026-main\havano-frappe-swagger-docs"
os.makedirs(out_dir, exist_ok=True)

spec = {
    "openapi": "3.0.3",
    "info": {
        "title": "Havano POS - Frappe & SaaS Backoffice API",
        "description": "API documentation for Frappe Framework core REST/RPC APIs and Havano POS SaaS backoffice endpoints. Target server: https://backoffice.havano.pro.",
        "version": "2026.1.0",
        "contact": {
            "name": "Havano Engineering",
            "url": "https://backoffice.havano.pro"
        }
    },
    "servers": [
        {
            "url": "https://backoffice.havano.pro",
            "description": "Production SaaS Server"
        }
    ],
    "tags": [
        {"name": "Frappe Core APIs", "description": "Standard Frappe Framework endpoints: Auth, DocType CRUD, RPCs, and System Methods"},
        {"name": "Auth & Terminals", "description": "POS authentication, terminal selection, user sessions and branches"},
        {"name": "Products & Bundles", "description": "Catalog sync, prices, barcodes, bundles, and item groups"},
        {"name": "Customers & Loyalty", "description": "Customer sync, creation, balance checks, and loyalty redemption"},
        {"name": "Sales Invoices & POS", "description": "POS sale submission, return credit notes, and sales invoices"},
        {"name": "Orders & Quotations", "description": "Sales orders and sales quotations creation and sync"},
        {"name": "Payments & Shifts", "description": "Payment entries, payment modes, cash transfers, and shift management"},
        {"name": "Expenses", "description": "Petty cash claims, categories, and approvals"},
        {"name": "Pharmacy & Medical", "description": "Doctors and prescription dosage directions"},
        {"name": "Inventory & Stock", "description": "Stock balance, stock entries, and warehouses"},
        {"name": "Suppliers & Purchasing", "description": "Vendors, purchase invoices, and GRVs"},
        {"name": "Master Data & Setup", "description": "Currencies, exchange rates, GL accounts, taxes, and users"},
        {"name": "ZIMRA Fiscalization", "description": "Fiscal day open/close, status, and ZIMRA invoice signatures"},
        {"name": "Restaurant & KDS", "description": "Dining tables, kitchen order tickets (KOT), and table orders"},
        {"name": "Subscriptions & Billing", "description": "SaaS plans, balance top-ups, and renewal payments"},
        {"name": "Reports & Analytics", "description": "Daily sales, profitability metrics, and Frappe reports"}
    ],
    "components": {
        "securitySchemes": {
            "FrappeTokenAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "Frappe API token format: `token <api_key>:<api_secret>`"
            },
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            },
            "CookieAuth": {
                "type": "apiKey",
                "in": "cookie",
                "name": "sid",
                "description": "Frappe session cookie established via POST /api/method/login"
            }
        }
    },
    "security": [
        {"FrappeTokenAuth": []},
        {"CookieAuth": []}
    ],
    "paths": {}
}

paths = spec["paths"]

def ep(path, method, tag, summary, desc, params=None, body_example=None, resp_example=None):
    if path not in paths:
        paths[path] = {}
    
    op = {
        "tags": [tag],
        "summary": summary,
        "description": desc,
        "parameters": params or [],
        "responses": {
            "200": {
                "description": "Successful operation",
                "content": {"application/json": {"example": resp_example or {"message": "Success"}}}
            },
            "401": {
                "description": "Unauthorized",
                "content": {"application/json": {"example": {"message": "Invalid credentials or session expired"}}}
            },
            "404": {
                "description": "Not Found"
            },
            "500": {
                "description": "Server Error",
                "content": {"application/json": {"example": {"exc": "frappe.exceptions.ValidationError"}}}
            }
        }
    }
    
    if body_example is not None:
        op["requestBody"] = {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {"type": "object"},
                    "example": body_example
                }
            }
        }
    
    paths[path][method.lower()] = op

# =========================================================================
# 1. FRAPPE CORE FRAMEWORK STANDARD APIS (FIRST AND AUTO-SELECTED)
# =========================================================================
ep(
    "/api/method/login", "POST", "Frappe Core APIs",
    "Standard Frappe Login",
    "Official Frappe Framework authentication endpoint. Takes username/email and password only. Sets session cookie 'sid' and returns user full name.",
    body_example={
        "usr": "administrator",
        "pwd": "admin_password"
    },
    resp_example={
        "message": "Logged In",
        "home_page": "/app",
        "full_name": "Administrator"
    }
)

ep(
    "/api/method/logout", "GET", "Frappe Core APIs",
    "Frappe Logout",
    "Destroys active Frappe session and invalidates session cookies.",
    resp_example={"message": "Logged Out"}
)

ep(
    "/api/method/frappe.auth.get_logged_user", "GET", "Frappe Core APIs",
    "Get Current Logged-in User",
    "Returns the email / user ID of the currently authenticated user.",
    resp_example={"message": "administrator"}
)

ep(
    "/api/method/frappe.ping", "GET", "Frappe Core APIs",
    "Frappe Ping (Health Check)",
    "Standard Frappe health check endpoint. Returns 'pong' if server is healthy.",
    resp_example={"message": "pong"}
)

ep(
    "/api/method/frappe.handler.version", "GET", "Frappe Core APIs",
    "Get Frappe Framework Version",
    "Returns active Frappe Framework version string.",
    resp_example={"message": "15.40.0"}
)

ep(
    "/api/resource/{doctype}", "GET", "Frappe Core APIs",
    "List DocType Records (Universal REST)",
    "Standard Frappe REST endpoint to query any DocType (e.g. Item, Customer, Sales Invoice, User, Mode of Payment). Supports JSON filters, field selection, sorting, and pagination.",
    params=[
        {"name": "doctype", "in": "path", "required": True, "schema": {"type": "string"}, "example": "Item"},
        {"name": "fields", "in": "query", "schema": {"type": "string"}, "example": "[\"name\", \"item_name\", \"standard_rate\"]"},
        {"name": "filters", "in": "query", "schema": {"type": "string"}, "example": "[[\"is_stock_item\",\"=\",1]]"},
        {"name": "order_by", "in": "query", "schema": {"type": "string"}, "example": "creation desc"},
        {"name": "limit_page_length", "in": "query", "schema": {"type": "integer", "default": 20}},
        {"name": "limit_start", "in": "query", "schema": {"type": "integer", "default": 0}}
    ],
    resp_example={"data": [{"name": "ITEM-00102", "item_name": "Paracetamol 500mg", "standard_rate": 2.50}]}
)

ep(
    "/api/resource/{doctype}", "POST", "Frappe Core APIs",
    "Create New Document (Universal REST)",
    "Creates a new record for any DocType in Frappe.",
    params=[{"name": "doctype", "in": "path", "required": True, "schema": {"type": "string"}, "example": "Customer"}],
    body_example={"customer_name": "Acme Holdings", "customer_group": "Commercial", "territory": "Zimbabwe"},
    resp_example={"data": {"name": "Acme Holdings", "doctype": "Customer", "customer_name": "Acme Holdings"}}
)

ep(
    "/api/resource/{doctype}/{docname}", "GET", "Frappe Core APIs",
    "Get Single Document (Universal REST)",
    "Fetches a document by its primary key/name, including all child tables.",
    params=[
        {"name": "doctype", "in": "path", "required": True, "schema": {"type": "string"}, "example": "Item"},
        {"name": "docname", "in": "path", "required": True, "schema": {"type": "string"}, "example": "ITEM-00102"}
    ],
    resp_example={"data": {"name": "ITEM-00102", "item_name": "Paracetamol 500mg", "stock_uom": "Pack", "standard_rate": 2.50}}
)

ep(
    "/api/resource/{doctype}/{docname}", "PUT", "Frappe Core APIs",
    "Update Document (Universal REST)",
    "Updates fields of an existing document.",
    params=[
        {"name": "doctype", "in": "path", "required": True, "schema": {"type": "string"}, "example": "Item"},
        {"name": "docname", "in": "path", "required": True, "schema": {"type": "string"}, "example": "ITEM-00102"}
    ],
    body_example={"standard_rate": 2.75},
    resp_example={"data": {"name": "ITEM-00102", "standard_rate": 2.75}}
)

ep(
    "/api/resource/{doctype}/{docname}", "DELETE", "Frappe Core APIs",
    "Delete Document (Universal REST)",
    "Deletes a document from Frappe database.",
    params=[
        {"name": "doctype", "in": "path", "required": True, "schema": {"type": "string"}, "example": "Item"},
        {"name": "docname", "in": "path", "required": True, "schema": {"type": "string"}, "example": "ITEM-00102"}
    ],
    resp_example={"message": "ok"}
)

ep(
    "/api/method/frappe.client.get", "POST", "Frappe Core APIs",
    "RPC: frappe.client.get",
    "RPC call returning full document dictionary.",
    body_example={"doctype": "Customer", "name": "Walk-in Customer"},
    resp_example={"message": {"name": "Walk-in Customer", "doctype": "Customer"}}
)

ep(
    "/api/method/frappe.client.get_list", "POST", "Frappe Core APIs",
    "RPC: frappe.client.get_list",
    "RPC call returning list of documents matching filters.",
    body_example={"doctype": "Item", "fields": ["name", "item_name"], "limit_page_length": 10},
    resp_example={"message": [{"name": "ITEM-00102", "item_name": "Paracetamol 500mg"}]}
)

ep(
    "/api/method/frappe.client.set_value", "POST", "Frappe Core APIs",
    "RPC: frappe.client.set_value",
    "RPC call to quickly update a single field on a document.",
    body_example={"doctype": "Item", "name": "ITEM-00102", "fieldname": "standard_rate", "value": 2.80},
    resp_example={"message": {"name": "ITEM-00102", "standard_rate": 2.80}}
)

ep(
    "/api/method/frappe.client.insert", "POST", "Frappe Core APIs",
    "RPC: frappe.client.insert",
    "RPC call inserting a document dictionary.",
    body_example={"doc": {"doctype": "Item Group", "item_group_name": "Supplements", "parent_item_group": "All Item Groups"}},
    resp_example={"message": {"name": "Supplements", "doctype": "Item Group"}}
)

# =========================================================================
# 2. AUTH & TERMINALS - EXACT CODEBASE STRUCTURE (USR, PWD, TIMEZONE)
# =========================================================================
ep(
    "/api/method/saas_api.www.api.login", "POST", "Auth & Terminals",
    "SaaS User Login (Direct from auth_service.py)",
    "Exact login payload sent by Havano POS `services/auth_service.py` to authenticate cashiers with the backoffice. Structure requires ONLY `usr`, `pwd`, and `timezone`. NO device id in payload.",
    body_example={
        "usr": "cashier@havano.pro",
        "pwd": "StrongPassword123!",
        "timezone": "Africa/Harare"
    },
    resp_example={
        "message": {
            "token": "YWJjNEBnbWFpbC5jb206SjFtNDkzMHdyMQ==",
            "token_string": "cashier@havano.pro:J1m4930wr1",
            "api_key": "cashier@havano.pro",
            "api_secret": "J1m4930wr1",
            "user": {
                "username": "cashier@havano.pro",
                "email": "cashier@havano.pro",
                "full_name": "John Doe",
                "company": "Havano Retail Ltd",
                "warehouse": "Machipisa Main Store - HRL",
                "cost_center": "Main - HRL",
                "roles": [
                    "Administrator",
                    "POS Cashier"
                ],
                "user_rights": {
                    "profile_name": "POS Cashier"
                },
                "shops": [
                    {
                        "id": 68,
                        "name": "Downtown Branch",
                        "warehouse": "Downtown Main Store - HRL",
                        "pricelist_names": [
                            "Retail USD",
                            "Retail ZiG"
                        ],
                        "default_pricelist_name": "Retail USD"
                    }
                ]
            }
        }
    }
)

ep(
    "/api/auth/login", "POST", "Auth & Terminals",
    "Direct API Login",
    "Alternative direct auth route taking `login` and `password`.",
    body_example={"login": "cashier@havano.pro", "password": "StrongPassword123!"},
    resp_example={"status": "success", "token": "token_abc123xyz"}
)

ep(
    "/api/user/select-terminal", "POST", "Auth & Terminals",
    "Bind POS Terminal",
    "Assigns a physical terminal slot to the cashier. Supports takeover if previously assigned.",
    body_example={
        "terminal_id": 186,
        "take_over": True,
        "device_hardware_id": "fortune0100",
        "app_version": "2.0.8.28",
        "user": "cashier@havano.pro"
    },
    resp_example={"status": "success", "message": "Terminal assigned", "terminal": {"id": 186, "name": "Till 1"}}
)

ep(
    "/api/user/shops", "GET", "Auth & Terminals",
    "User Assigned Shops & Price Lists",
    "Fetches stores and assigned price lists from `/api/user/shops`.",
    resp_example={"data": [{"shop_id": 68, "shop_name": "Downtown Branch", "default_pricelist_name": "Retail USD", "pricelist_names": ["Retail USD", "Retail ZiG"]}]}
)

ep(
    "/api/user/select-shop", "POST", "Auth & Terminals",
    "Switch Active Shop",
    "Switches session to target shop branch.",
    body_example={"shop_id": 68},
    resp_example={"status": "success", "active_shop": 68}
)

ep(
    "/api/user/current-session", "GET", "Auth & Terminals",
    "Current Session",
    "Returns current tenant session details.",
    resp_example={"user": "cashier@havano.pro", "tenant_id": 104, "terminal_id": 186}
)

# =========================================================================
# 3. PRODUCTS & BUNDLES
# =========================================================================
ep(
    "/api/method/saas_api.www.api.get_my_products", "GET", "Products & Bundles",
    "Sync Products Catalog",
    "Syncs products, barcodes, stock levels, and price lists down to local POS.",
    params=[
        {"name": "page", "in": "query", "schema": {"type": "integer", "default": 1}},
        {"name": "limit", "in": "query", "schema": {"type": "integer", "default": 250}}
    ],
    resp_example={"message": {"products": [{"item_code": "ITEM-00102", "item_name": "Paracetamol 500mg", "stock_uom": "Pack", "prices": [{"price_list": "Retail USD", "rate": 2.50}]}], "total": 1420}}
)

ep(
    "/api/method/havano_pos_integration.api.get_modified_products", "GET", "Products & Bundles",
    "Delta Modified Products",
    "Fetches products updated since last sync datetime.",
    params=[{"name": "last_sync_datetime", "in": "query", "required": True, "schema": {"type": "string"}, "example": "2026-11-01 08:00:00"}],
    resp_example={"message": {"updated_items": [], "deleted_items": []}}
)

ep(
    "/api/method/saas_api.www.api.get_my_product_bundles", "GET", "Products & Bundles",
    "Get Combo Product Bundles",
    "Retrieves combo bundle definitions with child component item lines.",
    resp_example={"message": [{"new_item_code": "COMBO-BURGER", "items": [{"item_code": "BURGER", "qty": 1}]}]}
)

ep(
    "/api/resource/Product%20Bundle", "POST", "Products & Bundles",
    "Create Product Bundle",
    "Creates a combo bundle in Frappe cloud.",
    body_example={"new_item_code": "COMBO-BURGER", "items": [{"item_code": "BURGER", "qty": 1}, {"item_code": "FRIES", "qty": 1}]},
    resp_example={"data": {"name": "COMBO-BURGER"}}
)

# =========================================================================
# 4. CUSTOMERS & LOYALTY
# =========================================================================
ep(
    "/api/method/saas_api.www.api.get_customers", "GET", "Customers & Loyalty",
    "Sync Customers List",
    "Fetches customer accounts, tax TIN numbers, and credit balances.",
    params=[{"name": "page", "in": "query", "schema": {"type": "integer", "default": 1}}],
    resp_example={"message": {"customers": [{"name": "Acme Corp", "customer_name": "Acme Corp", "tax_id": "200012345", "credit_limit": 5000.00}]}}
)

ep(
    "/api/method/saas_api.www.api.create_customer", "POST", "Customers & Loyalty",
    "Create Customer",
    "Registers a new customer record.",
    body_example={"customer_name": "Apex Mining Ltd", "customer_group": "Commercial", "tax_id": "200098765", "phone": "+263771000222"},
    resp_example={"message": {"success": True, "name": "Apex Mining Ltd"}}
)

ep(
    "/api/method/saas_api.www.api.get_customer_balance", "GET", "Customers & Loyalty",
    "Get Customer Live Balance",
    "Returns real-time account balance and available credit limit.",
    params=[{"name": "customer", "in": "query", "required": True, "schema": {"type": "string"}}],
    resp_example={"message": {"outstanding_balance": 350.00, "credit_limit": 1000.00, "available_credit": 650.00}}
)

# =========================================================================
# 5. SALES INVOICES & POS
# =========================================================================
ep(
    "/api/resource/Sales%20Invoice", "POST", "Sales Invoices & POS",
    "Submit Sales Invoice / Return Credit Note",
    "Pushes finalized POS sales invoice or return credit note (`is_return=1`) to Frappe.",
    body_example={
        "customer": "Walk-in Customer",
        "posting_date": "2026-11-03",
        "currency": "USD",
        "is_pos": 1,
        "is_return": 0,
        "items": [{"item_code": "ITEM-00102", "qty": 2, "rate": 2.50, "amount": 5.00}],
        "payments": [{"mode_of_payment": "Cash USD", "amount": 5.00, "account": "Cash - HRL"}]
    },
    resp_example={"data": {"name": "ACC-SINV-2026-00089", "grand_total": 5.00, "status": "Paid"}}
)

ep(
    "/api/method/saas_api.www.api.make_sale", "POST", "Sales Invoices & POS",
    "Make POS Sale (RPC)",
    "High-level RPC transaction to create invoice, process payment, and record sale.",
    body_example={"customer": "Walk-in Customer", "items": [{"item_code": "ITEM-00102", "qty": 1, "rate": 2.50}], "payments": [{"mode_of_payment": "Cash USD", "amount": 2.50}]},
    resp_example={"message": {"status": "success", "sale_id": "SALE-00123"}}
)

# =========================================================================
# 6. ORDERS & QUOTATIONS
# =========================================================================
ep(
    "/api/resource/Sales%20Order", "GET", "Orders & Quotations",
    "List Sales Orders",
    "Fetches draft/open sales orders.",
    resp_example={"data": [{"name": "SO-2026-0001", "customer": "Acme Corp"}]}
)

ep(
    "/api/method/saas_api.www.api.get_quotations", "GET", "Orders & Quotations",
    "Fetch Quotations",
    "Fetches quotations for POS cart loading.",
    resp_example={"message": {"quotations": [{"name": "QTN-001", "grand_total": 45.00}]}}
)

ep(
    "/api/method/saas_api.www.api.create_quotation", "POST", "Orders & Quotations",
    "Create Quotation",
    "Saves a quotation in Frappe cloud.",
    body_example={"party_name": "Acme Corp", "items": [{"item_code": "ITEM-00102", "qty": 5, "rate": 2.50}]},
    resp_example={"message": {"name": "QTN-002"}}
)

# =========================================================================
# 7. PAYMENTS & SHIFTS
# =========================================================================
ep(
    "/api/resource/Payment%20Entry", "POST", "Payments & Shifts",
    "Create Payment Entry",
    "Records payment reconciliation against an invoice or credit note.",
    body_example={"payment_type": "Receive", "party_type": "Customer", "party": "Walk-in Customer", "paid_amount": 5.00, "paid_to": "Cash - HRL"},
    resp_example={"data": {"name": "PE-2026-0001"}}
)

ep(
    "/api/method/saas_api.www.api.get_modes_of_payment", "GET", "Payments & Shifts",
    "Get Modes of Payment",
    "Fetches tender payment modes (Cash, Ecocash, Swipe, Laybye).",
    resp_example={"message": [{"mode_of_payment": "Cash USD", "type": "Cash"}]}
)

ep(
    "/api/method/saas_api.www.api.start_shift", "POST", "Payments & Shifts",
    "Start Shift",
    "Opens cashier shift with opening cash float.",
    body_example={"user": "cashier@havano.pro", "terminal_id": 186, "opening_float": 50.00},
    resp_example={"message": {"shift_id": "SHIFT-001"}}
)

ep(
    "/api/method/saas_api.www.api.close_shift", "POST", "Payments & Shifts",
    "Close Shift",
    "Closes shift and reconciles counted cash against expected sales.",
    body_example={"shift_id": "SHIFT-001", "counted_tenders": [{"currency": "USD", "counted": 550.00}]},
    resp_example={"message": {"status": "Closed", "discrepancy": 0.00}}
)

# =========================================================================
# 8. EXPENSES
# =========================================================================
ep(
    "/api/resource/Expense%20Claim%20Type", "GET", "Expenses",
    "List Expense Categories",
    "Fetches expense claim types (e.g. Fuel, Stationery).",
    resp_example={"data": [{"name": "Fuel"}]}
)

ep(
    "/api/resource/Expense%20Claim", "POST", "Expenses",
    "Submit Expense Claim",
    "Submits petty cash expense claim from POS terminal.",
    body_example={"employee": "EMP-001", "expenses": [{"expense_type": "Fuel", "claim_amount": 25.00}]},
    resp_example={"data": {"name": "EXP-001", "status": "Submitted"}}
)

# =========================================================================
# 9. PHARMACY & MEDICAL
# =========================================================================
ep(
    "/api/method/saas_api.www.api.get_doctors", "GET", "Pharmacy & Medical",
    "Get Doctors Directory",
    "Fetches medical doctors and practice numbers.",
    resp_example={"message": [{"name": "DOC-001", "full_name": "Dr. T. Moyo", "practice_no": "PRAC-88912"}]}
)

ep(
    "/api/method/saas_api.www.api.create_doctor", "POST", "Pharmacy & Medical",
    "Create Doctor",
    "Registers a new doctor profile.",
    body_example={"full_name": "Dr. S. Dube", "practice_no": "PRAC-99001", "phone": "+263771000111"},
    resp_example={"message": {"name": "DOC-002"}}
)

ep(
    "/api/method/saas_api.www.api.get_dosages", "GET", "Pharmacy & Medical",
    "Get Prescription Dosages",
    "Retrieves prescription dosage directions for medication dispensing.",
    resp_example={"message": [{"code": "1 TDS", "description": "Take one tablet three times daily"}]}
)

# =========================================================================
# 10. INVENTORY & STOCK
# =========================================================================
ep(
    "/api/method/erpnext.stock.utils.get_stock_balance", "GET", "Inventory & Stock",
    "Real-Time Stock Balance",
    "Queries live warehouse inventory balance for an item.",
    params=[{"name": "item_code", "in": "query", "required": True, "schema": {"type": "string"}}, {"name": "warehouse", "in": "query", "required": True, "schema": {"type": "string"}}],
    resp_example={"message": 48.0}
)

ep(
    "/api/resource/Stock%20Entry", "POST", "Inventory & Stock",
    "Submit Stock Entry",
    "Submits stock issues, transfers, or damage adjustments.",
    body_example={"stock_entry_type": "Material Issue", "items": [{"item_code": "ITEM-00102", "qty": 2}]},
    resp_example={"data": {"name": "STE-001"}}
)

# =========================================================================
# 11. SUPPLIERS & PURCHASING
# =========================================================================
ep(
    "/api/resource/Supplier", "GET", "Suppliers & Purchasing",
    "List Suppliers",
    "Fetches supplier accounts.",
    resp_example={"data": [{"name": "Varichem Ltd"}]}
)

ep(
    "/api/resource/Purchase%20Invoice", "POST", "Suppliers & Purchasing",
    "Submit Purchase Invoice (GRV)",
    "Records supplier stock delivery and invoice.",
    body_example={"supplier": "Varichem Ltd", "bill_no": "INV-101", "items": [{"item_code": "ITEM-00102", "qty": 100, "rate": 1.80}]},
    resp_example={"data": {"name": "PINV-001"}}
)

# =========================================================================
# 12. MASTER DATA & SETUP
# =========================================================================
ep(
    "/api/method/erpnext.setup.utils.get_exchange_rate", "GET", "Master Data & Setup",
    "Currency Exchange Rate",
    "Fetches current exchange rate between two currencies (e.g. USD to ZiG).",
    params=[{"name": "from_currency", "in": "query", "required": True, "schema": {"type": "string"}}, {"name": "to_currency", "in": "query", "required": True, "schema": {"type": "string"}}],
    resp_example={"message": 26.54}
)

ep(
    "/api/currencies", "GET", "Master Data & Setup",
    "List Currencies",
    "Fetches enabled currencies.",
    resp_example={"data": [{"currency": "USD"}, {"currency": "ZIG"}]}
)

# =========================================================================
# 13. ZIMRA FISCALIZATION
# =========================================================================
ep(
    "/api/method/havanozimracloud.api.token", "POST", "ZIMRA Fiscalization",
    "Get ZIMRA Cloud Token",
    "Authenticates with Havano ZIMRA fiscal gateway.",
    body_example={"device_model_name": "Havano Virtual Device", "device_model_version": "1.0"},
    resp_example={"message": {"token": "jwt_token_here", "expires_in": 86400}}
)

ep(
    "/api/method/havanozimracloud.api.openday", "POST", "ZIMRA Fiscalization",
    "Open Fiscal Day",
    "Opens fiscal day on ZIMRA FDMS gateway.",
    body_example={"fiscal_day_no": 142},
    resp_example={"message": {"status": "Opened"}}
)

ep(
    "/api/method/havanozimracloud.api.sendinvoice", "POST", "ZIMRA Fiscalization",
    "Send Fiscal Invoice to ZIMRA",
    "Submits invoice to ZIMRA for digital signature and QR verification code.",
    body_example={"invoice_num": "INV-001", "total_amount": 5.00, "buyer_tin": "200098765"},
    resp_example={"message": {"fiscal_code": "A9B2-CC41", "verification_url": "https://efdms.zimra.co.zw/verify?code=A9B2CC41"}}
)

# =========================================================================
# 14. RESTAURANT & KDS
# =========================================================================
ep(
    "/api/method/saas_api.www.api.get_restaurant_data", "GET", "Restaurant & KDS",
    "Get Tables & Floor Plan",
    "Fetches dining tables and occupancy status.",
    resp_example={"message": {"areas": [{"name": "Dining Room", "tables": [{"table_number": "T1", "status": "Available"}]}]}}
)

ep(
    "/api/method/saas_api.www.api.save_kitchen_order", "POST", "Restaurant & KDS",
    "Send Kitchen Order Ticket (KOT)",
    "Transmits food order to Kitchen Display System.",
    body_example={"table_number": "T1", "items": [{"item_code": "STEAK", "qty": 1}]},
    resp_example={"message": {"kot_id": "KOT-001"}}
)

# =========================================================================
# 15. SUBSCRIPTIONS & BILLING
# =========================================================================
ep(
    "/api/subscription/status", "GET", "Subscriptions & Billing",
    "Subscription Status",
    "Checks POS license status, active tier, and remaining days.",
    resp_example={"status": "Active", "plan": "Standard Single Till", "days_remaining": 58}
)

ep(
    "/api/subscription/plans", "GET", "Subscriptions & Billing",
    "Subscription Plans",
    "Lists license tier packages.",
    resp_example={"plans": [{"id": 1, "name": "Monthly", "price_usd": 25.0}]}
)

# =========================================================================
# 16. REPORTS & ANALYTICS
# =========================================================================
ep(
    "/api/method/saas_api.www.api.daily_sales", "GET", "Reports & Analytics",
    "Daily Sales Summary",
    "Returns sales volume and tender breakdown for a date.",
    params=[{"name": "date", "in": "query", "schema": {"type": "string"}, "example": "2026-11-03"}],
    resp_example={"message": {"date": "2026-11-03", "total_sales_usd": 1850.50}}
)

ep(
    "/api/method/frappe.desk.query_report.run", "POST", "Reports & Analytics",
    "Execute Frappe Report",
    "Executes Frappe Script or Query Report.",
    body_example={"report_name": "Item-wise Sales Register", "filters": {}},
    resp_example={"message": {"columns": [], "result": []}}
)

# Save openapi.json
spec_path = os.path.join(out_dir, "openapi.json")
with open(spec_path, "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=2)

print(f"Generated clean OpenAPI spec with {len(spec['paths'])} endpoints!")
