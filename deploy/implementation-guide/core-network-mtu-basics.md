# Core Network MTU Basics

## Overview

{% hint style="info" %}
**Key Points**

- * VergeOS targets **9000 MTU** for core and tenant core networks.
- * Physical MTU must provide for overhead 
-  Higher physical MTU values allow deeper tenant nesting without MTU reduction.
- If physical MTU is too low, VergeOS automatically adjusts Core and tenant MTUs downward.

{% endhint %}

**Core (virtual) network**

In a VergeOS system, the **'Core'** network carries vSAN traffic and node‑to‑node communication. VergeOS automatically creates this virtual network during installation, targeting  a **9000‑byte MTU** to support jumbo frames for guest‑to‑guest and intrasystem traffic.

A 9000‑byte MTU can only be used when the underlying physical networks support it *plus required overhead*. If the physical MTU is too small, the VergeOS installer automatically lowers the Core network MTU. 


## Physical Network MTU 

Multiple physical networks serve as the foundation for the 'Core' network, operating concurrently and providing redundancy.  During installation, you define MTU values for the physical networks that back the Core network.

* Enter the **maximum MTU to allow**.
* Every component in the path (NICs, switches, ports) must support this value.
* The installer default is **9192**, which is sufficient for the host core network and multiple layers of tenancy at a 9000-byte MTU, plus additional headroom.

---

## MTU Overhead by Layer

Each layer of tenancy adds encapsulation overhead. VergeOS will target a 9000‑byte MTU at the top-level Core network and each tenant layer, but will automatically reduce it if the physical MTU cannot support the required headroom.

**Physical Core network set at default 9192**
| Layer | cumulative overhead|  MTU
| --- | --- | --- | 
| Host core | 50 | 9000
| Tenant — level 1 | 100 | 9000
| Tenant — level 2 | 150 | 9000
| Tenant — level 3 | 200 | 8992

Starting with the default physical core MTU 9192 (set during installation) allows the host and 2 tenant layers to operate with a full 9000-byte MTU. 

---



