---
title: "Release notes"
description: "Overview of all VergeOS release versions, version numbering conventions, update process guidance, and links to detailed release notes for each version."
semantic_keywords:
  - "VergeOS release notes overview all versions"
  - "VergeOS version history and update path"
  - "VergeOS semantic versioning and version numbering"
  - "VergeOS end of life and supported versions"
use_cases:
  - check_current_supported_versions
  - plan_upgrade_path
  - understand_version_numbering
  - find_release_notes_by_version
tags:
  - release-notes
  - versioning
  - updates
  - upgrade-path
  - end-of-life
  - supported-versions
categories:
  - Release Notes
---

# Release notes

Release notes for every version of VergeOS. Select a version in the table below to see its detailed notes.

{% hint style="info" %}
**Recommendations**

- Stay on the latest patch/hotfix within your current minor release, and update to the latest minor release when you can
- For access to the latest features and functionality documented here, please ensure you are running the latest version of VergeOS
{% endhint %}

## Release Version Overview

| Release | Initial Release | Latest Version | Status | End-of-Life |
|--------|----------------|----------------|---------|-------------|
| [26.1](2026/26-1-release-notes.md) | January 2026 | 26.1.7 (July 2026) | Latest | TBD |
| [26.0](2026/26-0-release-notes.md) | October 2025 | 26.0.2.2 (December 2025) | Supported | TBD |
| [4.13](2025/4-13-release-notes.md) | November 2024 | 4.13.4.2 (August 2025) | Supported | TBD |
| [4.12](2025/4-12-release-notes.md) | February 2024 | 4.12.6 (July 2024) | Deprecated | January 2026 |
| [4.11](2025/4-11-release-notes.md) | February 2023 | 4.11.4.3 (January 2024) | Deprecated | December 2024 |
| [4.10](2025/4-10-release-notes.md) | June 2022 | 4.10.3.1 (January 2023) | Deprecated | June 2024 |
| [4.9](2025/4-9-release-notes.md) | October 2021 | 4.9.2 (February 2022) | Deprecated | February 2023 |

## Version Numbering and Updates

VergeOS uses semantic versioning with two different formats:

- **Legacy Format**: Major.Minor.Patch.Hotfix (e.g., 4.13.4.2)
- **New Format** (26.0+): Year.Quarter.Minor.Patch (e.g., 26.0.1)
    - First two digits represent the year (25 = 2025, 26 = 2026)
    - Third digit represents the quarter development started (0-3)
    - Remaining digits represent minor and patch versions

{% hint style="success" %}
**Update Process**

- **Minor**, **Patch**, and **Hotfix** updates support live system updates with no impact to running workloads
- **Major** version updates *may* require a system reboot to complete the update process
- Updates should always be performed sequentially within a major version (e.g., 4.13.2 → 4.13.3 → 4.13.4)
- When upgrading from 4.13.x to 26.0.x, follow the upgrade path through 4.13.4.2 first
{% endhint %}

{% hint style="info" %}
**Version Archive**

Release notes for versions prior to 4.9 have been archived and are not available in this documentation
{% endhint %}
