import json
import os

out_dir = r"c:\Users\user\Desktop\Havano_POS_2026-main\havano-frappe-swagger-docs"
os.makedirs(out_dir, exist_ok=True)

spec = {
    "openapi": "3.0.3",
    "info": {
        "title": "Havano POS API",
        "version": "1.0.0"
    },
    "servers": [
        {
            "url": "https://backoffice.havano.pro"
        }
    ],
    "tags": [
        {"name": "Frappe Core APIs", "description": "Standard Frappe REST & RPC methods"},
        {"name": "Auth & Terminals", "description": "Authentication and terminal binding"},
        {"name": "Products & Bundles", "description": "Catalog, prices, and bundles"},
        {"name": "Customers & Loyalty", "description": "Customer profiles and balances"},
        {"name": "Sales Invoices & POS", "description": "POS sales and returns"},
        {"name": "Orders & Quotations", "description": "Sales orders and quotations"},
        {"name": "Payments & Shifts", "description": "Payments, MOPs, and shift reconciliation"},
        {"name": "Expenses", "description": "Petty cash claims and categories"},
        {"name": "Pharmacy & Medical", "description": "Doctors and dosages"},
        {"name": "Inventory & Stock", "description": "Stock balance and movements"},
        {"name": "Suppliers & Purchasing", "description": "Vendors and GRVs"},
        {"name": "Master Data & Setup", "description": "Currencies, rates, taxes, and users"},
        {"name": "ZIMRA Fiscalization", "description": "Fiscal day and invoice signing"},
        {"name": "Restaurant & KDS", "description": "Tables, orders, and KOTs"},
        {"name": "Subscriptions & Billing", "description": "License plans and status"},
        {"name": "Reports & Analytics", "description": "Daily sales and reports"}
    ],
    "components": {
        "securitySchemes": {
            "FrappeTokenAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "token <api_key>:<api_secret>"
            },
            "CookieAuth": {
                "type": "apiKey",
                "in": "cookie",
                "name": "sid"
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

def ep(path, method, tag, summary, desc="", params=None, body_example=None, resp_example=None):
    if path not in paths:
        paths[path] = {}
    
    op = {
        "tags": [tag],
        "summary": summary,
        "description": desc or summary,
        "parameters": params or [],
        "responses": {
            "200": {
                "description": "OK",
                "content": {"application/json": {"example": resp_example or {"message": "Success"}}}
            },
            "401": {
                "description": "Unauthorized",
                "content": {"application/json": {"example": {"message": "Invalid credentials"}}}
            },
            "500": {
                "description": "Server Error"
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
# 1. FRAPPE CORE APIS
# =========================================================================
ep(
    "/api/method/login", "POST", "Frappe Core APIs",
    "Frappe Login",
    "Standard login with username and password.",
    body_example={"usr": "administrator", "pwd": "admin_password"},
    resp_example={"message": "Logged In", "home_page": "/app", "full_name": "Administrator"}
)

ep(
    "/api/method/logout", "GET", "Frappe Core APIs",
    "Frappe Logout",
    "Invalidates current session.",
    resp_example={"message": "Logged Out"}
)

ep(
    "/api/method/frappe.auth.get_logged_user", "GET", "Frappe Core APIs",
    "Get Logged User",
    "Returns current user ID.",
    resp_example={"message": "administrator"}
)

ep(
    "/api/method/frappe.ping", "GET", "Frappe Core APIs",
    "Ping Server",
    "Server health check.",
    resp_example={"message": "pong"}
)

ep(
    "/api/method/frappe.handler.version", "GET", "Frappe Core APIs",
    "Frappe Version",
    "Returns Frappe version.",
    resp_example={"message": "15.40.0"}
)

ep(
    "/api/resource/{doctype}", "GET", "Frappe Core APIs",
    "List Documents",
    "Query any Frappe DocType with filters.",
    params=[
        {"name": "doctype", "in": "path", "required": True, "schema": {"type": "string"}, "example": "Item"},
        {"name": "fields", "in": "query", "schema": {"type": "string"}, "example": "[\"name\", \"item_name\"]"},
        {"name": "filters", "in": "query", "schema": {"type": "string"}, "example": "[[\"disabled\",\"=\",0]]"},
        {"name": "limit_page_length", "in": "query", "schema": {"type": "integer", "default": 20}}
    ],
    resp_example={"data": [{"name": "ITEM-001", "item_name": "Sample Item"}]}
)

ep(
    "/api/resource/{doctype}", "POST", "Frappe Core APIs",
    "Create Document",
    "Create a new document for any DocType.",
    params=[{"name": "doctype", "in": "path", "required": True, "schema": {"type": "string"}, "example": "Customer"}],
    body_example={"customer_name": "Acme Holdings", "customer_group": "Commercial"},
    resp_example={"data": {"name": "Acme Holdings", "doctype": "Customer"}}
)

ep(
    "/api/resource/{doctype}/{docname}", "GET", "Frappe Core APIs",
    "Get Document",
    "Retrieve single document by name.",
    params=[
        {"name": "doctype", "in": "path", "required": True, "schema": {"type": "string"}, "example": "Item"},
        {"name": "docname", "in": "path", "required": True, "schema": {"type": "string"}, "example": "ITEM-001"}
    ],
    resp_example={"data": {"name": "ITEM-001", "item_name": "Sample Item"}}
)

ep(
    "/api/resource/{doctype}/{docname}", "PUT", "Frappe Core APIs",
    "Update Document",
    "Update existing document fields.",
    params=[
        {"name": "doctype", "in": "path", "required": True, "schema": {"type": "string"}, "example": "Item"},
        {"name": "docname", "in": "path", "required": True, "schema": {"type": "string"}, "example": "ITEM-001"}
    ],
    body_example={"standard_rate": 2.75},
    resp_example={"data": {"name": "ITEM-001", "standard_rate": 2.75}}
)

ep(
    "/api/resource/{doctype}/{docname}", "DELETE", "Frappe Core APIs",
    "Delete Document",
    "Delete document by name.",
    params=[
        {"name": "doctype", "in": "path", "required": True, "schema": {"type": "string"}, "example": "Item"},
        {"name": "docname", "in": "path", "required": True, "schema": {"type": "string"}, "example": "ITEM-001"}
    ],
    resp_example={"message": "ok"}
)

ep(
    "/api/method/frappe.client.get", "POST", "Frappe Core APIs",
    "RPC: Get Doc",
    "RPC to fetch document dict.",
    body_example={"doctype": "Customer", "name": "Walk-in Customer"},
    resp_example={"message": {"name": "Walk-in Customer", "doctype": "Customer"}}
)

ep(
    "/api/method/frappe.client.get_list", "POST", "Frappe Core APIs",
    "RPC: Get List",
    "RPC to fetch list of documents.",
    body_example={"doctype": "Item", "fields": ["name", "item_name"], "limit_page_length": 10},
    resp_example={"message": [{"name": "ITEM-001", "item_name": "Sample Item"}]}
)

ep(
    "/api/method/frappe.client.set_value", "POST", "Frappe Core APIs",
    "RPC: Set Value",
    "RPC to update single field.",
    body_example={"doctype": "Item", "name": "ITEM-001", "fieldname": "standard_rate", "value": 2.80},
    resp_example={"message": {"name": "ITEM-001", "standard_rate": 2.80}}
)

# =========================================================================
# 2. AUTH & TERMINALS
# =========================================================================
ep(
    "/api/method/saas_api.www.api.login", "POST", "Auth & Terminals",
    "POS Login",
    "Authenticate cashier with username, password, and timezone.",
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
                "full_name": "Cashier One",
                "company": "Havano Retail Ltd",
                "warehouse": "Machipisa Main Store - HRL",
                "cost_center": "Main - HRL",
                "roles": ["POS Cashier"],
                "shops": [
                    {
                        "id": 68,
                        "name": "Downtown Branch",
                        "default_pricelist_name": "Retail USD"
                    }
                ]
            }
        }
    }
)

ep(
    "/api/user/select-terminal", "POST", "Auth & Terminals",
    "Select Terminal",
    "Assign terminal slot to cashier.",
    body_example={
        "terminal_id": 186,
        "take_over": True,
        "user": "cashier@havano.pro"
    },
    resp_example={"status": "success", "terminal": {"id": 186, "name": "Till 1"}}
)

ep(
    "/api/user/shops", "GET", "Auth & Terminals",
    "Get Shops",
    "List assigned shops and price lists.",
    resp_example={"data": [{"shop_id": 68, "shop_name": "Downtown Branch", "default_pricelist_name": "Retail USD"}]}
)

ep(
    "/api/user/select-shop", "POST", "Auth & Terminals",
    "Select Shop",
    "Switch active store branch.",
    body_example={"shop_id": 68},
    resp_example={"status": "success", "active_shop": 68}
)

ep(
    "/api/user/current-session", "GET", "Auth & Terminals",
    "Get Session",
    "Get current tenant session.",
    resp_example={"user": "cashier@havano.pro", "tenant_id": 104, "terminal_id": 186}
)

# =========================================================================
# 3. PRODUCTS & BUNDLES
# =========================================================================
ep(
    "/api/method/saas_api.www.api.get_my_products", "GET", "Products & Bundles",
    "Sync Products",
    "Fetch product catalog and price list rates.",
    params=[
        {"name": "page", "in": "query", "schema": {"type": "integer", "default": 1}},
        {"name": "limit", "in": "query", "schema": {"type": "integer", "default": 250}}
    ],
    resp_example={"message": {"products": [{"item_code": "ITEM-00102", "item_name": "Paracetamol 500mg", "stock_uom": "Pack", "prices": [{"price_list": "Retail USD", "rate": 2.50}]}], "total": 1420}}
)

ep(
    "/api/method/havano_pos_integration.api.get_modified_products", "GET", "Products & Bundles",
    "Delta Sync Products",
    "Fetch products updated since timestamp.",
    params=[{"name": "last_sync_datetime", "in": "query", "required": True, "schema": {"type": "string"}, "example": "2026-11-01 08:00:00"}],
    resp_example={"message": {"updated_items": [], "deleted_items": []}}
)

ep(
    "/api/method/saas_api.www.api.get_my_product_bundles", "GET", "Products & Bundles",
    "Get Bundles",
    "Fetch combo bundles and components.",
    resp_example={"message": [{"new_item_code": "COMBO-BURGER", "items": [{"item_code": "BURGER", "qty": 1}]}]}
)

ep(
    "/api/resource/Product%20Bundle", "POST", "Products & Bundles",
    "Create Bundle",
    "Create combo bundle doc.",
    body_example={"new_item_code": "COMBO-BURGER", "items": [{"item_code": "BURGER", "qty": 1}, {"item_code": "FRIES", "qty": 1}]},
    resp_example={"data": {"name": "COMBO-BURGER"}}
)

# =========================================================================
# 4. CUSTOMERS & LOYALTY
# =========================================================================
ep(
    "/api/method/saas_api.www.api.get_customers", "GET", "Customers & Loyalty",
    "Sync Customers",
    "Fetch customer accounts and limits.",
    params=[{"name": "page", "in": "query", "schema": {"type": "integer", "default": 1}}],
    resp_example={"message": {"customers": [{"name": "Acme Corp", "customer_name": "Acme Corp", "tax_id": "200012345", "credit_limit": 5000.00}]}}
)

ep(
    "/api/method/saas_api.www.api.create_customer", "POST", "Customers & Loyalty",
    "Create Customer",
    "Register a customer.",
    body_example={"customer_name": "Apex Mining Ltd", "customer_group": "Commercial", "tax_id": "200098765", "phone": "+263771000222"},
    resp_example={"message": {"success": True, "name": "Apex Mining Ltd"}}
)

ep(
    "/api/method/saas_api.www.api.get_customer_balance", "GET", "Customers & Loyalty",
    "Get Balance",
    "Check live balance and credit limit.",
    params=[{"name": "customer", "in": "query", "required": True, "schema": {"type": "string"}}],
    resp_example={"message": {"outstanding_balance": 350.00, "credit_limit": 1000.00, "available_credit": 650.00}}
)

# =========================================================================
# 5. SALES INVOICES & POS
# =========================================================================
ep(
    "/api/resource/Sales%20Invoice", "POST", "Sales Invoices & POS",
    "Submit Invoice / Return",
    "Submit POS sales invoice or credit note (is_return=1).",
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
    "Make POS Sale",
    "Submit sale transaction via RPC.",
    body_example={"customer": "Walk-in Customer", "items": [{"item_code": "ITEM-00102", "qty": 1, "rate": 2.50}], "payments": [{"mode_of_payment": "Cash USD", "amount": 2.50}]},
    resp_example={"message": {"status": "success", "sale_id": "SALE-00123"}}
)

# =========================================================================
# 6. ORDERS & QUOTATIONS
# =========================================================================
ep(
    "/api/resource/Sales%20Order", "GET", "Orders & Quotations",
    "List Sales Orders",
    "Fetch open sales orders.",
    resp_example={"data": [{"name": "SO-2026-0001", "customer": "Acme Corp"}]}
)

ep(
    "/api/method/saas_api.www.api.get_quotations", "GET", "Orders & Quotations",
    "Fetch Quotations",
    "Fetch quotations from cloud.",
    resp_example={"message": {"quotations": [{"name": "QTN-001", "grand_total": 45.00}]}}
)

ep(
    "/api/method/saas_api.www.api.create_quotation", "POST", "Orders & Quotations",
    "Create Quotation",
    "Create quotation doc.",
    body_example={"party_name": "Acme Corp", "items": [{"item_code": "ITEM-00102", "qty": 5, "rate": 2.50}]},
    resp_example={"message": {"name": "QTN-002"}}
)

# =========================================================================
# 7. PAYMENTS & SHIFTS
# =========================================================================
ep(
    "/api/resource/Payment%20Entry", "POST", "Payments & Shifts",
    "Create Payment",
    "Record payment entry.",
    body_example={"payment_type": "Receive", "party_type": "Customer", "party": "Walk-in Customer", "paid_amount": 5.00, "paid_to": "Cash - HRL"},
    resp_example={"data": {"name": "PE-2026-0001"}}
)

ep(
    "/api/method/saas_api.www.api.get_modes_of_payment", "GET", "Payments & Shifts",
    "Get Payment Modes",
    "Fetch payment modes list.",
    resp_example={"message": [{"mode_of_payment": "Cash USD", "type": "Cash"}]}
)

ep(
    "/api/method/saas_api.www.api.start_shift", "POST", "Payments & Shifts",
    "Start Shift",
    "Open cashier shift with float.",
    body_example={"user": "cashier@havano.pro", "terminal_id": 186, "opening_float": 50.00},
    resp_example={"message": {"shift_id": "SHIFT-001"}}
)

ep(
    "/api/method/saas_api.www.api.close_shift", "POST", "Payments & Shifts",
    "Close Shift",
    "Close shift and reconcile tenders.",
    body_example={"shift_id": "SHIFT-001", "counted_tenders": [{"currency": "USD", "counted": 550.00}]},
    resp_example={"message": {"status": "Closed", "discrepancy": 0.00}}
)

# =========================================================================
# 8. EXPENSES
# =========================================================================
ep(
    "/api/resource/Expense%20Claim%20Type", "GET", "Expenses",
    "Expense Categories",
    "List expense claim categories.",
    resp_example={"data": [{"name": "Fuel"}]}
)

ep(
    "/api/resource/Expense%20Claim", "POST", "Expenses",
    "Submit Expense",
    "Submit petty cash expense claim.",
    body_example={"employee": "EMP-001", "expenses": [{"expense_type": "Fuel", "claim_amount": 25.00}]},
    resp_example={"data": {"name": "EXP-001", "status": "Submitted"}}
)

# =========================================================================
# 9. PHARMACY & MEDICAL
# =========================================================================
ep(
    "/api/method/saas_api.www.api.get_doctors", "GET", "Pharmacy & Medical",
    "Get Doctors",
    "Fetch medical doctors list.",
    resp_example={"message": [{"name": "DOC-001", "full_name": "Dr. T. Moyo", "practice_no": "PRAC-88912"}]}
)

ep(
    "/api/method/saas_api.www.api.create_doctor", "POST", "Pharmacy & Medical",
    "Create Doctor",
    "Register a new doctor.",
    body_example={"full_name": "Dr. S. Dube", "practice_no": "PRAC-99001", "phone": "+263771000111"},
    resp_example={"message": {"name": "DOC-002"}}
)

ep(
    "/api/method/saas_api.www.api.get_dosages", "GET", "Pharmacy & Medical",
    "Get Dosages",
    "Fetch prescription dosage directions.",
    resp_example={"message": [{"code": "1 TDS", "description": "Take one tablet three times daily"}]}
)

# =========================================================================
# 10. INVENTORY & STOCK
# =========================================================================
ep(
    "/api/method/erpnext.stock.utils.get_stock_balance", "GET", "Inventory & Stock",
    "Stock Balance",
    "Query live item quantity at warehouse.",
    params=[{"name": "item_code", "in": "query", "required": True, "schema": {"type": "string"}}, {"name": "warehouse", "in": "query", "required": True, "schema": {"type": "string"}}],
    resp_example={"message": 48.0}
)

ep(
    "/api/resource/Stock%20Entry", "POST", "Inventory & Stock",
    "Stock Entry",
    "Submit stock movements or adjustments.",
    body_example={"stock_entry_type": "Material Issue", "items": [{"item_code": "ITEM-00102", "qty": 2}]},
    resp_example={"data": {"name": "STE-001"}}
)

# =========================================================================
# 11. SUPPLIERS & PURCHASING
# =========================================================================
ep(
    "/api/resource/Supplier", "GET", "Suppliers & Purchasing",
    "List Suppliers",
    "Fetch supplier list.",
    resp_example={"data": [{"name": "Varichem Ltd"}]}
)

ep(
    "/api/resource/Purchase%20Invoice", "POST", "Suppliers & Purchasing",
    "Submit GRV Invoice",
    "Record supplier invoice and stock receipt.",
    body_example={"supplier": "Varichem Ltd", "bill_no": "INV-101", "items": [{"item_code": "ITEM-00102", "qty": 100, "rate": 1.80}]},
    resp_example={"data": {"name": "PINV-001"}}
)

# =========================================================================
# 12. MASTER DATA & SETUP
# =========================================================================
ep(
    "/api/method/erpnext.setup.utils.get_exchange_rate", "GET", "Master Data & Setup",
    "Exchange Rate",
    "Fetch rate between two currencies.",
    params=[{"name": "from_currency", "in": "query", "required": True, "schema": {"type": "string"}}, {"name": "to_currency", "in": "query", "required": True, "schema": {"type": "string"}}],
    resp_example={"message": 26.54}
)

ep(
    "/api/currencies", "GET", "Master Data & Setup",
    "Currencies",
    "List enabled currencies.",
    resp_example={"data": [{"currency": "USD"}, {"currency": "ZIG"}]}
)

# =========================================================================
# 13. ZIMRA FISCALIZATION
# =========================================================================
ep(
    "/api/method/havanozimracloud.api.token", "POST", "ZIMRA Fiscalization",
    "ZIMRA Token",
    "Authenticate with ZIMRA gateway.",
    body_example={"device_model_name": "Havano Device"},
    resp_example={"message": {"token": "jwt_token_here", "expires_in": 86400}}
)

ep(
    "/api/method/havanozimracloud.api.openday", "POST", "ZIMRA Fiscalization",
    "Open Fiscal Day",
    "Open fiscal day on ZIMRA FDMS.",
    body_example={"fiscal_day_no": 142},
    resp_example={"message": {"status": "Opened"}}
)

ep(
    "/api/method/havanozimracloud.api.sendinvoice", "POST", "ZIMRA Fiscalization",
    "Send Fiscal Invoice",
    "Transmit invoice for ZIMRA fiscal signature.",
    body_example={"invoice_num": "INV-001", "total_amount": 5.00, "buyer_tin": "200098765"},
    resp_example={"message": {"fiscal_code": "A9B2-CC41", "verification_url": "https://efdms.zimra.co.zw/verify?code=A9B2CC41"}}
)

# =========================================================================
# 14. RESTAURANT & KDS
# =========================================================================
ep(
    "/api/method/saas_api.www.api.get_restaurant_data", "GET", "Restaurant & KDS",
    "Restaurant Tables",
    "Fetch tables and layout status.",
    resp_example={"message": {"areas": [{"name": "Dining Room", "tables": [{"table_number": "T1", "status": "Available"}]}]}}
)

ep(
    "/api/method/saas_api.www.api.save_kitchen_order", "POST", "Restaurant & KDS",
    "Send KOT",
    "Send order ticket to kitchen display.",
    body_example={"table_number": "T1", "items": [{"item_code": "STEAK", "qty": 1}]},
    resp_example={"message": {"kot_id": "KOT-001"}}
)

# =========================================================================
# 15. SUBSCRIPTIONS & BILLING
# =========================================================================
ep(
    "/api/subscription/status", "GET", "Subscriptions & Billing",
    "Subscription Status",
    "Check license days remaining.",
    resp_example={"status": "Active", "days_remaining": 58}
)

# =========================================================================
# 16. REPORTS & ANALYTICS
# =========================================================================
ep(
    "/api/method/saas_api.www.api.daily_sales", "GET", "Reports & Analytics",
    "Daily Sales",
    "Daily sales turnover and count.",
    params=[{"name": "date", "in": "query", "schema": {"type": "string"}, "example": "2026-11-03"}],
    resp_example={"message": {"date": "2026-11-03", "total_sales_usd": 1850.50}}
)

# Save openapi.json
spec_path = os.path.join(out_dir, "openapi.json")
with open(spec_path, "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=2)

print(f"Generated clean OpenAPI spec with {len(spec['paths'])} endpoints!")
