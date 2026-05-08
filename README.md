# 🚀 CPU Scheduling Simulator (Maestro)

Este é um simulador avançado de algoritmos de escalonamento de CPU, desenvolvido para a disciplina de Sistemas Operacionais. O projeto oferece uma interface gráfica moderna e intuitiva para visualizar como o processador gerencia diferentes processos através de Diagramas de Gantt e logs detalhados.

![Screenshot da Interface](https://via.placeholder.com/800x450.png?text=Interface+do+Simulador+CPU)

## ✨ Funcionalidades

O simulador permite analisar o comportamento dos principais algoritmos utilizados em sistemas operacionais reais:

- **FCFS (First-Come, First-Served)**: Atendimento por ordem de chegada.
- **SJF (Shortest Job First) - Não-Preemptivo**: Prioriza os processos com menor tempo de execução.
- **SRTF (Shortest Remaining Time First)**: Versão preemptiva do SJF, onde o processo atual pode ser interrompido se um processo menor chegar.
- **Prioridade (Não-Preemptivo)**: Escalonamento baseado no nível de importância definido no CSV.
- **Round Robin**: Execução circular com tempo compartilhado (Quantum configurável na interface).

### Recursos Extras:
- **📊 Diagrama de Gantt**: Visualização gráfica e colorida da linha do tempo da CPU.
- **📝 Logs em Tempo Real**: Acompanhamento detalhado de cada evento (chegada, troca de contexto, conclusão).
- **📈 Estatísticas Médias**: Cálculo automático do **Tempo de Espera Médio** e **Tempo de Turnaround Médio**.

---

## 📂 Formato do Arquivo de Entrada (CSV)

O programa utiliza arquivos CSV para carregar os processos. O arquivo deve conter um cabeçalho e seguir este padrão:

`id,chegada,burst,prioridade`

| Coluna | Descrição | Exemplo |
| :--- | :--- | :--- |
| **id** | Nome ou identificador do processo | P1 |
| **chegada** | Tempo de chegada na fila (inteiro) | 0 |
| **burst** | Tempo total necessário na CPU (inteiro) | 10 |
| **prioridade** | Nível de prioridade (menor número = maior prioridade) | 1 |

### Exemplo de arquivo `processos.csv`:
```csv
id,chegada,burst,prioridade
P1,0,5,2
P2,1,3,1
P3,2,8,3
P4,3,6,2
```

---

## 🚀 Como Utilizar (Versão Executável)

Se você apenas deseja utilizar o programa sem configurar um ambiente de desenvolvimento:

1. Acesse a pasta `dist/`.
2. Execute o arquivo **`Simulador_Escalonamento.exe`**.
3. Na interface:
   - Clique em **"Carregar Arquivo CSV"** e selecione seu arquivo.
   - Escolha o **Algoritmo** desejado.
   - (Opcional) Defina o **Quantum** se estiver usando Round Robin.
   - Clique em **"Simular"**.

---

## 🛠️ Como Utilizar (Desenvolvedores)

Se você deseja modificar o código ou rodar via terminal:

### 1. Pré-requisitos
- Python 3.10 ou superior.

### 2. Configuração do Ambiente
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd CH5

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

### 3. Execução
```bash
python main.py
```

### 4. Gerar Novo Executável
Caso faça alterações e queira gerar um novo `.exe`, utilize o script de automação fornecido:
```bash
python build_exe.py
```

---

## 🧰 Tecnologias Utilizadas

- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)**: Interface gráfica moderna (Dark Mode nativo).
- **[Matplotlib](https://matplotlib.org/)**: Geração dinâmica de gráficos de Gantt.
- **[PyInstaller](https://pyinstaller.org/)**: Empacotamento de software para Windows.

---
Desenvolvido como parte do trabalho de **Mestrado**.
