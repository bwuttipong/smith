# รายงานประจำสัปดาห์ (1–6 มิถุนายน 2026)

📋 **สถานะโดยรวม**

| โครงการ | สถานะ | อัปเดตสำคัญ | อุปสรรค |
|---------|-------|-------------|---------|
| MRP (Infor Food Pkg) | 🟢 ตามแผน | MRP ปลดล็อคแล้ว — เคลียร์ปัญหาและ MRP Planning สามารถ generate ได้แล้ว | - |
| Returnable Box 🎨 | 🟡 กำลังดำเนินการ | กำหนดเกณฑ์ dimension ของ BOXSOFT แล้ว | — |
| Move Apps (Project) | 🟢 ตามแผน | ย้าย 3 โปรแกรมแล้ว (AI, Parameter Viewer, QC_HandSET) | — |
| TPK QA Hold | 🆕 ใหม่ | — | — |
| Store Ink | 🆕 ใหม่ | ประเภทธุรกรรม scrap/disposal | — |

## 📋 สรุปผู้บริหาร

📌 **จันทร์ 1 พ.ค. - ศุกร์ 5 มิ.ย.** — ความคืบหน้า Move Apps: ย้าย 3 โปรแกรมจาก TPN ไป TPK สำเร็จ (AI, Parameter Viewer, QC_HandSET — ทั้งหมดเป็นแอปของพี่มงคล) 🎉 MRP ปลดล็อคแล้ว! ปัญหา low level code error บน K1000006 เป็นปัญหา data integration — เคลียร์แล้วและ MRP Planning สามารถ generate ได้แล้ว

## 🚀 สัปดาห์นี้ *(25–30 พฤษภาคม 2026)*

1. ✅ [Box] Adjustment Stock — ผู้ใช้สามารถปรับปริมาณใน Stock FG ได้แล้ว
2. ✅ [Move Apps] กำหนดขอบเขตโครงการ — ย้าย server จาก TPN → TPK, จัดหมวดหมู่แอป (3 แอป)
3. ✅ [MRP] แก้ปัญหา Data integration + รัน MRP Planning

🔎 [Box] รอดำเนินการ: เจาะลึกเกณฑ์ Dimension (การแมป client ของ BOXSOFT)

## 🆕 กำหนดขอบเขตโครงการใหม่

1. [ShopFloor] TPK QA Hold — สร้างต่อจากโครงการเดิมสำหรับไซต์ TPK
2. [StoreInk] Scrap — ประเภทธุรกรรม disposal/destruction + ส่งออก Excel

---

🖥 *Move Apps — รายการโครงการ* *แต่ละโครงการใช้: database server, SQL instance, connection credentials และตำแหน่งไฟล์ config*

| โปรแกรม | สถานะ | ผู้เขียน | SQL Instance | Database | User | หมายเหตุ |
|---------|-------|----------|--------------|----------|------|----------|
| Outsource | Tracking | ภูธร | 192.168.10.19\SQLEXPRESS02 | TPNprinting | sa | IP Address ของภูธร `192.168.6.189` |
| OutsourceMobile | Tracking | ภูธร | — | — | — | `\\192.168.10.2\ShareCenter\Program\Outsource\config.json` |
| StockTPN | Tracking | ภูธร | 192.168.10.19\SQLEXPRESS02 | InventoryRMTPK | storerm | `\\192.168.95.200\Store\StoreRM\config.json` |
| StoreTPN | Tracking | ภูธร | — | InventoryTPK | — | เหมือนกับ StockTPN |
| AI | เสร็จแล้ว | มงคล | eset.tpk.thsg (192.168.57.38) MySQL | QC_Hand | root | AI QC/ASM — ข้อมูล prod |
| Parameter Viewer | เสร็จแล้ว | มงคล | PDDB.tpk.thsg (192.168.10.17) MySQL | Target_speed_DB | root | TPN host |
| QC_HandSET | เสร็จแล้ว | มงคล | PDDB.tpk.thsg\SQLEXPRESS | QC_Hand | sa | Assembly/Glue |

## 🥅 สัปดาห์หน้า

1. [MRP] เข้าสู่เฟสถัดไป
2. [Move Apps] ย้ายแอปถัดไป
3. [Box] เชื่อมต่อ notification flow: **Production → Delivery Order → Stock FG** alert
4. [Box] ค้นหากล่องตาม dimension
5. [Box] 📖 อัปเดตคู่มือผู้ใช้และคู่มือนักพัฒนา

## 🔥 บันทึกถึงตัวเอง

1. Move Apps: เสร็จ 3/7 เหลือ: Outsource, OutsourceMobile, StockTPN, StoreTPN (ทั้งหมดเป็นแอปของพี่ภูธร)
2. Move Apps: กำหนดเวลา 1 เดือน (หรืออย่างน้อย 2 สัปดาห์) ไฟล์ที่แชร์: TPNDBAPP21 (192.168.10.2) → Share Center → Program (TPN) และ \192.168.57.39\software\F_PROJECT (TPK)
3. Move Apps: BOXSOFT instance = TPK-REGULUS, DB = csgwin-tpk
4. Box: ค้นหา Dimension: รอไฟล์ลูกค้า → ใช้ BOXSOFT ถ้ามี

---

*อัปเดตโดย Wuttipong เมื่อ 2026-05-30*
