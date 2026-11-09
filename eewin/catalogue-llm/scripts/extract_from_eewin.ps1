# Export EEWin tables from the VM's SQL Server (EEWin2_zip) to data\raw\*.csv (UTF-8, comma).
param([string]$Root = (Split-Path $PSScriptRoot -Parent))
$vm = Get-VM -Name 'Windows 10 MSIX packaging environment' | Where-Object State -eq Running
$cred = New-Object PSCredential('test vm', (New-Object SecureString))
$s = New-PSSession -VMId $vm.Id -Credential $cred
$tables = [ordered]@{
  products     = "SELECT p.PRO_ID,p.CLEMANU,p.CLEDIST,p.CODECAT,p.[DESC],p.CODEFOUR,p.COUBRUTUNI,p.COUESC,p.PROMCOUNET,RTRIM(p.COUUM) COUUM,p.TEMPUNI,RTRIM(p.TEMPUM) TEMPUM,p.DATECOUT,p.DATECOUNET,ISNULL(b.PREFERED,p.PREFERED) PREFERED_ORIG FROM PRODUITS p LEFT JOIN zz_PrefBackup_20260930 b ON b.PRO_ID=p.PRO_ID"
  categories   = "SELECT CODECAT,[DESC] FROM PROCAT"
  assemblies   = "SELECT ENS_ID,[DESC],RTRIM(COUUM) COUUM,TEMPUNI,RTRIM(TEMPUM) TEMPUM,TEMPSEC,PROFIT,CLEPERS FROM ENSEMBLE"
  assembly_components = "SELECT ENS_ID,ORDRE,PRO_ID,QTE,RTRIM(QTEUM) QTEUM,TYPRATIO,DIV,RTRIM(DIVUM) DIVUM FROM ENSCOMPO"
  units        = "SELECT * FROM Sys_Units"
  unit_conversions = "SELECT UnitFrom,UnitTo,Ratio,UnitToUnit,PackageToUnit,UnitToPackage FROM Sys_UnitsConversion"
  labor_rates  = "SELECT ORDRE,DESCTAUX,COUTUNI,PROFIT FROM TAUX"
  quotes       = "SELECT SOU_ID,NODOC,DESCDOC,DATEDOC,STATUT,TYPEPROF,MATCOUTREL,MATCOUTMO,MATVENDCAL,SERHRESCAL,SERCOUTCAL,SERVENDCAL,AUTCOUTCAL,AUTVENDCAL,TOTCALCULE FROM SOUMIS"
  quote_lines  = "SELECT SOU_ID,BLO_ID,DIV_ID,TYPERELEVE,ORDRE,TYPEITEM,ITEM_ID,DESCR,QTE,SECTION,RTRIM(QTEUM) QTEUM,COUTANBRUT,TEMPSUNIT,TEMPSSEC,RTRIM(TEMPSUM) TEMPSUM FROM SOUREL"
  quote_blocks = "SELECT SOU_ID,BLO_ID,[DESC],MULT,ORDRE FROM SOUBLO"
  quote_products = "SELECT SOU_ID,PRO_ID,CLEMANU,[DESC],CODEFOUR,CODECAT,COUBRUTUNI,COUESC,PROMCOUNET,RTRIM(COUUM) COUUM,TEMPUNI,RTRIM(TEMPUM) TEMPUM,QTECOM,QTEENS,DATECOUT FROM SOUPRO"
  quote_assemblies = "SELECT SOU_ID,ENS_ID,ENS_ORG_ID,[DESC],RTRIM(COUUM) COUUM,TEMPUNI,RTRIM(TEMPUM) TEMPUM,TEMPSEC,QTETOT FROM SOUENS"
  quote_assembly_components = "SELECT SOU_ID,ENS_ID,PRO_ID,ORDRE,QTE,RTRIM(QTEUM) QTEUM,TYPRATIO,DIV,RTRIM(DIVUM) DIVUM FROM SOUENSCO"
}
Invoke-Command -Session $s -ArgumentList $tables -ScriptBlock {
  param($tables)
  New-Item -ItemType Directory -Force 'C:\ClaudeTools\export' | Out-Null
  $cn = New-Object System.Data.SqlClient.SqlConnection 'Server=.\EEWIN;Database=EEWin2_zip;Integrated Security=True'; $cn.Open()
  foreach ($k in $tables.Keys) {
    $cmd = $cn.CreateCommand(); $cmd.CommandText = $tables[$k]; $cmd.CommandTimeout = 600
    $dt = New-Object System.Data.DataTable; $dt.Load($cmd.ExecuteReader())
    $dt | Select-Object * -ExcludeProperty RowError, RowState, Table, ItemArray, HasErrors |
      Export-Csv "C:\ClaudeTools\export\$k.csv" -NoTypeInformation -Encoding UTF8
    "{0}: {1}" -f $k, $dt.Rows.Count
  }
  $cn.Close()
}
New-Item -ItemType Directory -Force "$Root\data\raw" | Out-Null
foreach ($k in $tables.Keys) { Copy-Item -FromSession $s "C:\ClaudeTools\export\$k.csv" "$Root\data\raw\$k.csv" -Force }
Remove-PSSession $s
