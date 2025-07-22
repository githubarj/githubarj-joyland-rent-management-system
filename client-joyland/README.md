# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type aware lint rules:

- Configure the top-level `parserOptions` property like this:

```js
export default {
  // other rules...
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: ['./tsconfig.json', './tsconfig.node.json'],
    tsconfigRootDir: __dirname,
  },
}
```

- Replace `plugin:@typescript-eslint/recommended` to `plugin:@typescript-eslint/recommended-type-checked` or `plugin:@typescript-eslint/strict-type-checked`
- Optionally add `plugin:@typescript-eslint/stylistic-type-checked`
- Install [eslint-plugin-react](https://github.com/jsx-eslint/eslint-plugin-react) and add `plugin:react/recommended` & `plugin:react/jsx-runtime` to the `extends` list


# 🏠 Rent Management System – Backend Roadmap (Django + React)

## ✅ 1. Project Setup
- [ ] Create Django project & initial apps (`users`, `properties`, `tenants`, `invoices`, `payments`)
- [ ] Set up virtual environment & `.env` config
- [ ] Install essential packages (`djangorestframework`, `django-cors-headers`, `dj-database-url`, etc.)
- [ ] Enable CORS for React frontend
- [ ] PostgreSQL setup

---

## 🔐 2. Authentication & Authorization
- [ ] Create `User` model (extend `AbstractUser` or use default)
- [ ] Add user roles: `Admin`, `Landlord`, `Tenant`
- [ ] JWT auth via `djangorestframework-simplejwt`
- [ ] Login / Logout / Password management APIs
- [ ] Role-based permissions (admin-only actions, landlord vs tenant access)
- [ ] Optional OAuth2 via `django-oauth-toolkit`
- [ ] Enable HTTPS in production
- [ ] CSRF protection for session auth (if used)
- [ ] Secure endpoints using DRF permission classes
- [ ] Add throttling to limit API abuse
- [ ] Use `django-axes` to block brute-force attempts
- [ ] Integrate `django-role-permissions` or `django-guardian`
- [ ] Validate input via serializers

---

## 🏘️ 3. Core Models & Structure

### 🧍 Users & Tenants
- `TenantProfile`: phone, unit (FK), status, move-in/out dates

### 🏢 Properties & Units
- `Property`: name, address, landlord (FK)
- `Unit`: property (FK), unit_number, rent_amount, is_occupied

### 📄 Invoices
- `Invoice`: invoice_number, tenant (FK), unit (FK), issue_date, due_date, total, status, type (standard/repair/expense)
- `InvoiceItem`: invoice (FK), item_name, cost, quantity, total_cost
- `CancelledInvoice`: original_invoice (FK), reason, cancelled_by, timestamp

### 💵 Payments & Transactions
- `Payment`: invoice (FK), amount_paid, payment_method, transaction_id, paid_by, date
- `TransactionRecord`: payment (FK), reference, status
- `CancelledPayment`: original_payment (FK), reason, timestamp

### 🛠️ Maintenance & Notifications (Optional)
- `MaintenanceRequest`: unit, tenant, description, status
- `Notification`: type, message, user (FK), created_at, is_read

---

## 📦 4. CRUD APIs
- [ ] Properties CRUD
- [ ] Units CRUD
- [ ] Tenants CRUD
- [ ] Invoices and Invoice Items CRUD
- [ ] Payments & Manual Payment Recording
- [ ] Maintenance Requests (optional)
- [ ] Filtering, pagination, search

---

## 📅 5. Rent Tracking & Reminders
- [ ] Auto-generate monthly invoices from leases
- [ ] Mark invoices as paid, overdue, upcoming
- [ ] Send reminders (email/SMS/notification)

---

## 📊 6. Reporting & Dashboard APIs
- [ ] Revenue by property, unit, or date
- [ ] Invoice summary (by status/date)
- [ ] Outstanding payments
- [ ] Export to CSV/PDF

---

## 🚀 7. Deployment & Production
- [ ] Use `.env` and `decouple` for config
- [ ] PostgreSQL DB
- [ ] Render / Railway / Qovery deployment
- [ ] Enable HTTPS, logging, custom domain

---

## ⚡ 8. Performance Enhancements
- [ ] Redis caching (Django cache framework)
- [ ] Optimize queries with `select_related`, `prefetch_related`
- [ ] Throttle requests with DRF
- [ ] CDN for static/media files
- [ ] Load balancing support (platform/nginx)

---

## 📋 9. Trello + GitHub Integration
- [ ] Create Trello board (`Rent Management System`)
- [ ] Lists: Ideas, To Do, In Progress, In Review, Done
- [ ] GitHub Power-Up (free on Trello)
- [ ] Use commit messages with `#cardID`
- [ ] Butler automation: auto-move card on PR merge
- [ ] Use labels (`backend`, `frontend`, `urgent`)
- [ ] Assign tasks to team members