# NovaStar MX (COEX) - SIMPL+ Module

### Release 2.20.1
**Author:** SAOA Consulting  
**Module Type:** SIMPL+ / SIMPL# Library  
**Target Platform:** Crestron 4-Series Processor

---

## Introduction

The **NovaStar MX30 SIMPL+ Module** provides direct TCP/IP control of NovaStar LED controllers over the standard API on port **8001**.

Typical use cases include:
- recalling presets
- setting brightness
- switching display mode
- monitoring active preset and display state feedback

---

## System Requirements

- **Processor:** Crestron 4-Series
- **Firmware:** v2.0 or newer
- **SIMPL Windows:** 4.17.00 or later
- **Network Access:** TCP port **8001** open between the Crestron processor and the NovaStar controller

This module is intended for 4-Series processors and is not designed for 3-Series.

---

## Inputs / Outputs

### TCP Settings
| Signal | Type | Description |
|--------|------|-------------|
| `Controller_IP$` | String | IP address of the NovaStar controller |
| `Controller_Port` | Analog | TCP port for API communication, default `8001` |

### Control Commands
| Signal | Type | Description |
|--------|------|-------------|
| `Get_Display_Mode` | Digital | Request current display mode |
| `Picture_Mute` | Digital | Mute the picture output |
| `Picture_UnMute` | Digital | Unmute the picture output |
| `Get_Presets` | Digital | Fetch preset names from the controller |
| `Set_Brightness` | Analog | Set brightness from `0` to `100` |
| `Set_Preset` | Analog | Recall preset number `1` to `10` |

### Feedback Signals
| Signal | Type | Description |
|--------|------|-------------|
| `DisplayMode_FB$` | String | Current display mode status |
| `Brightness_FB` | Analog | Current brightness feedback value |
| `PresetActive` | Analog | Currently active preset number |
| `PresetName$[1-10]` | String | Preset names returned by the controller |

---

## Release Notes

Release `2.20.1` is a packaging cleanup patch for the existing `2.20` module line.

Changes in this release:
- removed unused SIMPL# references from the build
- excluded XML documentation files from the packaged output
- reduced the compiled `.clz` size from about `3.8 MB` to about `1.4 MB`

There are no C# runtime logic changes in this patch release.

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 2.20.1 | 2026-04-03 | Packaging cleanup release. Reduced `.clz` size by removing unused dependencies and XML docs. No runtime logic changes. |
| 2.20 | 2026-01-08 | Stability update for MX30 state handling, heartbeat monitoring, and recovery behavior. |
| 2.1 | 2025-11-04 | Initial public release. |

---

## Support

For integration help or custom Crestron development:

**SAOA Consulting**  
[https://saoa.se](https://saoa.se)  
info@saoa.se
