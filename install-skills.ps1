# install-skills.ps1 — 安装/同步 skills/ 到 ~/.codex/skills，并检测两端漂移
#
# 用法：
#   powershell -ExecutionPolicy Bypass -File .\install-skills.ps1              # 安装：只覆盖有差异的技能
#   powershell -ExecutionPolicy Bypass -File .\install-skills.ps1 -Mode check  # 只检测漂移，不改动任何文件
#
# 行为约定：
# - install 按整目录重建目标技能目录，因此会清掉源端已删除的文件（真正的同步语义）。
# - 只处理源端 skills/ 下存在的技能目录；绝不触碰 ~/.codex/skills/.system 等其它内容。
# - check 模式：无漂移退出码 0，有漂移退出码 1，可直接用于 CI 或定期自检。
param(
    [ValidateSet('install', 'check')]
    [string]$Mode = 'install',
    [string]$SourceRoot = $PSScriptRoot,
    [string]$DestRoot = ''
)

$ErrorActionPreference = 'Stop'

if (-not $DestRoot) { $DestRoot = Join-Path $env:USERPROFILE '.codex\skills' }
$srcSkills = Join-Path $SourceRoot 'skills'

if (-not (Test-Path -LiteralPath $srcSkills)) {
    Write-Host "[错误] 未找到源目录：$srcSkills"
    exit 2
}

function Get-SkillFiles([string]$skillDir) {
    Get-ChildItem -LiteralPath $skillDir -Recurse -File | ForEach-Object {
        $_.FullName.Substring($skillDir.Length + 1)
    }
}

function Test-FileSame([string]$a, [string]$b) {
    (Get-FileHash -LiteralPath $a -Algorithm SHA256).Hash -eq (Get-FileHash -LiteralPath $b -Algorithm SHA256).Hash
}

$skillDirs = @(Get-ChildItem -LiteralPath $srcSkills -Directory | Sort-Object Name)
if ($skillDirs.Count -eq 0) {
    Write-Host "[错误] 源目录为空：$srcSkills"
    exit 2
}

$plan = @()
foreach ($s in $skillDirs) {
    $srcDir = $s.FullName
    $dstDir = Join-Path $DestRoot $s.Name
    $status = 'same'
    if (-not (Test-Path -LiteralPath $dstDir)) {
        $status = 'missing'
    }
    else {
        $srcFiles = @(Get-SkillFiles $srcDir)
        $dstFiles = @(Get-SkillFiles $dstDir)
        foreach ($f in $srcFiles) {
            $sf = Join-Path $srcDir $f
            $df = Join-Path $dstDir $f
            if (-not (Test-Path -LiteralPath $df)) { $status = 'drift'; break }
            if (-not (Test-FileSame $sf $df)) { $status = 'drift'; break }
        }
        if ($status -eq 'same') {
            foreach ($f in $dstFiles) {
                if ($srcFiles -notcontains $f) { $status = 'drift'; break }
            }
        }
    }
    $plan += [pscustomobject]@{ Skill = $s.Name; Status = $status; Src = $srcDir; Dst = $dstDir }
}

$label = @{ same = '一致    '; missing = '未安装'; drift = '有差异' }

Write-Host ''
Write-Host "源  ：$srcSkills"
Write-Host "目标：$DestRoot"
Write-Host "模式：$Mode"
Write-Host '-----------------------------------------'
foreach ($p in $plan) {
    Write-Host "  [$($label[$p.Status])] $($p.Skill)"
}
$pending = @($plan | Where-Object { $_.Status -ne 'same' })

if ($Mode -eq 'check') {
    Write-Host '-----------------------------------------'
    if ($pending.Count -eq 0) {
        Write-Host '结果：无漂移，源与安装端完全一致。'
        exit 0
    }
    Write-Host "结果：$($pending.Count) 个技能存在漂移（未安装或有差异）。运行不带参数的 install-skills.ps1 可修复。"
    exit 1
}

New-Item -ItemType Directory -Path $DestRoot -Force | Out-Null
foreach ($p in $plan) {
    if ($p.Status -eq 'same') { continue }
    if (Test-Path -LiteralPath $p.Dst) {
        Remove-Item -LiteralPath $p.Dst -Recurse -Force
    }
    Copy-Item -LiteralPath $p.Src -Destination $DestRoot -Recurse -Force
    Write-Host "  已安装/更新：$($p.Skill)"
}
Write-Host '-----------------------------------------'
Write-Host "完成：共 $($plan.Count) 个技能，本次更新 $($pending.Count) 个。"
Write-Host '提示：需重启 Codex 并新开会话，技能元数据才会被加载。'
exit 0
