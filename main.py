# Função para normalizar a lista de paineis
# (a, b): 'a' será sempre o maior lado
# Teste bem sucedido
def normalizacao(paineis):
    print(f"Vetor original: {paineis}")
    normalizar = []
    for a, b in paineis:
        if a < b:
            normalizar.append((b,a))
        else:
            normalizar.append((a,b))
    print(f"Vetor normalizado: {normalizar}")
    return normalizar

# Função para ordenar a lista de paineis
# Ordem decrescente
# (a, b): 'a' é o parâmetro de comparação
# Teste bem sucedido
def ordenar_primeira_posicao(paineis):
    normalizado = normalizacao(paineis)
    ordenado = sorted(normalizado, key=lambda x: x[0], reverse=True)
    print(f"Vetor ordenado: {ordenado}")
    return ordenado

# Função de validação da lista de painels
# A lista é rejeitada se algum painel:
# tem lado menor que o mínimo
# é maior que a folha de MDF
# Teste bem sucedido
def validar_paineis (paineis):
    for (l, a) in paineis:
        if min(l,a) < minimoComprimento:
            print("Existe um painel com pelo menos um lado menor que o mínimo")
            return False

        # Verifica se o painel cabe na posição horizontal ou vertical
        cabe_horizontal = (l <= larguraMDF and a <= alturaMDF)
        cabe_vertical = (a <= larguraMDF and l <= alturaMDF)
        cabe = (cabe_horizontal or cabe_vertical)

        # Se não couber em nenhuma posição
        if not cabe:
            print("Pelo menos um painel não cabe na folha de MDF")
            return False

    print(f"Individualmente cada painel cabe na folha de MDF")
    return True # Os paineis preenchem os requisitos

# Função de validação do somatório das áreas dos paineis
# A lista é rejeitada se o somatório alcança a aéra da folha menos um certo desperdício
# Teste bem sucedido
def validar_area(paineis):
    # Fator de desperdício
    fator_desperdicio = 0.1
    area_mdf = larguraMDF * alturaMDF
    area_paineis = sum (largura * altura for largura, altura in paineis)

    if not area_paineis <= area_mdf * (1 - fator_desperdicio):
        print(f"Os paineis não cabem na folha de MDF consiretando um desperdício de {(fator_desperdicio*100):.0f}.%")
        return False
    print(f"Paineis validados")
    return True # Os paineis cabem na folha de MDF

# Função recursiva de corte
# L: largura atual
# A: Altura atual
# Painéis restantes
# Memória no formato de tuplas (imutável)
# Essa função só deve ser utilizada se os paineis forem validados
# Retorno
# Valor: quantidade de paineis encaixados
# Plano: lista detalhada do plano de corte
def corte(L, A, paineis, memoria):
    # Converte em tuploa para garantir a imutabilidade da chave
    paineis = tuple(paineis)

    # Caso base: lista de paineis vazia
    if not paineis:
        return 0, []

    # Cria uma chave para ser memorizada
    chave = (L, A, paineis)
    if chave in memoria:
        return memoria[chave]

    melhor_valor = 0
    melhor_plano = []

    # Pega o primeiro painel
    largura, altura = paineis[0]
    # Armazena os paineis restantes
    paineis_restantes = paineis[1:]

    # Flag para indicar se ao menos um painel encaixou
    encaixou = False

    # Testa o painel nas duas orientações
    for rotacionado in [False, True]:
        if rotacionado:
            # Troca largura e altura
            l_painel, a_painel = altura, largura
        else:
            l_painel, a_painel = largura, altura

        # Verifica se o painel cabe na folha atual (sobra)
        if l_painel <= L and a_painel <= A:
            encaixou = True

            # Caminho 1:
            # Corte vertical se o painel não ocupa toda a largura da folha
            if l_painel < L:
                sobra_direita_L = L - l_painel - serra
                sobra_direita_A = a_painel
                sobra_baixo_L = L
                sobra_baixo_A = A - a_painel - serra

                # Sobra direita
                valor1, plano1 = 0, []
                if sobra_direita_L >= minimoComprimento and sobra_direita_A >= minimoComprimento:
                    valor1, plano1 = corte(sobra_direita_L, sobra_direita_A, paineis_restantes, memoria)

                # Sobra de baixo
                valor2, plano2 = 0, []
                if sobra_baixo_L >= minimoComprimento and sobra_baixo_A >= minimoComprimento:
                    valor2, plano2 = corte(sobra_baixo_L, sobra_baixo_A, paineis_restantes, memoria)

                # Armazena o total de paineis encaixados
                valor_atual = 1 + valor1 + valor2
                plano_atual = [((l_painel, a_painel), rotacionado, sobra_direita_L, sobra_baixo_A)] + plano1 + plano2

                if valor_atual > melhor_valor:
                    melhor_valor = valor_atual
                    melhor_plano = plano_atual

            # Caminho 2:
            # Corte horizontal se o painel não ocupa toda a altura da folha
            if a_painel < A:
                sobra_direita_L = L - l_painel - serra
                sobra1_A = A
                sobra_baixo_L = l_painel
                sobra_baixo_A = A - a_painel - serra

                valor1, plano1 = 0, []
                if sobra_direita_L >= minimoComprimento and sobra_direita_A >= minimoComprimento:
                    valor1, plano1 = corte(sobra_direita_L, sobra_direita_A, paineis_restantes, memoria)

                valor2, plano2 = 0, []
                if sobra_baixo_L >= minimoComprimento and sobra_baixo_A >= minimoComprimento:
                    valor2, plano2 = corte(sobra_baixo_L, sobra_baixo_A, paineis_restantes, memoria)

                valor_atual = 1 + valor1 + valor2
                plano_atual = [((l_painel, a_painel), rotacionado, sobra_direita_L, sobra_baixo_A)] + plano1 + plano2

                if valor_atual > melhor_valor:
                    melhor_valor = valor_atual
                    melhor_plano = plano_atual

  # Caso especial: painel ocupa toda a área
            if l_painel == L and a_painel == A:
                valor_atual = 1
                plano_atual = [((l_painel, a_painel), rotacionado, 0, 0)]
                
                valor_restante, plano_restante = corte(0, 0, paineis_restantes, memoria)
                valor_atual += valor_restante
                plano_atual += plano_restante
                
                if valor_atual > melhor_valor:
                    melhor_valor = valor_atual
                    melhor_plano = plano_atual
    
    # Se não encaixou, retorna zero e lista vazia
    if not encaixou:
        valor_restante, plano_restante = corte(L, A, paineis_restantes, memoria)
        memoria[chave] = (valor_restante, plano_restante)
        return valor_restante, plano_restante


    # Solução ótima para este subproblema
    memoria[chave] = (melhor_valor, melhor_plano)
    return melhor_valor, melhor_plano

# As medidas serão sempre em centímetros

# Lista de paineis de corte
# paineis = [(50, 60),(50, 40), (50, 90)]

# Menor dimensão que um lado pode ter
minimoComprimento = 10

# Largura da serra
serra = 2

# Dimensões da folha de MDF
larguraMDF = 183
alturaMDF = 275

# Memória
memoria = {}

# Casos de testes
#paineis = [(183, 275)] # cabe e não executa corte
paineis = [(50, 60),(50, 40), (50, 90)] # todos cabem
#paineis = [(184, 275), (183, 276)] # nenhum cabe
#paineis = [(184, 275), (183, 276), (50, 60)] # pelo menos um cabe
#paineis = [(184, 275), (50, 60), (183, 276)] # pelo menos um cabe
#paineis = [(50, 60), (184, 275), (183, 276)] # pelo menos um cabe

# Chama a função de corte
total_paineis, plano_corte = corte(larguraMDF, alturaMDF, paineis, memoria)

# Pré-processamento: ordenar e validar
paineis_ordenados = ordenar_primeira_posicao(paineis)

if validar_paineis(paineis_ordenados) and validar_area(paineis_ordenados):
    # Chama a função de corte
    total_paineis, plano_corte = corte(larguraMDF, alturaMDF, paineis_ordenados, memoria)

    # Imprime resultado
    print(f"\nTotal de painéis encaixados: {total_paineis}")
    print("Plano de corte:")
    
    for i, entrada in enumerate(plano_corte, 1):
        if len(entrada) >= 4:
            dimensoes, rotacionado, sobra_dir, sobra_baixo = entrada
            print(f"Painel {i}: Dimensões {dimensoes} {'(rotacionado)' if rotacionado else ''}")
            print(f"  Sobra à direita: {sobra_dir}cm, Sobra abaixo: {sobra_baixo}cm")
        else:
            print(f"Entrada inválida no plano: {entrada}")
else:
    print("Paineis não validados - não é possível gerar plano de corte")

# Imprime resultado
print(f"Total de painéis encaixados: {total_paineis}")
print("Plano de corte:")

for entrada in plano_corte:
    # estrutura: ((p_l, p_a), corte_vertical, corte_horizontal)
    corte_v, corte_h = entrada
    print(f"  Corte vertical em: {corte_v if corte_v is not None else 'sem corte vertical'}")
    print(f"  Corte horizontal em: {corte_h if corte_h is not None else 'sem corte horizontal'}\n")














