# EverLightOS Deployment Guide

## 🌐 **CLOUDFLARE PAGES DEPLOYMENT (Recommended)**

### **Step 1: Build Static Site**
```bash
npm install
npm run build
```
This creates a `dist/` folder with your static site.

### **Step 2: Deploy to Cloudflare Pages**

#### **Option A: GitHub Integration (Recommended)**
1. Push code to GitHub repository
2. Go to [Cloudflare Dashboard](https://dash.cloudflare.com) → Pages
3. Click "Create a project" → "Connect to Git"
4. Select your repository: `EverLightOS-SentinelSystems`
5. Configure build settings:
   - **Build command**: `npm run build`
   - **Build output directory**: `dist`
   - **Root directory**: `/` (leave empty)
6. Click "Save and Deploy"

#### **Option B: Direct Upload**
1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com) → Pages
2. Click "Create a project" → "Upload assets"
3. Upload the entire `dist/` folder
4. Set project name: `everlightos-com`

### **Step 3: Custom Domain (Optional)**
1. In Cloudflare Pages → Your project → Custom domains
2. Add `everlightos.com` and `www.everlightos.com`
3. Cloudflare will handle SSL certificates automatically

---

## ⚡ **THE ONE RING DEPLOYMENT (Advanced)**

### **Prerequisites**
- Cloudflare account with Workers Paid plan ($5/month)
- Ollama server running at `ai.omniversalaether.online`
- Environment variables in `DONTFORGETTHISHAWKEYE/omni-env.sh`

### **Step 1: Deploy Cloudflare Infrastructure**
```bash
# Load environment
source ./DONTFORGETTHISHAWKEYE/omni-env.sh

# Deploy Worker + D1 + Vectorize + R2 + KV
./DONTFORGETTHISHAWKEYE/deploy-one-ring.sh
```

### **Step 2: Deploy Static Site**
```bash
# Build static site
npm run build

# Deploy to Cloudflare Pages (same as above)
# The Worker will automatically handle /api/* routes
```

### **Step 3: Test Live AI**
```bash
# Test chat endpoint
curl -X POST "https://your-worker.your-subdomain.workers.dev/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from EverLightOS!", "model": "llama3.1:8b"}'

# Test search endpoint  
curl -X POST "https://your-worker.your-subdomain.workers.dev/api/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "federated intelligence"}'
```

---

## 🔧 **TROUBLESHOOTING**

### **Build Issues**
```bash
# Clear cache and rebuild
rm -rf node_modules dist
npm install
npm run build
```

### **Cloudflare Pages Issues**
- **Build fails**: Check build logs in Cloudflare Dashboard
- **404 errors**: Ensure build output directory is set to `dist`
- **Styling issues**: Check if Tailwind CSS is building correctly

### **The One Ring Issues**
- **Worker deployment fails**: Check `wrangler.toml` configuration
- **AI endpoints not working**: Verify Ollama server is accessible
- **Database errors**: Check D1 database schema deployment

---

## 📋 **DEPLOYMENT CHECKLIST**

### **Static Site Only**
- [ ] `npm install` completed
- [ ] `npm run build` creates `dist/` folder
- [ ] Cloudflare Pages project created
- [ ] Build settings configured (command: `npm run build`, output: `dist`)
- [ ] Custom domain added (optional)

### **The One Ring (Advanced)**
- [ ] Environment variables configured in `DONTFORGETTHISHAWKEYE/omni-env.sh`
- [ ] Ollama server accessible at `ai.omniversalaether.online`
- [ ] Cloudflare Workers Paid plan active
- [ ] `./DONTFORGETTHISHAWKEYE/deploy-one-ring.sh` executed successfully
- [ ] Static site deployed to Cloudflare Pages
- [ ] API endpoints tested and working

---

**RECOMMENDATION**: Start with static site deployment first, then add The One Ring features later if you want live AI functionality.