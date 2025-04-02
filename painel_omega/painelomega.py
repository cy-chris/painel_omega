import os
import datetime
import requests
import time
import whois
import socket
import subprocess
import shutil
import re
from fastapi import FastAPI

VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
HAVEIBEENPWNED_API_KEY = os.getenv("HAVEIBEENPWNED_API_KEY")
CPF_API = os.getenv("http://ifind.chapada.com.br:7777/?token=20491c06-5675-4e06-b2ae-4e3fcda2abdd&cpf=")

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def salvar_log(texto):
    with open("log_varredura.txt", "a") as log:
        log.write(f"{datetime.datetime.now()} - {texto}\n")

def obter_resultado_virus_total(scan_id):
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    url = f"https://www.virustotal.com/api/v3/analyses/{scan_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("data", {}).get("attributes", {}).get("results", {})
    return None

# === Subpainel: Varredura de Malware ===
def scan_completo():
    limpar_tela()
    print("Iniciando varredura completa...\n")
    comando = ["C:\\Program Files\\Windows Defender\\MpCmdRun.exe", "-Scan", "-ScanType", "2"]
    subprocess.run(comando)
    print("Varredura completa finalizada!")
    salvar_log("Varredura completa realizada.")

def scan_arquivo():
    limpar_tela()
    arquivo = input("Digite o caminho do arquivo a ser escaneado: ").strip()
    
    if not os.path.exists(arquivo):
        print("Arquivo nao encontrado!")
        return
    
    # Verifica se o clamscan está instalado
    if shutil.which("clamscan") is None:
        print("ClamAV nao encontrado no sistema!")
        return
    
    print(f"Escaneando: {arquivo}\n")
    comando = f"clamscan {arquivo}"
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    
    if "Infected files: 0" in resultado.stdout:
        print("Arquivo limpo!")
    else:
        print("Arquivo infectado!")
        print(resultado.stdout)
    
    salvar_log(f"Varredura realizada no arquivo: {arquivo}")

def scan_link():
    limpar_tela()
    url = input("Digite a URL a ser analisada: ").strip()
    
    if not url.startswith(("http://", "https://")):
        print("URL invalida! Certifique-se de incluir 'http://' ou 'https://'.")
        return
    
    print(f"Enviando URL para analise: {url}\n")
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    data = {"url": url}
    response = requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data=data)
    
    if response.status_code == 200:
        scan_id = response.json()["data"]["id"]
        print(f"URL enviada para analise! ID do escaneamento: {scan_id}")
        salvar_log(f"Varredura de link enviada: {url}")
        
        time.sleep(5)
        resultado = obter_resultado_virus_total(scan_id)
        if resultado:
            print("\n=== RESULTADO DA VARREDURA ===")
            for engine, data in resultado.items():
                print(f"{engine}: {'Malicioso' if data['category'] == 'malicious' else 'Seguro'}")
            salvar_log(f"Resultado da varredura de {url}: {resultado}")
        else:
            print("Nao foi possivel obter o resultado da varredura.")
    else:
        print("Erro ao enviar URL para analise.")

# === Subpainel: Ferramentas ===
def rastrear_ip():
    limpar_tela()
    ip = input("Digite o endereco IP para rastrear: ").strip()
    
    try:
        host = socket.gethostbyaddr(ip)
        print(f"Hostname associado: {host[0]}")
        salvar_log(f"Rastreamento de IP {ip} - Hostname: {host[0]}")
    except socket.herror as e:
        print(f"Erro ao rastrear IP: {e}")
    except socket.gaierror as e:
        print(f"Erro ao rastrear IP: {e}")

def rastrear_dominio():
    limpar_tela()
    dominio = input("Digite o dominio para rastrear: ").strip()
    
    dominio = re.sub(r'^https?://', '', dominio).strip('/')
    
    try:
        ip = socket.gethostbyname(dominio)
        print(f"Endereco IP: {ip}\n")
        salvar_log(f"Rastreamento de {dominio} - IP: {ip}")
        
        info = whois.whois(dominio)
        print("=== Informacoes WHOIS ===")
        print(f"Nome do dominio: {info.domain_name}")
        print(f"Registro: {info.registrar}")
        print(f"Servidor WHOIS: {info.whois_server}")
        print(f"Data de criacao: {info.creation_date}")
        print(f"Data de expiracao: {info.expiration_date}")
        salvar_log(f"Rastreamento WHOIS de {dominio}: {info}")
    except whois.parser.PywhoisError as e:
        print(f"Erro ao rastrear dominio: {e}")
    except socket.gaierror as e:
        print(f"Erro ao rastrear dominio: {e}")
    except Exception as e:
        print(f"Erro inesperado ao rastrear dominio: {e}")

def verificar_vazamento_email():
    limpar_tela()
    email = input("Digite o e-mail para verificar vazamentos: ").strip()
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {"hibp-api-key": HAVEIBEENPWNED_API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print(f"O e-mail {email} foi encontrado em vazamentos:\n", response.json())
    else:
        print("Nenhum vazamento encontrado para este e-mail.")

def consultar_cpf():
    limpar_tela()
    cpf = input("Digite o CPF para consulta: ").strip()

    if not re.match(r'^\d{11}$', cpf):
        print("CPF inválido! Certifique-se de que o CPF tem 11 dígitos.")
        return

    url = f"{CPF_API}{cpf}"
    response = requests.get(url)

    if response.status_code == 200:
        dados_cpf = response.json()
        if dados_cpf:
            print("Informações associadas ao CPF:")
            for chave, valor in dados_cpf.items():
                print(f"{chave}: {valor}")
            salvar_log(f"Consulta realizada para CPF {cpf}: {dados_cpf}")
        else:
            print("Nenhuma informação encontrada para este CPF.")
    else:
        print("Erro ao consultar CPF. Tente novamente mais tarde.")

def menu_ferramentas():
    while True:
        limpar_tela()
        print("=== Ferramentas ===")
        print("1 - Rastrear Dominio")
        print("2 - Rastrear IP")
        print("3 - Verificar Vazamento de E-mail")
        print("4 - Consultar CPF")
        print("5 - Voltar")
        opcao = input("\nEscolha uma opcao: ")
        
        if opcao == "1":
            rastrear_dominio()
        elif opcao == "2":
            rastrear_ip()
        elif opcao == "3":
            verificar_vazamento_email()
        elif opcao == "4":
            consultar_cpf()  # Chama a função para consultar o CPF
        elif opcao == "5":
            break
        else:
            print("\nOpcao invalida!")
        input("\nPressione ENTER para continuar...")

# === Menu Principal ===
def mostrar_logs():
    if os.path.exists("log_varredura.txt"):
        with open("log_varredura.txt", "r") as log:
            print(log.read())
    else:
        print("Arquivo de log nao encontrado!")

def menu():
    while True:
        limpar_tela()
        print("="*40)
        print("         Painel de Varredura")
        print("="*40)
        print("1 - Varredura de Malware")
        print("2 - Ferramentas")
        print("3 - Ver Logs")
        print("4 - Sair")
        opcao = input("\nEscolha uma opcao: ")
        
        if opcao == "1":
            scan_completo()
        elif opcao == "2":
            menu_ferramentas()
        elif opcao == "3":
            mostrar_logs()
        elif opcao == "4":
            print("\nSaindo...")
            break
        else:
            print("\nOpcao invalida!")
        input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    menu()
