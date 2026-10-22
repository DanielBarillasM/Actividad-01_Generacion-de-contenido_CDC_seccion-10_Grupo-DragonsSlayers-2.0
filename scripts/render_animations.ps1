param(
    [switch]$SkipRender,
    [ValidateSet('final', 'preview')]
    [string]$Profile = 'final'
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot

$ffmpegPath = python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"
if (-not (Test-Path -LiteralPath $ffmpegPath)) {
    throw "No se encontro FFmpeg en: $ffmpegPath"
}
$env:PATH = "$(Split-Path -Parent $ffmpegPath);$env:PATH"

$scenes = @(
    'HookScene',
    'PipelineScene',
    'LexerScene',
    'GrammarScene',
    'AstScene',
    'SemanticScene',
    'OptimizationScene',
    'StackScene',
    'RuntimeScene',
    'CreditsScene'
)

if (-not $SkipRender) {
    if ($Profile -eq 'preview') {
        python -m manim -qm audiovisual/scenes.py @scenes
    } else {
        python -m manim -r 1920,1080 --fps 30 audiovisual/scenes.py @scenes
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Manim termino con codigo $LASTEXITCODE"
    }
}

if ($Profile -eq 'preview') {
    $qualityDirectory = '720p30'
    $outputName = 'minilang-animaciones-preview-v02.mp4'
} else {
    $qualityDirectory = '1080p30'
    $outputName = 'minilang-animaciones-v02.mp4'
}

$videoDirectory = Join-Path $projectRoot "output/manim/videos/scenes/$qualityDirectory"
$outputDirectory = Join-Path $projectRoot 'output/video'
New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null

$concatFile = Join-Path $outputDirectory 'manim-clips.txt'
$concatLines = foreach ($scene in $scenes) {
    $videoPath = Join-Path $videoDirectory "$scene.mp4"
    if (-not (Test-Path -LiteralPath $videoPath)) {
        throw "Falta el clip renderizado: $videoPath"
    }
    "file '$($videoPath.Replace("'", "''"))'"
}
$utf8WithoutBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllLines($concatFile, $concatLines, $utf8WithoutBom)

& $ffmpegPath -y -f concat -safe 0 -i $concatFile -c copy (Join-Path $outputDirectory $outputName)
if ($LASTEXITCODE -ne 0) {
    throw "FFmpeg termino con codigo $LASTEXITCODE"
}

Write-Output "Animaciones: $videoDirectory"
Write-Output "Montaje: $(Join-Path $outputDirectory $outputName)"

