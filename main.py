# Importa a função randint para gerar números aleatórios (não usada no código atual)
from random import randint

# Lista que armazena todos os NPCs criados no jogo
lista_npcs = []

# Dicionário que representa o jogador com todas suas características
player = {
    "nome": "William",        # Nome do jogador
    "level": 1,              # Nível atual do jogador
    "exp": 0,                # Experiência atual do jogador
    "exp_max": 50,           # Experiência necessária para subir de nível
    "hp": 100,               # Pontos de vida atuais
    "hp_max": 100,           # Pontos de vida máximos
    "dano": 25,              # Dano que o jogador causa por ataque
}

# Função responsável por criar um novo NPC com base no level fornecido
def criar_npc(level):
    """
    Cria um novo NPC (monstro) com atributos baseados no level
    - Quanto maior o level, mais forte o NPC será
    """
    novo_npc = {
        "nome": f"Monstro #{level}#",      # Nome único baseado no level
        "level": level,                    # Level do NPC
        "dano": 5 * level,                # Dano cresce proporcionalmente ao level
        "hp": 100 * level,                # HP cresce proporcionalmente ao level
        "hp_max": 100 * level,            # HP máximo (para restauração)
        "exp": 7 * level,                 # EXP que o jogador ganha ao derrotar este NPC
    }
    return novo_npc

# Função que gera uma quantidade específica de NPCs e os adiciona na lista
def gerar_npcs(n_npcs):
    """
    Gera 'n_npcs' quantidade de NPCs, cada um com level crescente (1, 2, 3...)
    """
    for n in range(n_npcs):
        npc = criar_npc(n + 1)  # Cria NPC com level n+1 (começa do level 1)
        lista_npcs.append(npc)   # Adiciona o NPC na lista global

# Função que exibe todos os NPCs da lista
def exibir_npcs():
    """Percorre a lista de NPCs e exibe as informações de cada um"""
    for npc in lista_npcs:
        exibir_npc(npc)

# Função que exibe as informações de um NPC específico
def exibir_npc(npc):
    """Mostra todas as características do NPC de forma formatada"""
    print(f"NPC: {npc['nome']} | Level: {npc['level']} | Dano: {npc['dano']} | HP: {npc['hp']} | EXP: {npc['exp']}")

# Função que exibe as informações do jogador
def exibir_player():
    """Mostra todas as características do jogador de forma formatada"""
    print(f"Player: {player['nome']} | Level: {player['level']} | Dano: {player['dano']} | HP: {player['hp']}/{player['hp_max']} | EXP: {player['exp']}/{player['exp_max']}")

# Função que restaura o HP do jogador para o máximo
def reset_player():
    """Restaura o HP do jogador para o valor máximo (usado após batalhas)"""
    player["hp"] = player["hp_max"]

# Função que restaura o HP de um NPC para o máximo
def reset_npc(npc):
    """Restaura o HP do NPC para o valor máximo (reutilização do mesmo NPC)"""
    npc["hp"] = npc["hp_max"]

# Função que gerencia o sistema de level up do jogador
def level_up():
    """
    Verifica se o jogador tem EXP suficiente para subir de level
    - Pode subir múltiplos levels se tiver EXP suficiente
    - Aumenta atributos do jogador a cada level ganho
    - Restaura HP completamente ao subir de level
    """
    # Loop que continua enquanto o jogador tiver EXP suficiente para subir de level
    while player["exp"] >= player["exp_max"]:
        player["level"] += 1                           # Aumenta o level em 1
        player["exp"] -= player["exp_max"]             # Subtrai a EXP usada (mantém o excesso)
        player["exp_max"] = int(player["exp_max"] * 1.5)  # Aumenta EXP necessária para próximo level
        player["hp_max"] += 20                         # Aumenta HP máximo em 20
        player["dano"] += 5                            # Aumenta dano em 5
        player["hp"] = player["hp_max"]                # Restaura HP para o novo máximo
        
        # Exibe informações sobre o level up
        print(f"🎉 LEVEL UP! {player['nome']} agora é level {player['level']}!")
        print(f"💪 Novo HP máximo: {player['hp_max']}")
        print(f"⚔️ Novo dano: {player['dano']}")

# Função principal que gerencia uma batalha completa entre jogador e NPC
def iniciar_batalha(npc):
    """
    Controla todo o fluxo de uma batalha:
    1. Inicia a batalha
    2. Loop de combate (jogador e NPC se atacam)
    3. Determina vencedor
    4. Aplica consequências (EXP, level up, etc.)
    5. Reseta HP de ambos os personagens
    """
    # Cabeçalho da batalha
    print(f"\n⚔️ BATALHA INICIADA contra {npc['nome']}!")
    print("-" * 50)
    
    # Loop principal da batalha - continua enquanto ambos estiverem vivos
    while player["hp"] > 0 and npc["hp"] > 0:
        atacar_npc(npc)           # Jogador ataca o NPC
        if npc["hp"] > 0:         # NPC só contra-ataca se ainda estiver vivo
            atacar_player(npc)    # NPC ataca o jogador
        exibir_info_batalha(npc)  # Mostra status atual da batalha
        print("-" * 30)

    # Verifica quem venceu a batalha
    if player["hp"] > 0:
        # Jogador venceu - ganha EXP e possivelmente sobe de level
        print(f"🏆 Monstro derrotado! Ganhou: {npc['exp']} de EXP!")
        player["exp"] += npc["exp"]  # Adiciona EXP ganho ao jogador
        level_up()                   # Verifica e aplica level up se necessário
        exibir_player()              # Mostra status atualizado do jogador
    else:
        # Jogador perdeu
        print(f"💀 Você foi derrotado pelo {npc['nome']}")
        exibir_npc(npc)

    # Restaura HP de ambos personagens para próximas batalhas
    reset_player()  # Restaura HP do jogador
    reset_npc(npc)  # Restaura HP do NPC
    print("=" * 50)

# Função que executa o ataque do jogador contra um NPC
def atacar_npc(npc):
    """
    Processa o ataque do jogador:
    - Calcula dano real causado (não excede HP restante)
    - Reduz HP do NPC
    - Exibe mensagem do ataque
    """
    dano_causado = min(player["dano"], npc["hp"])    # Dano real (não maior que HP restante)
    npc["hp"] = max(0, npc["hp"] - player["dano"])   # Reduz HP (mínimo 0)
    print(f"🗡️ {player['nome']} atacou {npc['nome']} causando {dano_causado} de dano!")

# Função que executa o ataque do NPC contra o jogador
def atacar_player(npc):
    """
    Processa o ataque do NPC:
    - Calcula dano real causado (não excede HP restante)
    - Reduz HP do jogador
    - Exibe mensagem do ataque
    """
    dano_causado = min(npc["dano"], player["hp"])      # Dano real (não maior que HP restante)
    player["hp"] = max(0, player["hp"] - npc["dano"])  # Reduz HP (mínimo 0)
    print(f"👹 {npc['nome']} atacou {player['nome']} causando {dano_causado} de dano!")

# Função que exibe o status atual da batalha
def exibir_info_batalha(npc):
    """Mostra HP atual do jogador e do NPC durante a batalha"""
    print(f"Player: {player['nome']} | HP: {player['hp']}/{player['hp_max']}")
    print(f"NPC: {npc['nome']} | HP: {npc['hp']}/{npc['hp_max']}")

# ==================== EXECUÇÃO DO JOGO ====================
# Esta seção é onde o jogo realmente executa

print("🎮 INICIANDO JOGO RPG")
print("=" * 50)

# Gera 5 NPCs (Monstro #1#, Monstro #2#, etc.) e os adiciona na lista
gerar_npcs(5)

# Exibe status inicial do jogador
exibir_player()

# Seleciona o primeiro NPC da lista (Monstro #1#) para as batalhas
npc_selecionado = lista_npcs[0]

# Executa 5 batalhas consecutivas contra o mesmo NPC
# Cada batalha: jogador luta → ganha EXP → possivelmente sobe de level → HP resetado
for i in range(8):
    print(f"\n🔄 BATALHA {i+1}/5")  # Mostra qual batalha está acontecendo
    iniciar_batalha(npc_selecionado)  # Executa a batalha

# Exibe informações finais após todas as batalhas
print(f"\n🏁 JOGO FINALIZADO!")
print("Status final do jogador:")
exibir_player()  # Mostra como o jogador está após todas as batalhas