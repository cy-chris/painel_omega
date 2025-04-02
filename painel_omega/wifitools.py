import os
import subprocess
import platform
import time
import random
import colorama
from colorama import Fore, Style

def change_mac():
    """Altera o endereco MAC para protecao."""
    new_mac = "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    try:
        interface = "wlan0"
        subprocess.run(["ifconfig", interface, "down"], check=True)
        subprocess.run(["ifconfig", interface, "hw", "ether", new_mac], check=True)
        subprocess.run(["ifconfig", interface, "up"], check=True)
        print(f"{Fore.GREEN}✔ MAC Address alterado para: {new_mac}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Erro ao alterar MAC: {e}{Style.RESET_ALL}")

def list_wifi_networks():
    """Lista redes Wi-Fi disponiveis."""
    try:
        result = subprocess.check_output(["nmcli", "device", "wifi", "list"], encoding="utf-8")
        print(f"{Fore.CYAN}{result}{Style.RESET_ALL}")
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}❌ Erro ao listar redes Wi-Fi.{Style.RESET_ALL}")

def check_wps():
    """Verifica se uma rede tem WPS ativado usando wash."""
    try:
        result = subprocess.check_output(["wash", "-i", "wlan0mon", "-C"], encoding="utf-8")
        print(f"{Fore.YELLOW}{result}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Erro ao verificar WPS: {e}{Style.RESET_ALL}")

def capture_handshake():
    """Captura handshake WPA2."""
    print(f"{Fore.BLUE}🔍 Iniciando captura de handshake...{Style.RESET_ALL}")
    try:
        subprocess.run(["airodump-ng", "wlan0mon"], check=True)
    except Exception as e:
        print(f"{Fore.RED}❌ Erro ao capturar handshake: {e}{Style.RESET_ALL}")

def brute_force_attack():
    """Executa ataque de forca bruta WPA2 usando aircrack-ng."""
    wordlist = input(f"{Fore.YELLOW}Digite o caminho da wordlist: {Style.RESET_ALL}")
    handshake_file = input(f"{Fore.YELLOW}Digite o caminho do arquivo de handshake: {Style.RESET_ALL}")
    try:
        subprocess.run(["aircrack-ng", "-w", wordlist, "-b", "00:11:22:33:44:55", handshake_file], check=True)
    except Exception as e:
        print(f"{Fore.RED}❌ Erro no ataque de forca bruta: {e}{Style.RESET_ALL}")

def menu():
    """Menu interativo."""
    while True:
        print(f"\n{Fore.MAGENTA}=== Ferramenta de Auditoria Wi-Fi ==={Style.RESET_ALL}")
        print("1. Listar redes Wi-Fi")
        print("2. Verificar vulnerabilidade WPS")
        print("3. Capturar Handshake WPA2")
        print("4. Alterar MAC Address para protecao")
        print("5. Ataque de forca bruta WPA2")
        print("6. Sair")
        
        escolha = input(f"{Fore.YELLOW}Selecione uma opção: {Style.RESET_ALL}")
        
        if escolha == "1":
            list_wifi_networks()
        elif escolha == "2":
            check_wps()
        elif escolha == "3":
            capture_handshake()
        elif escolha == "4":
            change_mac()
        elif escolha == "5":
            brute_force_attack()
        elif escolha == "6":
            print(f"{Fore.CYAN}Saindo...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Opção inválida!{Style.RESET_ALL}")

if __name__ == "__main__":
    if platform.system() != "Linux":
        print(f"{Fore.YELLOW}⚠ Este script foi feito para Linux.{Style.RESET_ALL}")
    else:
        colorama.init()
        menu()
