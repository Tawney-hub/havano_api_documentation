import json
import os
import re

out_dir = r"c:\Users\user\Desktop\Havano_POS_2026-main\havano-frappe-swagger-docs"
os.makedirs(out_dir, exist_ok=True)

spec = {
    "openapi": "3.0.3",
    "info": {
        "title": "Havano POS - Frappe & SaaS API Specification",
        "description": "Comprehensive, interactive OpenAPI documentation for all Frappe framework RPCs, REST resources, SaaS multi-tenant routes, and ZIMRA fiscalization endpoints used by Havano POS System. Standard production SaaS Base URL is `https://backoffice.havano.pro`.",
        "version": "2026.1.0",
        "contact": {
            "name": "Havano POS Engineering",
            "url": "https://backoffice.havano.pro"
        }
    },
    "servers": [
        {
            "url": "https://backoffice.havano.pro",
            "description": "Havano Cloud SaaS Production Server (Default)"
        }
    ],
    "tags": [
        {"name": "Auth & Multi-Tenant Terminals", "description": "Authentication, terminal takeover/binding, user sessions, active shops and roles"},
        {"name": "Products, Catalog & Bundles", "description": "Product sync, price lists, barcodes, combo bundles, item groups, and UOMs"},
        {"name": "Customers & Loyalty", "description": "Customer accounts, sync, search, creation, balance checks, loyalty points and permissions"},
        {"name": "Sales Invoices & POS Upload", "description": "Sales invoice creation, return credit notes, POS submission, and invoice verification"},
        {"name": "Sales Orders & Quotations", "description": "Sales orders pulling/upload, quotations sync, creation, and cancellation"},
        {"name": "Payments, MOPs & Shifts", "description": "Payment entries, Modes of Payment, multi-currency rates, cash transfers, cashbook, and shift management"},
        {"name": "Expenses Management", "description": "Petty cash claims, expense categories, approvals, and expense synchronization"},
        {"name": "Medical & Pharmacy", "description": "Doctors and prescription dosage directions push and sync"},
        {"name": "Inventory & Stock", "description": "Real-time stock queries, stock entries, warehouse locations, and stock reconciliations"},
        {"name": "Suppliers & Purchasing", "description": "Supplier registration, purchase invoices, and procurement sync"},
        {"name": "Master Data & Setup", "description": "Currencies, exchange rates, chart of accounts, tax categories, countries, and company registration"},
        {"name": "ZIMRA Fiscalization", "description": "Havano ZIMRA cloud gateway: tokens, day open/close (Z-Report), status, and fiscal invoice transmission"},
        {"name": "Restaurant & Hospitality", "description": "Dining areas, table statuses, Kitchen Order Tickets (KOT), and table order closures"},
        {"name": "Subscriptions & Billing", "description": "SaaS subscription plans, status, balance top-ups, and subscription renewal payments"},
        {"name": "Reports & Analytics", "description": "Daily sales, gross margin analysis, cashier performance, and Frappe Query Reports"},
        {"name": "Support & Helpdesk", "description": "Support ticket creation and issue reporting directly from POS"}
    ],
    "components": {
        "securitySchemes": {
            "FrappeTokenAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "Frappe API token format: `token <api_key>:<api_secret>` (e.g. `token abc4@gmail.com:J1m4930wr1`)"
            },
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "SaaS JWT / session bearer token format: `Bearer <token>`"
            },
            "CsrfToken": {
                "type": "apiKey",
                "in": "header",
                "name": "X-Frappe-CSRF-Token",
                "description": "Frappe session CSRF token for state-changing browser calls"
            }
        },
        "schemas": {
            "StandardFrappeResponse": {
                "type": "object",
                "properties": {
                    "message": {"type": "object", "description": "RPC return object or array"}
                }
            },
            "StandardResourceResponse": {
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "DocType resource representation"}
                }
            },
            "ErrorResponse": {
                "type": "object",
                "properties": {
                    "exc": {"type": "string", "description": "Python traceback if debugging enabled"},
                    "exception": {"type": "string", "description": "Error class name"},
                    "_server_messages": {"type": "string", "description": "JSON string of user-facing error messages"}
                }
            }
        }
    },
    "security": [
        {"FrappeTokenAuth": []},
        {"BearerAuth": []}
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
                "content": {
                    "application/json": {
                        "example": resp_example or {"message": {"success": True}}
                    }
                }
            },
            "400": {
                "description": "Bad Request / Validation Error",
                "content": {
                    "application/json": {
                        "example": {"message": "Invalid request parameter or missing field"}
                    }
                }
            },
            "401": {
                "description": "Unauthorized - Missing or invalid credentials",
                "content": {
                    "application/json": {
                        "example": {"message": "Invalid credentials or session expired"}
                    }
                }
            },
            "404": {
                "description": "Resource or endpoint not found"
            },
            "500": {
                "description": "Internal server error",
                "content": {
                    "application/json": {
                        "example": {"exc": "frappe.exceptions.ValidationError"}
                    }
                }
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
# 1. AUTH & MULTI-TENANT TERMINALS
# =========================================================================
ep(
    "/api/method/saas_api.www.api.login", "POST", "Auth & Multi-Tenant Terminals",
    "SaaS User Login",
    "Authenticates cashier / store manager with Frappe SaaS backoffice. Returns credentials, assigned companies, role, shops, and API token.",
    body_example={"usr": "cashier@havano.pro", "pwd": "StrongPassword123!", "device_id": "POS-TERMINAL-01", "timezone": "Africa/Harare"},
    resp_example={"message": {"success": True, "token": "token_abc123xyz", "api_key": "user_api_key", "api_secret": "user_api_secret", "user": {"email": "cashier@havano.pro", "full_name": "John Doe", "role": "POS Cashier", "company": "Havano Retail Ltd"}, "shops": [{"id": 68, "name": "Downtown Branch", "price_lists": ["Standard Retail", "Wholesale USD"], "default_pricelist": "Standard Retail"}]}}
)
ep(
    "/api/auth/login", "POST", "Auth & Multi-Tenant Terminals",
    "Direct API Login",
    "Direct authentication route alternative to Frappe method login.",
    body_example={"login": "cashier@havano.pro", "password": "StrongPassword123!"},
    resp_example={"status": "success", "token": "token_abc123xyz", "user_id": 14}
)
ep(
    "/api/auth/reset_password", "POST", "Auth & Multi-Tenant Terminals",
    "Password Reset Request",
    "Triggers password reset verification email for a user account.",
    body_example={"email": "cashier@havano.pro"},
    resp_example={"status": "success", "message": "Password reset instructions sent"}
)
ep(
    "/api/user/select-terminal", "POST", "Auth & Multi-Tenant Terminals",
    "Assign or Takeover POS Terminal",
    "Registers the physical POS machine hardware ID to a specific terminal slot. If occupied, takeover=True reassigns it.",
    body_example={"terminal_id": 186, "user": "cashier@havano.pro", "take_over": True, "device_hardware_id": "fortune0100"},
    resp_example={"status": "success", "message": "Terminal assigned successfully", "terminal": {"id": 186, "name": "Till 1", "status": "Active", "hardware_id": "fortune0100"}}
)
ep(
    "/api/user/shops", "GET", "Auth & Multi-Tenant Terminals",
    "List User Assigned Shops & Price Lists",
    "Fetches all retail branches/shops assigned to authenticated user, along with associated price lists and defaults.",
    resp_example={"data": [{"shop_id": 68, "shop_name": "Machipisa Branch", "warehouse": "Machipisa Main Store - HRL", "pricelist_names": ["Retail USD", "Retail ZiG", "Promotional"], "default_pricelist_name": "Retail USD"}]}
)
ep(
    "/api/user/select-shop", "POST", "Auth & Multi-Tenant Terminals",
    "Select Active Shop / Branch",
    "Switches the session's active shop or store location.",
    body_example={"shop_id": 68},
    resp_example={"status": "success", "active_shop": 68}
)
ep(
    "/api/user/current-session", "GET", "Auth & Multi-Tenant Terminals",
    "Get Current Active Session",
    "Returns current tenant session state, logged user info, and active company assignment.",
    resp_example={"user": "cashier@havano.pro", "tenant_id": 104, "terminal_id": 186, "shop_id": 68}
)
ep(
    "/api/method/frappe.auth.get_logged_user", "GET", "Auth & Multi-Tenant Terminals",
    "Get Logged In User Email",
    "Standard Frappe method returning email of currently authenticated user session.",
    resp_example={"message": "cashier@havano.pro"}
)
ep(
    "/api/method/frappe.auth.get_version", "GET", "Auth & Multi-Tenant Terminals",
    "Frappe Auth Version Check",
    "Returns version string of backend auth module.",
    resp_example={"message": "1.0.0"}
)
ep(
    "/api/method/frappe.handler.version", "GET", "Auth & Multi-Tenant Terminals",
    "Frappe Framework Version",
    "Returns version info of running Frappe Framework instance.",
    resp_example={"message": "15.x.x"}
)

# =========================================================================
# 2. PRODUCTS, CATALOG & BUNDLES
# =========================================================================
ep(
    "/api/method/saas_api.www.api.get_my_products", "GET", "Products, Catalog & Bundles",
    "Get Tenant Products Catalog (SaaS Mode)",
    "Primary endpoint used by `product_sync_windows_service.py` to sync products, prices, barcodes, categories, and stock quantities down to local SQLite database.",
    params=[
        {"name": "page", "in": "query", "schema": {"type": "integer", "default": 1}, "description": "Page number"},
        {"name": "limit", "in": "query", "schema": {"type": "integer", "default": 250}, "description": "Items per page"},
        {"name": "shop_id", "in": "query", "schema": {"type": "integer"}, "description": "Optional shop filter"}
    ],
    resp_example={"message": {"products": [{"item_code": "ITEM-00102", "item_name": "Paracetamol 500mg 20s", "item_group": "Pharmaceuticals", "stock_uom": "Pack", "standard_rate": 2.50, "barcode": "6001234567890", "is_stock_item": 1, "has_variants": 0, "prices": [{"price_list": "Retail USD", "rate": 2.50, "currency": "USD"}, {"price_list": "Retail ZiG", "rate": 65.00, "currency": "ZIG"}]}], "total": 1420, "has_next": True}}
)
ep(
    "/api/method/saas_api.www.api.get_products", "GET", "Products, Catalog & Bundles",
    "Get Products Catalog (Alternative)",
    "Alternative catalog sync endpoint used when get_my_products is unavailable.",
    params=[{"name": "page", "in": "query", "schema": {"type": "integer", "default": 1}}, {"name": "limit", "in": "query", "schema": {"type": "integer", "default": 250}}],
    resp_example={"message": {"products": [], "total": 0}}
)
ep(
    "/api/method/saas_api.api.get_products", "GET", "Products, Catalog & Bundles",
    "SaaS API Products Fallback",
    "Direct saas_api module products fetch.",
    params=[{"name": "page", "in": "query", "schema": {"type": "integer", "default": 1}}],
    resp_example={"data": []}
)
ep(
    "/api/method/havano_pos_integration.api.get_products", "GET", "Products, Catalog & Bundles",
    "ERPNext Integration Product Sync",
    "Native ERPNext Frappe endpoint for syncing catalog items with price lists and warehouse quantities.",
    params=[{"name": "pos_profile", "in": "query", "schema": {"type": "string"}}, {"name": "company", "in": "query", "schema": {"type": "string"}}],
    resp_example={"message": {"items": []}}
)
ep(
    "/api/method/havano_pos_integration.api.get_modified_products", "GET", "Products, Catalog & Bundles",
    "Incremental Product Sync (Delta)",
    "Fetches only products modified since a given timestamp, reducing sync bandwidth.",
    params=[{"name": "last_sync_datetime", "in": "query", "required": True, "schema": {"type": "string"}, "example": "2026-11-01 08:00:00"}],
    resp_example={"message": {"updated_items": [], "deleted_items": []}}
)
ep(
    "/api/method/havano_pos_integration.api.get_single_product", "GET", "Products, Catalog & Bundles",
    "Get Single Product Details",
    "Fetches detailed pricing, barcodes, and variant attributes for a single product.",
    params=[{"name": "item_code", "in": "query", "required": True, "schema": {"type": "string"}}],
    resp_example={"message": {"item_code": "ITEM-00102", "item_name": "Paracetamol 500mg 20s"}}
)
ep(
    "/api/method/havano_pos_integration.api.get_item_variants", "GET", "Products, Catalog & Bundles",
    "Get Item Variants List",
    "Retrieves child variant products of a template item.",
    params=[{"name": "template_item", "in": "query", "required": True, "schema": {"type": "string"}}],
    resp_example={"message": [{"variant_code": "TSHIRT-RED-L", "color": "Red", "size": "L"}]}
)
ep(
    "/api/method/saas_api.www.api.get_my_product_bundles", "GET", "Products, Catalog & Bundles",
    "Get Product Bundles (Combos)",
    "Fetches bundle parent items and child components (e.g. Meal combos, gift packs) for local inventory explosion.",
    resp_example={"message": [{"new_item_code": "COMBO-BURGER-01", "items": [{"item_code": "BURGER-BEEF", "qty": 1, "uom": "Nos"}, {"item_code": "FRIES-MED", "qty": 1, "uom": "Portion"}, {"item_code": "COKE-CAN-330", "qty": 1, "uom": "Can"}]}]}
)
ep(
    "/api/resource/Product%20Bundle", "POST", "Products, Catalog & Bundles",
    "Create / Push Product Bundle DocType",
    "Creates a new product bundle in Frappe cloud from local POS bundle creation dialog.",
    body_example={"new_item_code": "BUNDLE-SUMMER-01", "items": [{"item_code": "ITEM-A", "qty": 2}, {"item_code": "ITEM-B", "qty": 1}]},
    resp_example={"data": {"name": "BUNDLE-SUMMER-01", "doctype": "Product Bundle"}}
)
ep(
    "/api/resource/Product%20Bundle", "GET", "Products, Catalog & Bundles",
    "List Product Bundles",
    "Retrieves product bundle master records.",
    resp_example={"data": [{"name": "BUNDLE-SUMMER-01", "new_item_code": "BUNDLE-SUMMER-01"}]}
)
ep(
    "/api/resource/Product%20Bundle/{name}", "GET", "Products, Catalog & Bundles",
    "Get Single Product Bundle Details",
    "Retrieves full product bundle doc with component line items.",
    params=[{"name": "name", "in": "path", "required": True, "schema": {"type": "string"}}],
    resp_example={"data": {"name": "BUNDLE-SUMMER-01", "items": []}}
)
ep(
    "/api/method/saas_api.www.api.create_item", "POST", "Products, Catalog & Bundles",
    "Create Item (RPC)",
    "Creates a new item via SaaS RPC endpoint.",
    body_example={"item_code": "PROD-99", "item_name": "Test Item", "standard_rate": 10.0},
    resp_example={"message": {"status": "success", "item_code": "PROD-99"}}
)
ep(
    "/api/method/saas_api.www.api.edit_item", "POST", "Products, Catalog & Bundles",
    "Edit Item (RPC)",
    "Updates item attributes, standard rate, or barcode.",
    body_example={"item_code": "PROD-99", "standard_rate": 12.0},
    resp_example={"message": {"status": "success", "item_code": "PROD-99"}}
)
ep(
    "/api/resource/Item", "GET", "Products, Catalog & Bundles",
    "Frappe REST Item Resource Query",
    "Queries standard Item DocType with fields and filters.",
    params=[
        {"name": "fields", "in": "query", "schema": {"type": "string"}, "example": "[\"name\",\"item_code\",\"item_name\",\"stock_uom\"]"},
        {"name": "filters", "in": "query", "schema": {"type": "string"}, "example": "[[\"disabled\",\"=\",0]]"},
        {"name": "limit_page_length", "in": "query", "schema": {"type": "integer", "default": 20}}
    ],
    resp_example={"data": [{"name": "ITEM-001", "item_code": "ITEM-001", "item_name": "Sample Product"}]}
)
ep(
    "/api/resource/Item", "POST", "Products, Catalog & Bundles",
    "Create Item DocType",
    "Creates a new inventory or service item in Frappe.",
    body_example={"item_code": "NEW-ITEM-99", "item_name": "Digital Gift Card", "item_group": "Services", "stock_uom": "Nos", "is_stock_item": 0},
    resp_example={"data": {"name": "NEW-ITEM-99", "doctype": "Item"}}
)
ep(
    "/api/resource/Item/{item_code}", "PUT", "Products, Catalog & Bundles",
    "Update Item DocType",
    "Updates existing item fields.",
    params=[{"name": "item_code", "in": "path", "required": True, "schema": {"type": "string"}}],
    body_example={"standard_rate": 15.00},
    resp_example={"data": {"name": "ITEM-001", "standard_rate": 15.00}}
)
ep(
    "/api/resource/Item%20Group", "GET", "Products, Catalog & Bundles",
    "Get Item Categories / Groups",
    "Retrieves the tree of item categories.",
    resp_example={"data": [{"name": "Beverages"}, {"name": "Groceries"}, {"name": "Pharmaceuticals"}]}
)
ep(
    "/api/method/saas_api.www.api.create_item_group", "POST", "Products, Catalog & Bundles",
    "Create Item Group",
    "Creates a new product category group.",
    body_example={"item_group_name": "Snacks & Confectionery", "parent_item_group": "All Item Groups"},
    resp_example={"message": {"item_group_name": "Snacks & Confectionery"}}
)
ep(
    "/api/resource/Item%20Price", "GET", "Products, Catalog & Bundles",
    "Query Price List Rates",
    "Fetches price list rates for items.",
    params=[{"name": "filters", "in": "query", "schema": {"type": "string"}, "example": "[[\"price_list\",\"=\",\"Retail USD\"]]"}],
    resp_example={"data": [{"item_code": "ITEM-00102", "price_list_rate": 2.50, "currency": "USD"}]}
)
ep(
    "/api/resource/Item%20Price", "POST", "Products, Catalog & Bundles",
    "Create Item Price Entry",
    "Adds a price rate for an item in a specific price list.",
    body_example={"item_code": "ITEM-00102", "price_list": "Retail USD", "price_list_rate": 2.50, "currency": "USD"},
    resp_example={"data": {"name": "IP-0001"}}
)
ep(
    "/api/uoms", "GET", "Products, Catalog & Bundles",
    "List Units of Measure (UOMs)",
    "Fetches active Units of Measure (Nos, Kg, Litre, Pack, Box).",
    resp_example={"data": [{"name": "Nos"}, {"name": "Kg"}, {"name": "Litre"}, {"name": "Pack"}]}
)

# =========================================================================
# 3. CUSTOMERS & LOYALTY
# =========================================================================
ep(
    "/api/method/saas_api.www.api.get_customers", "GET", "Customers & Loyalty",
    "Sync Customers List (SaaS Mode)",
    "Syncs all customer profiles from Frappe cloud down to local POS. Supports pagination.",
    params=[{"name": "page", "in": "query", "schema": {"type": "integer", "default": 1}}, {"name": "limit", "in": "query", "schema": {"type": "integer", "default": 250}}],
    resp_example={"message": {"customers": [{"name": "CUST-00042", "customer_name": "Acme Corporation", "customer_group": "Commercial", "tax_id": "200012345", "tax_category": "Standard", "mobile_no": "+263771234567", "email_id": "accounts@acme.co.zw", "credit_limit": 5000.00, "default_price_list": "Wholesale USD"}], "total": 380, "has_next": True}}
)
ep(
    "/api/method/havano_pos_integration.api.get_customer", "GET", "Customers & Loyalty",
    "Get Customer Details by Name / Code",
    "Fetches detailed profile, outstanding balances, and credit limit for a customer.",
    params=[{"name": "customer", "in": "query", "required": True, "schema": {"type": "string"}}],
    resp_example={"message": {"customer_name": "Acme Corporation", "outstanding_amount": 120.00}}
)
ep(
    "/api/method/saas_api.www.api.create_customer", "POST", "Customers & Loyalty",
    "Create New Customer",
    "Creates a new customer record from POS customer registration modal.",
    body_example={"customer_name": "Delta Logistics Ltd", "customer_group": "Commercial", "customer_type": "Company", "tax_id": "200098765", "tax_category": "Standard", "phone": "+263772000111", "email_id": "admin@deltalogistics.com", "address_line1": "12 Samora Machel Ave", "city": "Harare", "credit_limit": 10000.00},
    resp_example={"message": {"success": True, "name": "Delta Logistics Ltd", "customer_id": "CUST-00109"}}
)
ep(
    "/api/method/saas_api.www.api.get_customer_balance", "GET", "Customers & Loyalty",
    "Get Live Customer Account Balance",
    "Queries real-time outstanding ledger balance and available credit for account sales.",
    params=[{"name": "customer", "in": "query", "required": True, "schema": {"type": "string"}}],
    resp_example={"message": {"outstanding_balance": 340.50, "credit_limit": 1000.00, "available_credit": 659.50}}
)
ep(
    "/api/method/havano_pos_integration.api.redeem_loyalty_points", "POST", "Customers & Loyalty",
    "Redeem Customer Loyalty Points",
    "Redeems customer loyalty points against current cart value.",
    body_example={"customer": "CUST-00042", "points_to_redeem": 100, "pos_invoice": "INV-001"},
    resp_example={"message": {"discount_amount": 10.00, "remaining_points": 250}}
)
ep(
    "/api/resource/Customer", "GET", "Customers & Loyalty",
    "Query Customer DocTypes",
    "Queries Customer DocType records with filters.",
    params=[{"name": "fields", "in": "query", "schema": {"type": "string"}}, {"name": "filters", "in": "query", "schema": {"type": "string"}}],
    resp_example={"data": [{"name": "CUST-00042", "customer_name": "Acme Corporation"}]}
)
ep(
    "/api/resource/Customer/{name}", "GET", "Customers & Loyalty",
    "Verify Customer Exists in Frappe",
    "Checks if a specific customer name exists in Frappe cloud before attaching transactions.",
    params=[{"name": "name", "in": "path", "required": True, "schema": {"type": "string"}}],
    resp_example={"data": {"name": "Delta Logistics Ltd", "customer_name": "Delta Logistics Ltd"}}
)
ep(
    "/api/resource/User%20Permission", "POST", "Customers & Loyalty",
    "Assign User Permission for Customer",
    "Restricts or assigns permissions for a newly created customer to tenant company/user.",
    body_example={"user": "cashier@havano.pro", "allow": "Customer", "for_value": "Delta Logistics Ltd"},
    resp_example={"data": {"name": "UP-0001"}}
)

# =========================================================================
# 4. SALES INVOICES & POS UPLOAD
# =========================================================================
ep(
    "/api/resource/Sales%20Invoice", "POST", "Sales Invoices & POS Upload",
    "Submit POS Sales Invoice / Return Credit Note",
    "Primary endpoint used by `pos_upload_service.py` and `credit_note_sync_service.py` to push finalized sales or credit note returns to Frappe. If is_return=1, return_against points to original invoice.",
    body_example={"customer": "Walk-in Customer", "posting_date": "2026-11-03", "posting_time": "14:15:00", "currency": "USD", "conversion_rate": 1.0, "is_pos": 1, "is_return": 0, "update_stock": 1, "items": [{"item_code": "ITEM-00102", "qty": 2, "rate": 2.50, "amount": 5.00, "income_account": "Sales - HRL", "expense_account": "Cost of Goods Sold - HRL", "cost_center": "Main - HRL"}], "payments": [{"mode_of_payment": "Cash USD", "amount": 5.00, "account": "Cash - HRL"}]},
    resp_example={"data": {"name": "ACC-SINV-2026-00089", "grand_total": 5.00, "status": "Paid", "docstatus": 1}}
)
ep(
    "/api/resource/Sales%20Invoice", "GET", "Sales Invoices & POS Upload",
    "List Sales Invoices",
    "Queries remote sales invoices for cross-checking credit note returns and settlement status.",
    params=[{"name": "filters", "in": "query", "schema": {"type": "string"}}, {"name": "fields", "in": "query", "schema": {"type": "string"}}, {"name": "limit", "in": "query", "schema": {"type": "integer"}}],
    resp_example={"data": [{"name": "ACC-SINV-2026-00089", "grand_total": 5.00}]}
)
ep(
    "/api/resource/Sales%20Invoice/{name}", "GET", "Sales Invoices & POS Upload",
    "Get Sales Invoice Details",
    "Retrieves full invoice details including child item rows, taxes, and applied payments.",
    params=[{"name": "name", "in": "path", "required": True, "schema": {"type": "string"}}],
    resp_example={"data": {"name": "ACC-SINV-2026-00089", "items": [], "payments": []}}
)
ep(
    "/api/resource/POS%20Invoice", "POST", "Sales Invoices & POS Upload",
    "Submit POS Invoice DocType",
    "Creates a POS Invoice doc in ERPNext POS module.",
    body_example={"customer": "Walk-in Customer", "items": [{"item_code": "ITEM-00102", "qty": 1, "rate": 2.50}], "payments": [{"mode_of_payment": "Cash USD", "amount": 2.50}]},
    resp_example={"data": {"name": "POS-INV-2026-001"}}
)
ep(
    "/api/method/saas_api.www.api.create_invoice", "POST", "Sales Invoices & POS Upload",
    "Create SaaS Sales Invoice (RPC)",
    "RPC endpoint for submitting invoices in SaaS multi-tenant mode.",
    body_example={"customer": "Walk-in Customer", "items": []},
    resp_example={"message": {"invoice_id": "ACC-SINV-2026-00089", "status": "Success"}}
)
ep(
    "/api/method/saas_api.www.api.make_sale", "POST", "Sales Invoices & POS Upload",
    "Make POS Sale (High-level RPC)",
    "High-level RPC endpoint that validates stock, calculates multicurrency exchange rates, records invoice, payments, and fiscal signatures in a single transaction.",
    body_example={"customer": "Walk-in Customer", "items": [{"item_code": "ITEM-00102", "qty": 1, "rate": 2.50}], "payments": [{"mode_of_payment": "Cash USD", "amount": 2.50}]},
    resp_example={"message": {"status": "success", "sale_id": "SALE-00123"}}
)
ep(
    "/api/method/erp_api.api.create_sales_invoice", "POST", "Sales Invoices & POS Upload",
    "ERP API Create Invoice",
    "Alternative ERP invoice creation endpoint.",
    body_example={"customer": "Walk-in Customer", "items": []},
    resp_example={"message": {"name": "ACC-SINV-2026-00089"}}
)
ep(
    "/api/method/erp_api.api.get_sales_invoice", "GET", "Sales Invoices & POS Upload",
    "Fetch ERP Sales Invoice",
    "Paginates historical invoices from cloud ERP for offline lookups and return verification.",
    params=[{"name": "page", "in": "query", "schema": {"type": "integer", "default": 1}}, {"name": "limit", "in": "query", "schema": {"type": "integer", "default": 50}}],
    resp_example={"message": {"invoices": []}}
)

# =========================================================================
# 5. SALES ORDERS & QUOTATIONS
# =========================================================================
ep(
    "/api/resource/Sales%20Order", "GET", "Sales Orders & Quotations",
    "List Sales Orders",
    "Fetches active or draft sales orders from Frappe backoffice.",
    params=[{"name": "fields", "in": "query", "schema": {"type": "string"}, "example": "[\"name\",\"customer\",\"delivery_date\"]"}, {"name": "limit_page_length", "in": "query", "schema": {"type": "integer", "default": 0}}],
    resp_example={"data": [{"name": "SO-2026-0012", "customer": "Acme Corp"}]}
)
ep(
    "/api/resource/Sales%20Order/{name}", "GET", "Sales Orders & Quotations",
    "Get Sales Order Line Items",
    "Retrieves full sales order doc with all child item lines for fulfillment or conversion to invoice.",
    params=[{"name": "name", "in": "path", "required": True, "schema": {"type": "string"}}],
    resp_example={"data": {"name": "SO-2026-0012", "items": [{"item_code": "ITEM-00102", "qty": 10}]}}
)
ep(
    "/api/resource/Sales%20Order", "POST", "Sales Orders & Quotations",
    "Upload Sales Order",
    "Creates a new Sales Order in Frappe from offline POS sales order creation.",
    body_example={"customer": "Acme Corp", "delivery_date": "2026-11-10", "items": [{"item_code": "ITEM-00102", "qty": 10, "rate": 2.50}]},
    resp_example={"data": {"name": "SO-2026-0012", "doctype": "Sales Order"}}
)
ep(
    "/api/resource/Quotation", "GET", "Sales Orders & Quotations",
    "List Quotations (DocType)",
    "Queries Quotation DocType records.",
    resp_example={"data": [{"name": "QTN-2026-00045", "party_name": "Acme Corp"}]}
)
ep(
    "/api/resource/Quotation", "POST", "Sales Orders & Quotations",
    "Create Quotation (DocType)",
    "Creates a new quotation in Frappe via REST resource.",
    body_example={"party_name": "Acme Corp", "items": [{"item_code": "ITEM-00102", "qty": 5, "rate": 2.50}]},
    resp_example={"data": {"name": "QTN-2026-00047"}}
)
ep(
    "/api/method/saas_api.www.api.get_quotations", "GET", "Sales Orders & Quotations",
    "Fetch Quotations from Cloud",
    "Retrieves quotations submitted by sales reps or external portal for loading into POS cart.",
    params=[{"name": "page", "in": "query", "schema": {"type": "integer", "default": 1}}, {"name": "limit", "in": "query", "schema": {"type": "integer", "default": 100}}],
    resp_example={"message": {"quotations": [{"name": "QTN-2026-00045", "customer_name": "Acme Corp", "transaction_date": "2026-11-03", "grand_total": 450.00, "currency": "USD", "items": [{"item_code": "ITEM-00102", "qty": 180, "rate": 2.50}]}], "total": 12, "has_next": False}}
)
ep(
    "/api/method/saas_api.www.api.create_quotation", "POST", "Sales Orders & Quotations",
    "Create / Push Quotation to Cloud",
    "Saves a sales quotation generated locally to Frappe cloud.",
    body_example={"party_name": "Acme Corp", "transaction_date": "2026-11-03", "valid_till": "2026-11-17", "currency": "USD", "items": [{"item_code": "ITEM-00102", "qty": 10, "rate": 2.50}]},
    resp_example={"message": {"name": "QTN-2026-00046", "status": "Draft"}}
)
ep(
    "/api/method/saas_api.www.api.cancel_quotation", "POST", "Sales Orders & Quotations",
    "Cancel Quotation",
    "Cancels an existing quotation in Frappe cloud.",
    body_example={"name": "QTN-2026-00045"},
    resp_example={"message": {"success": True, "status": "Cancelled"}}
)

# =========================================================================
# 6. PAYMENTS, MOPS & SHIFTS
# =========================================================================
ep(
    "/api/resource/Payment%20Entry", "POST", "Payments, MOPs & Shifts",
    "Create Frappe Payment Entry",
    "Used by `payment_upload_service.py`, `payment_entry_sync_service.py`, `cn_payment_entry_service.py`, and `laybye_payment_entry_service.py` to record received or refunded customer payments and reconcile against invoices.",
    body_example={"payment_type": "Receive", "party_type": "Customer", "party": "Walk-in Customer", "paid_amount": 5.00, "received_amount": 5.00, "paid_from": "Debtors - HRL", "paid_to": "Cash - HRL", "reference_no": "POS-PAY-00441", "reference_date": "2026-11-03", "references": [{"reference_doctype": "Sales Invoice", "reference_name": "ACC-SINV-2026-00089", "allocated_amount": 5.00}]},
    resp_example={"data": {"name": "PE-2026-00055", "docstatus": 1}}
)
ep(
    "/api/resource/Payment%20Entry", "GET", "Payments, MOPs & Shifts",
    "Query Payment Entries",
    "Lists payment entries for audit and local reconciliation.",
    resp_example={"data": [{"name": "PE-2026-00055", "paid_amount": 5.00}]}
)
ep(
    "/api/method/erpnext.accounts.party.get_party_account", "GET", "Payments, MOPs & Shifts",
    "Get Customer Default Receivable Account",
    "Queries Frappe chart of accounts for customer's mapped Accounts Receivable GL account.",
    params=[{"name": "party_type", "in": "query", "required": True, "schema": {"type": "string", "default": "Customer"}}, {"name": "party", "in": "query", "required": True, "schema": {"type": "string"}}],
    resp_example={"message": "Debtors USD - HRL"}
)
ep(
    "/api/method/saas_api.www.api.get_modes_of_payment", "GET", "Payments, MOPs & Shifts",
    "Get SaaS Modes of Payment",
    "Retrieves modes of payment configured for company (Cash, Ecocash, Swipe, Laybye, etc.).",
    params=[{"name": "company", "in": "query", "schema": {"type": "string"}}],
    resp_example={"message": [{"mode_of_payment": "Cash USD", "type": "Cash", "currency": "USD"}, {"mode_of_payment": "Cash ZiG", "type": "Cash", "currency": "ZIG"}, {"mode_of_payment": "Swipe ZiG", "type": "Bank", "currency": "ZIG"}]}
)
ep(
    "/api/method/saas_api.www.api.get_account", "GET", "Payments, MOPs & Shifts",
    "Get GL Accounts & SaaS MOP Rates",
    "Fetches chart of accounts and multi-currency conversion rates for payment modes.",
    resp_example={"message": {"accounts": [{"name": "Cash - HRL", "account_type": "Cash"}], "rates": {"USD": 1.0, "ZIG": 26.5}}}
)
ep(
    "/api/resource/Mode%20of%20Payment", "GET", "Payments, MOPs & Shifts",
    "List Frappe Modes of Payment",
    "Standard Frappe resource listing payment mode configurations.",
    params=[{"name": "fields", "in": "query", "schema": {"type": "string"}, "example": "[\"name\",\"type\"]"}],
    resp_example={"data": [{"name": "Cash", "type": "Cash"}, {"name": "Bank Transfer", "type": "Bank"}]}
)
ep(
    "/api/resource/Mode%20of%20Payment%20Account", "GET", "Payments, MOPs & Shifts",
    "Get Payment Mode GL Account Links",
    "Fetches company-specific ledger account links for each payment mode.",
    resp_example={"data": [{"parent": "Cash", "company": "Havano Retail Ltd", "default_account": "Cash - HRL"}]}
)
ep(
    "/api/method/saas_api.www.api.create_cash_transfer", "POST", "Payments, MOPs & Shifts",
    "Record Cash Drop / Float Transfer",
    "Records petty cash movements, cashier float top-ups, or cash drops to safe.",
    body_example={"transfer_type": "Safe Drop", "amount": 300.00, "currency": "USD", "source_account": "Cash Drawer - HRL", "target_account": "Main Safe - HRL"},
    resp_example={"message": {"transfer_id": "TRANS-0012", "status": "Completed"}}
)
ep(
    "/api/method/saas_api.www.api.get_cash_transfers", "GET", "Payments, MOPs & Shifts",
    "Get Cash Transfers List",
    "Retrieves list of cash drop and float transfer transactions.",
    resp_example={"message": []}
)
ep(
    "/api/method/saas_api.www.api.get_cashbook", "GET", "Payments, MOPs & Shifts",
    "Get Cashbook Ledger",
    "Retrieves cash drawer movement log for active shift.",
    resp_example={"message": {"entries": [], "balance": 450.00}}
)
ep(
    "/api/method/saas_api.www.api.start_shift", "POST", "Payments, MOPs & Shifts",
    "Start Cashier Shift",
    "Opens a new cashier work shift with starting cash float breakdown.",
    body_example={"user": "cashier@havano.pro", "terminal_id": 186, "opening_float": 50.00, "currency": "USD"},
    resp_example={"message": {"shift_id": "SHIFT-00341", "status": "Open"}}
)
ep(
    "/api/method/saas_api.www.api.close_shift", "POST", "Payments, MOPs & Shifts",
    "Close Shift & Reconcile Cash",
    "Closes active cashier shift, comparing counted tender amounts against system sales for discrepancy reporting.",
    body_example={"shift_id": "SHIFT-00341", "closing_notes": "All balanced", "counted_tenders": [{"currency": "USD", "counted": 550.00}, {"currency": "ZIG", "counted": 2400.00}]},
    resp_example={"message": {"status": "Closed", "shortage_surplus": 0.00}}
)
ep(
    "/api/method/saas_api.www.api.get_current_shift", "GET", "Payments, MOPs & Shifts",
    "Get Current Shift Status",
    "Checks if a shift is currently open for cashier on this terminal.",
    resp_example={"message": {"active": True, "shift_id": "SHIFT-00341"}}
)
ep(
    "/api/method/havano_pos_integration.api.create_pos_opening_entry", "POST", "Payments, MOPs & Shifts",
    "ERPNext POS Opening Entry",
    "Native ERPNext POS Opening Entry creation.",
    body_example={"pos_profile": "Retail Till 1", "company": "Havano Retail Ltd", "balance_details": [{"mode_of_payment": "Cash USD", "opening_amount": 50.00}]},
    resp_example={"message": {"name": "POS-OPEN-2026-0001"}}
)
ep(
    "/api/resource/POS%20Closing%20Entry", "POST", "Payments, MOPs & Shifts",
    "ERPNext POS Closing Entry",
    "Native ERPNext POS Closing Entry submission.",
    body_example={"pos_opening_entry": "POS-OPEN-2026-0001", "payment_reconciliation": []},
    resp_example={"data": {"name": "POS-CLOSE-2026-0001"}}
)

# =========================================================================
# 7. EXPENSES MANAGEMENT
# =========================================================================
ep(
    "/api/resource/Expense%20Claim%20Type", "GET", "Expenses Management",
    "List Expense Categories",
    "Fetches expense claim categories (e.g. Fuel, Stationery, Refreshments) from Frappe.",
    resp_example={"data": [{"name": "Fuel", "expense_type": "Fuel"}, {"name": "Office Stationery", "expense_type": "Office Stationery"}]}
)
ep(
    "/api/resource/Expense%20Claim%20Type", "POST", "Expenses Management",
    "Create Expense Category",
    "Creates a new expense type on the fly.",
    body_example={"expense_type": "Vehicle Maintenance"},
    resp_example={"data": {"name": "Vehicle Maintenance"}}
)
ep(
    "/api/resource/Expense%20Claim", "POST", "Expenses Management",
    "Submit POS Expense Claim",
    "Submits petty cash or operational expense claims recorded at POS terminal to Frappe cloud. Supports single or batch submissions.",
    body_example={"employee": "EMP-0001", "posting_date": "2026-11-03", "payable_account": "Petty Cash - HRL", "expenses": [{"expense_type": "Fuel", "claim_amount": 25.00, "sanctioned_amount": 25.00, "description": "Generator petrol top-up"}]},
    resp_example={"data": {"name": "EXP-2026-0011", "status": "Submitted", "total_claimed_amount": 25.00}}
)
ep(
    "/api/resource/Expense%20Claim", "GET", "Expenses Management",
    "List Expense Claims",
    "Fetches list of submitted expense claims.",
    resp_example={"data": [{"name": "EXP-2026-0011", "total_claimed_amount": 25.00, "status": "Draft"}]}
)
ep(
    "/api/method/saas_api.www.api.approve_expense", "POST", "Expenses Management",
    "Approve Expense Claim",
    "Manager action approving a submitted petty cash expense.",
    body_example={"expense_id": "EXP-2026-0011"},
    resp_example={"message": {"status": "Approved"}}
)
ep(
    "/api/method/saas_api.www.api.reject_expense", "POST", "Expenses Management",
    "Reject Expense Claim",
    "Manager action rejecting an expense claim.",
    body_example={"expense_id": "EXP-2026-0011", "reason": "Missing receipt"},
    resp_example={"message": {"status": "Rejected"}}
)

# =========================================================================
# 8. MEDICAL & PHARMACY
# =========================================================================
ep(
    "/api/method/saas_api.www.api.get_doctors", "GET", "Medical & Pharmacy",
    "Get Doctors Directory",
    "Fetches medical practitioners and prescription issuers registered in system.",
    resp_example={"message": [{"name": "DOC-001", "full_name": "Dr. T. Moyo", "practice_no": "PRAC-88912", "phone": "+263773111222", "qualification": "MBChB"}]}
)
ep(
    "/api/method/saas_api.www.api.create_doctor", "POST", "Medical & Pharmacy",
    "Create Doctor Profile",
    "Registers a new doctor when dispensing prescription medication at POS.",
    body_example={"full_name": "Dr. Sarah Dube", "practice_no": "PRAC-99001", "phone": "+263774555666", "qualification": "MD", "school": "UZ College of Health Sciences"},
    resp_example={"message": {"name": "DOC-002", "full_name": "Dr. Sarah Dube"}}
)
ep(
    "/api/method/saas_api.www.api.update_doctor", "POST", "Medical & Pharmacy",
    "Update Doctor Profile",
    "Updates contact or qualification info for an existing doctor.",
    body_example={"name": "DOC-002", "phone": "+263774999888"},
    resp_example={"message": {"status": "Updated"}}
)
ep(
    "/api/method/saas_api.www.api.get_dosages", "GET", "Medical & Pharmacy",
    "Get Prescription Dosage Instructions",
    "Retrieves standard dosage instruction abbreviations (e.g., '1 tds', '2 bd pc') for label printing.",
    resp_example={"message": [{"code": "1 TDS", "description": "Take one tablet three times daily after meals"}, {"code": "2 BD", "description": "Take two tablets twice daily"}]}
)
ep(
    "/api/method/saas_api.www.api.create_dosage", "POST", "Medical & Pharmacy",
    "Create Dosage Instruction",
    "Adds a custom prescription dosage instruction code.",
    body_example={"code": "1 PRN", "description": "Take one tablet as needed for pain"},
    resp_example={"message": {"name": "DOS-003", "code": "1 PRN"}}
)
ep(
    "/api/method/saas_api.www.api.update_dosage", "POST", "Medical & Pharmacy",
    "Update Dosage Instruction",
    "Modifies an existing dosage instruction text.",
    body_example={"name": "DOS-003", "description": "Take one tablet as needed for severe pain"},
    resp_example={"message": {"status": "Updated"}}
)

# =========================================================================
# 9. INVENTORY & STOCK
# =========================================================================
ep(
    "/api/method/erpnext.stock.utils.get_stock_balance", "GET", "Inventory & Stock",
    "Get Real-Time Item Stock Balance",
    "Queries live stock quantity for an item at a specific warehouse location in Frappe.",
    params=[{"name": "item_code", "in": "query", "required": True, "schema": {"type": "string"}}, {"name": "warehouse", "in": "query", "required": True, "schema": {"type": "string"}}, {"name": "posting_date", "in": "query", "schema": {"type": "string"}}],
    resp_example={"message": 48.0}
)
ep(
    "/api/method/havano_pos_integration.api.get_stock_update", "GET", "Inventory & Stock",
    "Stream Stock Level Updates",
    "Fetches recent warehouse stock balance changes for cached items.",
    params=[{"name": "warehouse", "in": "query", "required": True, "schema": {"type": "string"}}],
    resp_example={"message": [{"item_code": "ITEM-00102", "actual_qty": 48.0}]}
)
ep(
    "/api/resource/Stock%20Entry", "POST", "Inventory & Stock",
    "Submit Stock Entry (Movement / Damage / Transfer)",
    "Submits stock movements such as Material Transfer between branches, Material Receipt, or Material Issue (breakages / expired items).",
    body_example={"stock_entry_type": "Material Issue", "company": "Havano Retail Ltd", "items": [{"item_code": "ITEM-00102", "s_warehouse": "Machipisa Main Store - HRL", "qty": 2, "basic_rate": 1.50}]},
    resp_example={"data": {"name": "STE-2026-00021", "docstatus": 1}}
)
ep(
    "/api/resource/Stock%20Entry/{name}", "GET", "Inventory & Stock",
    "Get Stock Entry Details",
    "Retrieves full details of a stock entry document.",
    params=[{"name": "name", "in": "path", "required": True, "schema": {"type": "string"}}],
    resp_example={"data": {"name": "STE-2026-00021", "stock_entry_type": "Material Issue"}}
)
ep(
    "/api/resource/Stock%20Reconciliation", "POST", "Inventory & Stock",
    "Stock Reconciliation (Cycle Count)",
    "Uploads physical stock count audits to adjust book inventory to actual count.",
    body_example={"company": "Havano Retail Ltd", "purpose": "Stock Reconciliation", "items": [{"item_code": "ITEM-00102", "warehouse": "Machipisa Main Store - HRL", "qty": 50, "valuation_rate": 1.50}]},
    resp_example={"data": {"name": "REC-2026-00005", "docstatus": 1}}
)
ep(
    "/api/resource/Warehouse", "GET", "Inventory & Stock",
    "List Warehouses",
    "Fetches all storage warehouses and retail store locations.",
    resp_example={"data": [{"name": "Machipisa Main Store - HRL"}, {"name": "Central Bulk Store - HRL"}]}
)
ep(
    "/api/method/havano_pos_integration.api.get_warehouses", "GET", "Inventory & Stock",
    "Get Warehouse Locations (POS)",
    "Retrieves warehouse list filtered for POS cashier operations.",
    resp_example={"message": [{"name": "Machipisa Main Store - HRL"}]}
)

# =========================================================================
# 10. SUPPLIERS & PURCHASING
# =========================================================================
ep(
    "/api/resource/Supplier", "GET", "Suppliers & Purchasing",
    "List Suppliers",
    "Fetches registered vendor and supplier accounts.",
    resp_example={"data": [{"name": "Varichem Pharmaceuticals Ltd", "supplier_group": "Local"}]}
)
ep(
    "/api/method/saas_api.www.api.create_supplier", "POST", "Suppliers & Purchasing",
    "Create New Supplier",
    "Registers a new supplier from Goods Receiving voucher screen.",
    body_example={"supplier_name": "Datlabs Zimbabwe", "supplier_group": "Pharmaceuticals", "phone": "+263242000222"},
    resp_example={"message": {"name": "Datlabs Zimbabwe", "status": "Created"}}
)
ep(
    "/api/resource/Purchase%20Invoice", "POST", "Suppliers & Purchasing",
    "Submit Purchase Invoice / GRV",
    "Records supplier invoice and stock receipt at POS receiving dock.",
    body_example={"supplier": "Varichem Pharmaceuticals Ltd", "bill_no": "INV-88910", "items": [{"item_code": "ITEM-00102", "qty": 100, "rate": 1.80}]},
    resp_example={"data": {"name": "PINV-2026-00012"}}
)
ep(
    "/api/resource/Purchase%20Invoice", "GET", "Suppliers & Purchasing",
    "List Purchase Invoices",
    "Lists purchase invoices for receipt status audit.",
    resp_example={"data": [{"name": "PINV-2026-00012", "grand_total": 180.00}]}
)

# =========================================================================
# 11. MASTER DATA & SETUP
# =========================================================================
ep(
    "/api/method/erpnext.setup.utils.get_exchange_rate", "GET", "Master Data & Setup",
    "Get Real-Time Currency Exchange Rate",
    "Fetches active exchange rate between two currencies (e.g. USD to ZiG, ZAR, BWP) from ERPNext Currency Exchange table.",
    params=[{"name": "from_currency", "in": "query", "required": True, "schema": {"type": "string", "example": "USD"}}, {"name": "to_currency", "in": "query", "required": True, "schema": {"type": "string", "example": "ZIG"}}, {"name": "transaction_date", "in": "query", "schema": {"type": "string"}}],
    resp_example={"message": 26.54}
)
ep(
    "/api/method/saas_api.www.api.get_exchange_rates", "GET", "Master Data & Setup",
    "Get All SaaS Exchange Rates",
    "Returns full matrix of active exchange rates against base currency.",
    resp_example={"message": {"base_currency": "USD", "rates": {"USD": 1.0, "ZIG": 26.54, "ZAR": 18.20, "BWP": 13.50}}}
)
ep(
    "/api/currencies", "GET", "Master Data & Setup",
    "List Enabled Currencies",
    "Fetches all currencies activated for transactions.",
    resp_example={"data": [{"currency": "USD", "symbol": "$"}, {"currency": "ZIG", "symbol": "ZiG"}, {"currency": "ZAR", "symbol": "R"}]}
)
ep(
    "/api/resource/Price%20List", "GET", "Master Data & Setup",
    "List Price Lists",
    "Fetches price list masters (e.g. Standard Retail, Wholesale, Happy Hour, Export).",
    resp_example={"data": [{"name": "Standard Retail", "currency": "USD"}, {"name": "Wholesale USD", "currency": "USD"}]}
)
ep(
    "/api/resource/Account", "GET", "Master Data & Setup",
    "List General Ledger Accounts",
    "Retrieves Chart of Accounts ledgers for income, expense, asset, and tax mapping.",
    params=[{"name": "filters", "in": "query", "schema": {"type": "string"}}, {"name": "fields", "in": "query", "schema": {"type": "string"}}],
    resp_example={"data": [{"name": "Debtors - HRL", "account_type": "Receivable"}]}
)
ep(
    "/api/resource/Tax%20Category", "GET", "Master Data & Setup",
    "Get Tax Categories",
    "Fetches tax categories (e.g. Standard 15%, Zero Rated, Exempt).",
    resp_example={"data": [{"name": "Standard"}, {"name": "Zero Rated"}, {"name": "Exempt"}]}
)
ep(
    "/api/taxes", "GET", "Master Data & Setup",
    "List Tax Rates & Accounts",
    "Fetches tax rates, percentages, and corresponding tax ledger accounts.",
    resp_example={"data": [{"title": "VAT Standard 15%", "rate": 15.0, "account_head": "VAT Output - HRL"}]}
)
ep(
    "/api/countries", "GET", "Master Data & Setup",
    "List Countries",
    "Returns countries list for addresses and customer setup.",
    resp_example={"data": [{"name": "Zimbabwe", "code": "ZW"}]}
)
ep(
    "/api/method/saas_api.www.api.get_users", "GET", "Master Data & Setup",
    "Sync System Users & Cashiers",
    "Fetches cashiers, supervisors, and managers with PIN codes and assigned roles.",
    resp_example={"message": [{"email": "cashier@havano.pro", "full_name": "John Doe", "enabled": 1, "role_profile_name": "POS Cashier"}]}
)
ep(
    "/api/method/saas_api.www.api.get_user", "GET", "Master Data & Setup",
    "Get User Profile",
    "Fetches single user details.",
    params=[{"name": "email", "in": "query", "schema": {"type": "string"}}],
    resp_example={"message": {"email": "cashier@havano.pro", "full_name": "John Doe"}}
)
ep(
    "/api/method/saas_api.www.api.create_user", "POST", "Master Data & Setup",
    "Create Cashier User",
    "Registers a new cashier account from POS manager interface.",
    body_example={"email": "newcashier@havano.pro", "full_name": "Mary Moyo", "role": "POS Cashier", "pin": "1234"},
    resp_example={"message": {"status": "User created", "email": "newcashier@havano.pro"}}
)
ep(
    "/api/resource/User", "GET", "Master Data & Setup",
    "Frappe User Resource Query",
    "Direct query for user credentials and active accounts.",
    resp_example={"data": [{"name": "cashier@havano.pro", "enabled": 1}]}
)
ep(
    "/api/method/havano_company.apis.company.register_company", "POST", "Master Data & Setup",
    "Register New Tenant Company",
    "Sets up a new company tenant on Havano backoffice.",
    body_example={"company_name": "Havano Supermarket", "currency": "USD", "country": "Zimbabwe"},
    resp_example={"message": {"company_id": 105, "status": "Registered"}}
)
ep(
    "/api/method/havano_company.apis.company.assign_user_to_company", "POST", "Master Data & Setup",
    "Assign User to Company",
    "Links a user email to an active company tenant.",
    body_example={"user_email": "cashier@havano.pro", "company_id": 105},
    resp_example={"message": {"status": "Assigned"}}
)

# =========================================================================
# 12. ZIMRA FISCALIZATION
# =========================================================================
ep(
    "/api/method/havanozimracloud.api.token", "POST", "ZIMRA Fiscalization",
    "Obtain ZIMRA Fiscal API Token",
    "Authenticates with Havano ZIMRA cloud service to obtain or refresh the Bearer authorization token.",
    body_example={"device_model_name": "Havano Virtual Fiscal Device", "device_model_version": "1.0", "certificate_pem": "-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----"},
    resp_example={"message": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "expires_in": 86400}}
)
ep(
    "/api/method/havanozimracloud.api.pingzimra", "POST", "ZIMRA Fiscalization",
    "Ping ZIMRA Cloud Gateway",
    "Tests connectivity to ZIMRA Tax Data Management System (FDMS) gateway.",
    resp_example={"message": {"status": "online", "latency_ms": 112}}
)
ep(
    "/api/method/havanozimracloud.api.openday", "POST", "ZIMRA Fiscalization",
    "Open ZIMRA Fiscal Day",
    "Sends opening fiscal day command to ZIMRA server. Required before transmitting fiscal invoices.",
    body_example={"fiscal_day_no": 142, "date": "2026-11-03"},
    resp_example={"message": {"status": "Fiscal Day Opened", "day_id": 142}}
)
ep(
    "/api/method/havanozimracloud.api.getdaystatus", "POST", "ZIMRA Fiscalization",
    "Get ZIMRA Fiscal Day Status",
    "Verifies if current fiscal day is open, closed, or pending close.",
    resp_example={"message": {"day_status": "FiscalDayOpened", "day_number": 142}}
)
ep(
    "/api/method/havanozimracloud.api.closeday", "POST", "ZIMRA Fiscalization",
    "Close ZIMRA Fiscal Day (Z-Report)",
    "Closes fiscal day with daily turnover totals, generating official ZIMRA Z-Report signature.",
    body_example={"fiscal_day_no": 142, "daily_turnover": {"USD": 450.00, "ZIG": 12000.00}},
    resp_example={"message": {"status": "Fiscal Day Closed", "z_number": "Z-00142"}}
)
ep(
    "/api/method/havanozimracloud.api.sendinvoice", "POST", "ZIMRA Fiscalization",
    "Transmit Fiscal Invoice to ZIMRA Cloud",
    "Submits POS invoice data to ZIMRA FDMS, receiving QR code URL, fiscal verification code, and electronic signature.",
    body_example={"invoice_num": "INV-2026-00089", "invoice_date": "2026-11-03T14:15:00Z", "tax_lines": [{"tax_code": "A", "tax_percent": 15.0, "tax_amount": 0.65, "net_amount": 4.35}], "total_amount": 5.00, "buyer_tin": "200098765"},
    resp_example={"message": {"fiscal_code": "A9B2-CC41-DE90", "verification_url": "https://efdms.zimra.co.zw/verify?code=A9B2CC41DE90", "qr_data": "https://efdms.zimra.co.zw/verify?code=A9B2CC41DE90", "device_sn": "HAV-FD-2026-009"}}
)

# =========================================================================
# 13. RESTAURANT & HOSPITALITY
# =========================================================================
ep(
    "/api/method/saas_api.www.api.get_restaurant_data", "GET", "Restaurant & Hospitality",
    "Get Restaurant Floors & Tables",
    "Retrieves dining floor layout, table names, seating capacity, and current occupied/vacant status.",
    resp_example={"message": {"areas": [{"name": "Patio", "tables": [{"table_number": "P1", "capacity": 4, "status": "Available"}]}, {"name": "Main Dining", "tables": [{"table_number": "T1", "capacity": 6, "status": "Occupied"}]}]}}
)
ep(
    "/api/method/saas_api.www.api.open_table", "POST", "Restaurant & Hospitality",
    "Open Dining Table",
    "Marks a dining table as occupied and assigns a server/waiter.",
    body_example={"table_number": "T1", "waiter": "Jane Server", "guests": 4},
    resp_example={"message": {"order_id": "TAB-ORDER-991", "table_number": "T1"}}
)
ep(
    "/api/method/saas_api.www.api.get_table_orders", "GET", "Restaurant & Hospitality",
    "Get Active Table Orders",
    "Fetches all open food and beverage tabs for an active dining table.",
    params=[{"name": "table_number", "in": "query", "required": True, "schema": {"type": "string"}}],
    resp_example={"message": {"table_number": "T1", "items": [{"item_code": "STEAK-RIBEYE", "qty": 2, "price": 18.00}]}}
)
ep(
    "/api/method/saas_api.www.api.save_kitchen_order", "POST", "Restaurant & Hospitality",
    "Send Kitchen Order Ticket (KOT)",
    "Transmits food and drink orders to Kitchen Display System (KDS) and preparation stations.",
    body_example={"table_number": "T1", "course": "Mains", "items": [{"item_code": "STEAK-RIBEYE", "qty": 2, "notes": "Medium rare, mushroom sauce"}, {"item_code": "SALAD-GREEK", "qty": 1, "notes": "No onions"}]},
    resp_example={"message": {"kot_id": "KOT-00812", "status": "Sent to Kitchen"}}
)
ep(
    "/api/method/saas_api.www.api.close_table_order", "POST", "Restaurant & Hospitality",
    "Close Table Order & Settle Bill",
    "Marks table order as settled, releasing table back to Available status.",
    body_example={"table_number": "T1", "invoice_num": "ACC-SINV-2026-00089"},
    resp_example={"message": {"table_number": "T1", "status": "Available"}}
)

# =========================================================================
# 14. SUBSCRIPTIONS & BILLING
# =========================================================================
ep(
    "/api/subscription/plans", "GET", "Subscriptions & Billing",
    "Get Subscription Plans",
    "Fetches tier pricing (Monthly, Quarterly, Annual) for Havano POS SaaS license.",
    resp_example={"plans": [{"id": 1, "name": "Standard Single Till", "price_usd": 25.0, "billing_period": "Monthly"}, {"id": 2, "name": "Enterprise Multi-Branch", "price_usd": 75.0, "billing_period": "Monthly"}]}
)
ep(
    "/api/subscription/status", "GET", "Subscriptions & Billing",
    "Get Current License Subscription Status",
    "Checks active subscription tier, days remaining, expiration timestamp, and max till limit.",
    resp_example={"status": "Active", "plan": "Standard Single Till", "expires_on": "2027-01-01", "days_remaining": 58}
)
ep(
    "/api/subscription/subscribe", "POST", "Subscriptions & Billing",
    "Activate Subscription Plan",
    "Activates or renews a license plan.",
    body_example={"plan_id": 1, "duration_months": 12},
    resp_example={"status": "success", "invoice_id": "SUB-INV-001"}
)
ep(
    "/api/subscription/pay", "POST", "Subscriptions & Billing",
    "Pay Subscription",
    "Submits payment confirmation for license renewal.",
    body_example={"subscription_id": 41, "payment_method": "Ecocash", "transaction_ref": "MP261103.1415.H001"},
    resp_example={"status": "success", "message": "Subscription renewed"}
)
ep(
    "/api/subscription/topup", "POST", "Subscriptions & Billing",
    "Top Up Account Balance",
    "Adds funds to tenant credit wallet for automated subscription renewals.",
    body_example={"amount": 100.00, "currency": "USD"},
    resp_example={"status": "success", "new_balance": 150.00}
)
ep(
    "/api/subscription/pay_from_balance", "POST", "Subscriptions & Billing",
    "Pay Subscription from Wallet Balance",
    "Renews subscription instantly deducting from tenant pre-funded credit balance.",
    body_example={"plan_id": 1},
    resp_example={"status": "success", "remaining_balance": 125.00}
)

# =========================================================================
# 15. REPORTS & ANALYTICS
# =========================================================================
ep(
    "/api/method/frappe.desk.query_report.run", "POST", "Reports & Analytics",
    "Execute Frappe Query Report",
    "Executes standard Frappe script and SQL reports (e.g. Sales Register, Stock Balance, Item-wise Sales).",
    body_example={"report_name": "Item-wise Sales Register", "filters": {"from_date": "2026-11-01", "to_date": "2026-11-03", "company": "Havano Retail Ltd"}},
    resp_example={"message": {"columns": [], "result": []}}
)
ep(
    "/api/method/saas_api.www.api.daily_sales", "GET", "Reports & Analytics",
    "Daily Sales Summary Report",
    "Fetches consolidated sales volume, gross profit, and tender breakdown for a specific date.",
    params=[{"name": "date", "in": "query", "schema": {"type": "string", "example": "2026-11-03"}}],
    resp_example={"message": {"date": "2026-11-03", "total_sales_usd": 1850.50, "total_sales_zig": 42500.00, "invoice_count": 142}}
)
ep(
    "/api/method/saas_api.www.api.category_profitability", "GET", "Reports & Analytics",
    "Category Profitability Report",
    "Analyzes margin and gross profit contribution per product category.",
    resp_example={"message": [{"category": "Beverages", "sales_usd": 450.0, "cogs_usd": 280.0, "margin_percent": 37.7}]}
)
ep(
    "/api/method/saas_api.www.api.cashier_profitability", "GET", "Reports & Analytics",
    "Cashier Performance Report",
    "Breakdown of sales, returns, and discounts processed per cashier.",
    resp_example={"message": [{"cashier": "cashier@havano.pro", "sales_count": 89, "total_sales_usd": 1200.00}]}
)
ep(
    "/api/method/saas_api.www.api.shop_profitability", "GET", "Reports & Analytics",
    "Branch / Shop Profitability Comparison",
    "Compares sales performance and margins across different retail store branches.",
    resp_example={"message": [{"shop": "Machipisa Branch", "total_sales": 12500.00, "net_margin": 18.5}]}
)
ep(
    "/api/method/havano_addons.www.api.user_stock_report", "GET", "Reports & Analytics",
    "User Stock Valuation Report",
    "Generates stock valuation report for the user's assigned warehouse.",
    resp_example={"message": {"total_valuation_usd": 45890.00, "items_count": 1420}}
)

# =========================================================================
# 16. SUPPORT & HELPDESK
# =========================================================================
ep(
    "/api/support/ticket", "POST", "Support & Helpdesk",
    "Submit POS Support Ticket",
    "Creates a support ticket or transmits crash telemetry from POS terminal to Havano support team.",
    body_example={"subject": "Receipt printer paper jam error", "priority": "Medium", "description": "Thermal printer failed to respond after invoice 0089", "logs": "Traceback..."},
    resp_example={"status": "success", "ticket_id": "TICKET-2026-044"}
)

# Save openapi.json
spec_path = os.path.join(out_dir, "openapi.json")
with open(spec_path, "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=2)

print(f"Generated comprehensive OpenAPI specification with {len(spec['paths'])} endpoints across {len(spec['tags'])} tags!")
print(f"Saved to: {spec_path}")

