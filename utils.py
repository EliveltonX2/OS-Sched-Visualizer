import csv
import matplotlib.pyplot as plt
import random
from processo import Processo

def ler_csv(caminho_arquivo: str) -> list[Processo]:
    """
    Lê o arquivo CSV contendo os processos.
    Espera o cabeçalho: id,chegada,burst,prioridade
    """
    processos = []
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as f:
            leitor = csv.reader(f)
            header = next(leitor, None)  # Pula o cabeçalho
            
            for linha in leitor:
                # Ignorar linhas vazias ou mal formatadas
                if not linha or len(linha) < 4:
                    continue
                    
                id_proc = linha[0].strip()
                chegada = int(linha[1].strip())
                burst = int(linha[2].strip())
                prioridade = int(linha[3].strip())
                
                processos.append(Processo(id_proc, chegada, burst, prioridade))
    except Exception as e:
        print(f"Erro ao ler CSV: {e}")
        
    return processos

def plotar_gantt(eventos: list[tuple[int, int, str]], tempo_espera_medio: float, turnaround_medio: float):
    """
    Desenha o Gráfico de Gantt usando Matplotlib.
    `eventos` é uma lista de tuplas: (tempo_inicio, tempo_fim, id_processo)
    """
    if not eventos:
        print("Aviso: Nenhum evento para exibir no Gráfico de Gantt.")
        return
        
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Extrair todos os IDs de processos únicos
    ids_processos = list(set([e[2] for e in eventos]))
    # Ordenar por ordem alfanumérica se possível (ex: P1, P2)
    ids_processos.sort()
    
    # Determinar a posição Y para cada processo
    pos_y = {pid: 10 * i + 10 for i, pid in enumerate(ids_processos)}
    
    # Gerar cores aleatórias para diferenciar os processos (barras)
    # Utilizamos um set predefinido para cores mais bonitas se houver poucos
    cores_padrao = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    cores = {}
    for i, pid in enumerate(ids_processos):
        cores[pid] = cores_padrao[i % len(cores_padrao)]
        
    for inicio, fim, pid in eventos:
        duracao = fim - inicio
        y = pos_y[pid]
        
        # Desenhar bloco na barra quebrada (broken_barh)
        ax.broken_barh([(inicio, duracao)], (y - 4, 8), facecolors=cores[pid], edgecolor='black')
        
        # Opcional: Adicionar texto com duração dentro ou em cima da barra
        meio_x = inicio + duracao / 2
        ax.text(meio_x, y, str(duracao), ha='center', va='center', color='white', fontweight='bold')

    # Configuração do eixo Y (Processos)
    ax.set_ylim(4, max(pos_y.values()) + 10)
    ax.set_yticks(list(pos_y.values()))
    ax.set_yticklabels(ids_processos)
    ax.set_ylabel('Processos')

    # Configuração do eixo X (Tempo)
    tempo_maximo = max([e[1] for e in eventos])
    ax.set_xlim(0, tempo_maximo + 1)
    ax.set_xlabel('Tempo')
    
    # Grid e Estética
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    # Título com os dados calculados
    titulo = (f"Diagrama de Gantt CPU\n"
              f"Tempo de Espera Médio: {tempo_espera_medio:.2f} u.t. | Turnaround Médio: {turnaround_medio:.2f} u.t.")
    plt.title(titulo, pad=15)
    
    plt.tight_layout()
    plt.show()
