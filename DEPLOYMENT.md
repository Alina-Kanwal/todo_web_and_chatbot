# Railway Deployment Guide

## ⚠️ CRITICAL: Root Directory Must Be Set

This is a **monorepo** (backend + frontend in one repo). Railway CANNOT auto-detect which folder to build.

**You MUST manually set the Root Directory in Railway UI!**

---

## Step-by-Step: Fix Backend Deployment

### Step 1: Go to Railway Dashboard
1. Visit: https://railway.app
2. Open your project: `efficient-acceptance`
3. Click on your service: `Todo_web_application`

### Step 2: Go to Settings Tab
Click **"Settings"** at the top (next to Deployments, Variables, Metrics)

### Step 3: Find "Deploy" in Right Sidebar
On the right side of the Settings page, you'll see a menu:
- Source
- Networking
- Scale
- Build
- **Deploy** ← Click this!
- Config-as-code
- Danger

### Step 4: Set Root Directory
After clicking "Deploy", you'll see:

```
┌──────────────────────────────────────────┐
│ Root Directory                           │
│ [  backend  ]  ← TYPE THIS!              │
└──────────────────────────────────────────┘
```

**Enter: `backend`** (without quotes)

### Step 5: Verify Start Command
Make sure the Start Command is:
```
uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

### Step 6: Remove Pre-deploy Command (if exists)
If you see "Pre-deploy Command" with `npm run migrate`, **delete it** or leave it empty.

### Step 7: Add Environment Variables
Click **"Variables"** tab at the top, then add:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | Your Neon PostgreSQL URL |
| `BETTER_AUTH_SECRET` | Random 32+ char string |

### Step 8: Deploy!
Click the purple **"Deploy"** button at the top left.

---

## Frontend Deployment (After Backend Works)

1. Click **"New"** → **"Empty Service"**
2. In Settings → Deploy section:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Start Command**: `npx next start -p $PORT`
3. Variables:
   - `NEXT_PUBLIC_API_BASE_URL`: Your backend Railway URL
   - `BETTER_AUTH_SECRET`: Same as backend

---

## Generate JWT Secret

Run this locally to generate a secure secret:
```bash
openssl rand -hex 32
```
Use the **same secret** for both backend and frontend.

---

## Environment Variables Summary

| Service | Variable | Value |
|---------|----------|-------|
| Backend | `DATABASE_URL` | Neon PostgreSQL connection string |
| Backend | `BETTER_AUTH_SECRET` | 32+ char random string |
| Frontend | `NEXT_PUBLIC_API_BASE_URL` | Railway backend URL |
| Frontend | `BETTER_AUTH_SECRET` | Same as backend |

---

## After Deployment

### Backend
- **URL**: `https://<backend-name>.railway.app`
- **API Docs**: `https://<backend-name>.railway.app/docs`
- **Health Check**: `https://<backend-name>.railway.app/api/health`

### Frontend
- **URL**: `https://<frontend-name>.railway.app`
- **Main App**: `https://<frontend-name>.railway.app`

---

## Troubleshooting

### Railpack could not determine how to build the app
- Ensure **Root Directory** is set to `backend` or `frontend` in Railway Settings
- Verify `requirements.txt` exists in `backend/`
- Verify `package.json` exists in `frontend/`

### Frontend can't connect to backend
- Ensure `NEXT_PUBLIC_API_BASE_URL` is set correctly
- Check CORS settings in backend allow the frontend URL

### Database connection fails
- Verify `DATABASE_URL` includes `?sslmode=require`
- Check Neon dashboard for connection limits

### Build fails
- Check Railway build logs
- Ensure all dependencies are in `requirements.txt` / `package.json`

---

## Useful Links

- [Railway Docs](https://docs.railway.app)
- [Neon Database](https://neon.tech)
- [Project Repo](https://github.com/Alina-Kanwal/Todo_web_application)
