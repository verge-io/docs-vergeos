---
title: "IPMI"
description: "How to configure and use IPMI integration in VergeOS for remote server power control, connectivity testing, credential management, and accessing the IPMI web interface."
semantic_keywords:
  - "VergeOS IPMI remote management configuration"
  - "IPMI connectivity test status credentials"
  - "remote server power control power cycle"
  - "IPMI web interface access node"
  - "baseboard management controller BMC"
use_cases:
  - test_ipmi_connectivity
  - change_ipmi_credentials
  - access_ipmi_web_interface
  - remote_power_control_node
tags:
  - ipmi
  - remote-management
  - nodes
  - hardware
  - power-control
  - bmc
categories:
  - System Administration
---

# IPMI

IPMI is a universal standard, supported by almost all hardware, for managing and accessing servers. It is accessible even when a server is powered off and allows for remotely controlling servers and monitoring hardware status, including things such as temperature, power consumption, voltage, hardware errors, etc. VergeOS integrates with IPMI to provide for remote server power control (power on, power cycle, etc.) and convenient access via the VergeOS user interface.

{% hint style="info" %}
Because IPMI deals with physical hardware, it only applies to host level nodes (not tenant nodes).
{% endhint %}

## Test IPMI Connectivity

1. Navigate to **Infrastructure** > **Nodes** from the top menu.
2. **Double-click the desired node** to access the node dashboard.
3. Under the **IPMI** submenu, click **Test** on the left menu.

### IPMI Connection Status

The node dashboard will indicate IPMI ***status*** and ***date/time of last time connected***:

- **IPMI Status** - "OK" indicates that the last attempt to connect was successful. If the last attempt was unsuccessful, an error message is displayed.

- **IPMI Last Connected** - displays the last date/time the VergeOS system successfully connected to IPMI. (If there was never a successful IPMI connection, the field will report "NA".)

## Change Stored IPMI login credentials

{% hint style="success" %}
The following instructions provide for changing the IPMI credentials a node will use to interface with IPMI. Changing these fields does not perform IPMI user administration; connect to your IPMI web interface to add or change IPMI users.
{% endhint %}

1. From the Node Dashboard, click **Edit** on the from the left menu.
2. Enter a valid ***IPMI User***. (IPMI user should have administrator-level privileges.)
3. Enter ***IPMI Password***.
4. Click **Submit** to save the changes to the node.

## Access the IPMI Web Interface

{% hint style="info" %}
Successfully connecting to the IPMI web interface through the VergeOS user interface requires valid IPMI username/password is stored and appropriate networking configuration is in place for the system to interact with the node's IPMI.
{% endhint %}

1. Navigate to **Infrastructure** > **Nodes** from the top menu.
2. **Double-click the desired node** to access the node dashboard.
3. Under the **IPMI** submenu on the left menu, click **Connect**.
4. A new browser tab is opened to the IPMI web interface login page.

## Manage IPMI Credentials via the REST API

IPMI credentials can also be read and updated through the VergeOS REST API. This is useful for managing credentials across many nodes or from automation scripts.

### Find the Node Key

API calls that target a node use the node's row key (`$key`). List the nodes to find the key:

```http
GET /api/v4/nodes
```

To locate a specific node by name:

```http
GET /api/v4/nodes?filter=name eq 'node1'
```

The response includes the `$key` value along with fields such as `name`, `ipmi_address`, and `ipmi_status`.

### Read IPMI Information

Retrieve a single node record:

```http
GET /api/v4/nodes/{key}
```

IPMI-related fields in the response:

| Field | Description |
|-------|-------------|
| `ipmi_address` | The BMC IP address or hostname. |
| `ipmi_user` | The BMC username. |
| `ipmi_password` | Write-only; not included in read responses. |
| `ipmi_status` | The connection status: `ready`, `connecting`, `offline`, or `error`. |
| `ipmi_sel_free` / `ipmi_sel_used` | System Event Log capacity counters. |

### Set IPMI Credentials

Update the stored credentials with a `PUT` request:

```http
PUT /api/v4/nodes/{key}
```

```json
{
  "ipmi_user": "admin",
  "ipmi_password": "newpassword"
}
```

Saving credentials automatically runs a connectivity test; a separate test action is not required. If the test cannot run — for example, the node has no IPMI address — the API returns an error and the update is not saved. To verify the update, read the node record again and confirm `ipmi_status` is `ready`.

### Trigger IPMI Actions

To run a connectivity test or clear the System Event Log without changing credentials, post a node action:

```http
POST /api/v4/node_actions
```

```json
{
  "$row": "/v4/nodes/{key}",
  "action": "ipmi_test"
}
```

The available IPMI actions are `ipmi_test` and `clear_sel`.

{% hint style="info" %}
IPMI applies to host-level nodes only, and `ipmi_password` cannot be read back through the API.
{% endhint %}
