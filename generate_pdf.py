from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak, KeepTogether)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
import os

OUTPUT = "/home/user/CR-NovaStar_COEX_Crestron_Module/NovaStar_MX_UserManual.pdf"

# ── Color palette ─────────────────────────────────────────────────────────────
NAVY    = colors.HexColor("#0D1B2A")
BLUE    = colors.HexColor("#00A8FF")
DKBLUE  = colors.HexColor("#063055")
LGRAY   = colors.HexColor("#CCDDEE")
MGRAY   = colors.HexColor("#88AACC")
WHITE   = colors.white
BLACK   = colors.black

W, H = A4  # 595 x 842 pt

# ── Page decorators ──────────────────────────────────────────────────────────
def cover_page(c, doc):
    c.saveState()
    # full-bleed background
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # accent stripe
    c.setFillColor(BLUE)
    c.rect(0, H*0.62, W, 4, fill=1, stroke=0)
    c.rect(0, H*0.38, W, 4, fill=1, stroke=0)
    # dark band
    c.setFillColor(DKBLUE)
    c.rect(0, H*0.38+4, W, H*0.62 - H*0.38 - 4, fill=1, stroke=0)
    # title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 36)
    c.drawString(2*cm, H*0.66, "NovaStar MX (COEX)")
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(BLUE)
    c.drawString(2*cm, H*0.60, "SIMPL+ Control Module")
    c.setFont("Helvetica", 16)
    c.setFillColor(LGRAY)
    c.drawString(2*cm, H*0.55, "User Manual & Integration Guide")
    # meta
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(WHITE)
    c.drawString(2*cm, H*0.46, "Release 2.20.1")
    c.setFont("Helvetica", 11)
    c.setFillColor(MGRAY)
    c.drawString(2*cm, H*0.42, "Crestron 4-Series  •  NovaStar COEX TCP/IP API")
    # footer
    c.setFont("Helvetica", 9)
    c.setFillColor(MGRAY)
    c.drawString(2*cm, 1.5*cm, "SAOA Consulting  •  info@saoa.se  •  https://saoa.se")
    c.restoreState()

def normal_page(c, doc):
    c.saveState()
    # header bar
    c.setFillColor(NAVY)
    c.rect(0, H-1.2*cm, W, 1.2*cm, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(0, H-1.2*cm, W, 2, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(2*cm, H-0.85*cm, "NovaStar MX (COEX) — SIMPL+ Module")
    c.setFont("Helvetica", 9)
    c.setFillColor(LGRAY)
    c.drawRightString(W-2*cm, H-0.85*cm, "User Manual  |  Release 2.20.1")
    # footer line
    c.setStrokeColor(BLUE)
    c.setLineWidth(1)
    c.line(2*cm, 1.5*cm, W-2*cm, 1.5*cm)
    c.setFillColor(MGRAY)
    c.setFont("Helvetica", 8)
    c.drawString(2*cm, 0.8*cm, "SAOA Consulting  •  info@saoa.se")
    c.drawRightString(W-2*cm, 0.8*cm, f"Page {doc.page}")
    c.restoreState()

# ── Styles ────────────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()
    s = {}
    s["h1"] = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=20,
                              textColor=BLUE, spaceAfter=6, spaceBefore=18)
    s["h2"] = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=14,
                              textColor=NAVY, spaceAfter=4, spaceBefore=12)
    s["body"] = ParagraphStyle("body", fontName="Helvetica", fontSize=10,
                                leading=15, spaceAfter=6, textColor=BLACK)
    s["note"] = ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=9,
                                leading=13, spaceAfter=6, textColor=MGRAY)
    s["code"] = ParagraphStyle("code", fontName="Courier", fontSize=9,
                                leading=13, spaceAfter=4, backColor=colors.HexColor("#EEF4FA"),
                                leftIndent=12, rightIndent=12,
                                borderPad=4)
    s["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=10,
                                  leading=15, leftIndent=14, bulletIndent=4,
                                  spaceAfter=3, textColor=BLACK)
    s["toc_h"] = ParagraphStyle("toc_h", fontName="Helvetica-Bold", fontSize=11,
                                 textColor=NAVY, spaceAfter=2)
    s["toc_e"] = ParagraphStyle("toc_e", fontName="Helvetica", fontSize=10,
                                 textColor=BLACK, leftIndent=10, spaceAfter=1)
    return s

ST = make_styles()

def H1(t): return Paragraph(t, ST["h1"])
def H2(t): return Paragraph(t, ST["h2"])
def P(t):  return Paragraph(t, ST["body"])
def Note(t): return Paragraph(f"<i>{t}</i>", ST["note"])
def Code(t): return Paragraph(t, ST["code"])
def Bullet(t): return Paragraph(f"• {t}", ST["bullet"])
def SP(n=6): return Spacer(1, n)
def HR(): return HRFlowable(width="100%", thickness=1, color=LGRAY, spaceAfter=8, spaceBefore=4)

def section_header(title, subtitle=None):
    items = [SP(4), H1(title)]
    if subtitle:
        items.append(P(f"<font color='#88AACC'>{subtitle}</font>"))
    items.append(HR())
    return items

TABLE_STYLE = TableStyle([
    ("BACKGROUND",  (0, 0), (-1, 0),  DKBLUE),
    ("TEXTCOLOR",   (0, 0), (-1, 0),  WHITE),
    ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
    ("FONTSIZE",    (0, 0), (-1, 0),  10),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#EEF4FA"), WHITE]),
    ("FONTNAME",    (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE",    (0, 1), (-1, -1), 9),
    ("GRID",        (0, 0), (-1, -1), 0.5, LGRAY),
    ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING",  (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING",(0,0), (-1,-1),  5),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
])

def styled_table(data, col_widths):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TABLE_STYLE)
    return t

# ── Build content ─────────────────────────────────────────────────────────────
story = []

# --- Cover placeholder (rendered by cover_page template) --------------------
story.append(PageBreak())

# ─── Table of Contents ──────────────────────────────────────────────────────
story += section_header("Table of Contents")
toc = [
    ("1.", "Introduction"),
    ("2.", "System Requirements"),
    ("3.", "Installation Guide"),
    ("4.", "Signal Reference"),
    ("5.", "Configuration & Usage"),
    ("6.", "Troubleshooting"),
    ("7.", "Release Notes"),
    ("8.", "Support & Contact"),
]
for num, title in toc:
    story.append(Paragraph(f"<b>{num}</b>  {title}", ST["toc_e"]))
    story.append(SP(2))
story.append(PageBreak())

# ─── 1. Introduction ─────────────────────────────────────────────────────────
story += section_header("1. Introduction",
    "NovaStar MX (COEX) SIMPL+ Module for Crestron 4-Series")

story.append(P(
    "The <b>NovaStar MX SIMPL+ Module</b> provides direct TCP/IP control of NovaStar LED "
    "processors (COEX platform, MX30 and compatible) from a Crestron 4-Series control system. "
    "Communication is handled over the standard NovaStar COEX API on <b>TCP port 8001</b>."
))
story.append(SP())
story.append(P("Typical use cases include:"))
for item in [
    "Recalling named presets stored on the NovaStar controller",
    "Adjusting LED wall brightness via an analog signal (0–100)",
    "Muting and unmuting the picture output",
    "Querying and displaying the current display mode",
    "Showing live preset names in a Crestron touch panel UI",
]:
    story.append(Bullet(item))
story.append(SP())
story.append(Note(
    "This module targets Crestron 4-Series processors only. It is not compatible with "
    "3-Series hardware."
))
story.append(PageBreak())

# ─── 2. System Requirements ──────────────────────────────────────────────────
story += section_header("2. System Requirements")

req_data = [
    ["Component", "Requirement"],
    ["Crestron Processor", "4-Series (CP4, MC4 or equivalent)"],
    ["Crestron Firmware",  "v2.0 or newer"],
    ["SIMPL Windows",      "Version 4.17.00 or later"],
    ["TCP Network Access", "Port 8001 open between processor and NovaStar unit"],
    ["NovaStar Hardware",  "MX30 controller (COEX platform)"],
    ["NovaStar Firmware",  "Compatible with the COEX TCP/IP API"],
]
story.append(styled_table(req_data, [6*cm, 10*cm]))
story.append(SP(12))
story.append(Note(
    "Ensure that any firewalls or VLAN ACLs between the Crestron processor and the "
    "NovaStar controller permit outbound TCP connections on port 8001."
))
story.append(PageBreak())

# ─── 3. Installation Guide ───────────────────────────────────────────────────
story += section_header("3. Installation Guide")

story.append(H2("3.1  Import the Module"))
steps = [
    ("Open your project in SIMPL Windows 4.17.00 or later."),
    ("Go to <b>File → Import</b> and select the <b>.usp</b> (SIMPL+) source file provided in the package."),
    ("Alternatively, place the pre-compiled <b>.clz</b> file in your project's module directory "
     "so SIMPL Windows picks it up automatically."),
    ("The module will appear in the Symbol Library under the imported modules category."),
]
for i, s in enumerate(steps, 1):
    story.append(Paragraph(f"<b>{i}.</b>  {s}", ST["bullet"]))
story.append(SP())

story.append(H2("3.2  Place the Symbol"))
story.append(P(
    "Drag the NovaStar MX symbol onto your SIMPL program sheet. Connect the required "
    "input and output signals as described in Section 4."
))
story.append(SP())

story.append(H2("3.3  TCP Client Configuration"))
story.append(P(
    "The module manages its own TCP client connection internally. "
    "You do <b>not</b> need to add a separate TCP/IP Client symbol. "
    "Simply drive the following signals at startup:"
))
story.append(Code("Controller_IP$  →  e.g. \"192.168.1.100\""))
story.append(Code("Controller_Port →  8001  (default — leave at 0 to use the built-in default)"))
story.append(SP())

story.append(H2("3.4  Compile & Upload"))
steps2 = [
    "Compile the SIMPL program (F5).",
    "Upload to the Crestron processor via Toolbox or SIMPL Windows.",
    "Verify the module connects by checking the <b>DisplayMode_FB$</b> signal — it should "
    "return a non-empty string within a few seconds of the processor booting.",
]
for i, s in enumerate(steps2, 1):
    story.append(Paragraph(f"<b>{i}.</b>  {s}", ST["bullet"]))
story.append(PageBreak())

# ─── 4. Signal Reference ─────────────────────────────────────────────────────
story += section_header("4. Signal Reference")

story.append(H2("4.1  TCP Settings"))
tcp_data = [
    ["Signal", "Type", "Description"],
    ["Controller_IP$",  "String", "IP address of the NovaStar controller"],
    ["Controller_Port", "Analog", "TCP port for API communication (default: 8001)"],
]
story.append(styled_table(tcp_data, [4.5*cm, 2.5*cm, 9*cm]))
story.append(SP(12))

story.append(H2("4.2  Control Inputs"))
ctrl_data = [
    ["Signal", "Type", "Description"],
    ["Get_Display_Mode",  "Digital", "Pulse HIGH to request the current display mode from the controller."],
    ["Picture_Mute",      "Digital", "Pulse HIGH to mute the LED wall output."],
    ["Picture_UnMute",    "Digital", "Pulse HIGH to unmute the LED wall output."],
    ["Get_Presets",       "Digital", "Pulse HIGH to fetch all preset names from the controller."],
    ["Set_Brightness",    "Analog",  "Drive 0–100 to set the LED wall brightness. Changes take effect immediately."],
    ["Set_Preset",        "Analog",  "Drive 1–10 to recall the corresponding preset on the controller."],
]
story.append(styled_table(ctrl_data, [4.5*cm, 2.5*cm, 9*cm]))
story.append(SP(12))

story.append(H2("4.3  Feedback Outputs"))
fb_data = [
    ["Signal", "Type", "Description"],
    ["DisplayMode_FB$",    "String", "Current display mode as a human-readable string."],
    ["Brightness_FB",      "Analog", "Live brightness value (0–100) reflected from the controller."],
    ["PresetActive",       "Analog", "The number (1–10) of the currently active preset."],
    ["PresetName$[1–10]",  "String", "Array of preset name strings returned by the controller (1-indexed)."],
]
story.append(styled_table(fb_data, [4.5*cm, 2.5*cm, 9*cm]))
story.append(PageBreak())

# ─── 5. Configuration & Usage ────────────────────────────────────────────────
story += section_header("5. Configuration & Usage")

story.append(H2("5.1  Initial Connection"))
story.append(P(
    "Set <b>Controller_IP$</b> to the NovaStar unit's IP address at system startup "
    "(e.g. from a string parameter or a persistent string signal). The module will "
    "establish the TCP connection automatically and begin heartbeat polling."
))
story.append(SP())

story.append(H2("5.2  Recalling Presets"))
story.append(P(
    "Drive the <b>Set_Preset</b> analog signal with a value of 1–10 to recall a preset. "
    "The <b>PresetActive</b> feedback will update to reflect the new active preset once "
    "the controller confirms the change."
))
story.append(SP())
story.append(Note(
    "Call <b>Get_Presets</b> at startup to populate the PresetName$[1–10] strings "
    "so your touch panel can display human-readable preset names."
))
story.append(SP())

story.append(H2("5.3  Brightness Control"))
story.append(P(
    "Connect a touch panel slider (0–100) or any analog source to <b>Set_Brightness</b>. "
    "The current value is reflected in <b>Brightness_FB</b> for UI feedback."
))
story.append(SP())

story.append(H2("5.4  Picture Mute"))
story.append(P(
    "Pulse <b>Picture_Mute</b> to blank the LED wall output. "
    "Pulse <b>Picture_UnMute</b> to restore it. "
    "These map directly to the corresponding COEX API commands."
))
story.append(SP())

story.append(H2("5.5  Automatic Reconnection"))
story.append(P(
    "The module includes a built-in heartbeat and recovery mechanism. "
    "If the TCP connection drops (e.g. due to a network interruption or controller reboot), "
    "the module will attempt to reconnect automatically — no intervention required."
))
story.append(PageBreak())

# ─── 6. Troubleshooting ──────────────────────────────────────────────────────
story += section_header("6. Troubleshooting")

issues = [
    (
        "No feedback received after boot",
        [
            "Verify the IP address in Controller_IP$ is correct.",
            "Confirm TCP port 8001 is reachable from the processor (use Toolbox TCP test).",
            "Check for firewall or VLAN rules blocking port 8001.",
            "Ensure the NovaStar MX30 controller is powered on and connected to the network.",
        ]
    ),
    (
        "PresetName$ strings are empty",
        [
            "Pulse Get_Presets to request the preset list from the controller.",
            "The controller must have presets configured before names are available.",
        ]
    ),
    (
        "Set_Preset has no effect",
        [
            "Ensure the value driven is in the range 1–10.",
            "Confirm the preset exists on the controller.",
            "Check that the TCP connection is established (DisplayMode_FB$ should be non-empty).",
        ]
    ),
    (
        "Module not found in SIMPL Windows",
        [
            "Verify the .usp or .clz file is in the correct module directory.",
            "Restart SIMPL Windows after placing the file.",
            "Check the SIMPL Windows version is 4.17.00 or later.",
        ]
    ),
]

for title, bullets in issues:
    story.append(KeepTogether([
        H2(title),
        *[Bullet(b) for b in bullets],
        SP(4),
    ]))
story.append(PageBreak())

# ─── 7. Release Notes ────────────────────────────────────────────────────────
story += section_header("7. Release Notes")

rel_data = [
    ["Version", "Date", "Changes"],
    ["2.20.1", "April 2026",
     "Packaging cleanup. Removed unused SIMPL# references and XML documentation files. "
     "Reduced compiled .clz size from ~3.8 MB to ~1.4 MB. No runtime logic changes."],
    ["2.20", "January 2026",
     "Stability update for MX30 state handling. Improved heartbeat monitoring and "
     "connection recovery behaviour under adverse network conditions."],
    ["2.1", "November 2025",
     "Initial public release of the NovaStar MX COEX SIMPL+ module."],
]
story.append(styled_table(rel_data, [2.2*cm, 3*cm, 10.8*cm]))
story.append(SP(12))
story.append(Note(
    "All releases within the 2.x line are backward-compatible. Upgrading from an earlier "
    "2.x version requires only replacing the module file and recompiling."
))
story.append(PageBreak())

# ─── 8. Support & Contact ────────────────────────────────────────────────────
story += section_header("8. Support & Contact")

story.append(P(
    "For integration assistance, custom Crestron development, or questions about this module, "
    "contact <b>SAOA Consulting</b>:"
))
story.append(SP())

contact_data = [
    ["", ""],
    ["Website",  "https://saoa.se"],
    ["Email",    "info@saoa.se"],
    ["Scope",    "Crestron integration, NovaStar LED control, AV system design"],
]
ct = Table(contact_data, colWidths=[3*cm, 13*cm])
ct.setStyle(TableStyle([
    ("FONTNAME",  (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTNAME",  (1, 0), (1, -1), "Helvetica"),
    ("FONTSIZE",  (0, 0), (-1,-1), 10),
    ("TEXTCOLOR", (1, 1), (1, 1),  BLUE),
    ("VALIGN",    (0, 0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",(0, 0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1),5),
]))
story.append(ct)
story.append(SP(20))
story.append(HR())
story.append(Note(
    "© 2026 SAOA Consulting. This document is provided for integration reference purposes. "
    "Specifications subject to change without notice."
))

# ── Assemble document ─────────────────────────────────────────────────────────
MARGIN = 2*cm

cover_frame  = Frame(0, 0, W, H, leftPadding=0, bottomPadding=0,
                     rightPadding=0, topPadding=0)
normal_frame = Frame(MARGIN, 2*cm, W-2*MARGIN, H-4*cm,
                     leftPadding=0, bottomPadding=0,
                     rightPadding=0, topPadding=0.5*cm)

doc = BaseDocTemplate(OUTPUT, pagesize=A4)
doc.addPageTemplates([
    PageTemplate(id="Cover",  frames=[cover_frame],  onPage=cover_page),
    PageTemplate(id="Normal", frames=[normal_frame], onPage=normal_page),
])

from reportlab.platypus import NextPageTemplate
story.insert(0, NextPageTemplate("Normal"))
story.insert(0, NextPageTemplate("Cover"))

doc.build(story)
print(f"Saved: {OUTPUT}")
