"""Inventaire E201 : coordonnées LUES À LA VUE sur les tuiles agrandies (2x) — aucune détection automatique.
Chaque entrée : (tuile, dx, dy, code) en pixels de la tuile agrandie ; abs = x0 + dx/2, y0 + dy/2 (px raster 5399x3600)."""
LAB={'L':'Luminaire cercle+support (corridor/hall) — à classer','W':'Appareil mural de porte (cercle à tige) — à classer',
'D':'Disque B1-xxx (secours ou détecteur) — à classer','O':'Capteur OS3 (étiqueté)','P':'Boîtier DP2 avec batterie — à classer',
'K':'Carré K (station/module) — à classer','X':'Enseigne de sortie','ISO':'Module ISO','RM':'Module RM','MRA':'Module MRA',
'MX':'Module Mx2','T':'Carré T (étiqueté)','A':'Bulle A','B':'Bulle B (boîtiers quincaillerie)','SW':'SW1 (étiqueté)','F':'Carré F',
'C':'Hexagone C (chauffage 1250 W ?) — à classer','R':'Carré R — à classer','N1':'Bulle 1 (renvoi)','N2':'Bulle 2 (renvoi)','VE':'Boîte VE-12 (étiquetée)','EB':'Boîte à diagonale + E (escalier) — à classer','PSU':'Carré à croix PSU1A-41 (étiqueté)',
'AV':'Avertisseur rectangle à pointes — à classer','H':'Cercle à point (près de H) — à classer','DB':'Icône sous Mx2/T (débit) — à classer','KO':'Symbole K○ (sas ascenseur) — à classer','SWX':'Icône ≈ sous T (compté SW1 par l\'estimateur) — à classer','TA':'Repère logement TYPE A','TB':'Repère logement TYPE B','TC':'Repère logement TYPE C','TD':'Repère logement TYPE D','TE':'Repère logement TYPE E','TF':'Repère logement TYPE F','TG':'Repère logement TYPE G'}
COM=[('t0',[(985,143,'L'),(1098,230,'L'),(1360,230,'L'),(1625,230,'L'),(1885,230,'L'),(1155,200,'W'),(1717,200,'W'),(1327,232,'D'),
 (1035,230,'O'),(1783,230,'O'),(1785,205,'P'),(965,215,'X'),(1025,127,'K'),(1025,100,'F'),(1075,108,'SW'),(1055,37,'MX'),(1038,58,'T'),(1095,5,'A')]),
('t1',[(348,230,'L'),(610,230,'L'),(872,230,'L'),(1135,230,'L'),(1381,230,'L'),(1643,230,'L'),(480,195,'W'),(1042,195,'W'),(1605,195,'W'),
 (435,232,'D'),(1305,228,'D'),(733,228,'O'),(1481,228,'O'),(1503,197,'K')]),
('t2',[(107,230,'L'),(292,195,'W'),(255,232,'D'),(288,250,'O'),(1360,230,'L'),(1617,230,'L'),(1878,230,'L'),(1160,195,'W'),(1720,195,'W'),
 (1205,228,'D'),(1955,230,'D'),(1182,250,'O'),(1830,232,'O'),(1680,197,'K'),(1790,245,'P')]),
('t3',[(340,230,'L'),(588,230,'L'),(850,230,'L'),(1112,230,'L'),(1375,230,'L'),(1637,230,'L'),(480,195,'W'),(1045,195,'W'),(1607,195,'W'),
 (1025,232,'D'),(780,232,'O'),(1530,232,'O')]),
('t4',[(100,230,'L'),(363,230,'L'),(477,143,'L'),(133,232,'D'),(292,200,'W'),(432,232,'O'),(495,215,'X'),(432,127,'K'),(432,103,'F'),
 (385,128,'SW'),(428,60,'MX'),(435,32,'T'),(378,10,'A')])]

# Hall + cage d'escalier centrale, lus sur hall_<étage>.png (3x ; abs = (2250+dx/3, y0+dy/3), y0 = 470 (3E) / 2345 (2E))
H_COMMUN=[(450,298,'L'),(684,298,'L'),(450,533,'L'),(684,533,'L'),(450,768,'L'),(684,768,'L'),(243,1000,'L'),(450,1000,'L'),(668,1000,'L'),
 (887,1000,'L'),(1063,1000,'L'),(1022,825,'L'),(412,298,'D'),(405,567,'D'),(610,980,'D'),(1002,580,'D'),(613,357,'O'),(627,928,'O'),(638,398,'P'),
 (1100,825,'W'),(778,155,'W'),(1105,628,'W'),(940,790,'X'),(1005,190,'EB'),(1000,625,'EB'),(425,160,'C'),(567,162,'C'),(942,160,'C'),
 (245,1128,'C'),(407,1128,'C'),(767,1128,'C'),(928,1128,'C'),(500,168,'R'),(878,1118,'R'),(1043,675,'MX'),(375,700,'T'),(1025,712,'T'),(195,1115,'F'),
 (968,695,'A'),(195,1083,'K'),(1015,770,'F'),(1103,913,'F'),(108,958,'ISO'),(192,975,'ISO'),(1108,990,'ISO'),(1222,1003,'ISO'),
 (115,1000,'RM'),(190,1042,'RM'),(1110,1060,'RM'),(1160,1003,'RM'),(75,1037,'MRA'),(1218,1035,'MRA'),(93,1088,'B'),(1180,1085,'B')]
H_3E=[(190,805,'W'),(330,748,'W'),(650,1085,'X'),(520,1128,'R'),(305,845,'MX'),(303,882,'MRA'),(510,877,'N2'),(457,935,'N1'),(293,795,'PSU')]
H_2E=[(330,775,'W'),(375,905,'W'),(650,1045,'X'),(518,1108,'R'),(245,745,'C'),(257,857,'MX'),(330,862,'T'),(250,893,'MRA'),(365,985,'N2'),(365,1055,'N1'),
 (105,818,'VE'),(295,820,'PSU'),(190,1283,'KO'),(190,1537,'KO'),(1090,1283,'KO')]
# cages d'escalier d'extrémité (boîtes E), px raster lus sur les vues de contrôle
STAIR_END={'3E':[(813,545),(818,685),(4115,555),(4115,680)],'2E':[(813,2420),(818,2560),(4115,2430),(4115,2555)]}
