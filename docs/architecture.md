# Architecture

## 1. Project Context
The bangjeje.dev platform is split into two entirely separate repositories:
- **Public Website:** `bangjeje-dev/revamp`
- **CMS:** `bangjeje-dev/admin`

The public website is a lightweight static HTML-based website. It must remain completely isolated from CMS development.

## 2. Public Website vs CMS Boundary
The CMS is an independent, administrative interface and must not become embedded inside the public website source code. Both projects must remain independently deployable.

**Conceptual Architecture:**
```
GitHub
│
├── bangjeje-dev/revamp
│      └── Public Website
│
└── bangjeje-dev/admin
       └── Bangjeje CMS
              │
              └── Future publishing/data workflow
                       │
                       ↓
                 Public Website
                       │
                       ↓
                 Cloudflare Pages
```

## 3. Technology Direction
The CMS leverages the existing TailAdmin HTML template as its UI foundation.

**Preferred Stack:**
- HTML
- Tailwind CSS
- Vanilla JavaScript
- Existing TailAdmin HTML structure/components
- Existing Webpack build tooling (as provided by TailAdmin)

**Constraints:**
- Do NOT introduce React, Next.js, Vue, Nuxt, Angular, Supabase, Firebase, or any heavy backend framework.
- Retain existing TailAdmin structure, components, and attribution/license files.

## 4. Future Deployment Direction
The CMS is intended to be deployed separately from the public website via a separate Cloudflare Pages deployment (e.g., `admin.bangjeje.dev`). 

*Note: Cloudflare configurations, Workers, R2, and authentication infrastructure will be implemented in later phases.*

## 5. Design System Direction
The CMS will eventually integrate Bangjeje's visual identity, overriding TailAdmin where appropriate in later phases.
- **Primary Brand Color:** `#9929EA`
- **Typography:** Outfit
- **Theme:** Light mode only (no dark mode).
