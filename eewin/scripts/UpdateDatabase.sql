/******************************************************************************/
/* Création des tables, champs et stored procedures nouvelles par rapport à   */
/* la DB originale. Les éléments ici présent devraient normalement être       */
/* intégré aux script de base pour permettre aux nouveaux client s d'être à   */
/* jour sans processus exécuter ce script. Aucun concept de versionning pour  */
/* l'instant.                                                                 */
/* Chaque exécution de procédure doit toujours être nommé selon le format     */
/* VX.#YYYY ou X représente le # de version de la DB originaire de la MaJ et  */
/* YYYY le # de la procédure de MaJ. Ce numéro doit TOUJOURS être unique      */
/* Globalement et non pas par version de MaJ!                                 */
/* Le tag de MaJ doit être ensuite ajouté aux éléments modifiés dans les      */
/* fichier CreateTables.sql, CreateScripts.sql, DeleteTables.sql et           */
/* DeleteScripts.sql                                                          */
/* Finalement, ce fichier doit toujours être identique au fichier             */
/* UpdateDatabase_Calgary.sql sauf pour les éléments propre à la version      */
/* interne.                                                                   */
/******************************************************************************/
/* V0, V1 -> Version SQL Beta                                                 */
/* V2 -> Version SQL Beta, Release candidate                                  */
/*    #0001 - Ajout du champ Champ COMMITEM                                   */
/*    #0002 - Ajout du copy paste de block/division dans soumission           */
/*    #0003 - Ajout du copy paste de block/division dans facture              */
/******************************************************************************/

/******************************************************************************/
/*                                                                            */
/* Nouveaux champs - V.2                                                      */
/*                                                                            */
/******************************************************************************/

  -- V2.#0001
  -- COMMITEM.NOTES - Ajouter le champ NOTES si absent de la table et met à jour la stored proc d'Update de la table
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'COMMITEM' AND COLUMN_NAME = 'NOTES')
BEGIN
   ALTER TABLE COMMITEM ADD NOTES TEXT NULL
  
  EXEC ('ALTER PROCEDURE [dbo].[up_COMMITEM_Update] (
    @UniqueId   bigint,
    @COM_ID     varchar(20),
    @ORDRE      varchar(6),
    @PRO_ID     varchar(20),
    @CLEMANU    varchar(20),
    @CLEDIST    varchar(20),
    @CLEPERS    varchar(20),
    @PRO_TYPE   varchar(1),
    @DESCR      varchar(60),
    @QTE_TOT    float,
    @COUBRUTUNI float,
    @COUUM      varchar(2),
    @COUESC     float,
    @PROMCOUNET float,
    @QPP        float,
    @MULCOM     float,
    @CODEIMPR   varchar(2),
    @NOTES      text        = ''''
  ) AS

  IF @UniqueId IS NULL
  BEGIN
    --Insert new data into table
    INSERT INTO COMMITEM (
      [COM_ID],
      [ORDRE],
      [PRO_ID],
      [CLEMANU],
      [CLEDIST],
      [CLEPERS],
      [PRO_TYPE],
      [DESCR],
      [QTE_TOT],
      [COUBRUTUNI],
      [COUUM],
      [COUESC],
      [PROMCOUNET],
      [QPP],
      [MULCOM],
      [CODEIMPR],
      [NOTES],
      SysDate)
    VALUES (
      @COM_ID,
      @ORDRE,
      @PRO_ID,
      @CLEMANU,
      @CLEDIST,
      @CLEPERS,
      @PRO_TYPE,
      @DESCR,
      @QTE_TOT,
      @COUBRUTUNI,
      @COUUM,
      @COUESC,
      @PROMCOUNET,
      @QPP,
      @MULCOM,
      @CODEIMPR,
      @NOTES,
      GETDATE())

    --Return new ID
    RETURN @@IDENTITY
  END ELSE
  BEGIN
    --Update data into table
    UPDATE
      COMMITEM
    SET
      [COM_ID]      = @COM_ID,
      [ORDRE]       = @ORDRE,
      [PRO_ID]      = @PRO_ID,
      [CLEMANU]     = @CLEMANU,
      [CLEDIST]     = @CLEDIST,
      [CLEPERS]     = @CLEPERS,
      [PRO_TYPE]    = @PRO_TYPE,
      [DESCR]       = @DESCR,
      [QTE_TOT]     = @QTE_TOT,
      [COUBRUTUNI]  = @COUBRUTUNI,
      [COUUM]       = @COUUM,
      [COUESC]      = @COUESC,
      [PROMCOUNET]  = @PROMCOUNET,
      [QPP]         = @QPP,
      [MULCOM]      = @MULCOM,
      [CODEIMPR]    = @CODEIMPR,
      [NOTES]       = @NOTES,
      SysDate       = GETDATE()
    WHERE
      UniqueId = @UniqueId

    --Return updated ID
    RETURN @UniqueId
  END
  ')  
END
GO

   -- V2.#0002
   -- up_CopySouBlocDiv - Stored proc de copy de block / division dans soumission
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_NAME = 'up_CopySouBlocDiv' )
BEGIN
  EXEC ('CREATE PROCEDURE [dbo].up_CopySouBlocDiv (
    @OldSouID     varchar(20), 
    @NewSouID     varchar(20),
    @OldBloc      varchar(3),  
    @NewBloc      varchar(3),
    @OldDivision  varchar(3),  
    @NewDivision  varchar(3)
  ) AS

    --Trouver le prochain ORDRE dans SOUREL
  DECLARE @LastSouRelOrdre varchar(6)
  SELECT @LastSouRelOrdre = ISNULL(MAX(ORDRE), ''000000'') 
    FROM SOUREL 
    WHERE SOU_ID = @NewSouID AND TYPERELEVE = ''P'' AND BLO_ID = @NewBloc AND DIV_ID = @NewDivision

  DECLARE @UniqueId int
  DECLARE CopySouRel CURSOR FOR
  
    SELECT UniqueId 
      FROM SOUREL 
      WHERE SOU_ID = @OldSouID 
        AND TYPERELEVE = ''P'' 
        AND BLO_ID = @OldBloc 
        AND DIV_ID = @OldDivision 
      ORDER BY ORDRE

  OPEN CopySouRel

  FETCH NEXT FROM CopySouRel INTO @UniqueId

  WHILE @@FETCH_STATUS = 0
  BEGIN
      --Augmenter le prochain ORDRE
    SELECT @LastSouRelOrdre = RIGHT(''000000'' + CAST(CAST(@LastSouRelOrdre as int) + 1000 as varchar), 6)

      --Copier ce SOUREL...
    INSERT INTO SOUREL (
      SOU_ID, 
      BLO_ID, 
      DIV_ID, 
      TYPERELEVE, 
      ORDRE,
      TYPEITEM, 
      ITEM_ID, 
      DESCR, 
      QTE, 
      SECTION, 
      QTEUM,
      PROFIT, 
      TYPETAXE, 
      CODEIMPR, 
      COUTANBRUT,
      TEMPSUNIT, 
      TEMPSSEC, 
      TEMPSUM, 
      PROFITPLUS, 
      PROFITMOIN
    )
    SELECT
      @NewSouID, 
      @NewBloc, 
      @NewDivision, 
      TYPERELEVE, 
      @LastSouRelOrdre,
      TYPEITEM, 
      ITEM_ID, 
      DESCR, 
      QTE, 
      SECTION, 
      QTEUM,
      PROFIT, 
      TYPETAXE, 
      CODEIMPR, 
      COUTANBRUT,
      TEMPSUNIT, 
      TEMPSSEC, 
      TEMPSUM, 
      PROFITPLUS, 
      PROFITMOIN
      FROM SOUREL
      WHERE UniqueId = @UniqueId

      -- This is executed as long as the previous fetch succeeds.
    FETCH NEXT FROM CopySouRel INTO @UniqueId
  END

  CLOSE CopySouRel
  DEALLOCATE CopySouRel

    --Liste des ensembles à copier
  IF OBJECT_ID(''tempdb..#AssembliesToCopy'') IS NOT NULL
    DROP TABLE #AssembliesToCopy

  SELECT ITEM_ID AS ENS_ID
    INTO #AssembliesToCopy
    FROM SOUREL
    WHERE TYPEITEM = ''A''
      AND SOU_ID = @OldSouID
      AND BLO_ID = @OldBloc
      AND DIV_ID = @OldDivision
      AND ITEM_ID NOT IN (SELECT ENS_ID FROM SOUENS WHERE SOU_ID = @NewSouID)
    GROUP BY ITEM_ID

    --Copier les SOUENS
  INSERT INTO SOUENS (
    SOU_ID, 
    ENS_ID, 
    [DESC],
    QTETOT, 
    QTETOTSECT, 
    CALCTIMSTP, 
    COUUM,
    TEMPUNI, 
    TEMPSEC, 
    TEMPUM,
    DATECREE, 
    OLDESTPROD, 
    CLEPERS, 
    PROFIT
  )
  SELECT DISTINCT
    @NewSouID, 
    ENS_ID, 
    [DESC],
    QTETOT, 
    QTETOTSECT, 
    CALCTIMSTP, 
    COUUM,
    TEMPUNI, 
    TEMPSEC, 
    TEMPUM,
    DATECREE, 
    OLDESTPROD, 
    CLEPERS, 
    PROFIT
    FROM SOUENS
    WHERE ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy)

    --Copier les SOUENSCO
  INSERT INTO SOUENSCO (
    SOU_ID, 
    ENS_ID, 
    PRO_ID,
    ORDRE, 
    QTE, 
    QTEUM,
    TYPRATIO, 
    DIV, 
    DIVUM
  )
  SELECT
    @NewSouID, 
    ENS_ID, 
    PRO_ID,
    ORDRE, 
    QTE, 
    QTEUM,
    TYPRATIO, 
    DIV, 
    DIVUM
    FROM SOUENSCO
    WHERE ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy)

    --Liste des lots à copier
  IF OBJECT_ID(''tempdb..#LotsToCopy'') IS NOT NULL
    DROP TABLE #LotsToCopy

  SELECT ITEM_ID AS LOTS_ID
    INTO #LotsToCopy
    FROM SOUREL
    WHERE TYPEITEM = ''L''
      AND SOU_ID = @OldSouID
      AND BLO_ID = @OldBloc
      AND DIV_ID = @OldDivision
      AND ITEM_ID NOT IN (SELECT LOTS_ID FROM SOULOTS WHERE SOU_ID = @NewSouID)
    GROUP BY ITEM_ID

    --Copier les SOULOTS
  INSERT INTO SOULOTS (
    SOU_ID, 
    LOTS_ID, 
    [DESC],
    QTETOT, 
    QTETOTSECT, 
    CALCTIMSTP, 
    COUUM,
    TEMPUNI, 
    TEMPUM, 
    DATECREE, 
    OLDESTPROD,
    CLEPERS, 
    PROFIT, 
    COUTANTSEL,
    COUTANT1, 
    COUTANT2, 
    COUTANT3, 
    COUTANT4
  )
  SELECT DISTINCT
    @NewSouID, 
    LOTS_ID, 
    [DESC],
    QTETOT, 
    QTETOTSECT, 
    CALCTIMSTP, 
    COUUM,
    TEMPUNI, 
    TEMPUM, 
    DATECREE, 
    OLDESTPROD,
    CLEPERS, 
    PROFIT, 
    COUTANTSEL,
    COUTANT1, 
    COUTANT2, 
    COUTANT3, 
    COUTANT4
  FROM SOULOTS
  WHERE LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy)

    --Copier les SOULOTSCO
  INSERT INTO SOULOTSCO (
    SOU_ID, 
    LOTS_ID, 
    PRO_ID, 
    ORDRE, 
    QTE, 
    QTEUM
  )
  SELECT
    @NewSouID, 
    LOTS_ID, 
    PRO_ID, 
    ORDRE, 
    QTE, 
    QTEUM
  FROM SOULOTSCO
  WHERE LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy)

    --Liste des produits à copier
  IF OBJECT_ID(''tempdb..#ProductsToCopy'') IS NOT NULL
    DROP TABLE #ProductsToCopy

    --Produits à copier...
  SELECT ITEM_ID AS PRO_ID
    INTO #ProductsToCopy
    FROM SOUREL
    WHERE TYPEITEM NOT IN (''A'', ''L'', ''T'')
      AND SOU_ID = @OldSouID
      AND BLO_ID = @OldBloc
      AND DIV_ID = @OldDivision
      AND ITEM_ID NOT IN (SELECT PRO_ID FROM SOUPRO WHERE SOU_ID = @NewSouID)
    GROUP BY ITEM_ID

    --Produits à copier (ensembles)
  INSERT INTO #ProductsToCopy (PRO_ID)
    SELECT PRO_ID
    FROM SOUENSCO
    WHERE ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy)
      AND PRO_ID NOT IN (SELECT PRO_ID FROM SOUPRO WHERE SOU_ID = @NewSouID)

    --Produits à copier (lots)
  INSERT INTO #ProductsToCopy (PRO_ID)
    SELECT PRO_ID
    FROM SOULOTSCO
    WHERE LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy)
      AND PRO_ID NOT IN (SELECT PRO_ID FROM SOUPRO WHERE SOU_ID = @NewSouID)

  INSERT INTO SOUPRO (
    SOU_ID, 
    PRO_ID, 
    CLEMANU, 
    CLEDIST, 
    CLEPERS, 
    [DESC],
    QTEENS, 
    QTELOT, 
    QTEOTH, 
    CALCTIMSTP, 
    COUBRUTUNI, 
    COUUM, 
    QPP, 
    COUESC,
    PROMCOUNET, 
    TEMPUNI, 
    TEMPUM, 
    MULCOM, 
    CODEIMPR, 
    CODEFOUR, 
    CODECAT,
    DATECOUT, 
    QTECOM, 
    QTEACOM
  )
  SELECT
    @NewSouID, 
    PRO_ID, 
    CLEMANU, 
    CLEDIST, 
    CLEPERS, 
    [DESC],
    QTEENS, 
    QTELOT, 
    QTEOTH, 
    CALCTIMSTP, 
    COUBRUTUNI, 
    COUUM, 
    QPP, 
    COUESC,
    PROMCOUNET, 
    TEMPUNI, 
    TEMPUM, 
    MULCOM, 
    CODEIMPR, 
    CODEFOUR, 
    CODECAT,
    DATECOUT, 
    QTECOM, 
    QTEACOM
    FROM SOUPRO
    WHERE PRO_ID IN (SELECT PRO_ID FROM #ProductsToCopy)

  DROP TABLE #AssembliesToCopy
  DROP TABLE #LotsToCopy
  DROP TABLE #ProductsToCopy
  ')
END
GO


   -- V2.#0003
   -- up_CopySouBlocDiv_FAC - Stored proc de copy de block / division dans facture
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_NAME = 'up_CopySouBlocDiv_FAC' )
BEGIN
  EXEC('CREATE PROCEDURE [dbo].up_CopySouBlocDiv_FAC (
    @OldSouID     varchar(20), 
    @NewSouID     varchar(20),
    @OldBloc      varchar(3),  
    @NewBloc      varchar(3),
    @OldDivision  varchar(3),  
    @NewDivision  varchar(3)
  ) AS

    --Trouver le prochain ORDRE dans FACREL
  DECLARE @LastSouRelOrdre varchar(6)
  SELECT @LastSouRelOrdre = ISNULL(MAX(ORDRE), ''000000'') 
    FROM FACREL 
    WHERE SOU_ID = @NewSouID 
      AND TYPERELEVE = ''P'' 
      AND BLO_ID = @NewBloc 
      AND DIV_ID = @NewDivision

  DECLARE @UniqueId int
  DECLARE CopySouRel CURSOR FOR
  
    SELECT UniqueId 
      FROM FACREL 
      WHERE SOU_ID = @OldSouID 
        AND TYPERELEVE = ''P'' 
        AND BLO_ID = @OldBloc 
        AND DIV_ID = @OldDivision 
      ORDER BY ORDRE 

  OPEN CopySouRel

  FETCH NEXT FROM CopySouRel INTO @UniqueId

  WHILE @@FETCH_STATUS = 0
  BEGIN
      --Augmenter le prochain ORDRE
    SELECT @LastSouRelOrdre = RIGHT(''000000'' + CAST(CAST(@LastSouRelOrdre as int) + 1000 as varchar), 6)

    --Copier ce FACREL...
    INSERT INTO FACREL (
      SOU_ID, 
      BLO_ID, 
      DIV_ID, 
      TYPERELEVE, 
      ORDRE,
      TYPEITEM, 
      ITEM_ID, 
      DESCR, 
      QTE, 
      SECTION, 
      QTEUM,
      PROFIT, 
      TYPETAXE, 
      CODEIMPR, 
      COUTANBRUT,
      TEMPSUNIT, 
      TEMPSSEC, 
      TEMPSUM, 
      PROFITPLUS, 
      PROFITMOIN
    )
    SELECT
      @NewSouID, 
      @NewBloc, 
      @NewDivision, 
      TYPERELEVE, 
      @LastSouRelOrdre,
      TYPEITEM, 
      ITEM_ID, 
      DESCR, 
      QTE, 
      SECTION, 
      QTEUM,
      PROFIT, 
      TYPETAXE, 
      CODEIMPR, 
      COUTANBRUT,
      TEMPSUNIT, 
      TEMPSSEC, 
      TEMPSUM, 
      PROFITPLUS, 
      PROFITMOIN
      FROM FACREL
      WHERE UniqueId = @UniqueId

      -- This is executed as long as the previous fetch succeeds.
    FETCH NEXT FROM CopySouRel INTO @UniqueId
  END

  CLOSE CopySouRel
  DEALLOCATE CopySouRel

    --Liste des ensembles à copier
  IF OBJECT_ID(''tempdb..#AssembliesToCopy'') IS NOT NULL
    DROP TABLE #AssembliesToCopy

  SELECT ITEM_ID AS ENS_ID
    INTO #AssembliesToCopy
    FROM FACREL
    WHERE TYPEITEM = ''A''
      AND SOU_ID = @OldSouID
      AND BLO_ID = @OldBloc
      AND DIV_ID = @OldDivision
      AND ITEM_ID NOT IN (SELECT ENS_ID FROM FACENS WHERE SOU_ID = @NewSouID)
    GROUP BY ITEM_ID

    --Copier les FACENS
  INSERT INTO FACENS (
    SOU_ID, 
    ENS_ID, 
    [DESC],
    QTETOT, 
    QTETOTSECT, 
    CALCTIMSTP, 
    COUUM,
    TEMPUNI, 
    TEMPSEC, 
    TEMPUM,
    DATECREE, 
    OLDESTPROD, 
    CLEPERS, 
    PROFIT
  )
  SELECT DISTINCT
    @NewSouID, 
    ENS_ID, 
    [DESC],
    QTETOT, 
    QTETOTSECT, 
    CALCTIMSTP, 
    COUUM,
    TEMPUNI, 
    TEMPSEC, 
    TEMPUM,
    DATECREE, 
    OLDESTPROD, 
    CLEPERS, 
    PROFIT
    FROM FACENS
    WHERE ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy)

    --Copier les FACENSCO
  INSERT INTO FACENSCO (
    SOU_ID, 
    ENS_ID, 
    PRO_ID,
    ORDRE, 
    QTE, 
    QTEUM,
    TYPRATIO, 
    DIV, 
    DIVUM
  )
  SELECT
    @NewSouID, 
    ENS_ID, 
    PRO_ID,
    ORDRE, 
    QTE, 
    QTEUM,
    TYPRATIO, 
    DIV, 
    DIVUM
    FROM FACENSCO
    WHERE ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy)

    --Liste des lots à copier
  IF OBJECT_ID(''tempdb..#LotsToCopy'') IS NOT NULL
    DROP TABLE #LotsToCopy

  SELECT ITEM_ID AS LOTS_ID
    INTO #LotsToCopy
    FROM FACREL
    WHERE TYPEITEM = ''L''
      AND SOU_ID = @OldSouID
      AND BLO_ID = @OldBloc
      AND DIV_ID = @OldDivision
      AND ITEM_ID NOT IN (SELECT LOTS_ID FROM FACLOTS WHERE SOU_ID = @NewSouID)
    GROUP BY ITEM_ID

    --Copier les FACLOTS
  INSERT INTO FACLOTS (
    SOU_ID, 
    LOTS_ID, 
    [DESC],
    QTETOT, 
    QTETOTSECT, 
    CALCTIMSTP, 
    COUUM,
    TEMPUNI, 
    TEMPUM, 
    DATECREE, 
    OLDESTPROD,
    CLEPERS, 
    PROFIT, 
    COUTANTSEL,
    COUTANT1, 
    COUTANT2, 
    COUTANT3, 
    COUTANT4
  )
  SELECT DISTINCT
    @NewSouID, 
    LOTS_ID, 
    [DESC],
    QTETOT, 
    QTETOTSECT, 
    CALCTIMSTP, 
    COUUM,
    TEMPUNI, 
    TEMPUM, 
    DATECREE, 
    OLDESTPROD,
    CLEPERS, 
    PROFIT, 
    COUTANTSEL,
    COUTANT1, 
    COUTANT2, 
    COUTANT3, 
    COUTANT4
    FROM FACLOTS
    WHERE LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy)

    --Copier les FACLOTSCO
  INSERT INTO FACLOTSCO (
    SOU_ID, 
    LOTS_ID, 
    PRO_ID, 
    ORDRE, 
    QTE, 
    QTEUM
  )
  SELECT
    @NewSouID, 
    LOTS_ID, 
    PRO_ID, 
    ORDRE, 
    QTE, 
    QTEUM
    FROM FACLOTSCO
    WHERE LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy)

    --Liste des produits à copier
  IF OBJECT_ID(''tempdb..#ProductsToCopy'') IS NOT NULL
    DROP TABLE #ProductsToCopy

    --Produits à copier...
  SELECT ITEM_ID AS PRO_ID
    INTO #ProductsToCopy
    FROM FACREL
    WHERE TYPEITEM NOT IN (''A'', ''L'', ''T'')
      AND SOU_ID = @OldSouID
      AND BLO_ID = @OldBloc
      AND DIV_ID = @OldDivision
      AND ITEM_ID NOT IN (SELECT PRO_ID FROM FACPRO WHERE SOU_ID = @NewSouID)
    GROUP BY ITEM_ID

    --Produits à copier (ensembles)
  INSERT INTO #ProductsToCopy (PRO_ID)
  SELECT PRO_ID
    FROM FACENSCO
    WHERE ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy)
      AND PRO_ID NOT IN (SELECT PRO_ID FROM FACPRO WHERE SOU_ID = @NewSouID)

    --Produits à copier (lots)
  INSERT INTO #ProductsToCopy (PRO_ID)
  SELECT PRO_ID
    FROM FACLOTSCO
    WHERE LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy)
      AND PRO_ID NOT IN (SELECT PRO_ID FROM FACPRO WHERE SOU_ID = @NewSouID)

  INSERT INTO FACPRO (
    SOU_ID, 
    PRO_ID, 
    CLEMANU, 
    CLEDIST, 
    CLEPERS, 
    [DESC],
    QTEENS, 
    QTELOT, 
    QTEOTH, 
    CALCTIMSTP, 
    COUBRUTUNI, 
    COUUM, 
    QPP, 
    COUESC,
    PROMCOUNET, 
    TEMPUNI, 
    TEMPUM, 
    MULCOM, 
    CODEIMPR, 
    CODEFOUR, 
    CODECAT,
    DATECOUT, 
    QTECOM, 
    QTEACOM
  )
  SELECT
    @NewSouID, 
    PRO_ID, 
    CLEMANU, 
    CLEDIST, 
    CLEPERS, 
    [DESC],
    QTEENS, 
    QTELOT, 
    QTEOTH, 
    CALCTIMSTP, 
    COUBRUTUNI, 
    COUUM, 
    QPP, 
    COUESC,
    PROMCOUNET, 
    TEMPUNI, 
    TEMPUM, 
    MULCOM, 
    CODEIMPR, 
    CODEFOUR, 
    CODECAT,
    DATECOUT, 
    QTECOM, 
    QTEACOM
    FROM FACPRO
    WHERE PRO_ID IN (SELECT PRO_ID FROM #ProductsToCopy)

  DROP TABLE #AssembliesToCopy
  DROP TABLE #LotsToCopy
  DROP TABLE #ProductsToCopy
  ')
END
GO
