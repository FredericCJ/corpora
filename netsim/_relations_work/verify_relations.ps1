# verify_relations.ps1 — headless-Chrome smoke over the 7 netsim views + the typed reading graph.
# Durable harness for the "typed relations + corpus expansion" endeavour. Run: pwsh -File verify_relations.ps1
#
# TWO Windows gotchas this encodes (both cost real debugging time):
#  1. The PowerShell &-call operator LOSES Chrome's stdout (Chrome relaunches a child; the parent returns
#     empty). Use Start-Process -Wait -RedirectStandardOutput instead.
#  2. If the user already has Chrome open, a new invocation FORWARDS the url to that session and dumps
#     nothing. An ISOLATED, fresh --user-data-dir forces a real headless run.
$ErrorActionPreference = 'Stop'
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
if (-not (Test-Path $chrome)) { $chrome = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe' }
$base   = 'file:///E:/dev/corpora/netsim/explorer/index.html'
$outdir = Join-Path $PSScriptRoot 'vout'
$prof   = Join-Path $outdir 'profile'
New-Item -ItemType Directory -Force -Path $outdir | Out-Null
Remove-Item -Recurse -Force $prof -ErrorAction SilentlyContinue

$cases = @(
  @{ n='anchor';     h='view=anchor';               e=@('Anchor map') },
  @{ n='reading';    h='view=reading';              e=@('Reading graph','how the resources relate','typed reading relations','band-label') },
  @{ n='overlays';   h='view=graph';                e=@('Overlays','EDITORIAL') },
  @{ n='facets';     h='view=facets';               e=@('Facets') },
  @{ n='timeline';   h='view=timeline';             e=@('Chronology') },
  @{ n='matlab';     h='view=matlab';               e=@('MATLAB') },
  @{ n='triage';     h='view=triage';               e=@('Triage') },
  @{ n='reading-sel';h='view=reading&sel=g166';     e=@('typed relations','Scheduling Algorithms','prerequisite-of') }
)
$errSig = @('ERROR:CONSOLE','Uncaught','unhandledrejection','ValidationError','error escaped every boundary','bootstrap failed')
$forbid = 'failed to load or validate'

$fail = 0
"{0,-14} {1,-6} {2}" -f 'CASE','RESULT','DETAIL'
"-" * 78
foreach ($c in $cases) {
  $dom = Join-Path $outdir ("dom_" + $c.n + ".html")
  $log = Join-Path $outdir ("log_" + $c.n + ".txt")
  $url = "$base#$($c.h)"
  $a = @('--headless=new','--disable-gpu','--no-sandbox','--no-first-run','--no-default-browser-check',
         '--window-size=1920,1080','--virtual-time-budget=6000','--enable-logging=stderr','--v=1',
         "--user-data-dir=$prof",'--dump-dom',$url)
  Start-Process -FilePath $chrome -ArgumentList $a -Wait -NoNewWindow -RedirectStandardOutput $dom -RedirectStandardError $log
  $domtxt = (Get-Content -Raw -Path $dom -ErrorAction SilentlyContinue); if ($null -eq $domtxt) { $domtxt = '' }
  $logtxt = (Get-Content -Raw -Path $log -ErrorAction SilentlyContinue); if ($null -eq $logtxt) { $logtxt = '' }
  $problems = @()
  if ($domtxt.Length -lt 1000) { $problems += "EMPTY-DOM($($domtxt.Length))" }
  foreach ($e in $c.e) { if ($domtxt -notlike "*$e*") { $problems += "missing:'$e'" } }
  if ($domtxt -like "*$forbid*") { $problems += "BACKSTOP-FIRED" }
  foreach ($s in $errSig) { if ($logtxt -match $s) { $problems += "console:$s" } }
  if ($problems.Count -eq 0) { "{0,-14} {1,-6} {2}" -f $c.n,'PASS','' }
  else { $fail++; "{0,-14} {1,-6} {2}" -f $c.n,'FAIL',($problems -join '; ') }
}
"-" * 78
if ($fail -eq 0) { "ALL PASS ($($cases.Count) cases)" } else { "$fail FAIL of $($cases.Count)" }
