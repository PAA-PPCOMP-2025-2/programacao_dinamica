# Função para normalizar a lista de paineis
# (a, b): 'a' será sempre o maior lado
# Teste bem sucedido
def normalizacao(paineis):
    print(f"Vetor original: {paineis}")
    normalizar = []
    for a, b in paineis:
        if a < b:
            normalizar.append((b, a))
        else:
            normalizar.append((a, b))
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

# Função de validação da lista de paineis
# A lista é rejeitada se algum painel:
# tem lado menor que o mínimo
# é maior que a folha de MDF
# Teste bem sucedido
def validar_paineis(paineis, minimoComprimento, larguraMDF, alturaMDF):
    for (l, a) in paineis:
        if min(l, a) < minimoComprimento:
            print("Existe um painel com pelo menos um lado menor que o mínimo")
            return False

        # Verifica se o painel cabe na posição horizontal ou vertical
        cabe_horizontal = (l <= larguraMDF and a <= alturaMDF)
        cabe_vertical = (a <= larguraMDF and l <= alturaMDF)
        cabe = (cabe_horizontal or cabe_vertical)

        # Se não couber em nenhuma posição
        if not cabe:
            print (f"Painel {l}x{a} não cabe na folha de MDF {larguraMDF}x{alturaMDF}")
            return False

    print("Individualmente cada painel cabe na folha de MDF")
    return True

# Função de validação do somatório das áreas dos paineis
# A lista é rejeitada se o somatório alcança a área da folha menos um certo desperdício
# Teste bem sucedido
def validar_area(paineis, larguraMDF, alturaMDF):
    # Fator de desperdício
    fator_desperdicio = 0.1
    area_mdf = larguraMDF * alturaMDF
    area_paineis = sum(largura * altura for largura, altura in paineis)

    if not area_paineis <= area_mdf * (1 - fator_desperdicio):
        print(f"Área dos painéis ({area_paineis} cm²) excede a área disponível considerando {(fator_desperdicio*100):.0f}% de desperdício.")
        return False
    
    print(f"Paineis validados")
    return True  # Os paineis cabem na folha de MDF

def optimize_cuts(paineis):
    minimoComprimento = 10
    serra = 2
    larguraMDF = 183
    alturaMDF = 275
    memoria = {}

    ordenados = ordenar_primeira_posicao(paineis)
    if not (validar_paineis(ordenados, minimoComprimento, larguraMDF, alturaMDF) and 
            validar_area(ordenados, larguraMDF, alturaMDF)):
        return []# Retorna lista vazia em vez de None

    def corte(L, A, paineis_restantes, usados=None):
        if usados is None:
            usados = set()
        # Simplificar para apenas dimensões, removendo índices desnecessários para teste
        paineis_restantes = [p for i, p in enumerate(paineis_restantes) if i not in usados]
        if not paineis_restantes:
            return 0, [], 0  # Valor, plano, área usada

        chave = (L, A, tuple(paineis_restantes))  # Usar tupla para memoização
        if chave in memoria:
            return memoria[chave]

        melhor_valor = 0
        melhor_plano = []
        max_area = 0
        for (l, a) in paineis_restantes:
            encaixou = False

            for rotacionado, (largura, altura) in enumerate([(l, a), (a, l)]):
                if largura <= L and altura <= A:
                    encaixou = True

                    if largura == L and altura == A:
                        memoria[chave] = (1, [(0, 0, largura, altura, rotacionado)], largura * altura)
                        return 1, [(0, 0, largura, altura, rotacionado)], largura * altura

                    # Corte vertical
                    if largura < L:
                        sobra1_L = L - largura - serra
                        sobra1_A = altura
                        sobra2_L = L
                        sobra2_A = A - altura - serra
                        valor1, plano1, area1 = (0, [], 0)
                        if sobra1_L >= minimoComprimento and sobra1_A >= minimoComprimento:
                            valor1, plano1, area1 = corte(sobra1_L, sobra1_A, paineis_restantes, {0})  # Usar primeiro painel como usado
                        valor2, plano2, area2 = (0, [], 0)
                        if sobra2_L >= minimoComprimento and sobra2_A >= minimoComprimento:
                            valor2, plano2, area2 = corte(sobra2_L, sobra2_A, paineis_restantes, {0})
                        valor_atual = 1 + valor1 + valor2
                        area_atual = largura * altura + area1 + area2
                        plano_atual = [(0, 0, largura, altura, rotacionado)] + \
                                     [(largura + serra + x, y, w, h, r) for x, y, w, h, r in plano1] + \
                                     [(x, altura + serra + y, w, h, r) for x, y, w, h, r in plano2]
                        if area_atual > max_area:
                            max_area = area_atual
                            melhor_valor = valor_atual
                            melhor_plano = plano_atual

                    # Corte horizontal
                    if altura < A:
                        sobra1_L = largura
                        sobra1_A = A - altura - serra
                        sobra2_L = L - largura - serra
                        sobra2_A = altura
                        valor1, plano1, area1 = (0, [], 0)
                        if sobra1_L >= minimoComprimento and sobra1_A >= minimoComprimento:
                            valor1, plano1, area1 = corte(sobra1_L, sobra1_A, paineis_restantes, {0})
                        valor2, plano2, area2 = (0, [], 0)
                        if sobra2_L >= minimoComprimento and sobra2_A >= minimoComprimento:
                            valor2, plano2, area2 = corte(sobra2_L, sobra2_A, paineis_restantes, {0})
                        valor_atual = 1 + valor1 + valor2
                        area_atual = largura * altura + area1 + area2
                        plano_atual = [(0, 0, largura, altura, rotacionado)] + \
                                     [(x, altura + serra + y, w, h, r) for x, y, w, h, r in plano1] + \
                                     [(largura + serra + x, y, w, h, r) for x, y, w, h, r in plano2]
                        if area_atual > max_area:
                            max_area = area_atual
                            melhor_valor = valor_atual
                            melhor_plano = plano_atual

        if not encaixou:
            memoria[chave] = (0, [], 0)
            return 0, [], 0

        memoria[chave] = (melhor_valor, melhor_plano, max_area)
        return melhor_valor, melhor_plano, max_area

    # Múltiplas tábuas
    tabuas = []
    paineis_restantes = list(ordenados)
    total_area_mdf = larguraMDF * alturaMDF
    while paineis_restantes:
        valor, plano, area = corte(larguraMDF, alturaMDF, paineis_restantes)
        if valor == 0:
            break
        tabuas.append({
            'num_cortes': len(plano) - 1,
            'num_retalhos': 1,  # Ajustar: contar sub-áreas vazias
            'area_retalhos': total_area_mdf - area,
            'cortes': plano  # (x, y, l, a, rotated)
        })
        # Remover o painel usado (primeiro da iteração)
        if plano:
            paineis_restantes = paineis_restantes[1:] if len(paineis_restantes) > 1 else []

    return tabuas

# Teste
#paineis = [(50, 60), (50, 40), (50, 90)]
paineis = [(184, 275), (183, 276)] # nenhum cabe
#paineis = [(184, 275), (183, 276), (50, 60)] # pelo menos um cabe
#paineis = [(184, 275), (50, 60), (183, 276)] # pelo menos um cabe
#paineis = [(50, 60), (184, 275), (183, 276)] # pelo menos um cabe
resultado = optimize_cuts(paineis)
for i, t in enumerate(resultado, 1):
    print(f"Tábua {i}:")
    print(f"  Número de cortes: {t['num_cortes']}")
    print(f"  Número de retalhos: {t['num_retalhos']}")
    print(f"  Área dos retalhos: {t['area_retalhos']} cm²")
    print(f"  Cortes: {t['cortes']}")














