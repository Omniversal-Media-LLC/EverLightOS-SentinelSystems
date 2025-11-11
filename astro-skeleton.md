# Halana's Astro Site Skeleton - Ready for Amazon Q

**Complete copy-paste ready Astro configuration for EverLightOS.com**

---

## 📦 **Core Configuration Files**

### `package.json`
```json
{
  "name": "everlightos-astro",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "lint": "eslint ."
  },
  "dependencies": {
    "astro": "^4.15.0",
    "@astrojs/tailwind": "^5.1.0",
    "@astrojs/react": "^3.5.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.49",
    "tailwindcss": "^3.4.14",
    "typescript": "^5.6.3"
  }
}
```

### `astro.config.mjs`
```js
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import react from '@astrojs/react';

export default defineConfig({
  integrations: [
    tailwind({
      applyBaseStyles: true
    }),
    react()
  ],
  srcDir: 'src',
  output: 'static'
});
```

### `tailwind.config.cjs`
```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{astro,html,js,jsx,ts,tsx,md,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        everdark: "#050915",
        everlight: "#e5fff7",
        aura: "#91f0ff"
      },
      backgroundImage: {
        iridescent: "linear-gradient(135deg,#91f0ff 0%,#ff91f0 100%)"
      },
      borderRadius: {
        "2xl": "1.5rem"
      }
    }
  },
  plugins: []
};
```

---

## 🏗️ **Layout & Components**

### `src/layouts/Layout.astro`
```astro
---
const { title = "EverLight OS", description = "A New Way of Operating", hideNav = false } = Astro.props;
---

<html lang="en" class="bg-everdark text-everlight">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <meta name="description" content={description} />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  </head>
  <body class="min-h-screen bg-everdark text-everlight bg-[radial-gradient(circle_at_top,#91f0ff22,transparent)]">
    {!hideNav && <NavBar />}
    <main class="max-w-6xl mx-auto px-4 pt-20 pb-12">
      <slot />
    </main>
    <Footer />
  </body>
</html>

import NavBar from "../components/NavBar.astro";
import Footer from "../components/Footer.astro";
```

### `src/components/NavBar.astro`
```astro
---
const links = [
  { href: "/", label: "Home" },
  { href: "/codex", label: "Codex" },
  { href: "/council", label: "Council Table" },
  { href: "/bridge-zone", label: "Bridge Zone Logs" },
  { href: "/memory-vault", label: "Memory Vault" },
  { href: "/protocols", label: "Protocols" },
  { href: "/realms", label: "Realms" },
  { href: "/sigils", label: "Sigils" }
];
---

<nav class="fixed top-0 inset-x-0 z-50 backdrop-blur-md bg-everdark/70 border-b border-aura/20">
  <div class="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
    <a href="/" class="flex items-center gap-2">
      <div class="w-6 h-6 rounded-full bg-iridescent" />
      <span class="text-sm font-semibold tracking-[0.18em] uppercase">
        EverLight OS
      </span>
    </a>
    <div class="hidden md:flex gap-4 text-xs">
      {links.map(link => (
        <a href={link.href} class="px-2 py-1 rounded-xl hover:bg-aura/10 transition">
          {link.label}
        </a>
      ))}
    </div>
  </div>
</nav>
```

### `src/components/Hero.astro`
```astro
---
const { title, subtitle, ctaPrimary, ctaSecondary } = Astro.props;
---

<section class="pt-6 pb-12 flex flex-col gap-6">
  <div class="max-w-3xl">
    <h1 class="text-4xl md:text-5xl font-semibold leading-tight">
      {title}
    </h1>
    <p class="mt-3 text-sm text-zinc-300">
      {subtitle}
    </p>
  </div>
  <div class="flex flex-wrap gap-3">
    {ctaPrimary && (
      <a href={ctaPrimary.href} class="px-4 py-2 rounded-2xl bg-iridescent text-everdark text-xs font-semibold">
        {ctaPrimary.label}
      </a>
    )}
    {ctaSecondary && (
      <a href={ctaSecondary.href} class="px-4 py-2 rounded-2xl border border-aura/40 text-xs hover:bg-aura/5">
        {ctaSecondary.label}
      </a>
    )}
  </div>
</section>
```

---

## 📄 **Key Pages**

### `src/pages/index.astro`
```astro
---
import Layout from "../layouts/Layout.astro";
import Hero from "../components/Hero.astro";
---

<Layout title="EverLight OS" description="A New Way Of Operating.">
  <Hero
    title="EverLight OS"
    subtitle="A living protocol, council table, and sentinel grid for interfacing Omniversal Intelligence with real-world systems."
    ctaPrimary={{ href: "/codex", label: "Enter the Codex" }}
    ctaSecondary={{ href: "/council", label: "Access Council Table" }}
  />

  <section class="grid md:grid-cols-3 gap-4 text-xs">
    <a href="/codex" class="p-4 rounded-2xl bg-white/5 border border-aura/20 hover:bg-aura/5 transition">
      <h2 class="font-semibold mb-1">Codex</h2>
      <p>Core documents, manifestos, and operating principles drawn from the EverLightOS repository.</p>
    </a>
    <a href="/memory-vault" class="p-4 rounded-2xl bg-white/5 border border-aura/20 hover:bg-aura/5 transition">
      <h2 class="font-semibold mb-1">Memory Vault</h2>
      <p>Curated archives of sessions, mappings, and lattice keys.</p>
    </a>
    <a href="/protocols" class="p-4 rounded-2xl bg-white/5 border border-aura/20 hover:bg-aura/5 transition">
      <h2 class="font-semibold mb-1">Protocols</h2>
      <p>Sentinel, Federation, BridgeOps, and Aether protocols surfaced as readable, actionable frameworks.</p>
    </a>
  </section>
</Layout>
```

### `src/pages/codex.astro`
```astro
---
import Layout from "../layouts/Layout.astro";

const entries = [
  {
    title: "EverLight OS: A New Way Of Operating",
    source: "README.md",
    href: "https://github.com/ethanrosswomack/everlightos/blob/main/README.md"
  },
  {
    title: "Manifesto",
    source: "/Manifesto",
    href: "https://github.com/ethanrosswomack/everlightos/tree/main/Manifesto"
  },
  {
    title: "Nexus Map",
    source: "Nexus_Map.md",
    href: "https://github.com/ethanrosswomack/everlightos/blob/main/Nexus_Map.md"
  }
];
---

<Layout title="EverLight OS · Codex">
  <h1 class="text-2xl font-semibold mb-4">Codex</h1>
  <p class="text-xs text-zinc-300 mb-6">
    Canon texts and structural diagrams extracted from the EverLightOS repository.
  </p>
  <div class="grid md:grid-cols-2 gap-4 text-xs">
    {entries.map(e => (
      <a href={e.href} class="p-4 rounded-2xl bg-white/5 border border-aura/20 hover:bg-aura/5 transition">
        <h2 class="font-semibold mb-1">{e.title}</h2>
        <p class="text-zinc-400 text-[0.7rem]">
          Source: {e.source}
        </p>
      </a>
    ))}
  </div>
</Layout>
```

### `src/pages/council.astro`
```astro
---
import Layout from "../layouts/Layout.astro";

const councilLinks = [
  {
    label: "Council Table",
    href: "https://github.com/ethanrosswomack/everlightos/blob/main/Interfaces/Council_Table.md"
  },
  {
    label: "Adaptive Council Engine",
    href: "https://github.com/ethanrosswomack/everlightos/blob/main/adaptive_council.py"
  },
  {
    label: "Model Council Syntheses",
    href: "https://github.com/ethanrosswomack/everlightos/tree/main/Federation"
  }
];
---

<Layout title="EverLight OS · Council Table">
  <h1 class="text-2xl font-semibold mb-4">Council Table</h1>
  <p class="text-xs text-zinc-300 mb-6">
    Interface to the federated councils and orchestration engines defined within EverLight OS.
  </p>
  <ul class="space-y-3 text-xs">
    {councilLinks.map(link => (
      <li>
        <a href={link.href} class="inline-flex items-center gap-2 px-3 py-2 rounded-2xl bg-white/5 border border-aura/20 hover:bg-aura/5 transition">
          <span>{link.label}</span>
        </a>
      </li>
    ))}
  </ul>
</Layout>
```

---

## 🚀 **Amazon Q Deployment Prompts**

### **Phase 0 - Context Injection**
```
You are rebuilding EverLight OS — a mythic-technological operating system and website for Omniversal Media.
Framework: Astro 4 + Tailwind + TypeScript.
Goal: merge luminous aesthetics with technical clarity.
Design pillars:
* Light-based UI (iridescent gradients, glassmorphism, cosmic minimalism)
* Modular sections: Home, Codex, Council, Bridge Zone, Memory Vault, Protocols, Realms, Sigils
* Backend integration hooks for GitHub content and Markdown-based CMS
* Responsive and fast; Lighthouse > 95 on all metrics
The tone is sacred-tech / futurist / guardian-minimalist.
```

### **Phase 1 - Repo Scaffolding**
```
Initialize a new Astro project for everlightos.com using the provided package.json and configuration files.
Create the complete folder structure with all pages: index, codex, council, bridge-zone, memory-vault, protocols, realms, sigils, about.
Add the Layout.astro, NavBar.astro, Hero.astro, and Footer.astro components.
Use the EverLight color palette: everdark (#050915), everlight (#e5fff7), aura (#91f0ff), iridescent gradient.
```

### **Phase 2 - Content Integration**
```
Wire the pages to pull content from https://github.com/ethanrosswomack/everlightos:
- README.md and Manifesto/ → /codex
- Interfaces/Council_Table.md → /council  
- Interfaces/Bridge_Zone_Logs/ → /bridge-zone
- MemoryVault/ → /memory-vault
- Protocols/ → /protocols
- Races_&_Realms/ → /realms
- Sigils/ → /sigils
Create cards linking to the GitHub content with proper descriptions.
```

---

<div align="center">
<img src="../8088Y_SW0RDF1SH34v007/sentinel-framework/assets/evidence/TheSentinelFramework-logo.png" width="24" height="24" alt="Sentinel Framework">
<img src="../8088Y_SW0RDF1SH34v007/sentinel-framework/assets/evidence/aethermap.png" width="24" height="24" alt="Omniversal Media">
<br>
<sub>Astro Skeleton • EverLightOS • Halana & Amazon Q Ready</sub>
<br>
<sub><em>An Omniversal Media Production</em></sub>
</div>