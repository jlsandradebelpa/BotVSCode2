<#
.SYNOPSIS
    Instala atalhos do BotVSCode na Area de Trabalho e no Menu Iniciar.
.DESCRIPTION
    Cria atalhos para executar o BotVSCode (🚀 BotVSCode).
.NOTES
    Versao: 1.3
    Executar como usuario comum (sem admin).
    Requer permissao de escrita na Area de Trabalho.
#>

$AppName     = "BotVSCode"
$ProjectRoot  = "C:\Projetos\botvscode"
$IconPath     = "$ProjectRoot\assets\icons\botvscode.ico"
$ScriptPath   = "$ProjectRoot\app\main.py"
$Description  = "🚀 BotVSCode - Assistente para preparacao automatica do ambiente de desenvolvimento."

$Shell = New-Object -ComObject WScript.Shell

# Atalho na Area de Trabalho
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$DesktopShortcut = "$DesktopPath\$AppName.lnk"

$Shortcut = $Shell.CreateShortcut($DesktopShortcut)
$Shortcut.TargetPath = "python"
$Shortcut.Arguments = [string]::Format('"{0}"', $ScriptPath)
$Shortcut.WorkingDirectory = $ProjectRoot
$Shortcut.Description = $Description
if (Test-Path $IconPath) {
    $Shortcut.IconLocation = $IconPath
}
$Shortcut.Save()

Write-Host "[OK] Atalho criado na Area de Trabalho: $DesktopShortcut"

# Atalho no Menu Iniciar
$StartMenuDir = [Environment]::GetFolderPath("StartMenu") + "\Programs"
if (-not (Test-Path $StartMenuDir)) {
    $null = New-Item -ItemType Directory -Path $StartMenuDir -Force
}
$StartMenuShortcut = "$StartMenuDir\$AppName.lnk"

$Shortcut2 = $Shell.CreateShortcut($StartMenuShortcut)
$Shortcut2.TargetPath = "python"
$Shortcut2.Arguments = [string]::Format('"{0}"', $ScriptPath)
$Shortcut2.WorkingDirectory = $ProjectRoot
$Shortcut2.Description = $Description
if (Test-Path $IconPath) {
    $Shortcut2.IconLocation = $IconPath
}
$Shortcut2.Save()

Write-Host "[OK] Atalho criado no Menu Iniciar: $StartMenuShortcut"

Write-Host ""
Write-Host "Instalacao concluida."
