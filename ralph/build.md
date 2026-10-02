Tu es le BUILDER de la boucle Ralph pour la soumission S-1849 SIP CHUM. Objectif : rendre la sortie conforme au dossier de référence Granby, SANS rien inventer. Tu es autonome : fais tout toi-même (python ou python3, PowerShell), ne pose aucune question.

RÉFÉRENCE Granby (lis ses vrais en-têtes CSV et son manifest.json pour copier les conventions octet pour octet) : C:\Users\fvegi\Downloads\Granby-page-by-page-20260930-151234
SOURCE S-1849 (BOM corrigé, base64 -> CSV) : D:\claude\dre-estimation\ralph\bom_s1849.b64
  colonnes : Plan,Discipline,Code Canonique DR,Description Technique,Modele/Ref,Localisation,Qte Brute,Correction/Regle,Qte Finale,Unite,Statut Action,Notes Chantier,Reference feuille
SORTIE : D:\claude\dre-estimation\out\S-1849-CHUM-page-by-page-legion  (crée le dossier)

RÈGLES :
- 1 CSV par feuille réelle au schéma équipement Granby : en-tête exact "Type,Description,Quantité,Source", UTF-8 avec BOM, fins de ligne CRLF ; Type<-Code Canonique DR, Description<-Description Technique, Quantité<-Qte Finale, Source<-Reference feuille.
- Les lignes de dépose consolidée (Plan « ...P2-2-0 / 3-0 ») ne sont PAS une feuille : fichier nommé explicitement S-1849-CHUM-1-D-EL-50-P2-depose-2-0+3-0-equipment.csv (idem P3, P4, P5).
- Consolidé enrichi (traçabilité), sommaire, READ-ME.txt accentué, CRLF, sections CONTENU / PORTÉE / RÉSERVES / CHIFFRAGE / RÈGLE + « ÉLÉMENTS RÉSERVÉS — NON PRODUITS » (JPG annoté supervisé ; xlsx taux de pose ; feuille P1-3-0 absente de la source). Compte exact : « 15 feuilles + 1 groupe lots devis (16 CSV) ».
- manifest.json = [{file,bytes,sha256}] sur les CSV seulement (exclut README + manifest), trié insensible à la casse (key=str.lower), indent 2, CRLF, SANS saut de ligne final (comme Granby).
- Ne fabrique NI JPG annoté NI prix. Vérifie : luminaires INSTALLER = 507 (317 + 190), dépose 507, grillage 4, magasin 5, lots 4.
Si des « ECARTS FERMABLES A TRAITER » sont joints ci-dessous, ferme uniquement ceux-là.