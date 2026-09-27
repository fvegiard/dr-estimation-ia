set -u
P='EeWin!Dr2026x'
order="CreateTables.sql CreateScripts.sql CreateData.sql Central_CreateTables.sql Central_CreateScripts.sql V0_UpdateDatabase.sql UpdateDatabase.sql"
for i in $(seq 3 45); do order="$order V${i}_UpdateDatabase.sql"; done
for f in $order; do
  p=$(ls /src/$f /src/${f%.sql}.SQL 2>/dev/null | head -1)
  [ -z "$p" ] && { echo "MISSING $f"; continue; }
  out=$(/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$P" -C -d EE -f 1252 -I -i "$p" 2>&1)
  err=$(echo "$out" | grep -c "Msg ")
  echo "$f errors=$err"
  [ "$err" -gt 0 ] && echo "$out" | grep -A2 "Msg " | head -12
done
