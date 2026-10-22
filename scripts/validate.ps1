$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot

Write-Output '1/5 Pruebas del compilador'
python -m pytest -q
if ($LASTEXITCODE -ne 0) { throw 'Fallaron las pruebas de MiniLang.' }

Write-Output '2/5 Ejecución de demostración'
$demoOutput = python -m minilang examples/demo.mini --run
if ($LASTEXITCODE -ne 0) { throw 'No se pudo ejecutar examples/demo.mini.' }
if (($demoOutput | Select-Object -Last 1) -ne '42') {
    throw "Se esperaba 42 y se obtuvo: $demoOutput"
}

Write-Output '3/5 Integridad de entregables'
$requiredFiles = @(
    'guion/guion.tex',
    'output/pdf/guion.pdf',
    'presentacion/index.html',
    'audiovisual/scenes.py',
    'output/video/minilang-animaciones-v02.mp4',
    'output/storyboard/manim-v02-contact-sheet.png',
    'docs/plan-animacion-manim.md',
    'docs/brief-creativo-minilang.md',
    'docs/fuentes-y-licencias.md',
    'youtube/descripcion.md'
)
foreach ($requiredFile in $requiredFiles) {
    if (-not (Test-Path -LiteralPath $requiredFile)) {
        throw "Falta el entregable: $requiredFile"
    }
}

Write-Output '4/5 Integrantes autorizados'
$forbiddenMarkers = @('Pendiente', 'Integrante 4', 'Integrante 5')
foreach ($marker in $forbiddenMarkers) {
    $matches = rg -n --glob '!README.md' --glob '!scripts/validate.ps1' --glob '!output/**' --fixed-strings $marker . 2>$null
    if ($LASTEXITCODE -eq 0) {
        throw "Se encontró un marcador descartado ($marker):`n$matches"
    }
    if ($LASTEXITCODE -gt 1) { throw "rg falló al buscar: $marker" }
}

Write-Output '5/5 Especificaciones del maestro audiovisual'
$videoJson = python -c "import av,json; c=av.open('output/video/minilang-animaciones-v02.mp4'); v=next(s for s in c.streams if s.type=='video'); print(json.dumps({'duration': float(c.duration/av.time_base), 'width': v.codec_context.width, 'height': v.codec_context.height, 'fps': float(v.average_rate)}))"
if ($LASTEXITCODE -ne 0) { throw 'No se pudo inspeccionar el maestro audiovisual.' }
$video = $videoJson | ConvertFrom-Json
if ($video.width -ne 1920 -or $video.height -ne 1080 -or [math]::Round($video.fps) -ne 30) {
    throw "Formato audiovisual inesperado: $($video.width)x$($video.height) a $($video.fps) fps."
}
if ($video.duration -lt 190) {
    throw "El paquete audiovisual dura menos de lo esperado: $($video.duration) segundos."
}

Write-Output 'Validación completada: compilador correcto y entregables presentes.'
