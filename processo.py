class Processo:
    def __init__(self, id_processo: str, tempo_chegada: int, tempo_burst: int, prioridade: int):
        self.id = id_processo
        self.tempo_chegada = tempo_chegada
        self.tempo_burst = tempo_burst
        self.prioridade = prioridade
        
        # Atributos calculados durante o escalonamento
        self.tempo_espera = 0
        self.tempo_turnaround = 0
        self.tempo_restante = tempo_burst
        self.tempo_finalizacao = 0

    def resetar(self):
        """Reseta os atributos de tempo para uma nova simulação, preservando os dados originais."""
        self.tempo_espera = 0
        self.tempo_turnaround = 0
        self.tempo_restante = self.tempo_burst
        self.tempo_finalizacao = 0
        
    def __repr__(self):
        return f"Processo(ID={self.id}, Chegada={self.tempo_chegada}, Burst={self.tempo_burst}, Prio={self.prioridade})"
