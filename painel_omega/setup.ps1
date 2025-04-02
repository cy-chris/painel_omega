# Eleva para Administrador se necessario
$CurrentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$Principal = New-Object Security.Principal.WindowsPrincipal($CurrentUser)
$AdminRole = [Security.Principal.WindowsBuiltInRole]::Administrator

if (-Not $Principal.IsInRole($AdminRole)) {
    Write-Host "O script precisa ser executado como Administrador. Reiniciando com permissoes elevadas..."
    Start-Process powershell.exe -ArgumentList "-File `"$PSCommandPath`"" -Verb RunAs
    exit
}

Write-Host "Iniciando a instalacao das dependencias..."

# Verifica se o Chocolatey esta instalado
if (-Not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Instalando Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    refreshenv
}

# Instala Python e pip
Write-Host "Instalando Python..."
choco install python -y
refreshenv

# Instala pacotes Python necessarios
Write-Host "Instalando bibliotecas Python..."
python -m pip install --upgrade pip
pip install requests whois python-whois

# Instala ClamAV
Write-Host "Instalando ClamAV..."
choco install clamav -y

# Atualiza ClamAV
Write-Host "Atualizando banco de virus do ClamAV..."
Start-Process -NoNewWindow -Wait -FilePath "C:\Program Files\ClamAV\freshclam.exe"

# Instala Whois para rastreamento de dominio
Write-Host "Instalando Whois..."
choco install whois -y

# Verifica se o Windows Defender esta ativado
Write-Host "Verificando Windows Defender..."
if (-Not (Get-Command "MpCmdRun.exe" -ErrorAction SilentlyContinue)) {
    Write-Host "Windows Defender nao encontrado. Instalando..."
    Enable-WindowsOptionalFeature -Online -FeatureName Windows-Defender-Features -All -NoRestart
}

# Instala ferramentas de rede
Write-Host "Instalando ferramentas de rede..."
choco install sysinternals -y

Write-Host "Instalacao concluida. Agora voce pode rodar o script Python."
