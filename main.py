import customtkinter as ctk
import os
from PIL import Image

# ── Importação segura das telas ──────────────────────────────────────────────
try:
    from tela_cursos import TelaCadastroCurso
except ImportError:
    TelaCadastroCurso = None

try:
    from tela_turmas import TelaCadastroTurmas
except ImportError:
    TelaCadastroTurmas = None

try:
    from tela_alunos import TelaCadastroAlunos
except ImportError:
    TelaCadastroAlunos = None


class SistemaAvisosMain:
    # ── Paleta de cores ──────────────────────────────────────────────────────
    COR = {
        "sidebar":        "#002B5C",
        "sidebar_hover":  "#004080",
        "sidebar_ativo":  "#0056B3",
        "sidebar_txt":    "#FFFFFF",
        "sidebar_sub":    "#A0BDD8",
        "sidebar_sep":    "#1A4070",
        "conteudo_bg":    ("#F0F4F8", "#0D1B2A"),
        "azul":           ("#0056B3", "#3B82F6"),
        "titulo":         ("#002B5C", "#93C5FD"),
        "texto":          ("#1E3A5F", "#E2EAF8"),
        "suave":          ("#5A7A9F", "#6B9ED2"),
        "card":           ("#FFFFFF", "#152032"),
        "borda":          ("#D1DCF0", "#1E3A5F"),
        "perigo":         "#DC2626",
        "perigo_hov":     "#991B1B",
    }

    def __init__(self, app: ctk.CTk):
        self.app       = app
        self.tela_ativa = None

        self.app.title("Sistema de Avisos Automatizados — Painel Univap")
        self.app.geometry("1350x760")
        self.app.minsize(1000, 600)
        self.app.state("zoomed")

        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        self._build_layout()
        self._mostrar_inicial()

    # ════════════════════════════════════════════
    #  LAYOUT PRINCIPAL
    # ════════════════════════════════════════════
    def _build_layout(self):
        # ── Sidebar ──
        self.sidebar = ctk.CTkFrame(
            self.app, width=220, corner_radius=0,
            fg_color=self.COR["sidebar"])
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self._build_sidebar()

        # ── Área de conteúdo ──
        self.area = ctk.CTkFrame(
            self.app, fg_color=self.COR["conteudo_bg"],
            corner_radius=0)
        self.area.pack(side="right", fill="both", expand=True)

    def _build_sidebar(self):
        sb = self.sidebar

        # Logo no topo
        logo_frame = ctk.CTkFrame(sb, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(30, 0))

        logo_lbl = self._make_sidebar_logo(logo_frame)
        logo_lbl.pack(side="left", padx=(0, 12))

        txt_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        txt_frame.pack(side="left")
        ctk.CTkLabel(txt_frame, text="PAINEL",
                     font=ctk.CTkFont("Segoe UI", 20, "bold"),
                     text_color="white").pack(anchor="w")
        ctk.CTkLabel(txt_frame, text="UNIVAP",
                     font=ctk.CTkFont("Segoe UI", 20, "bold"),
                     text_color="#7EC8F0").pack(anchor="w")

        # Subtítulo
        ctk.CTkLabel(sb, text="Gestão de Avisos Escolares",
                     font=ctk.CTkFont(size=11),
                     text_color=self.COR["sidebar_sub"]).pack(pady=(8, 0))

        # Separador
        ctk.CTkFrame(sb, height=1, fg_color=self.COR["sidebar_sep"]).pack(
            fill="x", padx=20, pady=24)

        # Rótulo do menu
        ctk.CTkLabel(sb, text="MENU PRINCIPAL",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=self.COR["sidebar_sub"]).pack(anchor="w", padx=22, pady=(0, 8))

        # Botões de navegação
        self.btn_inicio = self._sidebar_btn(
            sb, "🏠  Início", self._mostrar_inicial)
        self.btn_cursos = self._sidebar_btn(
            sb, "📚  Gerenciar Cursos", self._abrir_cursos)
        self.btn_turmas = self._sidebar_btn(
            sb, "🏫  Gerenciar Turmas", self._abrir_turmas)
        self.btn_alunos = self._sidebar_btn(
            sb, "👤  Gerenciar Alunos", self._abrir_alunos)

        self._btns_nav = [
            self.btn_inicio,
            self.btn_cursos,
            self.btn_turmas,
            self.btn_alunos,
        ]

        # Espaçador
        ctk.CTkFrame(sb, fg_color="transparent").pack(fill="both", expand=True)

        # Separador inferior
        ctk.CTkFrame(sb, height=1, fg_color=self.COR["sidebar_sep"]).pack(
            fill="x", padx=20, pady=(0, 16))

        # Botão sair
        ctk.CTkButton(
            sb, text="⏻  Sair do Sistema",
            height=44, corner_radius=8,
            fg_color=self.COR["perigo"],
            hover_color=self.COR["perigo_hov"],
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.app.quit
        ).pack(fill="x", padx=16, pady=(0, 20))

    # ════════════════════════════════════════════
    #  TELA INICIAL
    # ════════════════════════════════════════════
    def _mostrar_inicial(self):
        self._limpar_area()
        self._marcar_ativo(self.btn_inicio)

        frame = ctk.CTkFrame(self.area, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        # Centraliza verticalmente
        spacer_top = ctk.CTkFrame(frame, fg_color="transparent")
        spacer_top.pack(expand=True)

        center = ctk.CTkFrame(frame, fg_color="transparent")
        center.pack()

        # Ícone grande
        ctk.CTkLabel(center, text="🎓",
                     font=ctk.CTkFont(size=72)).pack(pady=(0, 16))

        ctk.CTkLabel(center,
                     text="Bem-vindo ao Sistema Univap",
                     font=ctk.CTkFont("Segoe UI", 30, "bold"),
                     text_color=self.COR["titulo"]).pack()

        ctk.CTkLabel(center,
                     text="Selecione uma opção no menu lateral para começar",
                     font=ctk.CTkFont("Segoe UI", 15),
                     text_color=self.COR["suave"]).pack(pady=(8, 40))

        # Cards de atalho
        cards_frame = ctk.CTkFrame(center, fg_color="transparent")
        cards_frame.pack()

        self._card_atalho(cards_frame, "📚", "Cursos",
                          "Cadastre e gerencie\nos cursos disponíveis",
                          self._abrir_cursos).pack(side="left", padx=10)
        self._card_atalho(cards_frame, "🏫", "Turmas",
                          "Vincule turmas aos\ncursos cadastrados",
                          self._abrir_turmas).pack(side="left", padx=10)
        self._card_atalho(cards_frame, "👤", "Alunos",
                          "Gerencie os alunos\ne suas matrículas",
                          self._abrir_alunos).pack(side="left", padx=10)

        ctk.CTkFrame(frame, fg_color="transparent").pack(expand=True)

    # ════════════════════════════════════════════
    #  NAVEGAÇÃO
    # ════════════════════════════════════════════
    def _abrir_cursos(self):
        self._limpar_area()
        self._marcar_ativo(self.btn_cursos)
        if TelaCadastroCurso:
            TelaCadastroCurso(self.area).pack(fill="both", expand=True)
        else:
            self._tela_erro("tela_cursos.py", "TelaCadastroCurso")

    def _abrir_turmas(self):
        self._limpar_area()
        self._marcar_ativo(self.btn_turmas)
        if TelaCadastroTurmas:
            TelaCadastroTurmas(self.area).pack(fill="both", expand=True)
        else:
            self._tela_erro("tela_turmas.py", "TelaCadastroTurmas")

    def _abrir_alunos(self):
        self._limpar_area()
        self._marcar_ativo(self.btn_alunos)
        if TelaCadastroAlunos:
            TelaCadastroAlunos(self.area).pack(fill="both", expand=True)
        else:
            self._tela_erro("tela_alunos.py", "TelaCadastroAlunos")

    # ════════════════════════════════════════════
    #  UTILITÁRIOS DE UI
    # ════════════════════════════════════════════
    def _limpar_area(self):
        for w in self.area.winfo_children():
            w.destroy()

    def _marcar_ativo(self, btn_ativo):
        for b in self._btns_nav:
            b.configure(
                fg_color=self.COR["sidebar_ativo"] if b is btn_ativo else "transparent")

    def _sidebar_btn(self, parent, texto, cmd):
        btn = ctk.CTkButton(
            parent, text=texto,
            height=44, corner_radius=8,
            fg_color="transparent",
            hover_color=self.COR["sidebar_hover"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.COR["sidebar_txt"],
            anchor="w",
            command=cmd)
        btn.pack(fill="x", padx=12, pady=3)
        return btn

    def _card_atalho(self, parent, icone, titulo, descricao, cmd):
        card = ctk.CTkFrame(parent,
                            fg_color=self.COR["card"],
                            border_width=1, border_color=self.COR["borda"],
                            corner_radius=14, width=200, height=160)
        card.pack_propagate(False)

        ctk.CTkLabel(card, text=icone,
                     font=ctk.CTkFont(size=34)).pack(pady=(22, 6))
        ctk.CTkLabel(card, text=titulo,
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=self.COR["azul"]).pack()
        ctk.CTkLabel(card, text=descricao,
                     font=ctk.CTkFont(size=11),
                     text_color=self.COR["suave"],
                     justify="center").pack(pady=(4, 12))

        # Clique em qualquer parte do card navega
        for widget in [card] + card.winfo_children():
            widget.bind("<Button-1>", lambda _, c=cmd: c())
            widget.bind("<Enter>",
                lambda e, w=card: w.configure(border_color=self.COR["azul"]))
            widget.bind("<Leave>",
                lambda e, w=card: w.configure(border_color=self.COR["borda"]))
        return card

    def _tela_erro(self, arquivo, classe):
        f = ctk.CTkFrame(self.area, fg_color="transparent")
        f.pack(fill="both", expand=True)
        ctk.CTkLabel(f, text="⚠️ Erro ao carregar tela",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#DC2626").pack(pady=(200, 12))
        ctk.CTkLabel(f,
                     text=f"Não foi possível carregar '{arquivo}'.\n"
                          f"Certifique-se de que o arquivo está na mesma pasta que o main.py\n"
                          f"e que a classe se chama '{classe}'.",
                     font=ctk.CTkFont(size=14),
                     justify="center").pack()

    def _make_sidebar_logo(self, parent):
        path = "logo_univap.png"
        if os.path.exists(path):
            try:
                img  = Image.open(path)
                cimg = ctk.CTkImage(light_image=img, dark_image=img, size=(48, 48))
                return ctk.CTkLabel(parent, image=cimg, text="")
            except Exception:
                pass
        return ctk.CTkLabel(parent, text="U",
                            font=ctk.CTkFont(weight="bold", size=22),
                            fg_color="#0056B3", text_color="white",
                            width=48, height=48, corner_radius=10)


# ── Ponto de entrada ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = ctk.CTk()
    SistemaAvisosMain(app)
    app.mainloop() 