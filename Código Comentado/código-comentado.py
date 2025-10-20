# Sistema de Paginação de Memória
# Implementação dos algoritmos FIFO, LRU e MRU

from collections import deque, defaultdict
from typing import List, Tuple

class AlgoritmoPaginacao:
    """Classe base para algoritmos de paginação"""
    
    def __init__(self, numero_quadros: int):
        """
        Inicializa o algoritmo de paginação
        
        Args:
            numero_quadros: Quantidade de quadros disponíveis na memória
        """
        self.numero_quadros = numero_quadros
        self.quadros_memoria = []
        self.numero_paginas_faltantes = 0
        self.historico_estado = []
    
    def resetar(self):
        """Reseta o estado da memória"""
        self.quadros_memoria = []
        self.numero_paginas_faltantes = 0
        self.historico_estado = []
    
    def exibir_resultado(self, pagina_procurada: int, sequencia: List[int]):
        """Exibe o resultado da execução do algoritmo"""
        print(f"\nSequência de páginas: {sequencia}")
        print(f"Número de quadros: {self.numero_quadros}")
        print(f"Página faltante (page fault): {self.numero_paginas_faltantes}")
        
        # Encontra em qual quadro está a página procurada
        if pagina_procurada in self.quadros_memoria:
            quadro = self.quadros_memoria.index(pagina_procurada)
            print(f"✓ Página {pagina_procurada} está no quadro: {quadro}")
        else:
            print(f"✗ Página {pagina_procurada} não está na memória no final da execução")

class FIFO(AlgoritmoPaginacao):
    """
    Algoritmo FIFO (First In First Out)
    Remove a página mais antiga da memória quando necessário
    """
    
    def executar(self, sequencia_paginas: List[int]) -> int:
        """
        Executa o algoritmo FIFO
        
        Args:
            sequencia_paginas: Lista de páginas a serem acessadas
            
        Returns:
            Número de page faults ocorridos
        """
        self.resetar()
        fila_substituicao = deque()
        
        for pagina in sequencia_paginas:
            # Se a página já está na memória, continua
            if pagina in self.quadros_memoria:
                continue
            
            # Page fault ocorreu
            self.numero_paginas_faltantes += 1
            
            # Se há espaço disponível, adiciona a página
            if len(self.quadros_memoria) < self.numero_quadros:
                self.quadros_memoria.append(pagina)
                fila_substituicao.append(pagina)
            else:
                # Remove a página mais antiga (FIFO)
                pagina_removida = fila_substituicao.popleft()
                self.quadros_memoria.remove(pagina_removida)
                self.quadros_memoria.append(pagina)
                fila_substituicao.append(pagina)
            
            self.historico_estado.append(self.quadros_memoria.copy())
        
        return self.numero_paginas_faltantes

class LRU(AlgoritmoPaginacao):
    """
    Algoritmo LRU (Least Recently Used)
    Remove a página menos recentemente usada quando necessário
    """
    
    def executar(self, sequencia_paginas: List[int]) -> int:
        """
        Executa o algoritmo LRU
        
        Args:
            sequencia_paginas: Lista de páginas a serem acessadas
            
        Returns:
            Número de page faults ocorridos
        """
        self.resetar()
        tempo_ultimo_uso = {}
        tempo_atual = 0
        
        for pagina in sequencia_paginas:
            tempo_atual += 1
            
            # Se a página já está na memória, atualiza seu tempo de uso
            if pagina in self.quadros_memoria:
                tempo_ultimo_uso[pagina] = tempo_atual
                continue
            
            # Page fault ocorreu
            self.numero_paginas_faltantes += 1
            
            # Se há espaço disponível, adiciona a página
            if len(self.quadros_memoria) < self.numero_quadros:
                self.quadros_memoria.append(pagina)
                tempo_ultimo_uso[pagina] = tempo_atual
            else:
                # Remove a página menos recentemente usada
                pagina_menos_usada = min(self.quadros_memoria, 
                                        key=lambda p: tempo_ultimo_uso.get(p, 0))
                self.quadros_memoria.remove(pagina_menos_usada)
                del tempo_ultimo_uso[pagina_menos_usada]
                
                self.quadros_memoria.append(pagina)
                tempo_ultimo_uso[pagina] = tempo_atual
            
            self.historico_estado.append(self.quadros_memoria.copy())
        
        return self.numero_paginas_faltantes

class MRU(AlgoritmoPaginacao):
    """
    Algoritmo MRU (Most Recently Used)
    Remove a página mais recentemente usada quando necessário
    """
    
    def executar(self, sequencia_paginas: List[int]) -> int:
        """
        Executa o algoritmo MRU
        
        Args:
            sequencia_paginas: Lista de páginas a serem acessadas
            
        Returns:
            Número de page faults ocorridos
        """
        self.resetar()
        tempo_ultimo_uso = {}
        tempo_atual = 0
        
        for pagina in sequencia_paginas:
            tempo_atual += 1
            
            # Se a página já está na memória, atualiza seu tempo de uso
            if pagina in self.quadros_memoria:
                tempo_ultimo_uso[pagina] = tempo_atual
                continue
            
            # Page fault ocorreu
            self.numero_paginas_faltantes += 1
            
            # Se há espaço disponível, adiciona a página
            if len(self.quadros_memoria) < self.numero_quadros:
                self.quadros_memoria.append(pagina)
                tempo_ultimo_uso[pagina] = tempo_atual
            else:
                # Remove a página mais recentemente usada
                pagina_mais_usada = max(self.quadros_memoria, 
                                       key=lambda p: tempo_ultimo_uso.get(p, 0))
                self.quadros_memoria.remove(pagina_mais_usada)
                del tempo_ultimo_uso[pagina_mais_usada]
                
                self.quadros_memoria.append(pagina)
                tempo_ultimo_uso[pagina] = tempo_atual
            
            self.historico_estado.append(self.quadros_memoria.copy())
        
        return self.numero_paginas_faltantes

# ============= EXECUÇÃO E TESTES =============

def executar_testes():
    """Executa todos os testes com as sequências de páginas"""
    
    numero_quadros = 8
    
    # Sequências de teste
    sequencias = {
        'Sequência A': (
            [4, 3, 25, 8, 19, 6, 25, 8, 16, 35, 45, 22, 8, 3, 16, 25, 7],
            7
        ),
        'Sequência B': (
            [4, 5, 7, 9, 46, 45, 14, 4, 64, 7, 65, 2, 1, 6, 8, 45, 14, 11],
            11
        ),
        'Sequência C': (
            [4, 6, 7, 8, 1, 6, 10, 15, 16, 4, 2, 1, 4, 6, 12, 15, 16, 11],
            11
        )
    }
    
    resultados_comparacao = {}
    
    for nome_sequencia, (sequencia, pagina_procurada) in sequencias.items():
        print("\n" + "="*70)
        print(f"\n{nome_sequencia}")
        print("="*70)
        
        resultados_comparacao[nome_sequencia] = {}
        
        # Testa FIFO
        print("\n--- ALGORITMO FIFO ---")
        fifo = FIFO(numero_quadros)
        fifo.executar(sequencia)
        fifo.exibir_resultado(pagina_procurada, sequencia)
        resultados_comparacao[nome_sequencia]['FIFO'] = fifo.numero_paginas_faltantes
        
        # Testa LRU
        print("\n--- ALGORITMO LRU ---")
        lru = LRU(numero_quadros)
        lru.executar(sequencia)
        lru.exibir_resultado(pagina_procurada, sequencia)
        resultados_comparacao[nome_sequencia]['LRU'] = lru.numero_paginas_faltantes
        
        # Testa MRU
        print("\n--- ALGORITMO MRU ---")
        mru = MRU(numero_quadros)
        mru.executar(sequencia)
        mru.exibir_resultado(pagina_procurada, sequencia)
        resultados_comparacao[nome_sequencia]['MRU'] = mru.numero_paginas_faltantes
    
    # Exibe comparação geral
    print("\n" + "="*70)
    print("\nCOMPARAÇÃO GERAL - Page Faults por Algoritmo")
    print("="*70)
    for nome_seq, resultados in resultados_comparacao.items():
        print(f"\n{nome_seq}:")
        for algo, falhas in resultados.items():
            print(f"  {algo}: {falhas} page faults")
        
        melhor = min(resultados.items(), key=lambda x: x[1])
        print(f"  → Melhor: {melhor[0]} com {melhor[1]} page faults")

if __name__ == "__main__":
    executar_testes()