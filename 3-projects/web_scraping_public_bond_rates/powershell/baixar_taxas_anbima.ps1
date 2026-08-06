[CmdletBinding()]
param([string]$Destino = "downloads_anbima")

$ErrorActionPreference = "Stop"
$pagina = "https://www.anbima.com.br/pt_br/informar/taxas-de-titulos-publicos.htm"
$urlArquivo = "https://www.anbima.com.br/informacoes/merc-sec/arqs/m26ago04.xls"
$sessao = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$headers = @{ "User-Agent" = "Mozilla/5.0 (compatible; ANBIMA-downloader/2.0)" }

try {
    $destinoCompleto = [System.IO.Path]::GetFullPath($Destino)
    [System.IO.Directory]::CreateDirectory($destinoCompleto) | Out-Null
    $arquivo = Join-Path $destinoCompleto "m26ago04.xls"
    $temporario = "$arquivo.part"

    Invoke-WebRequest -Uri $urlArquivo -OutFile $temporario -WebSession $sessao `
        -Headers ($headers + @{ Referer = $pagina })

    $bytes = [System.IO.File]::ReadAllBytes($temporario)
    $ehOle = $bytes.Length -ge 8 -and ([BitConverter]::ToString($bytes, 0, 8) -eq "D0-CF-11-E0-A1-B1-1A-E1")
    $ehZip = $bytes.Length -ge 4 -and ([BitConverter]::ToString($bytes, 0, 4) -eq "50-4B-03-04")
    if (-not ($ehOle -or $ehZip)) {
        Remove-Item -LiteralPath $temporario -Force
        throw "O link retornado não contém uma planilha Excel válida."
    }

    Move-Item -LiteralPath $temporario -Destination $arquivo -Force
    Write-Host "Baixado: $arquivo" -ForegroundColor Green
} catch {
    Write-Error $_.Exception.Message
    exit 1
}
