# Core Network MTU Basics

## Overview

The **Core (virtual fabric) network** carries vSAN traffic and node‑to‑node communication. VergeOS automatically creates this network during installation and attempts to use a **9000‑byte MTU** to support jumbo frames for all guest‑to‑guest and inter‑system traffic.

A 9000‑byte MTU can only be used when the underlying physical networks support it *plus required overhead*. If the physical MTU is too small, VergeOS automatically lowers the Core MTU.

---

## Physical Network MTU

During installation, you specify MTU values for the physical networks that back the Core network.

* Enter the **maximum MTU your physical hardware supports**.
* Every component in the path (NICs, switches, ports) must support this value.
* The installer default is **9192**, which is sufficient for a Core MTU of 9000.

To support a **9000‑byte Core MTU**, the physical network must support **at least 9050 bytes**.

---

## MTU Overhead by Layer

Each layer of tenancy adds encapsulation overhead. VergeOS will target a 9000‑byte MTU for each tenant’s Core network, but will automatically reduce it if the physical MTU cannot support the required headroom.

| Layer | Cumulative Overhead | Minimum Physical MTU for 9000 Guest MTU | 
| --- | --- | --- | 
| Core fabric network | 50 bytes | 9050 | 
| Tenant — level 1 | 100 bytes | 9100 | 
| Tenant — level 2 | 150 bytes | 9150 | 
| Tenant — level 3 | 200 bytes | 9200 | 
A physical MTU of **9216**—common on many NICs and switches—supports three tenant layers with room to spare.

---

## Key Takeaways

* VergeOS targets **9000 MTU** for Core and tenant networks.
* Physical MTU must include **9000 bytes + overhead**.
* Higher physical MTU values allow deeper tenant nesting without MTU reduction.
* If physical MTU is too low, VergeOS automatically adjusts Core and tenant MTUs downward.
