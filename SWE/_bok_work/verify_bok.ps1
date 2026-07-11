# verify_bok.ps1 — headless-Chrome smoke over the Body-of-Knowledge views (Node unavailable).
# Durable copy of the harness used to verify the BoK endeavour. Run:  pwsh -File verify_bok.ps1
#
# TWO Windows gotchas this encodes (both cost real debugging time):
#  1. The PowerShell &-call operator LOSES Chrome's stdout — Chrome's launcher relaunches a child and
#     the parent returns empty. Use Start-Process -Wait -RedirectStandardOutput instead.
#  2. If the user already has Chrome open, a new invocation FORWARDS the url to that session ("Opening in
#     existing browser session") and dumps nothing. An ISOLATED, fresh --user-data-dir forces a real headless run.
$ErrorActionPreference = 'Stop'
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
$base   = 'file:///E:/dev/corpora/SWE/explorer/index.html'
$outdir = Join-Path $PSScriptRoot 'vout'
$prof   = Join-Path $outdir 'profile'
New-Item -ItemType Directory -Force -Path $outdir | Out-Null
Remove-Item -Recurse -Force $prof -ErrorAction SilentlyContinue

$cases = @(
  @{ n='graph';        h='view=graph';                          e=@('major works','Reading graph') },
  @{ n='facets';       h='view=facets';                          e=@('match','branch','teaches') },
  @{ n='timeline-bok'; h='view=timeline';                        e=@('body of knowledge by year','Body of Knowledge','Elements','p8') },
  @{ n='timeline-el';  h='view=timeline&tlmode=elements';        e=@('named its concepts','UNRESOLVED','2000s') },
  @{ n='overlap';      h='view=overlap';                         e=@('corpora','span') },
  @{ n='anchors';      h='view=anchors';                         e=@('start','island hubs') },
  @{ n='el-taxonomy';  h='view=el-taxonomy';                     e=@('Element','taxonomy') },
  @{ n='el-coverage';  h='view=el-coverage';                     e=@('coverage') },
  @{ n='el-atlas';     h='view=el-atlas';                        e=@('rchipelago') },
  @{ n='el-bridgeflow';h='view=el-bridgeflow';                   e=@('ridge') },
  @{ n='deeplink-elsel';h='view=timeline&tlmode=elements&sel=buffer-pool'; e=@('Buffer Pool','pass 8') }
)
$errSig = @('ERROR:CONSOLE','Uncaught','unhandledrejection','\[swe\] uncaught','\[swe\] bootstrap failed')
$forbidAll = 'failed to load or validate'

$fail = 0
"{0,-16} {1,-6} {2}" -f 'CASE','RESULT','DETAIL'
"-" * 72
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
  if ($domtxt -like "*$forbidAll*") { $problems += "BACKSTOP-FIRED" }
  foreach ($s in $errSig) { if ($logtxt -match $s) { $problems += "console:$s" } }
  if ($problems.Count -eq 0) { "{0,-16} {1,-6} {2}" -f $c.n,'PASS','' }
  else { $fail++; "{0,-16} {1,-6} {2}" -f $c.n,'FAIL',($problems -join '; ') }
}
"-" * 72
if ($fail -eq 0) { "ALL PASS ($($cases.Count) cases)" } else { "$fail FAIL of $($cases.Count)" }
