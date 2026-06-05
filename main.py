import customtkinter as ctk

# Tentativas de importação das telas
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
    def __init__(self, app):
        self.app = app
        self.app.title("Sistema de Avisos Automatizados - Painel Univap")
        self.app.geometry("1200x700")
        self.app.state('zoomed')
        
        ctk.set_appearance_mode("Light")
        
        # Paleta de cores
        self.cor_univap_azul = ("#0056B3", "#3B82F6")
        self.cor_univap_escuro = ("#003366", "#60A5FA")
        
        self.criar_sidebar()
        self.mostrar_tela_inicial()

    def criar_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.app, width=260, corner_radius=0, fg_color=self.cor_univap_escuro)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False) 
        
        lbl_titulo = ctk.CTkLabel(self.sidebar, text="PAINEL\nUNIVAP", font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"), text_color="white")
        lbl_titulo.pack(pady=(40, 10))
        
        lbl_sub = ctk.CTkLabel(self.sidebar, text="Gestão de Avisos Escolares", font=ctk.CTkFont(size=13), text_color="#E2E8F0")
        lbl_sub.pack(pady=(0, 50))
        
        self.btn_cursos = ctk.CTkButton(self.sidebar, text="📚 Gerenciar Cursos", height=45, fg_color="transparent", hover_color=self.cor_univap_azul, font=ctk.CTkFont(size=15, weight="bold"), anchor="w", command=self.abrir_cursos)
        self.btn_cursos.pack(fill="x", padx=15, pady=8)
        
        self.btn_turmas = ctk.CTkButton(self.sidebar, text="🏫 Gerenciar Turmas", height=45, fg_color="transparent", hover_color=self.cor_univap_azul, font=ctk.CTkFont(size=15, weight="bold"), anchor="w", command=self.abrir_turmas)
        self.btn_turmas.pack(fill="x", padx=15, pady=8)
        
        self.btn_alunos = ctk.CTkButton(self.sidebar, text="👨‍🎓 Gerenciar Alunos", height=45, fg_color="transparent", hover_color=self.cor_univap_azul, font=ctk.CTkFont(size=15, weight="bold"), anchor="w", command=self.abrir_alunos)
        self.btn_alunos.pack(fill="x", padx=15, pady=8)
        
        spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.pack(fill="both", expand=True)
        
        self.btn_sair = ctk.CTkButton(self.sidebar, text="🚪 Sair do Sistema", height=45, fg_color="#EF4444", hover_color="#B91C1C", font=ctk.CTkFont(size=14, weight="bold"), command=self.app.quit)
        self.btn_sair.pack(fill="x", padx=15, pady=25)

    def limpar_conteudo_principal(self):
        for widget in self.app.winfo_children():
            if widget != self.sidebar:
                widget.destroy()

    def mostrar_tela_inicial(self):
        self.limpar_conteudo_principal()
        
        frame_inicial = ctk.CTkFrame(self.app, fg_color="transparent")
        frame_inicial.pack(fill="both", expand=True)
        
        lbl_bem_vindo = ctk.CTkLabel(frame_inicial, text="Bem-vindo ao Sistema Automatizado Univap", font=ctk.CTkFont(size=28, weight="bold"), text_color=self.cor_univap_escuro)
        lbl_bem_vindo.pack(expand=True)

    def _empacotar_tela(self, tela_instanciada):
        """Método auxiliar robusto para empacotar a tela independentemente de como foi construída"""
        if hasattr(tela_instanciada, 'pack'):
            # Se a classe herda de CTkFrame
            tela_instanciada.pack(fill="both", expand=True)
        elif hasattr(tela_instanciada, 'frame'):
            # Se a classe tem um atributo chamado 'frame'
            tela_instanciada.frame.pack(fill="both", expand=True)
        elif hasattr(tela_instanciada, 'frame_principal'):
            # Se a classe tem um atributo chamado 'frame_principal'
            tela_instanciada.frame_principal.pack(fill="both", expand=True)
        else:
            self.mostrar_erro_importacao("Desconhecido", "A classe não é um CTkFrame e não possui um frame interno acessível.")

    def abrir_cursos(self):
        self.limpar_conteudo_principal()
        if TelaCadastroCurso:
            tela = TelaCadastroCurso(self.app)
            self._empacotar_tela(tela)
        else:
            self.mostrar_erro_importacao("tela_cursos.py", "TelaCadastroCurso")

    def abrir_turmas(self):
        self.limpar_conteudo_principal()
        if TelaCadastroTurmas:
            tela = TelaCadastroTurmas(self.app)
            self._empacotar_tela(tela)
        else:
            self.mostrar_erro_importacao("tela_turmas.py", "TelaCadastroTurmas")

    def abrir_alunos(self):
        self.limpar_conteudo_principal()
        if TelaCadastroAlunos:
            tela = TelaCadastroAlunos(self.app)
            self._empacotar_tela(tela)
        else:
            self.mostrar_erro_importacao("tela_alunos.py", "TelaCadastroAlunos")

    def mostrar_erro_importacao(self, arquivo, classe):
        frame_erro = ctk.CTkFrame(self.app, fg_color="transparent")
        frame_erro.pack(fill="both", expand=True)
        
        msg = f"Não foi possível carregar o arquivo '{arquivo}'.\nCertifique-se de que ele está na mesma pasta que o main.py\ne que a classe se chama '{classe}'."
        ctk.CTkLabel(frame_erro, text="⚠️ Erro de Conexão de Tela", font=ctk.CTkFont(size=22, weight="bold"), text_color="#EF4444").pack(pady=(200, 15))
        ctk.CTkLabel(frame_erro, text=msg, font=ctk.CTkFont(size=16)).pack()


if __name__ == "__main__":
    app = ctk.CTk()
    painel = SistemaAvisosMain(app)
    app.mainloop()