# Weekly (May 25–30, 2026) — Summary

## Status at a Glance

| Project | Status | Key Update | Blocker |
|---------|--------|------------|---------|
| MRP (Infor Food Pkg) | 🔴 Blocked | Import order K0 → K1→ K2→ K7 defined | ERP Syteline Infor — MRP Planning won't generate (data integration issue) |
| Returnable Box 🎨 | 🟡 In Progress | BOXSOFT dimension criteria scoped | — |
| Move Apps (Project) | 🟢 On Track | Server migration TPN → TPK scoped | Current version folder mismatch |

## Executive Summary

- **MRP Phase 3 stalled**: ERP Syteline Info unable to generate MRP Planning, likely due to incorrect data integration. This pushes all Phase 3 execution to next week. Phase 1 & 2 groundwork continued.
- **Returnable Box**: Moving forward on Adjustment process; notification feature and documentation updates remain pending.
- **Move Apps**: Server migration from TPN to TPK in progress.

## This Week (May 25–30)

1. [Move Apps] Project scoped — server migration TPN → TPK, apps catalogued (4 - 8 apps)
2. ❌ [MRP] Phase 3: MRP Planning run — blocked, ERP Syteline Infor cannot generate
3. [Box] Build Adjustment form details fetcher
4. 🔎 [Box] Pending: Dimension criteria dig-in (BOXSOFT client mapping)

## Next Week (Carried Forward)

1. [Move Apps] Start with P' Manoon — begin server migration
2. [Move Apps] DB server: current 192.168.10.17 → target 192.168.95.100
3. [MRP] Fix data integration so ERP Syteline Infor can generate MRP Planning
4. [MRP] Run MRP Planning once data integration is correct (~2–3 hrs)
5. [Box] Build on top Adjustment program from usual
6. [Box] Wire up notification flow: **Production → Delivery Order → Stock FG** alert
7. [Box] Box search by dimension
8. [Box] 📖 Update User Manual & Developer Guide

## Notes to Self

- Move Apps: 1 month deadline (or at least 2 weeks). Shared files: TPNDBAPP21 (192.168.10.2) → Share Center → Program (TPN) and `\\192.168.57.39\software\F_PROJECT` (TPK)
- Move Apps: BOXSOFT instance = TPK-REGULUS, DB = csgwin-tpk
- Box: Dimension search: waiting on customer file → leverage BOXSOFT if available

---

*Updated by Wuttipong on 2026-05-30*
