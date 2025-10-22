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
        print(f"Total de page faults: {self.numero_paginas_faltantes}")
        
        # Encontra em qual quadro está a página procurada
        if pagina_procurada in self.quadros_memoria:
            quadro = self.quadros_memoria.index(pagina_procurada)
            print(f"✓ Página {pagina_procurada} está no quadro: {quadro}")
        else:
            print(f"✗ Página {pagina_procurada} não está na memória no final da execução")
    
    def exibir_passo_a_passo(self):
        """Exibe o histórico completo de estados da memória"""
        print("\n" + "="*80)
        print("EXECUÇÃO PASSO A PASSO")
        print("="*80)
        for passo, estado in enumerate(self.historico_estado, 1):
            print(f"Passo {passo}: {estado}")
        print("="*80)

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
        
        print("\n--- Iniciando execução FIFO ---")
        
        for idx, pagina in enumerate(sequencia_paginas, 1):
            print(f"\nPasso {idx}: Acessando página {pagina}")
            
            # Se a página já está na memória, continua
            if pagina in self.quadros_memoria:
                print(f"  ✓ Página {pagina} já está na memória (HIT)")
                print(f"  Estado da memória: {self.quadros_memoria}")
                continue
            
            # Page fault ocorreu
            self.numero_paginas_faltantes += 1
            print(f"  ✗ Page Fault! Página {pagina} não está na memória")
            
            # Se há espaço disponível, adiciona a página
            if len(self.quadros_memoria) < self.numero_quadros:
                self.quadros_memoria.append(pagina)
                fila_substituicao.append(pagina)
                print(f"  → Adicionando página {pagina} no quadro {len(self.quadros_memoria)-1}")
            else:
                # Remove a página mais antiga (FIFO)
                pagina_removida = fila_substituicao.popleft()
                quadro_removido = self.quadros_memoria.index(pagina_removida)
                self.quadros_memoria.remove(pagina_removida)
                self.quadros_memoria.append(pagina)
                fila_substituicao.append(pagina)
                print(f"  → Removendo página {pagina_removida} do quadro {quadro_removido} (mais antiga)")
                print(f"  → Adicionando página {pagina} no quadro {quadro_removido}")
            
            print(f"  Estado da memória: {self.quadros_memoria}")
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
        
        print("\n--- Iniciando execução LRU ---")
        
        for idx, pagina in enumerate(sequencia_paginas, 1):
            tempo_atual += 1
            print(f"\nPasso {idx}: Acessando página {pagina}")
            
            # Se a página já está na memória, atualiza seu tempo de uso
            if pagina in self.quadros_memoria:
                tempo_ultimo_uso[pagina] = tempo_atual
                print(f"  ✓ Página {pagina} já está na memória (HIT)")
                print(f"  → Atualizando timestamp da página {pagina} para {tempo_atual}")
                print(f"  Estado da memória: {self.quadros_memoria}")
                continue
            
            # Page fault ocorreu
            self.numero_paginas_faltantes += 1
            print(f"  ✗ Page Fault! Página {pagina} não está na memória")
            
            # Se há espaço disponível, adiciona a página
            if len(self.quadros_memoria) < self.numero_quadros:
                self.quadros_memoria.append(pagina)
                tempo_ultimo_uso[pagina] = tempo_atual
                print(f"  → Adicionando página {pagina} no quadro {len(self.quadros_memoria)-1}")
            else:
                # Remove a página menos recentemente usada
                pagina_menos_usada = min(self.quadros_memoria, 
                                        key=lambda p: tempo_ultimo_uso.get(p, 0))
                quadro_removido = self.quadros_memoria.index(pagina_menos_usada)
                print(f"  → Removendo página {pagina_menos_usada} do quadro {quadro_removido} (menos recentemente usada, timestamp: {tempo_ultimo_uso.get(pagina_menos_usada, 0)})")
                
                self.quadros_memoria.remove(pagina_menos_usada)
                del tempo_ultimo_uso[pagina_menos_usada]
                
                self.quadros_memoria.append(pagina)
                tempo_ultimo_uso[pagina] = tempo_atual
                print(f"  → Adicionando página {pagina} no quadro {quadro_removido}")
            
            print(f"  Estado da memória: {self.quadros_memoria}")
            print(f"  Timestamps: {tempo_ultimo_uso}")
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
        
        print("\n--- Iniciando execução MRU ---")
        
        for idx, pagina in enumerate(sequencia_paginas, 1):
            tempo_atual += 1
            print(f"\nPasso {idx}: Acessando página {pagina}")
            
            # Se a página já está na memória, atualiza seu tempo de uso
            if pagina in self.quadros_memoria:
                tempo_ultimo_uso[pagina] = tempo_atual
                print(f"  ✓ Página {pagina} já está na memória (HIT)")
                print(f"  → Atualizando timestamp da página {pagina} para {tempo_atual}")
                print(f"  Estado da memória: {self.quadros_memoria}")
                continue
            
            # Page fault ocorreu
            self.numero_paginas_faltantes += 1
            print(f"  ✗ Page Fault! Página {pagina} não está na memória")
            
            # Se há espaço disponível, adiciona a página
            if len(self.quadros_memoria) < self.numero_quadros:
                self.quadros_memoria.append(pagina)
                tempo_ultimo_uso[pagina] = tempo_atual
                print(f"  → Adicionando página {pagina} no quadro {len(self.quadros_memoria)-1}")
            else:
                # Remove a página mais recentemente usada
                pagina_mais_usada = max(self.quadros_memoria, 
                                       key=lambda p: tempo_ultimo_uso.get(p, 0))
                quadro_removido = self.quadros_memoria.index(pagina_mais_usada)
                print(f"  → Removendo página {pagina_mais_usada} do quadro {quadro_removido} (mais recentemente usada, timestamp: {tempo_ultimo_uso.get(pagina_mais_usada, 0)})")
                
                self.quadros_memoria.remove(pagina_mais_usada)
                del tempo_ultimo_uso[pagina_mais_usada]
                
                self.quadros_memoria.append(pagina)
                tempo_ultimo_uso[pagina] = tempo_atual
                print(f"  → Adicionando página {pagina} no quadro {quadro_removido}")
            
            print(f"  Estado da memória: {self.quadros_memoria}")
            print(f"  Timestamps: {tempo_ultimo_uso}")
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
    
    # Pergunta ao usuário qual visualização deseja
    print("="*80)
    print("SISTEMA DE TESTE DE ALGORITMOS DE PAGINAÇÃO")
    print("="*80)
    print("\nEscolha o modo de execução:")
    print("1 - Visualização COMPLETA (passo a passo detalhado)")
    print("2 - Visualização RESUMIDA (apenas resultados finais)")
    
    try:
        opcao = input("\nDigite sua opção (1 ou 2): ").strip()
        modo_detalhado = (opcao == "1")
    except:
        print("\nOpção inválida. Executando em modo RESUMIDO.")
        modo_detalhado = False
    
    for nome_sequencia, (sequencia, pagina_procurada) in sequencias.items():
        print("\n" + "="*80)
        print(f"\n{nome_sequencia}")
        print("="*80)
        
        resultados_comparacao[nome_sequencia] = {}
        
        # Testa FIFO
        print("\n" + "="*80)
        print("ALGORITMO FIFO")
        print("="*80)
        fifo = FIFO(numero_quadros)
        if modo_detalhado:
            fifo.executar(sequencia)
        else:
            # Execução silenciosa para modo resumido
            import sys
            from io import StringIO
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            fifo.executar(sequencia)
            sys.stdout = old_stdout
        fifo.exibir_resultado(pagina_procurada, sequencia)
        resultados_comparacao[nome_sequencia]['FIFO'] = fifo.numero_paginas_faltantes
        
        # Testa LRU
        print("\n" + "="*80)
        print("ALGORITMO LRU")
        print("="*80)
        lru = LRU(numero_quadros)
        if modo_detalhado:
            lru.executar(sequencia)
        else:
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            lru.executar(sequencia)
            sys.stdout = old_stdout
        lru.exibir_resultado(pagina_procurada, sequencia)
        resultados_comparacao[nome_sequencia]['LRU'] = lru.numero_paginas_faltantes
        
        # Testa MRU
        print("\n" + "="*80)
        print("ALGORITMO MRU")
        print("="*80)
        mru = MRU(numero_quadros)
        if modo_detalhado:
            mru.executar(sequencia)
        else:
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            mru.executar(sequencia)
            sys.stdout = old_stdout
        mru.exibir_resultado(pagina_procurada, sequencia)
        resultados_comparacao[nome_sequencia]['MRU'] = mru.numero_paginas_faltantes
    
    # Exibe comparação geral
    print("\n" + "="*80)
    print("COMPARAÇÃO GERAL - Page Faults por Algoritmo")
    print("="*80)
    for nome_seq, resultados in resultados_comparacao.items():
        print(f"\n{nome_seq}:")
        for algo, falhas in resultados.items():
            print(f"  {algo}: {falhas} page faults")
        
        melhor = min(resultados.items(), key=lambda x: x[1])
        print(f"  → Melhor: {melhor[0]} com {melhor[1]} page faults")

if __name__ == "__main__":
    executar_testes()