# Essai comparatif des fournisseurs sur UNE MÊME feuille (branche test/fournisseurs-externes).
# Usage (PowerShell, yogafv) :  .\releve\comparer_fournisseurs.ps1 TEST-E103
# Clés lues dans l'environnement du processus seulement (jamais dans le dépôt) :
#   $env:NVIDIA_API_KEY = "..."   $env:GEMINI_API_KEY = "..."
# Résultat : D:\claude\releve-auto\OUTBOX\<NOM>-<fournisseur>\ pour chaque route, puis un tableau récapitulatif.
param([Parameter(Mandatory)][string]$Nom)
$base = "D:\claude\releve-auto"
$routes = @(
  @{agent="sdk";    modele=""},                       # Claude (OAuth Max), modèle = alias opus
  @{agent="nvidia"; modele="moonshotai/kimi-k3"},
  @{agent="gemini"; modele="gemini-3.8-flash"},
  @{agent="gemini"; modele="gemini-4-argon"}
)
$rows = @()
foreach ($r in $routes) {
  $tag = if ($r.modele) { "$($r.agent)-" + ($r.modele -replace '[^a-z0-9]','') } else { $r.agent }
  $dst = "$base\INBOX\$Nom-$tag"
  if (-not (Test-Path $dst)) { Copy-Item "$base\INBOX\$Nom" $dst -Recurse }
  $env:RELEVE_AGENT = $r.agent
  if ($r.agent -eq "sdk") { Remove-Item Env:RELEVE_NVIDIA_MODEL -ErrorAction SilentlyContinue } else { $env:RELEVE_NVIDIA_MODEL = $r.modele }
  $t = Measure-Command { uv run releve/run.py "$Nom-$tag" }
  $res = Get-Content "$base\OUTBOX\$Nom-$tag\travail\agent-resultat.json" | ConvertFrom-Json
  $occ = (Import-Csv "$base\OUTBOX\$Nom-$tag\travail\occurrences-visuel.csv" -ErrorAction SilentlyContinue).Count +
         (Import-Csv "$base\OUTBOX\$Nom-$tag\travail\occurrences-texte.csv"  -ErrorAction SilentlyContinue).Count
  $rows += [pscustomobject]@{ route=$tag; subtype=$res.subtype; tours=$res.num_turns; minutes=[math]::Round($t.TotalMinutes,1);
                             reperes=$occ; conforme=$res.qualite.conforme; erreurs=$res.qualite.erreurs; cout_usd=$res.total_cost_usd }
}
$rows | Format-Table -AutoSize
$rows | Export-Csv "$base\OUTBOX\$Nom-comparaison.csv" -NoTypeInformation -Encoding UTF8
