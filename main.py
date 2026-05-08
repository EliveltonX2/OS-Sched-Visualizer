import customtkinter as ctk
from tkinter import filedialog
from utils import ler_csv, plotar_gantt
from escalonadores import fcfs, sjf_nao_preemptivo, sjf_preemptivo, prioridade, round_robin

# Configurações globais do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Simulador de Escalonamento de CPU")
        self.geometry("800x600")
        
        # Variável para armazenar o caminho do arquivo selecionado
        self.caminho_arquivo = None
        
        # -- Layout da Janela Principal --
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # 1. Painel Superior: Botão e Label para o Arquivo CSV
        self.frame_top = ctk.CTkFrame(self)
        self.frame_top.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_carregar = ctk.CTkButton(self.frame_top, text="Carregar Arquivo CSV", command=self.carregar_csv)
        self.btn_carregar.pack(side="left", padx=10, pady=10)
        
        self.lbl_arquivo = ctk.CTkLabel(self.frame_top, text="Nenhum arquivo selecionado", text_color="gray")
        self.lbl_arquivo.pack(side="left", padx=10, pady=10)

        # 2. Painel Central: Algoritmos e Opções
        self.frame_mid = ctk.CTkFrame(self)
        self.frame_mid.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.lbl_algo = ctk.CTkLabel(self.frame_mid, text="Algoritmo:")
        self.lbl_algo.pack(side="left", padx=10, pady=10)
        
        self.algoritmos = [
            "FCFS", 
            "SJF (Não-Preemptivo)", 
            "SJF (Preemptivo - SRTF)", 
            "Prioridade", 
            "Round Robin"
        ]
        self.cb_algo = ctk.CTkComboBox(self.frame_mid, values=self.algoritmos, command=self.on_algo_change, width=200)
        self.cb_algo.pack(side="left", padx=10, pady=10)
        self.cb_algo.set("FCFS")
        
        self.lbl_quantum = ctk.CTkLabel(self.frame_mid, text="Quantum:")
        self.lbl_quantum.pack(side="left", padx=10, pady=10)
        
        self.entry_quantum = ctk.CTkEntry(self.frame_mid, width=60)
        self.entry_quantum.pack(side="left", padx=10, pady=10)
        self.entry_quantum.insert(0, "2")
        self.entry_quantum.configure(state="disabled") # Desabilitado, só liga no RR
        
        self.btn_simular = ctk.CTkButton(self.frame_mid, text="Simular", fg_color="green", hover_color="darkgreen", command=self.simular)
        self.btn_simular.pack(side="right", padx=10, pady=10)

        # 3. Painel Inferior: Área de Logs
        self.lbl_logs = ctk.CTkLabel(self, text="Logs de Execução:")
        self.lbl_logs.grid(row=2, column=0, padx=20, pady=(5, 0), sticky="w")
        
        self.textbox_logs = ctk.CTkTextbox(self, width=760, height=300)
        self.textbox_logs.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
    def on_algo_change(self, valor):
        """Habilita ou desabilita o campo Quantum dependendo do algoritmo atual."""
        if valor == "Round Robin":
            self.entry_quantum.configure(state="normal")
        else:
            self.entry_quantum.configure(state="disabled")
            
    def carregar_csv(self):
        """Abre o diálogo de arquivos para buscar o CSV de processos."""
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo CSV de Processos",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            self.caminho_arquivo = caminho
            nome_arquivo = caminho.split("/")[-1]
            self.lbl_arquivo.configure(text=nome_arquivo, text_color="white")
            self.escrever_log(f"[*] Arquivo carregado: {nome_arquivo}\n")
            
    def simular(self):
        """Fluxo principal ao clicar em Simular."""
        if not self.caminho_arquivo:
            self.escrever_log("[ERRO] Por favor, carregue um arquivo CSV antes de testar.\n")
            return
            
        processos = ler_csv(self.caminho_arquivo)
        if not processos:
            self.escrever_log("[ERRO] Falha ao ler processos do CSV ou arquivo vazio/inválido.\n")
            return
            
        algo_selecionado = self.cb_algo.get()
        
        self.escrever_log("="*60 + "\n")
        self.escrever_log(f"[*] Iniciando Simulação do Algoritmo: {algo_selecionado}\n")
        
        try:
            # Selecionando o despachante baseado na ComboBox
            if algo_selecionado == "FCFS":
                logs, eventos, waits, turns = fcfs(processos)
            elif algo_selecionado == "SJF (Não-Preemptivo)":
                logs, eventos, waits, turns = sjf_nao_preemptivo(processos)
            elif algo_selecionado == "SJF (Preemptivo - SRTF)":
                logs, eventos, waits, turns = sjf_preemptivo(processos)
            elif algo_selecionado == "Prioridade":
                logs, eventos, waits, turns = prioridade(processos)
            elif algo_selecionado == "Round Robin":
                try:
                    quantum = int(self.entry_quantum.get())
                    if quantum <= 0: raise ValueError
                except ValueError:
                    self.escrever_log("[ERRO] Quantum precisa ser um número inteiro maior que 0.\n")
                    return
                logs, eventos, waits, turns = round_robin(processos, quantum)
            else:
                return
                
            # Exibe os logs na área de texto
            for linha in logs:
                self.escrever_log(linha + "\n")
            
            resumo = f"\n    >> Tempo de Espera Médio: {waits:.2f} u.t."
            resumo += f"\n    >> Tempo de Turnaround Médio: {turns:.2f} u.t.\n"
            self.escrever_log(resumo)
            self.escrever_log("="*60 + "\n")
            
            # Chama o Matplotlib para exibir o gráfico de Gantt 
            # Vai abrir uma nova janela na frente da interface principal.
            plotar_gantt(eventos, waits, turns)
            
        except Exception as e:
            self.escrever_log(f"[ERRO ENCONTRADO]: {e}\n")
            
    def escrever_log(self, texto):
        """Método auxiliar para inserir e rolar o texto na Textbox de forma fácil."""
        self.textbox_logs.insert("end", texto)
        self.textbox_logs.see("end") # Rola a barra até o fim, sempre visualizando o log mais novo

if __name__ == "__main__":
    app = App()
    app.mainloop()
