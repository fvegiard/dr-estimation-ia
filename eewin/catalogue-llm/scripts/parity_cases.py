"""Emit SQL that checks the cloud functions against the local engine (returns only mismatches)."""
import json, random, sqlite3
from dre_estimation.store import Store
random.seed(7)
s = Store(); con = sqlite3.connect("data/dre.sqlite")
prods = [r[0] for r in con.execute("select code from products where price > 0 order by random() limit 200")]
prods += [r[0] for r in con.execute("select code from products where price = 0 order by random() limit 20")]
asms = [r[0] for r in con.execute("select code from assemblies order by random() limit 80")]
units = ["", "", "U", "C", "F", "M", "CF", "KM", "L"]
lines = [{"code": c, "qty": random.choice([1, 3, 12.5, 40, 250]), "unit": random.choice(units)} for c in prods]
lines += [{"code": c, "qty": random.choice([1, 4, 30, 150]), "sections": random.choice([0, 0, 2])} for c in asms]
exp = [s.estimate([ln])["lines"][0] for ln in lines]
cases = [ln | {"exp_m": e["material"], "exp_h": e["hours"]} for ln, e in zip(lines, exp)]
queries = ["prise 30A 125V", "boite 4 po carre", "EMT 3/4 connector", "disjoncteur 15A 1P", "plaque 1G acier inox",
           "cable armé 14/2 alu", "luminaire LED 4 pi", "thermostat", "interrupteur 3 voies", "TMEC 1 po", "GFI"]
sq = [{"q": q, "exp": [r["code"] for r in s.search_products(q, 5)]} for q in queries]
tot = s.estimate(lines, 72, 15, 10)["totals"]
print(json.dumps({"cases": cases, "search": sq, "totals": tot, "lines": lines}))
