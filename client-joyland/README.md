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
- [ ] Create Django project & initial app (`rentals`, `users`, etc.)
- [ ] Set up virtual environment & `.env` config
- [ ] Install essential packages (`djangorestframework`, `django-cors-headers`, `dj-database-url`, etc.)
- [ ] Enable CORS for React frontend

---

## 🔐 2. Authentication & Authorization
- [ ] Create `User` model (extend `AbstractUser` or use default)
- [ ] Add user roles: `Admin`, `Landlord`, `Tenant`
- [ ] JWT or session-based auth (`djangorestframework-simplejwt`)
- [ ] Login / Logout / Password change APIs
- [ ] Permissions based on role (e.g., only Admin can delete users)
- [ ] Use `djangorestframework-simplejwt` for token-based auth
- [ ] Consider integrating OAuth2 with `django-oauth-toolkit` (optional)
- [ ] Enable HTTPS (especially in production)
- [ ] Use CSRF protection for session-based auth (if used)
- [ ] Secure all endpoints with permission classes
- [ ] Use throttling (`DEFAULT_THROTTLE_CLASSES`) to prevent abuse
- [ ] Install `django-axes` or similar for brute-force protection
- [ ] Use `django-role-permissions` or `django-guardian` for role-based permissions
- [ ] Create custom permissions for role-based API access
- [ ] Validate all input with serializers to avoid injection

---

## 🏘️ 3. Core Models & API Structure
- [ ] **Property** model (name, address, units, landlord, etc.)
- [ ] **Unit** model (belongs to property, rent amount, status)
- [ ] **Tenant** profile (linked to user)
- [ ] **Lease** model (unit, tenant, start/end date, monthly rent)
- [ ] **Payment** model (amount, date, method, linked lease)
- [ ] **MaintenanceRequest** model (tenant, unit, description, status)
- [ ] **Notification** system (optional for overdue rent, upcoming due)

---

## 📦 4. Admin & CRUD APIs
- [ ] Admin panel customization (if needed)
- [ ] API endpoints for all models using Django REST Framework:
  - [ ] Properties CRUD
  - [ ] Units CRUD
  - [ ] Leases CRUD
  - [ ] Tenants CRUD
  - [ ] Payments (list, create, update)
  - [ ] Maintenance Requests
- [ ] Pagination, filtering, and search

---

## 📅 5. Rent Tracking & Reminders
- [ ] Auto-generate rent due entries each month
- [ ] Status: paid, overdue, upcoming
- [ ] Email or notification system (sendgrid/smtp)

---

## 📊 6. Reporting & Dashboard APIs
- [ ] Monthly revenue per property
- [ ] Occupancy rate
- [ ] Outstanding payments
- [ ] Export to CSV/PDF (optional)

---

## 🚀 7. Deployment & Production
- [ ] Use `.env` and `decouple` for secrets
- [ ] PostgreSQL database
- [ ] Render / Railway / DigitalOcean / Qovery deployment
- [ ] Set up domain, HTTPS, and logs

## ⚡ 8. Performance Enhancements

- [ ] Add Redis for caching (Django `cache` framework)
- [ ] Cache frequent reads (e.g., property lists, tenant profiles)
- [ ] Enable database query optimization (e.g., `.select_related`)
- [ ] Use `django-ratelimit` or DRF throttling
- [ ] Use a CDN (like Cloudflare) for static/media files
- [ ] Load balancing via platform (Render, Railway, or NGINX config)


## 📋 9. Trello + GitHub Integration for Dev Workflow
- [ ] Create Trello board (`Rent Management System`)
- [ ] Set up lists: Ideas, To Do, In Progress, In Review, Done
- [ ] Install **GitHub Power-Up** (free on Trello)
- [ ] Link GitHub commits/PRs using `#cardID` in commit messages
- [ ] Enable **Butler automations**:
  - [ ] Auto-move cards when PR is merged
  - [ ] Mark checklist items on commit
- [ ] Use labels for task types (e.g., `backend`, `frontend`, `bug`)
- [ ] Assign team members to cards
