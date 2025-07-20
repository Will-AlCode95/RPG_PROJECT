from random import randint

lista_npcs = []

player = {
   "nome": "William",
   "level": 1,
   "exp": 0,
   "exp_max": 50,
    "hp": 100,
    "hp_max": 100,
    "dano": 25,
}


def criar_npc(level):
    novo_npc = {  # cria um nps aletoriamente
        "nome": f"Monstro #{level}#",
        "level": level,
        "dano": 5 * level,  # dano do monstro varia de acordo ao level
        "hp": 100 * level,
        "exp": 7 * level,
    }

    return novo_npc


def gerar_npcs(n_npcs):
    for n in range(n_npcs):
        npc = criar_npc(n + 1)
        lista_npcs.append(npc)
        

def exibir_npcs():
  for npc in lista_npcs:
    print(
        f"Nome: {npc['nome']} | Level: {npc['level']} | Dano: {npc['dano']} | HP: {npc['hp']} |  EXP: {npc["exp"]}")

def atacar_npc(npc):
    npc["hp"] -= player["dano"] # hp inimigo - dano do player

gerar_npcs(5)
exibir_npcs()

npc_selecionado = lista_npcs[0]

print("NPC selecionado:", npc_selecionado)
atacar_npc(npc_selecionado)

print("NPC sofreu ataque:", npc_selecionado)




