import os
import subprocess
import platform
import colorama
from colorama import Fore, Style

def install_dependencies():
    """Instala todas as dependencias necessarias para o script principal rodar."""
    dependencies = ["scapy", "colorama", "wifi"]
    
    for dep in dependencies:
        try:
            subprocess.check_call(["pip", "install", dep])
            print(f"{Fore.GREEN}✔ {dep} instalado com sucesso!{Style.RESET_ALL}")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}❌ Erro ao instalar {dep}.{Style.RESET_ALL}")

def list_wifi_networks():
    """Lista as redes Wi-Fi disponiveis no Windows."""
    try:
        result = subprocess.check_output("netsh wlan show networks mode=bssid", shell=True, encoding="utf-8")
        print(f"{Fore.CYAN}{result}{Style.RESET_ALL}")
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}❌ Erro ao listar redes Wi-Fi.{Style.RESET_ALL}")

if __name__ == "__main__":
    if platform.system() != "Windows":
        print(f"{Fore.YELLOW}⚠ Este script foi feito para Windows.{Style.RESET_ALL}")
    else:
        print(f"{Fore.BLUE}🔍 Listando redes Wi-Fi disponiveis...{Style.RESET_ALL}")
        list_wifi_networks()
        install_dependencies()
