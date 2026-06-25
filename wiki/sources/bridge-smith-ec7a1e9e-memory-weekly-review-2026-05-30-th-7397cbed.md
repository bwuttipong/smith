---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-weekly-review-2026-05-30-th-7397cbed
title: "Memory Bridge (smith): weekly-review-2026-05-30-th"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/weekly-review-2026-05-30-th.md
bridgeRelativePath: memory/weekly-review-2026-05-30-th.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-05-30T07:04:13.344Z
---

# Memory Bridge (smith): weekly-review-2026-05-30-th

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/weekly-review-2026-05-30-th.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-05-30T07:04:13.344Z

## Content
```markdown
# รายงานประจำสัปดาห์ — 25–30 พฤษภาคม 2569

---

## 📋 สถานะโดยรวม

| โครงการ | สถานะ | ความคืบหน้า | ปัญหา/ตัวบล็อก |
|---|---|---|---|
| MRP (Infor Food Packaging) | 🔴 ติดบล็อก | กำหนดลำดับนำเข้า K0→K1→K2→K7 แล้ว | ERP Syteline Infor — ยัง generate MRP Planning ไม่ได้ (data integration ยังไม่ถูกต้อง) |
| Returnable Box 🎨 | 🟡 กำลังดำเนินการ | สำรวจการค้นหาตามขนาดผ่าน BOXSOFT | — |
| Move Apps (Project) | 🟢 ตามแผน | ย้ายเซิร์ฟเวอร์จาก TPN ไป TPK — เก็บข้อมูล project ทั้งสองฝั่งแล้ว | — |

---

## 📋 สรุปภาพรวม

📌 *เสาร์ 24 พฤษภาคม – ศุกร์ 30 พฤษภาคม 2569* — MRP เฟส 3 ติดบล็อก: ERP Syteline Infor ยังไม่สามารถ generate MRP Planning ได้ คาดว่าสาเหตุมาจาก data integration ยังไม่ถูกต้อง เลื่อนทั้งหมดไปสัปดาห์หน้า งานเฟส 1 และ 2 ยังดำเนินต่อไป Returnable Box กำลังพัฒนาเรื่อง criteria search ผ่าน BOXSOFT; ระบบแจ้งเตือนและการอัปเดตคู่มือยังรอดำเนินการ Move Apps อยู่ระหว่าง scope งาน — จัดทำ project list ทั้ง TPN และ TPK พร้อมรายละเอียด DB/server/connection string

📌 *ศุกร์ 22 พฤษภาคม — Box Support* — ผู้ใช้แจ้งว่าไม่สามารถย้าย location ได้ ระบบระบุว่าจำนวนที่ต้องการโอนเกินกว่าสต็อกที่มี (89 กล่อง) แนะนำให้ใช้โปรแกรม Adjustment ก่อน: Inventory → Transaction → Adjustment เพื่อปรับยอดให้ตรงกัน แล้วค่อยลองย้าย location อีกครั้ง

---

## 🚀 สัปดาห์นี้ (24–30 พ.ค. 2569)

- ✅ [MRP] เฟส 1: เช็คอินประจำวัน 14:00 น. — Planning + IT ทำงานร่วมกันต่อเนื่อง
- ✅ [MRP] เฟส 1: ยืนยันกระบวนการนำเข้าด้วย Excel template และใช้งานจริง
- ✅ [MRP] เฟส 2: ทดสอบแบบขนาน (Print → Laminate → Bag) อยู่ระหว่างดำเนินการ
- ✅ [MRP] เฟส 3: กำหนดลำดับนำเข้ามาตรฐาน — K0 → K1 → K2 → K7
- ✅ [MRP] เฟส 3: กำหนด validation checklist (จำนวนแถว, nulls, spot-check ใน UI)
- ❌ [MRP] เฟส 3: รัน MRP Planning — ติดบล็อก ERP Syteline Infor ไม่สามารถ generate ได้
- ✅ [Box] สำรวจ BOXSOFT dimension criteria integration
- ✅ [Box] Build ฟอร์มดึงข้อมูล Adjustment
- ✅ [Move Apps] Scope งาน — ย้ายเซิร์ฟเวอร์ TPN→TPK, เก็บรายการแอปครบ (TPK: 3, TPN: 9)
- 🔎 รอดำเนินการ: เลือกวิธีนำเข้ามาตรฐาน (A/B/C), ชื่อ SQL table ของแต่ละกลุ่ม, ยืนยัน K7, แก้ไข data integration

---

## 🖥 Move Apps — Project List (TPN)

_รายละเอียดแต่ละโปรเจกต์: database server, SQL instance, connection credentials, และ config file locations_

| Program | Status | Writer | SQL Instance | Database | User | Remark |
|---|---|---|---|---|---|---|
| Outsource | Tracking | Phutorn | 192.168.10.19\\SQLEXPRESS02 | TPNprinting | sa | IP: 192.168.6.189 @Supp0rt@IT |
| OutsourceMobile | Tracking | Phutorn | — | — | — | config: \\\\192.168.10.2\\ShareCenter\\Program\\Outsource\\config.json |
| StockTPN | Tracking | Phutorn | 192.168.10.19\\SQLEXPRESS02 | InventoryRMTPK | storerm | config: \\\\192.168.95.200\\Store\\StoreRM\\config.json |
| StoreTPN | Tracking | Phutorn | — | InventoryTPK | — | เหมือน StockTPN |

*Skip / เลิกใช้แล้ว:* eBox (new), Joborder, QR-Code, Sampo, UnMergeExcel, กล่องหมุนเวียน

---

## 🖥 Move Apps — Project List (TPK)

_รายละเอียดแต่ละโปรเจกต์: database server, SQL instance, connection credentials, และ config file locations_

| Program | Status | Writer | Server/IP | Database | User | Remark |
|---|---|---|---|---|---|---|
| AI | Tracking | Manoon | eset.tpk.thsg (192.168.57.38) MySQL | QC_Hand | root | AI QC/ASM — ข้อมูลการผลิต |
| Parameter Viewer | Tracking | Manoon | PDDB.tpk.thsg (192.168.10.17) MySQL | Target_speed_DB | root | ใช้ TPN host |
| QC_HandSET | Tracking | Manoon | PDDB.tpk.thsg\\SQLEXPRESS | QC_Hand | sa | แผนก assembly/glue |

---

## 🥅 สัปดาห์หน้า

- [ ] [MRP] แก้ไข data integration ให้ ERP Syteline Infor generate MRP Planning ได้
- [ ] [MRP] รัน MRP Planning หลัง data integration ถูกต้อง (~2–3 ชม.)
- [ ] [MRP] ยืนยันกลุ่ม K7 กับผู้จัดการ
- [ ] [MRP] ตัดสินใจและบันทึกวิธีการนำเข้ามาตรฐาน (A / B / C)
- [ ] [MRP] บันทึก target SQL table/schema names ของแต่ละกลุ่ม (K0/K1/K2/K7)
- [ ] [MRP] เฟส 2 — มอบหมายผู้ดูแลเครื่อง
- [ ] [MRP] เฟส 2 — บังคับใช้ database + จัดเก็บ BOM & lead time
- [ ] [Box] พัฒนา criteria search — ค้นหาตามขนาด (กว้าง×สูง×ยาว) ผ่าน BOXSOFT
- [ ] [Box] ต่อระบบแจ้งเตือน: Production → Delivery Order → Stock FG alert
- [ ] [Box] 📖 อัปเดต User Manual & Developer Guide
- [ ] [Move Apps] เริ่มงานกับพี่มานูน — เริ่มย้ายเซิร์ฟเวอร์
- [ ] [Move Apps] ยืนยัน IP: 192.168.10.25
- [ ] [Move Apps] ย้าย DB server: ปัจจุบัน 192.168.10.17 → เป้าหมาย 192.168.95.100

---

## 🔥 โน้ตถึงตัวเอง

- 🚨 MRP เฟส 3 ติดบล็อก — ERP Syteline Infor generate MRP Planning ไม่ได้; data integration น่าจะยังไม่ถูกต้อง ต้องแก้เป็นอันดับแรกสัปดาห์หน้า
- เฟส 2 ต้องการคนดูแลเครื่องโดยเฉพาะ — รัน 7 วัน + ปรับสมดุล 2 วัน
- เฟส 3 ต้องเลือกวิธีนำเข้ามาตรฐานก่อนรัน production
- K7: ถามผู้จัดการเพื่อยืนยันประเภทกลุ่มสินค้า
- Box notification feature เลยกำหนด (15 พ.ค.) — ต้องเร่ง
- Box dimension search: รอไฟล์จากลูกค้า → ใช้ BOXSOFT ถ้ามี
- Box location transfer (22 พ.ค.): 89 กล่องในสต็อก, จำนวนโอนเกินสต็อก → ใช้ Adjustment (Inventory → Transaction → Adjustment) ก่อน
- Move Apps: deadline 1 เดือน (หรืออย่างน้อย 2 สัปดาห์)
- Move Apps: BOXSOFT instance = TPK-REGULUS, DB = csgwin-tpkp

---

_สร้างโดย Smith | ข้อมูลจาก Notion + Todoist_
_30 พฤษภาคม 2569_
```

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->
