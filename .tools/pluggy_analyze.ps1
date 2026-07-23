#Requires -Version 5.1
<#
.SYNOPSIS
  Отправляет .plugin файл в Pluggy API и сохраняет отчёт безопасности.

.DESCRIPTION
  POST https://pluggy.mk69.dev/api/analyze (multipart/form-data, поле "files").
  Лимит API: ~1 запрос в минуту — при нескольких файлах пауза 65 с между вызовами.

  Переменные окружения:
    PLUGGY_SESSION — значение cookie pluggy_session
    PLUGGY_CSRF    — значение pluggy_csrf / заголовок x-csrf-token

.EXAMPLE
  $env:PLUGGY_SESSION = "..."
  $env:PLUGGY_CSRF = "..."
  .\.tools\pluggy_analyze.ps1 -PluginFile WSBypass\releases\v3.1.4\wsbypass_v3.1.4.plugin

.EXAMPLE
  .\.tools\pluggy_analyze.ps1 -PluginFile a.plugin,b.plugin -DelaySeconds 65
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string[]] $PluginFile,

    [string] $OutputFile,

    [int] $DelaySeconds = 65,

    [string] $ApiUrl = "https://pluggy.mk69.dev/api/analyze"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-PluggyCredentials {
    $session = $env:PLUGGY_SESSION
    $csrf = $env:PLUGGY_CSRF
    if ([string]::IsNullOrWhiteSpace($session) -or [string]::IsNullOrWhiteSpace($csrf)) {
        throw @"
Не заданы PLUGGY_SESSION и/или PLUGGY_CSRF.

1. Откройте https://pluggy.mk69.dev в браузере
2. DevTools → Application → Cookies → pluggy_session, pluggy_csrf
3. В PowerShell:
   `$env:PLUGGY_SESSION = '<pluggy_session>'
   `$env:PLUGGY_CSRF = '<pluggy_csrf>'
"@
    }
    return @{ Session = $session.Trim(); Csrf = $csrf.Trim() }
}

function Get-DefaultOutputPath {
    param([string] $PluginPath)
    $dir = Split-Path -Parent $PluginPath
    $name = [System.IO.Path]::GetFileNameWithoutExtension($PluginPath)
    if ($name -match '_v?(\d+\.\d+\.\d+)$') {
        return Join-Path $dir ("secure_{0}.md" -f $Matches[1])
    }
    return Join-Path $dir ("secure_{0}.md" -f $name)
}

function Format-PluggyReport {
    param([string] $Body, [string] $PluginPath)
    $trimmed = $Body.Trim()
    if ($trimmed.StartsWith("{")) {
        try {
            $json = $trimmed | ConvertFrom-Json
            if ($json.kind -eq "single" -and $json.results -and $json.results.Count -gt 0) {
                return Convert-PluggyJsonToMarkdown -Result $json.results[0]
            }
            if ($json.report) { return [string]$json.report }
            if ($json.markdown) { return [string]$json.markdown }
            if ($json.text) { return [string]$json.text }
            if ($json.result) { return [string]$json.result }
        }
        catch {
            # не JSON — сохраняем как есть
        }
    }
    return $trimmed
}

function Convert-PluggyJsonToMarkdown {
    param($Result)
    $verdict = switch ($Result.risk_level) {
        "low" { "❔ Низкий риск" }
        "medium" { "⚠️ Осторожно" }
        "high" { "📛 Высокий риск" }
        "critical" { "🚨 Критический риск" }
        default { "❔ $($Result.risk)" }
    }
    $lines = @(
        "Проверенно с помощью Pluggy Bot (pluggy_robot.t.me)",
        "",
        "> Версия **$($Result.version)** · плагин: ``$($Result.plugin_id)``",
        "",
        "$verdict Отчёт • Pluggy API",
        "",
        "✦ Метаданные плагина ✦",
        "┌ Название: $($Result.plugin_name)",
        "├ ID: $($Result.plugin_id)",
        "├ Версия: $($Result.version)",
        "└ Файл: $($Result.name)",
        "",
        $($Result.explanation),
        ""
    )
    if ($Result.network_intel) {
        $lines += ""
        $lines += $Result.network_intel
    }
    if ($Result.threats -and $Result.threats.Count -gt 0) {
        $lines += ""
        $lines += "✦ Детали угроз ✦"
        foreach ($t in $Result.threats) {
            $lines += "• $t"
        }
    }
    return ($lines -join "`n")
}

function Invoke-PluggyAnalyze {
    param(
        [string] $PluginPath,
        [string] $OutPath,
        [hashtable] $Creds,
        [string] $Url
    )

    $resolved = Resolve-Path -LiteralPath $PluginPath
    $fileName = [System.IO.Path]::GetFileName($resolved.Path)

    Add-Type -AssemblyName System.Net.Http
    Add-Type -AssemblyName System.Net.Primitives
    $handler = New-Object System.Net.Http.HttpClientHandler
    $handler.CookieContainer = New-Object System.Net.CookieContainer
    $uri = [Uri]$Url
    $handler.CookieContainer.Add($uri, (New-Object System.Net.Cookie("pluggy_session", $Creds.Session, "/", $uri.Host)))
    $handler.CookieContainer.Add($uri, (New-Object System.Net.Cookie("pluggy_csrf", $Creds.Csrf, "/", $uri.Host)))

    $client = New-Object System.Net.Http.HttpClient($handler)
    $client.DefaultRequestHeaders.Add("x-csrf-token", $Creds.Csrf)
    $client.DefaultRequestHeaders.Add("accept", "*/*")
    $client.DefaultRequestHeaders.Add("origin", "https://pluggy.mk69.dev")
    $client.DefaultRequestHeaders.Add("referer", "https://pluggy.mk69.dev/")

    $content = New-Object System.Net.Http.MultipartFormDataContent
    $fileStream = [System.IO.File]::OpenRead($resolved.Path)
    try {
        $streamContent = New-Object System.Net.Http.StreamContent($fileStream)
        $streamContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse("application/octet-stream")
        $content.Add($streamContent, "files", $fileName)

        $response = $client.PostAsync($Url, $content).GetAwaiter().GetResult()
        $body = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
        $status = [int]$response.StatusCode

        if (-not $response.IsSuccessStatusCode) {
            throw "Pluggy API HTTP $status`: $body"
        }

        $report = Format-PluggyReport -Body $body -PluginPath $resolved.Path
        if ([string]::IsNullOrWhiteSpace($report)) {
            throw "Пустой ответ от Pluggy API"
        }

        $outDir = Split-Path -Parent $OutPath
        if ($outDir -and -not (Test-Path -LiteralPath $outDir)) {
            New-Item -ItemType Directory -Force -Path $outDir | Out-Null
        }

        $report | Out-File -LiteralPath $OutPath -Encoding utf8 -NoNewline
        Write-Host "OK HTTP $status -> $OutPath ($fileName)"
    }
    finally {
        $fileStream.Dispose()
        $client.Dispose()
    }
}

$creds = Get-PluggyCredentials
$files = @()
foreach ($item in $PluginFile) {
    $files += ($item -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ })
}

if ($files.Count -eq 0) {
    throw "Не указаны файлы .plugin"
}

for ($i = 0; $i -lt $files.Count; $i++) {
    $plugin = $files[$i]
    if (-not (Test-Path -LiteralPath $plugin)) {
        throw "Файл не найден: $plugin"
    }

    if ($files.Count -eq 1 -and $OutputFile) {
        $out = $OutputFile
    }
    else {
        $out = Get-DefaultOutputPath -PluginPath $plugin
    }

    if ($i -gt 0) {
        Write-Host "Пауза ${DelaySeconds}с (лимит Pluggy 1 req/min)..."
        Start-Sleep -Seconds $DelaySeconds
    }

    Invoke-PluggyAnalyze -PluginPath $plugin -OutPath $out -Creds $creds -Url $ApiUrl
}
