from processo import Processo

def fcfs(processos: list[Processo]):
    for p in processos: p.resetar()
    processos_ordenados = sorted(processos, key=lambda x: x.tempo_chegada)
    
    tempo_atual = 0
    eventos = []
    logs = []
    
    for p in processos_ordenados:
        if tempo_atual < p.tempo_chegada:
            logs.append(f"Tempo {tempo_atual} a {p.tempo_chegada}: CPU Ociosa")
            tempo_atual = p.tempo_chegada
            
        tempo_inicio = tempo_atual
        tempo_atual += p.tempo_burst
        tempo_fim = tempo_atual
        
        p.tempo_finalizacao = tempo_fim
        p.tempo_turnaround = p.tempo_finalizacao - p.tempo_chegada
        p.tempo_espera = p.tempo_turnaround - p.tempo_burst
        
        eventos.append((tempo_inicio, tempo_fim, p.id))
        logs.append(f"Tempo {tempo_inicio} a {tempo_fim}: Processo {p.id} executando")
        
    return _calcular_medias_e_retornar(processos, logs, eventos)

def sjf_nao_preemptivo(processos: list[Processo]):
    for p in processos: p.resetar()
    nao_chegados = sorted(processos, key=lambda x: x.tempo_chegada)
    prontos = []
    
    tempo_atual = 0
    eventos = []
    logs = []
    concluidos = []
    n = len(processos)
    
    while len(concluidos) < n:
        while nao_chegados and nao_chegados[0].tempo_chegada <= tempo_atual:
            prontos.append(nao_chegados.pop(0))
            
        if not prontos:
            if nao_chegados:
                ocioso_inicio = tempo_atual
                tempo_atual = nao_chegados[0].tempo_chegada
                logs.append(f"Tempo {ocioso_inicio} a {tempo_atual}: CPU Ociosa")
            continue
            
        prontos.sort(key=lambda x: (x.tempo_burst, x.tempo_chegada))
        p = prontos.pop(0)
        
        tempo_inicio = tempo_atual
        tempo_atual += p.tempo_burst
        tempo_fim = tempo_atual
        
        p.tempo_finalizacao = tempo_fim
        p.tempo_turnaround = p.tempo_finalizacao - p.tempo_chegada
        p.tempo_espera = p.tempo_turnaround - p.tempo_burst
        
        eventos.append((tempo_inicio, tempo_fim, p.id))
        logs.append(f"Tempo {tempo_inicio} a {tempo_fim}: Processo {p.id} executando (Burst: {p.tempo_burst})")
        concluidos.append(p)
        
    return _calcular_medias_e_retornar(processos, logs, eventos)

def sjf_preemptivo(processos: list[Processo]): # SRTF
    for p in processos: p.resetar()
    nao_chegados = sorted(processos, key=lambda x: x.tempo_chegada)
    prontos = []
    
    tempo_atual = 0
    eventos = []
    logs = []
    concluidos = []
    n = len(processos)
    
    processo_atual = None
    tempo_inicio_execucao = 0
    
    while len(concluidos) < n:
        while nao_chegados and nao_chegados[0].tempo_chegada <= tempo_atual:
            prontos.append(nao_chegados.pop(0))
            
        candidatos = prontos + ([processo_atual] if processo_atual else [])
        if candidatos:
            melhor_p = min(candidatos, key=lambda x: (x.tempo_restante, x.tempo_chegada))
            
            if processo_atual != melhor_p:
                if processo_atual is not None and tempo_atual > tempo_inicio_execucao:
                    eventos.append((tempo_inicio_execucao, tempo_atual, processo_atual.id))
                    logs.append(f"Tempo {tempo_inicio_execucao} a {tempo_atual}: Processo {processo_atual.id} preemptado (Restante: {processo_atual.tempo_restante})")
                    prontos.append(processo_atual)
                
                processo_atual = melhor_p
                if processo_atual in prontos:
                    prontos.remove(processo_atual)
                tempo_inicio_execucao = tempo_atual
                
            processo_atual.tempo_restante -= 1
            tempo_atual += 1
            
            if processo_atual.tempo_restante == 0:
                eventos.append((tempo_inicio_execucao, tempo_atual, processo_atual.id))
                logs.append(f"Tempo {tempo_inicio_execucao} a {tempo_atual}: Processo {processo_atual.id} finalizou")
                
                processo_atual.tempo_finalizacao = tempo_atual
                processo_atual.tempo_turnaround = processo_atual.tempo_finalizacao - processo_atual.tempo_chegada
                processo_atual.tempo_espera = processo_atual.tempo_turnaround - processo_atual.tempo_burst
                concluidos.append(processo_atual)
                
                processo_atual = None
                tempo_inicio_execucao = tempo_atual
        else:
            if nao_chegados:
                ocioso_inicio = tempo_atual
                tempo_atual = nao_chegados[0].tempo_chegada
                logs.append(f"Tempo {ocioso_inicio} a {tempo_atual}: CPU Ociosa")
            else:
                break
                
    # Mesclar eventos contíguos do mesmo processo para o Gráfico de Gantt (limpar poluição)
    eventos_limpos = []
    if eventos:
        inicio_atual, fim_atual, id_atual = eventos[0]
        for start, end, pid in eventos[1:]:
            if pid == id_atual and start == fim_atual:
                fim_atual = end
            else:
                eventos_limpos.append((inicio_atual, fim_atual, id_atual))
                inicio_atual, fim_atual, id_atual = start, end, pid
        eventos_limpos.append((inicio_atual, fim_atual, id_atual))
        
    return _calcular_medias_e_retornar(processos, logs, eventos_limpos)

def prioridade(processos: list[Processo]):
    """ Prioridade Não-Preemptiva, menor número = maior prioridade """
    for p in processos: p.resetar()
    nao_chegados = sorted(processos, key=lambda x: x.tempo_chegada)
    prontos = []
    
    tempo_atual = 0
    eventos = []
    logs = []
    concluidos = []
    n = len(processos)
    
    while len(concluidos) < n:
        while nao_chegados and nao_chegados[0].tempo_chegada <= tempo_atual:
            prontos.append(nao_chegados.pop(0))
            
        if not prontos:
            if nao_chegados:
                ocioso_inicio = tempo_atual
                tempo_atual = nao_chegados[0].tempo_chegada
                logs.append(f"Tempo {ocioso_inicio} a {tempo_atual}: CPU Ociosa")
            continue
            
        prontos.sort(key=lambda x: (x.prioridade, x.tempo_chegada))
        p = prontos.pop(0)
        
        tempo_inicio = tempo_atual
        tempo_atual += p.tempo_burst
        tempo_fim = tempo_atual
        
        p.tempo_finalizacao = tempo_fim
        p.tempo_turnaround = p.tempo_finalizacao - p.tempo_chegada
        p.tempo_espera = p.tempo_turnaround - p.tempo_burst
        
        eventos.append((tempo_inicio, tempo_fim, p.id))
        logs.append(f"Tempo {tempo_inicio} a {tempo_fim}: Processo {p.id} executando (Prio: {p.prioridade})")
        concluidos.append(p)
        
    return _calcular_medias_e_retornar(processos, logs, eventos)

def round_robin(processos: list[Processo], quantum: int):
    for p in processos: p.resetar()
    nao_chegados = sorted(processos, key=lambda x: x.tempo_chegada)
    fila = []
    
    tempo_atual = 0
    eventos = []
    logs = []
    concluidos = []
    n = len(processos)
    
    if nao_chegados and nao_chegados[0].tempo_chegada > tempo_atual:
        tempo_atual = nao_chegados[0].tempo_chegada
        
    while nao_chegados and nao_chegados[0].tempo_chegada <= tempo_atual:
        fila.append(nao_chegados.pop(0))

    while len(concluidos) < n:
        if not fila:
            if nao_chegados:
                ocioso_inicio = tempo_atual
                tempo_atual = nao_chegados[0].tempo_chegada
                logs.append(f"Tempo {ocioso_inicio} a {tempo_atual}: CPU Ociosa")
                while nao_chegados and nao_chegados[0].tempo_chegada <= tempo_atual:
                    fila.append(nao_chegados.pop(0))
            continue
            
        p = fila.pop(0)
        
        tempo_inicio = tempo_atual
        tempo_execucao = min(p.tempo_restante, quantum)
        
        p.tempo_restante -= tempo_execucao
        tempo_atual += tempo_execucao
        tempo_fim = tempo_atual
        
        eventos.append((tempo_inicio, tempo_fim, p.id))
        logs.append(f"Tempo {tempo_inicio} a {tempo_fim}: Processo {p.id} executou (Restante: {p.tempo_restante})")
        
        while nao_chegados and nao_chegados[0].tempo_chegada <= tempo_atual:
            fila.append(nao_chegados.pop(0))
            
        if p.tempo_restante == 0:
            p.tempo_finalizacao = tempo_fim
            p.tempo_turnaround = p.tempo_finalizacao - p.tempo_chegada
            p.tempo_espera = p.tempo_turnaround - p.tempo_burst
            concluidos.append(p)
            logs.append(f"-> Processo {p.id} finalizou!")
        else:
            fila.append(p)
            
    # Mesclar eventos contíguos caso mesmo processo rode repetidamente contínuo (por ex, se os outros já terminaram)
    eventos_limpos = []
    if eventos:
        inicio_atual, fim_atual, id_atual = eventos[0]
        for start, end, pid in eventos[1:]:
            if pid == id_atual and start == fim_atual:
                fim_atual = end
            else:
                eventos_limpos.append((inicio_atual, fim_atual, id_atual))
                inicio_atual, fim_atual, id_atual = start, end, pid
        eventos_limpos.append((inicio_atual, fim_atual, id_atual))

    return _calcular_medias_e_retornar(processos, logs, eventos_limpos)

def _calcular_medias_e_retornar(processos, logs, eventos):
    n = len(processos)
    if n == 0:
        return logs, eventos, 0.0, 0.0
    espera_media = sum(p.tempo_espera for p in processos) / n
    turnaround_medio = sum(p.tempo_turnaround for p in processos) / n
    return logs, eventos, espera_media, turnaround_medio
