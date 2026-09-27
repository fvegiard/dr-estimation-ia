  -- 2015-02-10 EE-263 EMadore 
  -- Script de MaJ pour prix net rexel phase 2

  -- New field - Produits.PREFERED
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'PRODUITS'
    AND [COLUMN_NAME] = 'PREFERED' )
BEGIN
  ALTER TABLE
    PRODUITS
  ADD
    PREFERED VARCHAR(1)
END
GO

ALTER PROCEDURE [dbo].[up_PRODUITS_Update] (
  @UniqueId bigint,
  @PRO_ID varchar(20),
  @CLEMANU varchar(20),
  @CLEPERS varchar(20),
  @CLEDIST varchar(20),
  @CODEUPC varchar(12),
  @CODECAT varchar(3),
  @DESCDIST varchar(60),
  @DESC varchar(60),
  @COUBRUTUNI float,
  @COUUM varchar(2),
  @QPP float,
  @COUESC float,
  @PROMCOUNET float,
  @PROFIT float,
  @MULCOM float,
  @TEMPUNI float,
  @TEMPUM varchar(2),
  @CODEFOUR varchar(2),
  @NOUVEAU varchar(1),
  @DNR varchar(1),
  @DATECOUT datetime,
  @DATECOUNET datetime,   -- V7 EE-222 - Prix net Rexel
  @RESCOUNET int,         -- V7 EE-222 - Prix net Rexel
  @DATECREE datetime,
  @PATHPICT varchar(60),
  @PATHSPEC varchar(60),
  @IMAGE varchar(1),
  @USER1 varchar(20),
  @USER2 varchar(20),
  @PREFERED varchar(1)    -- V8 EE-263 - Prix net Rexel Phase 2
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO PRODUITS (
    [PRO_ID],
    [CLEMANU],
    [CLEPERS],
    [CLEDIST],
    [CODEUPC],
    [CODECAT],
    [DESCDIST],
    [DESC],
    [COUBRUTUNI],
    [COUUM],
    [QPP],
    [COUESC],
    [PROMCOUNET],
    [PROFIT],
    [MULCOM],
    [TEMPUNI],
    [TEMPUM],
    [CODEFOUR],
    [NOUVEAU],
    [DNR],
    [DATECOUT],
    [DATECOUNET],   -- V7 EE-222 - Prix net Rexel
    [RESCOUNET],    -- V7 EE-222 - Prix net Rexel
    [DATECREE],
    [PATHPICT],
    [PATHSPEC],
    [IMAGE],
    [USER1],
    [USER2],
    [PREFERED],     -- V8 EE-263 - Prix net Rexel Phase 2
    SysDate)
  VALUES (
    @PRO_ID,
    @CLEMANU,
    @CLEPERS,
    @CLEDIST,
    @CODEUPC,
    @CODECAT,
    @DESCDIST,
    @DESC,
    @COUBRUTUNI,
    @COUUM,
    @QPP,
    @COUESC,
    @PROMCOUNET,
    @PROFIT,
    @MULCOM,
    @TEMPUNI,
    @TEMPUM,
    @CODEFOUR,
    @NOUVEAU,
    @DNR,
    @DATECOUT,
    @DATECOUNET,  -- V7 EE-222 - Prix net Rexel
    @RESCOUNET,   -- V7 EE-222 - Prix net Rexel
    @DATECREE,
    @PATHPICT,
    @PATHSPEC,
    @IMAGE,
    @USER1,
    @USER2,
    @PREFERED,    -- V8 EE-263 - Prix net Rexel Phase 2
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    PRODUITS
  SET
    [PRO_ID] = @PRO_ID,
    [CLEMANU] = @CLEMANU,
    [CLEPERS] = @CLEPERS,
    [CLEDIST] = @CLEDIST,
    [CODEUPC] = @CODEUPC,
    [CODECAT] = @CODECAT,
    [DESCDIST] = @DESCDIST,
    [DESC] = @DESC,
    [COUBRUTUNI] = @COUBRUTUNI,
    [COUUM] = @COUUM,
    [QPP] = @QPP,
    [COUESC] = @COUESC,
    [PROMCOUNET] = @PROMCOUNET,
    [PROFIT] = @PROFIT,
    [MULCOM] = @MULCOM,
    [TEMPUNI] = @TEMPUNI,
    [TEMPUM] = @TEMPUM,
    [CODEFOUR] = @CODEFOUR,
    [NOUVEAU] = @NOUVEAU,
    [DNR] = @DNR,
    [DATECOUT] = @DATECOUT,
    [DATECOUNET] = @DATECOUNET,   -- V7 EE-222 - Prix net Rexel
    [RESCOUNET] = @RESCOUNET,     -- V7 EE-222 - Prix net Rexel
    [DATECREE] = @DATECREE,
    [PATHPICT] = @PATHPICT,
    [PATHSPEC] = @PATHSPEC,
    [IMAGE] = @IMAGE,
    [USER1] = @USER1,
    [USER2] = @USER2,
    [PREFERED] = CASE WHEN @PREFERED IS NULL THEN [PREFERED] ELSE @PREFERED END,  -- V8 EE-263 - Prix net Rexel Phase 2
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- Procedure pour retourner des messages à l'application appelante
IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'upbi_ReturnMessage')
  DROP PROCEDURE upbi_ReturnMessage
GO

CREATE PROCEDURE [dbo].upbi_ReturnMessage(
    @EnglishMessage varchar(255),
    @FrenchMessage varchar(255) = '',
    @PrintEnglish bit = 1,
    @PrintMessages bit = 1,
    @MessageState int = 1,        -- Maximum 255, voir raiseerror
    @MessageSeverity int = 1      -- voir RAISERROR
  ) AS
BEGIN
  IF @PrintMessages = 1
  BEGIN
    IF @PrintEnglish = 1
      RAISERROR (@EnglishMessage, @MessageState, @MessageSeverity) WITH NOWAIT
    ELSE
      RAISERROR (@FrenchMessage, @MessageState, @MessageSeverity) WITH NOWAIT
  END
END
GO

  -- Procedure pour assigner en lots les produits préféré selon leurs usages dans le système
IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'upbi_ProductsPrefered_BatchAssign')
  DROP PROCEDURE upbi_ProductsPrefered_BatchAssign
GO

CREATE PROCEDURE [dbo].upbi_ProductsPrefered_BatchAssign(
    @ConsiderPersonalKey bit,
    @ConsiderAssemblies bit,
    @ConsiderPurchases bit,
    @ConsiderQuotations bit,
    @ConsiderInvoices bit,
    @LimitDate datetime,

    @ShowEnglish bit = 1,
    @ShowMessages bit = 1
  ) AS
BEGIN 
  SET NOCOUNT ON

	IF OBJECT_ID('tempdb..#CandidatesProducts') IS NOT NULL
		DROP TABLE #CandidatesProducts

  CREATE TABLE [dbo].#CandidatesProducts (
      PRO_ID    varchar(20) COLLATE DATABASE_DEFAULT
    ) 

    -- Produits candidats depuis la clé personelles
  IF @ConsiderPersonalKey = 1
  BEGIN
    EXEC upbi_ReturnMessage 'Scanning Personal Keys...', 'Évaluation des clés personnelles...', @ShowEnglish, @ShowMessages
   
    INSERT INTO 
      #CandidatesProducts
    SELECT
      PRO_ID
    FROM
      PRODUITS
    WHERE
      CLEPERS <> ''
  END

    -- Produits candidats depuis les ensembles
  IF @ConsiderAssemblies = 1
  BEGIN 
    EXEC upbi_ReturnMessage 'Scanning Assemblies...', 'Évaluation des ensembles...', @ShowEnglish, @ShowMessages

    INSERT INTO 
      #CandidatesProducts
    SELECT
      PRO_ID
    FROM
      ENSCOMPO
    GROUP BY
      PRO_ID
  END

    -- Produits candidats depuis les commandes d'achats
  IF @ConsiderPurchases = 1
  BEGIN 
    EXEC upbi_ReturnMessage 'Scanning Purchases...', 'Évaluation des achats...', @ShowEnglish, @ShowMessages
    
    INSERT INTO 
      #CandidatesProducts
    SELECT
      COMMITEM.PRO_ID
    FROM
      COMMITEM
      INNER JOIN COMMANDE
      ON COMMITEM.COM_ID = COMMANDE.COM_ID
    WHERE
      LEFT(COMMITEM.PRO_ID, 3) <> 'NLS'
      AND COMMANDE.DATE_CREE >= @LimitDate  
    GROUP BY
      COMMITEM.PRO_ID
  END

    -- Produits candidats depuis les soumissions
  IF @ConsiderQuotations = 1
  BEGIN 
    EXEC upbi_ReturnMessage 'Scanning Quotations...', 'Évaluation des soumissions...', @ShowEnglish, @ShowMessages

    INSERT INTO 
      #CandidatesProducts
    SELECT
      SOUPRO.PRO_ID
    FROM
      SOUPRO
      INNER JOIN SOUMIS
      ON SOUPRO.SOU_ID = SOUMIS.SOU_ID  
    WHERE
      LEFT(SOUPRO.PRO_ID, 3) <> 'NLS'  
      AND SOUMIS.DATEDOC >= @LimitDate  
    GROUP BY
      SOUPRO.PRO_ID
  END

    -- Produits candidats depuis les factures
  IF @ConsiderInvoices = 1
  BEGIN 
    EXEC upbi_ReturnMessage 'Scanning Invoices...', 'Évaluation des factures...', @ShowEnglish, @ShowMessages

    INSERT INTO 
      #CandidatesProducts
    SELECT
      FACPRO.PRO_ID
    FROM
      FACPRO
      INNER JOIN FACTURES
      ON FACPRO.SOU_ID = FACTURES.SOU_ID  
    WHERE
      LEFT(FACPRO.PRO_ID, 3) <> 'NLS'  
      AND FACTURES.DATEDOC >= @LimitDate  
    GROUP BY
      FACPRO.PRO_ID
  END

    -- Mise à jour de l'état préféré
  EXEC upbi_ReturnMessage 'Updating products...', 'Mise à jour des produits...', @ShowEnglish, @ShowMessages

  UPDATE
    PRODUITS
  SET
    PREFERED = '1'
  FROM
    PRODUITS
    INNER JOIN #CandidatesProducts
    ON PRODUITS.PRO_ID = #CandidatesProducts.PRO_ID
  WHERE
    (PRODUITS.PREFERED = '') OR (PRODUITS.PREFERED IS NULL)

    -- Nécessaire pour être Compatible Feedback. Doit avoir un ResultSet car les procedure bidirectionelles s'ouvre avec u Open
  SELECT 1
END
GO

  -- Procedure pour retirer en lots les produits préféré selon leurs usages dans le système
IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'upbi_ProductsPrefered_BatchRemove')
  DROP PROCEDURE upbi_ProductsPrefered_BatchRemove
GO

CREATE PROCEDURE [dbo].upbi_ProductsPrefered_BatchRemove(
    @PreserveByPersonnalKey bit,
    @PreserveByAssemblies bit,
    @LimitDate datetime,

    @ShowEnglish bit = 1,
    @ShowMessages bit = 1
  ) AS
BEGIN 
  SET NOCOUNT ON

	IF OBJECT_ID('tempdb..#PreferedProducts') IS NOT NULL
		DROP TABLE #PreferedProducts

  CREATE TABLE [dbo].#PreferedProducts (
      PRO_ID    varchar(20) COLLATE DATABASE_DEFAULT
    ) 

	IF OBJECT_ID('tempdb..#CandidatesProducts') IS NOT NULL
		DROP TABLE #CandidatesProducts

  CREATE TABLE [dbo].#CandidatesProducts (
      PRO_ID    varchar(20) COLLATE DATABASE_DEFAULT
    ) 

    -- Commence par extraire les produits préféré
  EXEC upbi_ReturnMessage 'Identifying prefered products...', 'Identification des produits préférés...', @ShowEnglish, @ShowMessages
   
  INSERT INTO 
    #PreferedProducts
  SELECT
    PRO_ID
  FROM
    PRODUITS
  WHERE
    PREFERED <> ''

    -- Vérifie si les produits avec clé personelle sont admissible
  IF @PreserveByPersonnalKey = 1
  BEGIN
    EXEC upbi_ReturnMessage 'Scanning Personal Keys...', 'Évaluation des clés personnelles...', @ShowEnglish, @ShowMessages
   
    INSERT INTO 
      #CandidatesProducts
    SELECT
      #PreferedProducts.PRO_ID
    FROM
      #PreferedProducts
      INNER JOIN PRODUITS
      ON #PreferedProducts.PRO_ID = PRODUITS.PRO_ID
    WHERE
      PRODUITS.CLEPERS <> ''
  END

    -- Vérifie si les produits présent dans les ensembles sont admissibles
  IF @PreserveByAssemblies = 1
  BEGIN 
    EXEC upbi_ReturnMessage 'Scanning Assemblies...', 'Évaluation des ensembles...', @ShowEnglish, @ShowMessages

    INSERT INTO 
      #CandidatesProducts
    SELECT
      #PreferedProducts.PRO_ID
    FROM
      #PreferedProducts
      INNER JOIN ENSCOMPO
      ON #PreferedProducts.PRO_ID = ENSCOMPO.PRO_ID
  END

    -- Détermine ce qui à été utilisé dernièrement 
  EXEC upbi_ReturnMessage 'Scanning Purchases...', 'Évaluation des achats...', @ShowEnglish, @ShowMessages
    
  INSERT INTO 
    #CandidatesProducts
  SELECT
    #PreferedProducts.PRO_ID
  FROM
    #PreferedProducts
    INNER JOIN COMMITEM
    ON #PreferedProducts.PRO_ID = COMMITEM.PRO_ID
    INNER JOIN COMMANDE
    ON COMMITEM.COM_ID = COMMANDE.COM_ID
  WHERE
    COMMANDE.DATE_CREE >= @LimitDate  


  EXEC upbi_ReturnMessage 'Scanning Quotations...', 'Évaluation des soumissions...', @ShowEnglish, @ShowMessages
    
  INSERT INTO 
    #CandidatesProducts
  SELECT
    #PreferedProducts.PRO_ID
  FROM
    #PreferedProducts
    INNER JOIN SOUPRO
    ON #PreferedProducts.PRO_ID = SOUPRO.PRO_ID
    INNER JOIN SOUMIS
    ON SOUPRO.SOU_ID = SOUMIS.SOU_ID
  WHERE
    SOUMIS.DATEDOC >= @LimitDate  

  EXEC upbi_ReturnMessage 'Scanning Invoices...', 'Évaluation des factures...', @ShowEnglish, @ShowMessages
    
  INSERT INTO 
    #CandidatesProducts
  SELECT
    #PreferedProducts.PRO_ID
  FROM
    #PreferedProducts
    INNER JOIN FACPRO
    ON #PreferedProducts.PRO_ID = FACPRO.PRO_ID
    INNER JOIN FACTURES
    ON FACPRO.SOU_ID = FACTURES.SOU_ID
  WHERE
    FACTURES.DATEDOC >= @LimitDate  

    -- Mise à jour de l'état préféré
  EXEC upbi_ReturnMessage 'Updating products...', 'Mise à jour des produits...', @ShowEnglish, @ShowMessages

  UPDATE
    PRODUITS
  SET
    PREFERED = ''
  FROM
    PRODUITS
    INNER JOIN #PreferedProducts
    ON PRODUITS.PRO_ID = #PreferedProducts.PRO_ID 
    FULL JOIN #CandidatesProducts
    ON #PreferedProducts.PRO_ID = #CandidatesProducts.PRO_ID
  WHERE
    #CandidatesProducts.PRO_ID is NULL

    -- Nécessaire pour être Compatible Feedback. Doit avoir un ResultSet car les procedure bidirectionelles s'ouvre avec u Open
  SELECT 1
END
GO
