# CMS Development Roadmap

This roadmap outlines the provisional stages for the development of the Bangjeje CMS. It serves as a strategic timeline and may be refined as development progresses.

## PHASE 0: Foundation & Architecture
Establish and document the CMS architecture, information architecture, content models, technical boundaries, and implementation plan. Ensure strict separation between the CMS and the public website. (Current Phase)

## PHASE 1: CMS Design System
Integrate the Bangjeje visual identity (Primary Color: `#9929EA`, Typography: Outfit, Light mode only) into the TailAdmin foundation.

## PHASE 2: Dashboard
Build the Dashboard UI, incorporating the required statistics, recent content lists, and executive overview metrics.

## PHASE 3: Articles
Develop the Articles module, including the listing, create/edit workflows, and integration of the Article content model.

## PHASE 4: Case Studies
Develop the Case Studies module, ensuring it is built upon its distinct content model independent of Articles.

## PHASE 5: Digital Assets
Develop the Digital Assets module to support both free and paid asset management schemas.

## PHASE 6: Publishing & Website Integration
Design and implement the data synchronization mechanism and publishing workflow connecting GitHub (CMS source of truth) with the public website deployment.

## PHASE 7: Authentication & Security
Set up the necessary security boundaries, authentication infrastructure, and user access controls.

## PHASE 8: Deployment & Production Hardening
Configure Cloudflare deployment (`admin.bangjeje.dev`), Workers, R2 (if required), and finalize performance/security hardening for production release.
