"""Modern desktop interface for the Freelance Brief Analyzer."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import customtkinter as ctk
from tkinter import filedialog, messagebox

from .analyzer import BriefAnalysis, analyze_brief

# Every pair is ordered as: (light-mode colour, dark-mode colour).
# Keep visual choices here so the theme can be changed without hunting through the UI code.
PALETTE = {
    "accent": ("#A563E0", "#8888CF"),
    "accent_hover": ("#8D46CB", "#A3A3E0"),
    "border": ("#E5E7EB", "#4C1D95"),
    "surface": ("#F5F0FF", "#2B1B3A"),
    "header": ("#F5F3FF", "#1E1633"),
    "heading": ("#3B0764", "#EDE9FE"),
    "muted": ("#6B7280", "#C4B5FD"),
}


class BriefAnalyzerApp(ctk.CTk):
    """System-theme-aware desktop application for project brief discovery."""

    def __init__(self) -> None:
        super().__init__()
        self.analysis: BriefAnalysis | None = None
        self.client_name = ctk.StringVar()
        self.project_title = ctk.StringVar()
        self.contact_email = ctk.StringVar()
        self.status = ctk.StringVar(value="Complete the form to create a project analysis.")

        self.title("Freelance Brief Analyzer")
        self.geometry("1120x760")
        self.minsize(900, 620)
        self.configure(fg_color=("#FFFFFF", "#1A1A1A"))
        self.grid_columnconfigure((0, 1), weight=1, uniform="columns")
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_input_panel()
        self._build_analysis_panel()
        self._build_footer()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self, corner_radius=0, fg_color=PALETTE["header"])
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header, text="Freelance Brief Analyzer", font=ctk.CTkFont(size=28, weight="bold"),
            text_color=PALETTE["heading"],
        ).grid(row=0, column=0, sticky="w", padx=32, pady=(24, 2))
        ctk.CTkLabel(
            header, text="Turn a client request into a clear delivery checklist.",
            font=ctk.CTkFont(size=14), text_color=PALETTE["muted"],
        ).grid(row=1, column=0, sticky="w", padx=32, pady=(0, 24))

    def _build_input_panel(self) -> None:
        panel = ctk.CTkFrame(self, corner_radius=20, fg_color=PALETTE["surface"], border_width=1, border_color=PALETTE["border"])
        panel.grid(row=1, column=0, sticky="nsew", padx=(28, 12), pady=24)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(9, weight=1)

        self._section_title(panel, "Client & project details", "Enter the information received from the client.")
        self._label(panel, "Client or company name *", 2)
        ctk.CTkEntry(panel, textvariable=self.client_name, placeholder_text="e.g. Acme Studio", border_color=PALETTE["border"]).grid(row=3, column=0, sticky="ew", padx=22, pady=(5, 12))
        self._label(panel, "Project title", 4)
        ctk.CTkEntry(panel, textvariable=self.project_title, placeholder_text="e.g. Customer support assistant", border_color=PALETTE["border"]).grid(row=5, column=0, sticky="ew", padx=22, pady=(5, 12))
        self._label(panel, "Client email", 6)
        ctk.CTkEntry(panel, textvariable=self.contact_email, placeholder_text="e.g. hello@acme.com", border_color=PALETTE["border"]).grid(row=7, column=0, sticky="ew", padx=22, pady=(5, 12))
        self._label(panel, "Project brief *", 8)
        self.brief_text = ctk.CTkTextbox(panel, corner_radius=12, border_width=1, border_color=PALETTE["border"], font=ctk.CTkFont(size=14))
        self.brief_text.grid(row=9, column=0, sticky="nsew", padx=22, pady=(6, 16))

        controls = ctk.CTkFrame(panel, fg_color="transparent")
        controls.grid(row=10, column=0, sticky="ew", padx=22, pady=(0, 22))
        controls.grid_columnconfigure(0, weight=1)
        ctk.CTkButton(controls, text="Analyze project brief", height=42, corner_radius=12, font=ctk.CTkFont(size=14, weight="bold"), fg_color=PALETTE["accent"], hover_color=PALETTE["accent_hover"], command=self.analyze).grid(row=0, column=0, sticky="ew")
        ctk.CTkButton(controls, text="Clear form", height=36, corner_radius=12, fg_color="transparent", border_width=1, border_color=PALETTE["border"], text_color=PALETTE["accent"], hover_color=("#EDE9FE", "#2E1065"), command=self.clear).grid(row=1, column=0, sticky="ew", pady=(10, 0))

    def _build_analysis_panel(self) -> None:
        panel = ctk.CTkFrame(self, corner_radius=20, fg_color=PALETTE["surface"], border_width=1, border_color=PALETTE["border"])
        panel.grid(row=1, column=1, sticky="nsew", padx=(12, 28), pady=24)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(2, weight=1)

        self._section_title(panel, "Project analysis", "Review the findings before writing a proposal or estimate.")
        self.result_text = ctk.CTkTextbox(panel, corner_radius=12, border_width=1, border_color=PALETTE["border"], font=ctk.CTkFont(family="Consolas", size=13), state="disabled")
        self.result_text.grid(row=2, column=0, sticky="nsew", padx=22, pady=(18, 16))
        ctk.CTkButton(panel, text="Save JSON result", height=40, corner_radius=12, fg_color=PALETTE["accent"], hover_color=PALETTE["accent_hover"], command=self.save_json).grid(row=3, column=0, sticky="ew", padx=22, pady=(0, 22))

    def _build_footer(self) -> None:
        ctk.CTkLabel(self, textvariable=self.status, anchor="w", text_color=PALETTE["muted"]).grid(row=2, column=0, columnspan=2, sticky="ew", padx=32, pady=(0, 18))

    @staticmethod
    def _section_title(parent: ctk.CTkFrame, title: str, subtitle: str) -> None:
        ctk.CTkLabel(parent, text=title, font=ctk.CTkFont(size=19, weight="bold")).grid(row=0, column=0, sticky="w", padx=22, pady=(22, 2))
        ctk.CTkLabel(parent, text=subtitle, text_color=PALETTE["muted"], wraplength=440, justify="left").grid(row=1, column=0, sticky="w", padx=22)

    @staticmethod
    def _label(parent: ctk.CTkFrame, text: str, row: int) -> None:
        ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=13, weight="bold")).grid(row=row, column=0, sticky="w", padx=22)

    def analyze(self) -> None:
        try:
            self.analysis = analyze_brief(self.client_name.get(), self.brief_text.get("1.0", "end-1c"))
        except ValueError as error:
            messagebox.showerror("Missing information", str(error), parent=self)
            return
        self._set_result(self._format_analysis(self.analysis))
        self.status.set("Analysis complete. Review it, then save a JSON copy if needed.")

    def save_json(self) -> None:
        if self.analysis is None:
            messagebox.showinfo("No analysis yet", "Analyze a project brief before saving.", parent=self)
            return
        destination = filedialog.asksaveasfilename(parent=self, title="Save analysis as JSON", defaultextension=".json", filetypes=[("JSON files", "*.json")], initialfile="brief-analysis.json")
        if not destination:
            return
        payload: dict[str, Any] = self.analysis.to_dict()
        payload["client_details"] = {"project_title": self.project_title.get().strip() or None, "contact_email": self.contact_email.get().strip() or None}
        Path(destination).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        self.status.set(f"Saved JSON analysis to {destination}")

    def clear(self) -> None:
        self.client_name.set("")
        self.project_title.set("")
        self.contact_email.set("")
        self.brief_text.delete("1.0", "end")
        self.analysis = None
        self._set_result("")
        self.status.set("Form cleared. Add a new client brief to begin.")

    def _set_result(self, content: str) -> None:
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", content)
        self.result_text.configure(state="disabled")

    @staticmethod
    def _format_analysis(analysis: BriefAnalysis) -> str:
        def list_items(items: list[str]) -> str:
            return "\n".join(f"• {item}" for item in items)
        return f"CLIENT\n{analysis.client}\n\nSUMMARY\n{analysis.summary}\n\nLIKELY WORK AREAS\n{list_items(analysis.technologies)}\n\nDELIVERY RISKS\n{list_items(analysis.risks)}\n\nDISCOVERY QUESTIONS\n{list_items(analysis.discovery_questions)}"


def main() -> None:
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    BriefAnalyzerApp().mainloop()
