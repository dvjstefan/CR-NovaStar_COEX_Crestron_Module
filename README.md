# NovaStar MX (COEX) – SIMPL+ Module

### Version 2.17  
**Author:** SAOA Consulting 
**Module Type:** SIMPL+ / SIMPL# Library  
**Target Platform:** Crestron 4-Series Processor  

---

## 🧩 Introduction

The **NovaStar MX30 SIMPL+ Module** provides direct TCP/IP control of NovaStar LED controllers.  
It allows Crestron systems to manage display modes, brightness, picture mute states, and recall presets seamlessly.  
The module is built for reliable real-time interaction with NovaStar controllers, using their standard API over port **8001**.

Typical use cases include:
- Controlling LED walls or large-format displays in conference rooms and auditoriums.
- Recalling preconfigured display presets (layouts, brightness levels, color settings).
- Monitoring current display mode and active preset status.

---

## ⚙️ System Requirements

- **Processor:** Crestron 4-Series (e.g. CP4, CP4N, MC4, etc.)  
- **Firmware:** v2.0 or newer  
- **SIMPL Windows:** 4.17.00 or later  
- **Network Access:** TCP Port **8001** open between processor and NovaStar MX30  

> ⚠️ Note: This module is designed specifically for 4-Series processors and **does not support 3-Series**.

---

## 🔌 Inputs / Outputs

Below is a full list of signal definitions available in this SIMPL+ module.

### **TCP Settings**
| Signal | Type | Description |
|--------|------|-------------|
| `Controller_IP$` | String | IP address of the NovaStar MX30 controller |
| `Controller_Port` | Analog | TCP port for API connection (default **8001**) |

---

### **Control Commands**
| Signal | Type | Description |
|--------|------|-------------|
| `Get_Display_Mode` | Digital | Request current display mode |
| `Picture_Mute` | Digital | Mute the picture output |
| `Picture_UnMute` | Digital | Unmute the picture output |
| `Get_Presets` | Digital | Fetch list of presets from controller (max 10) |
| `Set_Brightness` | Analog | Set brightness level (0–100%) |
| `Set_Preset` | Analog | Recall preset number (1–10) |

---

### **Feedback Signals**
| Signal | Type | Description |
|--------|------|-------------|
| `DisplayMode_FB$` | String | Current display mode status |
| `Brightness_FB` | Analog | Current brightness feedback value (0–100%) |
| `PresetActive` | Analog | Currently active preset number |
| `PresetName$[1–10]` | String | Name of preset 1–10 as reported by the controller |

---

## 💡 Example Use

Example workflow in SIMPL:
1. Set the **Controller_IP** and **Controller_Port** (usually 8001).  
2. Pulse **Get_Presets** → the module fetches and fills all preset names.  
3. Use **Set_Preset (Analog)** to recall a specific preset number (e.g. 3).  
4. Monitor **PresetActive** and **PresetName$X** for feedback.  
5. Use **Set_Brightness (Analog)** to adjust LED wall brightness dynamically.  

---

## 🧠 Notes

- Connection is established over standard TCP/IP (no authentication).  
- If feedback is missing, verify IP routing and port settings on both devices.  
- Maximum of **10 presets** are currently supported in this release.  

---

## 🧾 Revision History

| Version | Date | Changes |
|----------|------|----------|
| 2.17 | 2025-11-04 | Initial public release |

---

## 📧 Support

For questions, integration help, or custom Crestron development:  
**SAOA Consulting**  
🌐 [https://saoa.se](https://saoa.se)  
📧 info@saoa.se

---
