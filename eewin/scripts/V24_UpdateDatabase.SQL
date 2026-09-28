
----- corriger les nom de sp SOUMIS/FACTURES

IF (OBJECT_ID(N'dbo.sp_UpdateQteTotalOth', N'P') IS NOT NULL) AND
   (OBJECT_ID(N'dbo.sp_SOU_UpdateQteTotalOth', N'P') IS NULL)
  EXEC sp_rename 'dbo.sp_UpdateQteTotalOth', 'dbo.sp_SOU_UpdateQteTotalOth';
GO

IF (OBJECT_ID(N'dbo.sp_UpdateQteTotalEns', N'P') IS NOT NULL) AND
   (OBJECT_ID(N'dbo.sp_SOU_UpdateQteTotalEns', N'P') IS NULL)
  EXEC sp_rename 'dbo.sp_UpdateQteTotalEns', 'dbo.sp_SOU_UpdateQteTotalEns';
GO

IF (OBJECT_ID(N'dbo.sp_UpdateQteTotalLots', N'P') IS NOT NULL) AND
   (OBJECT_ID(N'dbo.sp_SOU_UpdateQteTotalLots', N'P') IS NULL)
  EXEC sp_rename 'dbo.sp_UpdateQteTotalLots', 'dbo.sp_SOU_UpdateQteTotalLots';
GO

IF (OBJECT_ID(N'dbo.sp_CalculQteTotalItem', N'P') IS NOT NULL) AND
   (OBJECT_ID(N'dbo.sp_SOU_CalculQteTotalItem', N'P') IS NULL)
  EXEC sp_rename 'dbo.sp_CalculQteTotalItem', 'dbo.sp_SOU_CalculQteTotalItem';
GO

IF (OBJECT_ID(N'dbo.sp_GetAssemblyCompositionConcat', N'P') IS NOT NULL) AND
   (OBJECT_ID(N'dbo.sp_SOU_GetAssemblyCompositionConcat', N'P') IS NULL)
  EXEC sp_rename 'dbo.sp_GetAssemblyCompositionConcat', 'dbo.sp_SOU_GetAssemblyCompositionConcat';
GO

IF (OBJECT_ID(N'dbo.sp_CalculProductUsageInAssemblies', N'P') IS NOT NULL) AND
   (OBJECT_ID(N'dbo.sp_SOU_CalculProductUsageInAssemblies', N'P') IS NULL)
  EXEC sp_rename 'dbo.sp_CalculProductUsageInAssemblies', 'dbo.sp_SOU_CalculProductUsageInAssemblies';
GO

IF (OBJECT_ID(N'dbo.sp_CalculCodeImpr', N'P') IS NOT NULL) AND
   (OBJECT_ID(N'dbo.sp_SOU_CalculCodeImpr', N'P') IS NULL)
  EXEC sp_rename 'dbo.sp_CalculCodeImpr', 'dbo.sp_SOU_CalculCodeImpr';
GO

IF (OBJECT_ID(N'dbo.up_SOUPRO_Quantity', N'P') IS NOT NULL) AND
   (OBJECT_ID(N'dbo.sp_SOUPRO_Quantity', N'P') IS NULL)
  EXEC sp_rename 'dbo.up_SOUPRO_Quantity', 'dbo.sp_SOUPRO_Quantity';
GO




--------  V21_UpdateDatabase pour Factures


IF OBJECT_ID(N'dbo.sp_FAC_UpdateQteTotalOth', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_FAC_UpdateQteTotalOth ;
GO

CREATE PROCEDURE [dbo].sp_FAC_UpdateQteTotalOth (@SOU_ID VARCHAR(20), @ITEM_ID VARCHAR(20), @CALCTIMSTP VARCHAR(14), @UID VARCHAR(14), @QTE_TOTAL FLOAT)
AS BEGIN
   IF @CALCTIMSTP = @UID 
   BEGIN
     UPDATE FACPRO
     SET   QTEOTH   = QTEOTH + @QTE_TOTAL
     WHERE   SOU_ID = @SOU_ID
     AND     PRO_ID = @ITEM_ID 
   END ELSE
   BEGIN
     UPDATE FACPRO
     SET QTEOTH     = @QTE_TOTAL,
         CALCTIMSTP = @UID
     WHERE   SOU_ID = @SOU_ID
     AND     PRO_ID = @ITEM_ID     
   END
END
GO

IF OBJECT_ID(N'dbo.sp_FAC_UpdateQteTotalEns', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_FAC_UpdateQteTotalEns ;
GO

CREATE PROCEDURE [dbo].sp_FAC_UpdateQteTotalEns (@SOU_ID VARCHAR(20), @ITEM_ID VARCHAR(20), @CALCTIMSTP VARCHAR(14), @UID VARCHAR(14), @QTE_TOTAL FLOAT)
AS BEGIN
   IF @CALCTIMSTP = @UID 
   BEGIN
     UPDATE FACPRO
     SET   QTEENS   = QTEENS + @QTE_TOTAL
     WHERE   SOU_ID = @SOU_ID
     AND     PRO_ID = @ITEM_ID 
   END ELSE
   BEGIN
     UPDATE FACPRO
     SET QTEENS     = @QTE_TOTAL,
         CALCTIMSTP = @UID
     WHERE   SOU_ID = @SOU_ID
     AND     PRO_ID = @ITEM_ID     
   END
END
GO

IF OBJECT_ID(N'dbo.sp_FAC_UpdateQteTotalLots', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_FAC_UpdateQteTotalLots ;
GO

CREATE PROCEDURE [dbo].sp_FAC_UpdateQteTotalLots (@SOU_ID VARCHAR(20), @ITEM_ID VARCHAR(20), @CALCTIMSTP VARCHAR(14), @UID VARCHAR(14), @QTE_TOTAL FLOAT)
AS BEGIN
   IF @CALCTIMSTP = @UID 
   BEGIN
     UPDATE FACPRO
     SET   QTELOT   = QTELOT + @QTE_TOTAL
     WHERE   SOU_ID = @SOU_ID
     AND     PRO_ID = @ITEM_ID 
   END ELSE
   BEGIN
     UPDATE FACPRO
     SET QTELOT     = @QTE_TOTAL,
         CALCTIMSTP = @UID
     WHERE   SOU_ID = @SOU_ID
     AND     PRO_ID = @ITEM_ID     
   END
END
GO


IF OBJECT_ID(N'dbo.sp_FAC_CalculQteTotalItem', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_FAC_CalculQteTotalItem ;
GO

CREATE PROCEDURE [dbo].sp_FAC_CalculQteTotalItem (@SOU_ID VARCHAR(20), @ITEM_ID VARCHAR(20), @TYPEITEM VARCHAR(1), @BLO_ID_REL VARCHAR(3), @QTE FLOAT, @QTEUM VARCHAR(2) , @UID VARCHAR(14))
AS BEGIN
  DECLARE @COUUM_FACPRO   VARCHAR(2)
  DECLARE @QPP_FACPRO     INT
  DECLARE @MULT_BLOC      INT
  DECLARE @QTE_TOTAL      FLOAT
  DECLARE @CALCTIMSTP     VARCHAR(14)
       
  SET @QTE_TOTAL = 0;


  SELECT @COUUM_FACPRO = P.COUUM,  @QPP_FACPRO = P.QPP , @CALCTIMSTP = P.CALCTIMSTP
    FROM FACPRO P
   WHERE P.SOU_ID = @SOU_ID
     AND P.PRO_ID = @ITEM_ID

  SET @QTE_TOTAL = @QTE * DBO.fn_UM_GetRatioDeConversion  (@QTEUM, DBO.fn_UM_GetUniteDeBase(@COUUM_FACPRO),  @QPP_FACPRO)
     
  SELECT @MULT_BLOC = B.MULT
    FROM FACBLO B
   WHERE B.BLO_ID = @BLO_ID_REL
     AND B.SOU_ID = @SOU_ID

  IF @MULT_BLOC IS NOT NULL 
  BEGIN
    SET @QTE_TOTAL = @QTE_TOTAL * @MULT_BLOC
  END


  IF @CALCTIMSTP <> @UID 
  BEGIN
    UPDATE FACPRO
      SET   QTEOTH = 0, 
            QTEENS = 0,
            QTELOT = 0
    WHERE   SOU_ID = @SOU_ID
    AND     PRO_ID = @ITEM_ID 
  END

  IF ((@TYPEITEM = 'P') OR (@TYPEITEM = 'N'))
    EXEC dbo.sp_FAC_UpdateQteTotalOth @SOU_ID, @ITEM_ID, @CALCTIMSTP, @UID , @QTE_TOTAL  
  ELSE IF @TYPEITEM = 'A'
    EXEC dbo.sp_FAC_UpdateQteTotalEns @SOU_ID, @ITEM_ID, @CALCTIMSTP, @UID , @QTE_TOTAL  
  ELSE IF @TYPEITEM = 'L'
    EXEC dbo.sp_FAC_UpdateQteTotalLots @SOU_ID, @ITEM_ID, @CALCTIMSTP, @UID , @QTE_TOTAL  

END 
GO

  -- New field - FACPRO.INASSEMBLIE
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACPRO'
    AND [COLUMN_NAME] = 'INASSEMBLIE' )
BEGIN
  ALTER TABLE
    FACPRO
  ADD
    INASSEMBLIE  VARCHAR(2000);--NVARCHAR(MAX)
END
GO

IF OBJECT_ID(N'dbo.sp_FAC_GetAssemblyCompositionConcat', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.sp_FAC_GetAssemblyCompositionConcat ;
GO

 CREATE FUNCTION [dbo].sp_FAC_GetAssemblyCompositionConcat  
( @SOU_ID VARCHAR(20),
  @PRO_ID VARCHAR(20))
RETURNS VARCHAR(2000)
AS 
BEGIN
  DECLARE @s VARCHAR(2000);  
  SELECT @s = COALESCE(@s , N'') + 
              E.[DESC] + CHAR(13) +  CHAR(10) +  '> ' + LTRIM(STR(C.QTE, 10, 2)) + ' ' + C.QTEUM + ' / 1.00 '+ E.COUUM + 
              CHAR(13) + CHAR(10) 
    FROM FACENS E, FACENSCO C , FACREL L
   WHERE E.ENS_ID = C.ENS_ID
     AND E.SOU_ID = C.SOU_ID
     AND L.SOU_ID = E.SOU_ID
     AND L.ITEM_ID = E.ENS_ID
     AND C.SOU_ID = @SOU_ID
     AND C.PRO_ID = @PRO_ID;

  RETURN (@s);
END
GO

IF OBJECT_ID(N'dbo.sp_FAC_CalculProductUsageInAssemblies', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_FAC_CalculProductUsageInAssemblies ;
GO

CREATE PROCEDURE [dbo].sp_FAC_CalculProductUsageInAssemblies (@SOU_ID VARCHAR(20), @LANG INT)
AS BEGIN
  DECLARE  @TITLE  VARCHAR(60);
  DECLARE  @DESCR  VARCHAR(2000);  
  DECLARE  @FACID  VARCHAR(20);
  DECLARE  @PRO_ID VARCHAR(20);



  IF @LANG = 1 
    SET @TITLE = 'Dans les ensembles'
  ELSE
    SET @TITLE = 'In assemblies '

  SET @TITLE =    @TITLE + CHAR(13) + CHAR(10) + REPLICATE('-', LEN(@TITLE))

  DECLARE CUR_1 CURSOR FOR 
   
   SELECT E.SOU_ID, C.PRO_ID , DESCR = @TITLE +  CHAR(13) + CHAR(10) + dbo.sp_FAC_GetAssemblyCompositionConcat(E.SOU_ID, C.PRO_ID)    
   FROM FACENS E, FACENSCO C , FACREL L
      WHERE E.ENS_ID = C.ENS_ID
        AND E.SOU_ID = C.SOU_ID
        AND L.SOU_ID = E.SOU_ID
        AND L.ITEM_ID = E.ENS_ID
        AND C.SOU_ID = @SOU_ID    
  GROUP BY  E.SOU_ID, C.PRO_ID

  OPEN CUR_1
  FETCH NEXT FROM CUR_1
  INTO @FACID, @PRO_ID, @DESCR

  WHILE @@FETCH_STATUS = 0
   BEGIN
     UPDATE FACPRO
        SET INASSEMBLIE = @DESCR
      WHERE PRO_ID = @PRO_ID 
        AND SOU_ID = @FACID 

     FETCH NEXT FROM CUR_1
     INTO @FACID, @PRO_ID, @DESCR
   END
  CLOSE CUR_1;
  DEALLOCATE CUR_1;

END
GO


IF OBJECT_ID(N'dbo.sp_FAC_CalculCodeImpr', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_FAC_CalculCodeImpr ;
GO

CREATE PROCEDURE [dbo].sp_FAC_CalculCodeImpr(@SOU_ID VARCHAR(20), @PRO_ID  VARCHAR(20), @value  VARCHAR(36))
AS BEGIN
   if ( @value is not null ) AND (@value <> '')
   BEGIN
    UPDATE FACPRO
      SET CODEIMPR = dbo.fn_STR_AddAndSortChars(CODEIMPR, @value) 
    WHERE   SOU_ID = @SOU_ID
    AND     PRO_ID = @PRO_ID 
   END
END
GO


-- procedure de calcule des quantités


IF OBJECT_ID(N'dbo.sp_FACPRO_Quantity', N'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_FACPRO_Quantity ;
GO


CREATE PROCEDURE [dbo].sp_FACPRO_Quantity (@SOU_ID VARCHAR(20), @REPLACE_FILTER INT)
AS BEGIN

   DECLARE @UID            VARCHAR(14)
   DECLARE @QTE            FLOAT    
   DECLARE @QTEUM          VARCHAR(2)
    --
   DECLARE @TYPERELEVE_REL CHAR
   DECLARE @TYPEITEM_REL   CHAR
   DECLARE @QTE_REL        FLOAT 
   DECLARE @QTEUM_REL      VARCHAR(2)
   DECLARE @ITEM_ID_REL    VARCHAR(20)
   DECLARE @BLO_ID_REL     VARCHAR(3)
   DECLARE @SECTION_REL    FLOAT 
   DECLARE @CODEIMPR_REL   VARCHAR(36)
    --
   DECLARE @QPP_FACPRO     INT
    --
   DECLARE @COUUM_ENS      VARCHAR(2)
   DECLARE @QTEUM_ENSCO    VARCHAR(2)
   DECLARE @TYPRATIO_ENSCO VARCHAR(1)
   DECLARE @QTE_ENSCO      FLOAT 
   DECLARE @ENS_ID_ENS     VARCHAR(20)
   DECLARE @PRO_ID_ENSCO   VARCHAR(20)
    --
   DECLARE @COUUM_LOT      VARCHAR(2)
   DECLARE @QTE_LOTCO      FLOAT
   DECLARE @QTEUM_LOTCO    VARCHAR(2)
   DECLARE @PRO_ID_LOTCO   VARCHAR(20)
    --
   DECLARE CUR_FACREL CURSOR FOR 
      SELECT S.ITEM_ID , S.TYPERELEVE, S.TYPEITEM, S.QTE, S.QTEUM, S.BLO_ID, S.SECTION, S.CODEIMPR
   FROM FACREL S
   WHERE S.SOU_ID = @SOU_ID
  
   SELECT @UID = DBO.fn_DateTime_GetTimeStampStr()

   ----------------------------------
   ---- Pour les codes d'impression : 0 Pour Ne pas traiter , 1 Pour Ajouter, 2 pour remplacer
   ----------------------------------

   IF @REPLACE_FILTER = 2 
   BEGIN
     UPDATE   FACPRO
        SET CODEIMPR = ''
        WHERE   SOU_ID = @SOU_ID
   END
 
   -----------------------------------

   OPEN CUR_FACREL
   FETCH NEXT FROM CUR_FACREL
   INTO @ITEM_ID_REL, @TYPERELEVE_REL, @TYPEITEM_REL, @QTE_REL, @QTEUM_REL, @BLO_ID_REL, @SECTION_REL, @CODEIMPR_REL


   UPDATE FACTURES 
      SET CALCTIMSTP = @UID
    WHERE SOU_ID = @SOU_ID 


   UPDATE FACPRO 
      SET QTEOTH = 0,  
          QTEENS = 0, 
          QTELOT = 0  
    WHERE SOU_ID = @SOU_ID 


   WHILE @@FETCH_STATUS = 0
   BEGIN
     IF ((@TYPERELEVE_REL = 'P') AND (@TYPEITEM_REL <> 'T'))
     BEGIN
       --------------------------------------
       ---- Produits-------------------------
       --------------------------------------
       IF ((@TYPEITEM_REL = 'P') OR (@TYPEITEM_REL = 'N'))
       BEGIN

         SET @QTE   = @QTE_REL
         SET @QTEUM = @QTEUM_REL

         EXEC dbo.sp_FAC_CalculQteTotalItem @SOU_ID, 
                                            @ITEM_ID_REL, 
                                            @TYPEITEM_REL,
                                            @BLO_ID_REL, 
                                            @QTE, 
                                            @QTEUM, 
                                            @UID

         IF @REPLACE_FILTER > 0
         BEGIN
          EXEC dbo.sp_FAC_CalculCodeImpr @SOU_ID, @ITEM_ID_REL, @CODEIMPR_REL
         END

       END ELSE
       --------------------------------------
       ---- Ensembles------------------------
       --------------------------------------
       IF (@TYPEITEM_REL = 'A')
       BEGIN

         DECLARE CUR_PRODUITSENS CURSOR FOR
            SELECT E.COUUM, C.QTEUM, C.TYPRATIO,
                    CASE 
                      WHEN (C.TYPRATIO = 'L') AND (E.COUUM <> '') AND (DBO.fn_UM_GetNatureUnite(E.COUUM) = 'L') THEN 
                        CASE 
                          WHEN (C.DIV <> '')  THEN (C.QTE / C.DIV) * DBO.fn_UM_GetRatioDeConversion  (E.COUUM, C.DIVUM,  0)   
                          ELSE 0
                        END
                      ELSE C.QTE          
                    END AS QTE_ENSCO , E.ENS_ID, C.PRO_ID

            FROM FACENS E, FACENSCO C
            WHERE E.SOU_ID = C.SOU_ID
            AND   E.ENS_ID = C.ENS_ID
            AND   E.SOU_ID = @SOU_ID
            AND   E.ENS_ID = @ITEM_ID_REL               
        ----------------------------------


         OPEN CUR_PRODUITSENS

         FETCH NEXT FROM CUR_PRODUITSENS
         INTO @COUUM_ENS, @QTEUM_ENSCO, @TYPRATIO_ENSCO, @QTE_ENSCO, @ENS_ID_ENS, @PRO_ID_ENSCO

         WHILE @@FETCH_STATUS = 0
         BEGIN
           SET @QTE = 0;

           IF @TYPRATIO_ENSCO = 'L'
             SET @QTE = (@QTE_ENSCO * @QTE_REL * DBO.fn_UM_GetRatioDeConversion  (@QTEUM_REL, @COUUM_ENS,  0))
           ELSE
             SET @QTE = (@QTE_ENSCO * @SECTION_REL)

           SET @QTEUM = @QTEUM_ENSCO

           EXEC dbo.sp_FAC_CalculQteTotalItem @SOU_ID, 
                                              @PRO_ID_ENSCO, 
                                              @TYPEITEM_REL,
                                              @BLO_ID_REL, 
                                              @QTE, 
                                              @QTEUM, 
                                              @UID

           IF @REPLACE_FILTER > 0
           BEGIN
             EXEC dbo.sp_FAC_CalculCodeImpr @SOU_ID, @PRO_ID_ENSCO, @CODEIMPR_REL
           END

           FETCH NEXT FROM CUR_PRODUITSENS
           INTO @COUUM_ENS, @QTEUM_ENSCO, @TYPRATIO_ENSCO, @QTE_ENSCO, @ENS_ID_ENS, @PRO_ID_ENSCO
         END

         CLOSE CUR_PRODUITSENS;
         DEALLOCATE CUR_PRODUITSENS;
       END ELSE
       --------------------------------------
       ---- Lots-----------------------------
       --------------------------------------
       IF (@TYPEITEM_REL = 'L')
       BEGIN

       ----------------------------------

         DECLARE CUR_PRODUITSLOTS CURSOR FOR
            SELECT L.COUUM, C.QTE, C.QTEUM, C.PRO_ID
            FROM FACLOTS L, FACLOTSCO C
            WHERE L.LOTS_ID = C.LOTS_ID
            AND   L.SOU_ID = @SOU_ID

         OPEN CUR_PRODUITSLOTS

         FETCH NEXT FROM CUR_PRODUITSLOTS
         INTO @COUUM_LOT, @QTE_LOTCO, @QTEUM_LOTCO, @PRO_ID_LOTCO

         WHILE @@FETCH_STATUS = 0
         BEGIN

           SELECT @QPP_FACPRO = P.QPP
            FROM FACPRO P
           WHERE P.SOU_ID = @SOU_ID
             AND P.PRO_ID = @ITEM_ID_REL

           SET @QTE = (@QTE_LOTCO * @QTE_REL * DBO.fn_UM_GetRatioDeConversion  (@QTEUM_REL, @COUUM_LOT,  @QPP_FACPRO))

           SET @QTEUM = @QTEUM_LOTCO

           EXEC dbo.sp_FAC_CalculQteTotalItem @SOU_ID, 
                                              @PRO_ID_LOTCO, 
                                              @TYPEITEM_REL,
                                              @BLO_ID_REL, 
                                              @QTE, 
                                              @QTEUM, 
                                              @UID

           IF @REPLACE_FILTER > 0
           BEGIN
             EXEC dbo.sp_FAC_CalculCodeImpr @SOU_ID, @PRO_ID_LOTCO, @CODEIMPR_REL
           END

           FETCH NEXT FROM CUR_PRODUITSLOTS
           INTO @COUUM_LOT, @QTE_LOTCO, @QTEUM_LOTCO, @PRO_ID_LOTCO 

         END

         CLOSE CUR_PRODUITSLOTS;
         DEALLOCATE CUR_PRODUITSLOTS;
       END
       --------------------------------------
     END
     FETCH NEXT FROM CUR_FACREL
     INTO @ITEM_ID_REL, @TYPERELEVE_REL, @TYPEITEM_REL, @QTE_REL, @QTEUM_REL, @BLO_ID_REL, @SECTION_REL, @CODEIMPR_REL

   END
   CLOSE CUR_FACREL;
   DEALLOCATE CUR_FACREL;

END
GO

--------  V22_UpdateDatabase pour Factures



  -- New field - FACTURES.USER_ID
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACTURES'
    AND [COLUMN_NAME] = 'USER_ID' )
BEGIN
  ALTER TABLE
    FACTURES
  ADD
    USER_ID  VARCHAR(20);
END
GO

  -- New field - FACTURES.BRANCH_ID
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACTURES'
    AND [COLUMN_NAME] = 'BRANCH_ID' )
BEGIN
  ALTER TABLE
    FACTURES
  ADD
    BRANCH_ID  VARCHAR(20);
END
GO

  -- New field - FACTURES.OWC
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACTURES'
    AND [COLUMN_NAME] = 'OWC' )
BEGIN
  ALTER TABLE
    FACTURES
  ADD
    OWC  VARCHAR(2);
END
GO


  -- New field - BDEE.CUSTDESC
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'BDEE'
    AND [COLUMN_NAME] = 'CUSTDESC' )
BEGIN
  ALTER TABLE
    BDEE
  ADD
    CUSTDESC  VARCHAR(30);
END
GO


IF OBJECT_ID(N'dbo.up_BDEE_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_BDEE_Update ;
GO

CREATE PROCEDURE [dbo].[up_BDEE_Update] (
  @UniqueId bigint,
  @LVERSION	  int,
  @CODEVER	  varchar(20),
  @DATA       varchar(30),
  @NODIST	    varchar(12),
  @NOEEWIN	  varchar(6),
  @NOGEM	    varchar(6),
  @ISINT      bit,
  @DIVISIONPX varchar(2),
  @DIVISION	  varchar(3),
  @DESCR	    varchar(40),
  @URLFR	    varchar(100),
  @URLEN	    varchar(100),
  @ORDERURLFR varchar(200),
  @ORDERURLEN varchar(200),
  @PRICEURL   varchar(200),
  @AUTHURL    varchar(200),
  @AUTHGLOKEY varchar(64),
  @AUTHCLIKEY varchar(64),
  @URLMODE    char(1),
  @ISDEMO	    bit,
  @DEMOEND	  datetime,
  @SUPPORTEND	datetime,
  @MAXUSERS	  int,
  @ISSQL	    bit,
  @ISACOMBA	  bit,
  @ISAVANTAGE	bit,
  @ISSAGE50	  bit,
  @ISQUICKBK	bit,
  @MODULES    varchar(32),
  @KVERSION	  int,
  @LICENCEKEY	varchar(128),
  @CUSTDESC   varchar(30)  
  
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO BDEE (
    LVERSION, 
    CODEVER, 
    DATA, 
    NODIST, 
    NOEEWIN, 
    NOGEM, 
    ISINT, 
    DIVISIONPX, 
    DIVISION, 
    DESCR, 
    URLFR, 
    URLEN, 
    ORDERURLFR, 
    ORDERURLEN, 
    PRICEURL, 
    AUTHURL, 
    AUTHGLOKEY,
    AUTHCLIKEY,
    URLMODE,
    ISDEMO, 
    DEMOEND, 
    SUPPORTEND, 
    MAXUSERS, 
    ISSQL, 
    ISACOMBA, 
    ISAVANTAGE, 
    ISSAGE50, 
    ISQUICKBK,
    MODULES, 
    KVERSION, 
    LICENCEKEY, 
	CUSTDESC,
    SysDate
    )
  VALUES (
    @LVERSION, 
    @CODEVER, 
    @DATA, 
    @NODIST, 
    @NOEEWIN, 
    @NOGEM, 
    @ISINT, 
    @DIVISIONPX, 
    @DIVISION, 
    @DESCR, 
    @URLFR, 
    @URLEN, 
    @ORDERURLFR, 
    @ORDERURLEN, 
    @PRICEURL, 
    @AUTHURL,
    @AUTHGLOKEY,
    @AUTHCLIKEY, 
    @URLMODE,
    @ISDEMO, 
    @DEMOEND, 
    @SUPPORTEND, 
    @MAXUSERS, 
    @ISSQL, 
    @ISACOMBA, 
    @ISAVANTAGE, 
    @ISSAGE50, 
    @ISQUICKBK, 
    @MODULES,
    @KVERSION, 
    @LICENCEKEY, 
	@CUSTDESC,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    BDEE
  SET
    LVERSION    = @LVERSION,
    CODEVER     = @CODEVER,
    DATA        = @DATA,
    NODIST      = @NODIST,
    NOEEWIN     = @NOEEWIN,
    NOGEM       = @NOGEM,
    ISINT       = @ISINT,
    DIVISIONPX  = @DIVISIONPX,
    DIVISION    = @DIVISION,
    DESCR       = @DESCR,
    URLFR       = @URLFR,
    URLEN       = @URLEN,
    ORDERURLFR  = @ORDERURLFR,
    ORDERURLEN  = @ORDERURLEN,
    PRICEURL    = @PRICEURL,
    AUTHURL     = @AUTHURL,
    AUTHGLOKEY  = @AUTHGLOKEY,
    AUTHCLIKEY  = @AUTHCLIKEY,
    URLMODE     = @URLMODE,
    ISDEMO      = @ISDEMO,
    DEMOEND     = @DEMOEND,
    SUPPORTEND  = @SUPPORTEND,
    MAXUSERS    = @MAXUSERS,
    ISSQL       = @ISSQL,
    ISACOMBA    = @ISACOMBA,
    ISAVANTAGE  = @ISAVANTAGE,
    ISSAGE50    = @ISSAGE50,
    ISQUICKBK   = @ISQUICKBK,
    MODULES     = @MODULES,
    KVERSION    = @KVERSION,
    LICENCEKEY  = @LICENCEKEY,
	CUSTDESC    = @CUSTDESC,
    SysDate     = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO



--------  V23_UpdateDatabase pour Factures




  -- New field - FACTURES.USER_ID_UP
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACTURES'
    AND [COLUMN_NAME] = 'USER_ID_UP' )
BEGIN
  ALTER TABLE
    FACTURES
  ADD
    USER_ID_UP  VARCHAR(20);
END
GO



  -- New field - FACTURES.USER_UPDATE
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACTURES'
    AND [COLUMN_NAME] = 'USER_UPDATE' )
BEGIN
  ALTER TABLE
    FACTURES
  ADD
    USER_UPDATE DATETIME NULL;
END
GO


----

IF OBJECT_ID(N'dbo.sp_Update_FacturesUserSession', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_Update_FacturesUserSession ;
GO

CREATE PROCEDURE [dbo].sp_Update_FacturesUserSession(@SOU_ID VARCHAR(20))
AS
  DECLARE @OLDUSERID VARCHAR(20)
  DECLARE @NEWUSERID VARCHAR(20)
  DECLARE @LASTUPDATE DATETIME
    
  SELECT @NEWUSERID = dbo.GetCurrentUserSession()
  SELECT @OLDUSERID = USER_ID_UP, @LASTUPDATE = USER_UPDATE FROM FACTURES WHERE SOU_ID = @SOU_ID

  IF (ISNULL(@NEWUSERID,'') = '') OR (ISNULL(@OLDUSERID,'') = '') OR (ISNULL(@LASTUPDATE,'') = '') OR (@NEWUSERID <> @OLDUSERID) OR
     ((@NEWUSERID = @OLDUSERID) AND (DATEDIFF(second, @LASTUPDATE, GETDATE()) > 60))
  BEGIN
    UPDATE FACTURES
       SET USER_ID_UP = @NEWUSERID,
           USER_UPDATE = GETDATE()
     WHERE SOU_ID = @SOU_ID 
  END;
GO

-------------------------------------------

IF OBJECT_ID(N'dbo.up_FACAMD_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_FACAMD_Update ;
GO


CREATE PROCEDURE [dbo].[up_FACAMD_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DIV_ID varchar(3),
  @FACTMD float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACAMD (
    [SOU_ID],
    [BLO_ID],
    [DIV_ID],
    [FACTMD],
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DIV_ID,
    @FACTMD,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACAMD
  SET
    [SOU_ID] = @SOU_ID,
    [BLO_ID] = @BLO_ID,
    [DIV_ID] = @DIV_ID,
    [FACTMD] = @FACTMD,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating FACTURES
  exec dbo.sp_Update_FacturesUserSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_FACBLO_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_FACBLO_Update ;
GO

CREATE PROCEDURE [dbo].[up_FACBLO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DESC varchar(40),
  @ACC_NO varchar(20),
  @ACH_NO varchar(20),
  @MULT int
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACBLO (
    [SOU_ID],
    [BLO_ID],
    [DESC],
    [ACC_NO],
    [ACH_NO],
    [MULT],
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DESC,
    @ACC_NO,
    @ACH_NO,
    @MULT,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACBLO
  SET
    [SOU_ID] = @SOU_ID,
    [BLO_ID] = @BLO_ID,
    [DESC] = @DESC,
    [ACC_NO] = @ACC_NO,
    [ACH_NO] = @ACH_NO,
    [MULT] = @MULT,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating FACTURES
  exec dbo.sp_Update_FacturesUserSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_FACDIV_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_FACDIV_Update ;
GO

CREATE PROCEDURE [dbo].[up_FACDIV_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @DIV_ID varchar(3),
  @ACT_NO VARCHAR(20),  
  @DESC varchar(40)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACDIV (
    [SOU_ID],
    [DIV_ID],
    [ACT_NO],	
    [DESC],
    SysDate)
  VALUES (
    @SOU_ID,
    @DIV_ID,
    @ACT_NO,	
    @DESC,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACDIV
  SET
    [SOU_ID] = @SOU_ID,
    [DIV_ID] = @DIV_ID,
    [ACT_NO] = @ACT_NO,	
    [DESC]   = @DESC,
    SysDate  = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating FACTURES
  exec dbo.sp_Update_FacturesUserSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_FACENS_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_FACENS_Update ;
GO


CREATE PROCEDURE [dbo].[up_FACENS_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @ENS_ID varchar(20),
  @ENS_ORG_ID varchar(20),  -- 2014-08-12 EMadore V6 : New
  @DESC varchar(60),        -- 2012-01-19 EMadore V3 : Passage de 40 à 60 chars
  @QTETOT float,
  @QTETOTSECT float,
  @CALCTIMSTP varchar(14),
  @COUUM varchar(2),
  @TEMPUNI float,
  @TEMPSEC float,
  @TEMPUM varchar(2),
  @DATECREE datetime,
  @OLDESTPROD datetime,
  @CLEPERS varchar(40),
  @PROFIT float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACENS (
    [SOU_ID],
    [ENS_ID],
    [ENS_ORG_ID],
    [DESC],
    [QTETOT],
    [QTETOTSECT],
    [CALCTIMSTP],
    [COUUM],
    [TEMPUNI],
    [TEMPSEC],
    [TEMPUM],
    [DATECREE],
    [OLDESTPROD],
    [CLEPERS],
    [PROFIT],
    SysDate)
  VALUES (
    @SOU_ID,
    @ENS_ID,
    @ENS_ORG_ID,
    @DESC,
    @QTETOT,
    @QTETOTSECT,
    @CALCTIMSTP,
    @COUUM,
    @TEMPUNI,
    @TEMPSEC,
    @TEMPUM,
    @DATECREE,
    @OLDESTPROD,
    @CLEPERS,
    @PROFIT,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACENS
  SET
    [SOU_ID] = @SOU_ID,
    [ENS_ID] = @ENS_ID,
    [ENS_ORG_ID] = @ENS_ORG_ID,
    [DESC] = @DESC,
    [QTETOT] = @QTETOT,
    [QTETOTSECT] = @QTETOTSECT,
    [CALCTIMSTP] = @CALCTIMSTP,
    [COUUM] = @COUUM,
    [TEMPUNI] = @TEMPUNI,
    [TEMPSEC] = @TEMPSEC,
    [TEMPUM] = @TEMPUM,
    [DATECREE] = @DATECREE,
    [OLDESTPROD] = @OLDESTPROD,
    [CLEPERS] = @CLEPERS,
    [PROFIT] = @PROFIT,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating FACTURES
  exec dbo.sp_Update_FacturesUserSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_FACENSCO_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_FACENSCO_Update ;
GO

CREATE PROCEDURE [dbo].[up_FACENSCO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @ENS_ID varchar(20),
  @PRO_ID varchar(20),
  @ORDRE varchar(6),
  @QTE float,
  @QTEUM varchar(2),
  @TYPRATIO varchar(1),
  @DIV float,
  @DIVUM varchar(2)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACENSCO (
    [SOU_ID],
    [ENS_ID],
    [PRO_ID],
    [ORDRE],
    [QTE],
    [QTEUM],
    [TYPRATIO],
    [DIV],
    [DIVUM],
    SysDate)
  VALUES (
    @SOU_ID,
    @ENS_ID,
    @PRO_ID,
    @ORDRE,
    @QTE,
    @QTEUM,
    @TYPRATIO,
    @DIV,
    @DIVUM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACENSCO
  SET
    [SOU_ID] = @SOU_ID,
    [ENS_ID] = @ENS_ID,
    [PRO_ID] = @PRO_ID,
    [ORDRE] = @ORDRE,
    [QTE] = @QTE,
    [QTEUM] = @QTEUM,
    [TYPRATIO] = @TYPRATIO,
    [DIV] = @DIV,
    [DIVUM] = @DIVUM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating FACTURES
  exec dbo.sp_Update_FacturesUserSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_FACLOTS_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_FACLOTS_Update ;
GO

CREATE PROCEDURE [dbo].[up_FACLOTS_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @LOTS_ID varchar(20),
  @DESC varchar(60),         -- 2012-01-19 EMadore V3 : Passage de 40 à 60 chars
  @QTETOT float,
  @QTETOTSECT float,
  @CALCTIMSTP varchar(14),
  @COUUM varchar(2),
  @TEMPUNI float,
  @TEMPUM varchar(2),
  @DATECREE datetime,
  @OLDESTPROD datetime,
  @CLEPERS varchar(40),
  @PROFIT float,
  @COUTANTSEL int,
  @COUTANT1 float,
  @COUTANT2 float,
  @COUTANT3 float,
  @COUTANT4 float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACLOTS (
    [SOU_ID],
    [LOTS_ID],
    [DESC],
    [QTETOT],
    [QTETOTSECT],
    [CALCTIMSTP],
    [COUUM],
    [TEMPUNI],
    [TEMPUM],
    [DATECREE],
    [OLDESTPROD],
    [CLEPERS],
    [PROFIT],
    [COUTANTSEL],
    [COUTANT1],
    [COUTANT2],
    [COUTANT3],
    [COUTANT4],
    SysDate)
  VALUES (
    @SOU_ID,
    @LOTS_ID,
    @DESC,
    @QTETOT,
    @QTETOTSECT,
    @CALCTIMSTP,
    @COUUM,
    @TEMPUNI,
    @TEMPUM,
    @DATECREE,
    @OLDESTPROD,
    @CLEPERS,
    @PROFIT,
    @COUTANTSEL,
    @COUTANT1,
    @COUTANT2,
    @COUTANT3,
    @COUTANT4,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACLOTS
  SET
    [SOU_ID] = @SOU_ID,
    [LOTS_ID] = @LOTS_ID,
    [DESC] = @DESC,
    [QTETOT] = @QTETOT,
    [QTETOTSECT] = @QTETOTSECT,
    [CALCTIMSTP] = @CALCTIMSTP,
    [COUUM] = @COUUM,
    [TEMPUNI] = @TEMPUNI,
    [TEMPUM] = @TEMPUM,
    [DATECREE] = @DATECREE,
    [OLDESTPROD] = @OLDESTPROD,
    [CLEPERS] = @CLEPERS,
    [PROFIT] = @PROFIT,
    [COUTANTSEL] = @COUTANTSEL,
    [COUTANT1] = @COUTANT1,
    [COUTANT2] = @COUTANT2,
    [COUTANT3] = @COUTANT3,
    [COUTANT4] = @COUTANT4,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating FACTURES
  exec dbo.sp_Update_FacturesUserSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_FACLOTSCO_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_FACLOTSCO_Update ;
GO


CREATE PROCEDURE [dbo].[up_FACLOTSCO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @LOTS_ID varchar(20),
  @PRO_ID varchar(20),
  @ORDRE varchar(6),
  @QTE float,
  @QTEUM varchar(2)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACLOTSCO (
    [SOU_ID],
    [LOTS_ID],
    [PRO_ID],
    [ORDRE],
    [QTE],
    [QTEUM],
    SysDate)
  VALUES (
    @SOU_ID,
    @LOTS_ID,
    @PRO_ID,
    @ORDRE,
    @QTE,
    @QTEUM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACLOTSCO
  SET
    [SOU_ID] = @SOU_ID,
    [LOTS_ID] = @LOTS_ID,
    [PRO_ID] = @PRO_ID,
    [ORDRE] = @ORDRE,
    [QTE] = @QTE,
    [QTEUM] = @QTEUM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating FACTURES
  exec dbo.sp_Update_FacturesUserSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_FACPRO_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_FACPRO_Update ;
GO


CREATE PROCEDURE [dbo].[up_FACPRO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @PRO_ID varchar(20),
  @CLEMANU varchar(30),
  @CLEDIST varchar(20),
  @CLEPERS varchar(20),
  @DESC varchar(60),
  @QTEENS float,
  @QTELOT float,
  @QTEOTH float,
  @CALCTIMSTP varchar(14),
  @COUBRUTUNI float,
  @COUUM varchar(2),
  @QPP float,
  @COUESC float,
  @PROMCOUNET float,
  @TEMPUNI float,
  @TEMPUM varchar(2),
  @MULCOM float,
  @CODEIMPR varchar(20),
  @CODEFOUR varchar(2),
  @CODECAT varchar(3),
  @DATECOUT datetime,
  @DATECOUNET datetime,   -- V7 EE-222 - Prix net Rexel
  @RESCOUNET int,         -- V7 EE-222 - Prix net Rexel
  @QTECOM float,
  @QTEACOM float,
  @ISVIRT bit,
  @VIRTCOUNT int
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACPRO (
    [SOU_ID],
    [PRO_ID],
    [CLEMANU],
    [CLEDIST],
    [CLEPERS],
    [DESC],
    [QTEENS],
    [QTELOT],
    [QTEOTH],
    [CALCTIMSTP],
    [COUBRUTUNI],
    [COUUM],
    [QPP],
    [COUESC],
    [PROMCOUNET],
    [TEMPUNI],
    [TEMPUM],
    [MULCOM],
    [CODEIMPR],
    [CODEFOUR],
    [CODECAT],
    [DATECOUT],
    [DATECOUNET],   -- V7 EE-222 - Prix net Rexel
    [RESCOUNET],    -- V7 EE-222 - Prix net Rexel
    [QTECOM],
    [QTEACOM],
    [ISVIRT],
    [VIRTCOUNT],
    SysDate)
  VALUES (
    @SOU_ID,
    @PRO_ID,
    @CLEMANU,
    @CLEDIST,
    @CLEPERS,
    @DESC,
    @QTEENS,
    @QTELOT,
    @QTEOTH,
    @CALCTIMSTP,
    @COUBRUTUNI,
    @COUUM,
    @QPP,
    @COUESC,
    @PROMCOUNET,
    @TEMPUNI,
    @TEMPUM,
    @MULCOM,
    @CODEIMPR,
    @CODEFOUR,
    @CODECAT,
    @DATECOUT,
    @DATECOUNET,  -- V7 EE-222 - Prix net Rexel
    @RESCOUNET,   -- V7 EE-222 - Prix net Rexel
    @QTECOM,
    @QTEACOM,
    @ISVIRT,
    @VIRTCOUNT,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACPRO
  SET
    [SOU_ID] = @SOU_ID,
    [PRO_ID] = @PRO_ID,
    [CLEMANU] = @CLEMANU,
    [CLEDIST] = @CLEDIST,
    [CLEPERS] = @CLEPERS,
    [DESC] = @DESC,
    [QTEENS] = @QTEENS,
    [QTELOT] = @QTELOT,
    [QTEOTH] = @QTEOTH,
    [CALCTIMSTP] = @CALCTIMSTP,
    [COUBRUTUNI] = @COUBRUTUNI,
    [COUUM] = @COUUM,
    [QPP] = @QPP,
    [COUESC] = @COUESC,
    [PROMCOUNET] = @PROMCOUNET,
    [TEMPUNI] = @TEMPUNI,
    [TEMPUM] = @TEMPUM,
    [MULCOM] = @MULCOM,
    [CODEIMPR] = @CODEIMPR,
    [CODEFOUR] = @CODEFOUR,
    [CODECAT] = @CODECAT,
    [DATECOUT] = @DATECOUT,
    [DATECOUNET] = @DATECOUNET,   -- V7 EE-222 - Prix net Rexel
    [RESCOUNET] = @RESCOUNET,     -- V7 EE-222 - Prix net Rexel
    [QTECOM] = @QTECOM,
    [QTEACOM] = @QTEACOM,
    [ISVIRT] = @ISVIRT,
    [VIRTCOUNT] = @VIRTCOUNT,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating FACTURES
  exec dbo.sp_Update_FacturesUserSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_FACREL_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_FACREL_Update ;
GO

CREATE PROCEDURE [dbo].[up_FACREL_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DIV_ID varchar(3),
  @TYPERELEVE varchar(1),
  @EXT_ID varchar(20),
  @ORDRE varchar(6),
  @TYPEITEM varchar(1),
  @ITEM_ID varchar(20),
  @DESCR varchar(60),
  @QTE float,
  @SECTION float,
  @QTEUM varchar(2),
  @PROFIT float,
  @TYPETAXE varchar(1),
  @CODEIMPR varchar(2),
  @COUTANBRUT float,
  @TEMPSUNIT float,
  @TEMPSSEC float,
  @TEMPSUM varchar(2),
  @PROFITPLUS float,
  @PROFITMOIN float,
  @ACC_NO varchar(20),
  @ACH_NO varchar(20),
  @ACT_NO varchar(20)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACREL (
    [SOU_ID],
    [BLO_ID],
    [DIV_ID],
    [TYPERELEVE],
    [EXT_ID],
    [ORDRE],
    [TYPEITEM],
    [ITEM_ID],
    [DESCR],
    [QTE],
    [SECTION],
    [QTEUM],
    [PROFIT],
    [TYPETAXE],
    [CODEIMPR],
    [COUTANBRUT],
    [TEMPSUNIT],
    [TEMPSSEC],
    [TEMPSUM],
    [PROFITPLUS],
    [PROFITMOIN],
    [ACC_NO],
    [ACH_NO],
    [ACT_NO],
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DIV_ID,
    @TYPERELEVE,
    @EXT_ID,
    @ORDRE,
    @TYPEITEM,
    @ITEM_ID,
    @DESCR,
    @QTE,
    @SECTION,
    @QTEUM,
    @PROFIT,
    @TYPETAXE,
    @CODEIMPR,
    @COUTANBRUT,
    @TEMPSUNIT,
    @TEMPSSEC,
    @TEMPSUM,
    @PROFITPLUS,
    @PROFITMOIN,
    @ACC_NO,
    @ACH_NO,
    @ACT_NO,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACREL
  SET
    [SOU_ID] = @SOU_ID,
    [BLO_ID] = @BLO_ID,
    [DIV_ID] = @DIV_ID,
    [TYPERELEVE] = @TYPERELEVE,
    [EXT_ID] = @EXT_ID,
    [ORDRE] = @ORDRE,
    [TYPEITEM] = @TYPEITEM,
    [ITEM_ID] = @ITEM_ID,
    [DESCR] = @DESCR,
    [QTE] = @QTE,
    [SECTION] = @SECTION,
    [QTEUM] = @QTEUM,
    [PROFIT] = @PROFIT,
    [TYPETAXE] = @TYPETAXE,
    [CODEIMPR] = @CODEIMPR,
    [COUTANBRUT] = @COUTANBRUT,
    [TEMPSUNIT] = @TEMPSUNIT,
    [TEMPSSEC] = @TEMPSSEC,
    [TEMPSUM] = @TEMPSUM,
    [PROFITPLUS] = @PROFITPLUS,
    [PROFITMOIN] = @PROFITMOIN,
    [ACC_NO] = @ACC_NO,
    [ACH_NO] = @ACH_NO,
    [ACT_NO] = @ACT_NO,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating FACTURES
  exec dbo.sp_Update_FacturesUserSession @SOU_ID

  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_FACWEBLOG_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_FACWEBLOG_Update ;
GO

CREATE PROCEDURE [dbo].[up_FACWEBLOG_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @WEB_ID varchar(15),
  @TRF_DATE varchar(25),
  @RESULT varchar(10),
  @MESSAGE varchar(60)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACWEBLOG (
    [SOU_ID],
    [WEB_ID],
    [TRF_DATE],
    [RESULT],
    [MESSAGE],
    SysDate)
  VALUES (
    @SOU_ID,
    @WEB_ID,
    @TRF_DATE,
    @RESULT,
    @MESSAGE,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACWEBLOG
  SET
    [SOU_ID] = @SOU_ID,
    [WEB_ID] = @WEB_ID,
    [TRF_DATE] = @TRF_DATE,
    [RESULT] = @RESULT,
    [MESSAGE] = @MESSAGE,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating FACTURES
  exec dbo.sp_Update_FacturesUserSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_FACTURES_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_FACTURES_Update ;
GO


CREATE PROCEDURE [dbo].[up_FACTURES_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @ORIGIN char(1),          -- 2014-07-31 EMadore V6 - Ajout  
  @ORIGINREF varchar(200),  -- 2014-07-31 EMadore V6 - Ajout  
  @EXTAPP char(1),          -- 2014-07-31 EMadore V6 - Ajout  
  @EXTFILE varchar(200),    -- 2014-07-31 EMadore V6 - Ajout  
  @NODOC varchar(12),
  @DESCDOC varchar(200),
  @DATECREE datetime,
  @DATEDOC datetime,
  @DATEEXP datetime,
  @REF_ID varchar(20),
  @STATUT int,
  @NOCOMMANDE varchar(20),
  @NOTEINTERN text,
  @CLIENTNO varchar(20),
  @CLIENTCIE varchar(50),
  @CLIENTCNT varchar(50),
  @CLIENTRUE1 varchar(50),
  @CLIENTRUE2 varchar(50),
  @CLIENTVILL varchar(40),
  @CLIENTCP varchar(7),
  @CLIENTPROV varchar(40),
  @CLIENTPAYS varchar(40),
  @CLIENTBP varchar(30),
  @CLIENTTEL1 varchar(20),
  @CLIENTTEL2 varchar(20),
  @CLIENTTEL3 varchar(20),
  @CLIENTFAX varchar(20),
  @CLIENTEMAI varchar(80),  -- 2012-01-19 EMadore V3 : Ajout
  @MEMESITE bit,
  @SITENO varchar(20),
  @SITECIE varchar(50),
  @SITECNT varchar(50),
  @SITERUE1 varchar(50),
  @SITERUE2 varchar(50),
  @SITEVILLE varchar(40),
  @SITECP varchar(7),
  @SITEPROV varchar(40),
  @SITEPAYS varchar(40),
  @SITEBP varchar(30),
  @SITETEL1 varchar(20),
  @SITETEL2 varchar(20),
  @SITETEL3 varchar(20),
  @SITEFAX varchar(20),
  @SITEEMAIL varchar(80),  -- 2012-01-19 EMadore V3 : Ajout
  @MATTOTALMD float,
  @NOTEPRINC text,
  @MATCOUTREL float,
  @MATCOUTLOT float,
  @MATVENDCAL float,
  @MATPORTTVP float,
  @SERCOUTCAL float,
  @SERVENDCAL float,
  @SERHRESCAL float,
  @SERPORTTVP float,
  @AUTCOUTCAL float,
  @AUTVENDCAL float,
  @AUTPORTTVP float,
  @OPTIONSSOM varchar(40),
  @MATCOUTMO float,
  @SERCOUTMO float,
  @AUTCOUTMO float,
  @MATADMPC float,
  @SERADMPC float,
  @AUTADMPC float,
  @MATADMMO float,
  @SERADMMO float,
  @AUTADMMO float,
  @MATPROFPC float,
  @SERPROFPC float,
  @AUTPROFPC float,
  @MATPROFMO float,
  @SERPROFMO float,
  @AUTPROFMO float,
  @GLOBAJUPC float,
  @GLOBAJUMO float,
  @GLOBEXPLIC varchar(40),
  @GLOBAJU2PC float,
  @GLOBAJU2MO float,
  @GLOBEXPL2 varchar(40),
  @OPTIONSIMP varchar(50),
  @OPIMPADJMA varchar(40),
  @OPIMPADJLA varchar(40),
  @OPIMPADJOT varchar(40),
  @NOTEBAS text,
  @MATTAXAB1 float,
  @MATTAXAB2 float,
  @MATTAXAB3 float,
  @MATTAXAB4 float,
  @MATTAXAB5 float,
  @MATTAXAB6 float,
  @SERTAXAB1 float,
  @SERTAXAB2 float,
  @SERTAXAB3 float,
  @SERTAXAB4 float,
  @SERTAXAB5 float,
  @SERTAXAB6 float,
  @AUTTAXAB1 float,
  @AUTTAXAB2 float,
  @AUTTAXAB3 float,
  @AUTTAXAB4 float,
  @AUTTAXAB5 float,
  @AUTTAXAB6 float,
  @TAXTYPCAL int,
  @AJUTAXAB1 float,
  @AJUTAXAB2 float,
  @AJUTAXAB3 float,
  @AJUTAXAB4 float,
  @AJUTAXAB5 float,
  @TOTTAXFED float,
  @TOTTAXPRV float,
  @TAX_ID varchar(20),
  @APPLIQUTVF bit,
  @APPLIQUTVP bit,
  @TVPSURCOUT bit,
  @TOTCALCULE bit,
  @CALCTIMSTP varchar(14),
  @UMPLAN varchar(2),
  @TYPEPROF varchar(1),
  @MATPROFDEF float,
  @TYPESRVPRO varchar(1),
  @TAUXMD float,
  @NUMLOTEXP float,
  @SYSTEM bit,
  @USER1 varchar(20),
  @USER2 varchar(20),
  @EST_NAME varchar(50),
  @ACCTRANSNO varchar(12),
  @PRJTRANSNO varchar(15),
  @STATUTLIBF varchar(30), 
  @STATUTLIBE varchar(30),
  @USER_ID varchar(20),
  @BRANCH_ID varchar(20),
  @OWC varchar(2)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACTURES (
    [SOU_ID],
    [ORIGIN],     -- 2014-07-31 EMadore V6 - Ajout
    [ORIGINREF],  -- 2014-07-31 EMadore V6 - Ajout
    [EXTAPP],     -- 2014-07-31 EMadore V6 - Ajout
    [EXTFILE],    -- 2014-07-31 EMadore V6 - Ajout
    [NODOC],
    [DESCDOC],
    [DATECREE],
    [DATEDOC],
    [DATEEXP],
    [REF_ID],
    [STATUT],
    [NOCOMMANDE],
    [NOTEINTERN],
    [CLIENTNO],
    [CLIENTCIE],
    [CLIENTCNT],
    [CLIENTRUE1],
    [CLIENTRUE2],
    [CLIENTVILL],
    [CLIENTCP],
    [CLIENTPROV],
    [CLIENTPAYS],
    [CLIENTBP],
    [CLIENTTEL1],
    [CLIENTTEL2],
    [CLIENTTEL3],
    [CLIENTFAX],
    [CLIENTEMAI],  -- 2012-01-19 EMadore V3 : Ajout
    [MEMESITE],
    [SITENO],
    [SITECIE],
    [SITECNT],
    [SITERUE1],
    [SITERUE2],
    [SITEVILLE],
    [SITECP],
    [SITEPROV],
    [SITEPAYS],
    [SITEBP],
    [SITETEL1],
    [SITETEL2],
    [SITETEL3],
    [SITEFAX],
    [SITEEMAIL],  -- 2012-01-19 EMadore V3 : Ajout 
    [MATTOTALMD],
    [NOTEPRINC],
    [MATCOUTREL],
    [MATCOUTLOT],
    [MATVENDCAL],
    [MATPORTTVP],
    [SERCOUTCAL],
    [SERVENDCAL],
    [SERHRESCAL],
    [SERPORTTVP],
    [AUTCOUTCAL],
    [AUTVENDCAL],
    [AUTPORTTVP],
    [OPTIONSSOM],
    [MATCOUTMO],
    [SERCOUTMO],
    [AUTCOUTMO],
    [MATADMPC],
    [SERADMPC],
    [AUTADMPC],
    [MATADMMO],
    [SERADMMO],
    [AUTADMMO],
    [MATPROFPC],
    [SERPROFPC],
    [AUTPROFPC],
    [MATPROFMO],
    [SERPROFMO],
    [AUTPROFMO],
    [GLOBAJUPC],
    [GLOBAJUMO],
    [GLOBEXPLIC],
    [GLOBAJU2PC],
    [GLOBAJU2MO],
    [GLOBEXPL2],
    [OPTIONSIMP],
    [OPIMPADJMA],
    [OPIMPADJLA],
    [OPIMPADJOT],
    [NOTEBAS],
    [MATTAXAB1],
    [MATTAXAB2],
    [MATTAXAB3],
    [MATTAXAB4],
    [MATTAXAB5],
    [MATTAXAB6],
    [SERTAXAB1],
    [SERTAXAB2],
    [SERTAXAB3],
    [SERTAXAB4],
    [SERTAXAB5],
    [SERTAXAB6],
    [AUTTAXAB1],
    [AUTTAXAB2],
    [AUTTAXAB3],
    [AUTTAXAB4],
    [AUTTAXAB5],
    [AUTTAXAB6],
    [TAXTYPCAL],
    [AJUTAXAB1],
    [AJUTAXAB2],
    [AJUTAXAB3],
    [AJUTAXAB4],
    [AJUTAXAB5],
    [TOTTAXFED],
    [TOTTAXPRV],
    [TAX_ID],
    [APPLIQUTVF],
    [APPLIQUTVP],
    [TVPSURCOUT],
    [TOTCALCULE],
    [CALCTIMSTP],
    [UMPLAN],
    [TYPEPROF],
    [MATPROFDEF],
    [TYPESRVPRO],
    [TAUXMD],
    [NUMLOTEXP],
    [SYSTEM],
    [USER1],
    [USER2],
    [EST_NAME],
    [ACCTRANSNO],
    [PRJTRANSNO],
    [STATUTLIBF], 
    [STATUTLIBE],  	
    [USER_ID],
    [BRANCH_ID], 
    [OWC], 
    SysDate)
  VALUES (
    @SOU_ID,
    @ORIGIN,    -- 2014-07-31 EMadore V6 - Ajout
    @ORIGINREF, -- 2014-07-31 EMadore V6 - Ajout
    @EXTAPP,    -- 2014-07-31 EMadore V6 - Ajout
    @EXTFILE,   -- 2014-07-31 EMadore V6 - Ajout
    @NODOC,
    @DESCDOC,
    @DATECREE,
    @DATEDOC,
    @DATEEXP,
    @REF_ID,
    @STATUT,
    @NOCOMMANDE,
    @NOTEINTERN,
    @CLIENTNO,
    @CLIENTCIE,
    @CLIENTCNT,
    @CLIENTRUE1,
    @CLIENTRUE2,
    @CLIENTVILL,
    @CLIENTCP,
    @CLIENTPROV,
    @CLIENTPAYS,
    @CLIENTBP,
    @CLIENTTEL1,
    @CLIENTTEL2,
    @CLIENTTEL3,
    @CLIENTFAX,
    @CLIENTEMAI,  -- 2012-01-19 EMadore V3 : Ajout
    @MEMESITE,
    @SITENO,
    @SITECIE,
    @SITECNT,
    @SITERUE1,
    @SITERUE2,
    @SITEVILLE,
    @SITECP,
    @SITEPROV,
    @SITEPAYS,
    @SITEBP,
    @SITETEL1,
    @SITETEL2,
    @SITETEL3,
    @SITEFAX,
    @SITEEMAIL,    -- 2012-01-19 V3 : Ajout
    @MATTOTALMD,
    @NOTEPRINC,
    @MATCOUTREL,
    @MATCOUTLOT,
    @MATVENDCAL,
    @MATPORTTVP,
    @SERCOUTCAL,
    @SERVENDCAL,
    @SERHRESCAL,
    @SERPORTTVP,
    @AUTCOUTCAL,
    @AUTVENDCAL,
    @AUTPORTTVP,
    @OPTIONSSOM,
    @MATCOUTMO,
    @SERCOUTMO,
    @AUTCOUTMO,
    @MATADMPC,
    @SERADMPC,
    @AUTADMPC,
    @MATADMMO,
    @SERADMMO,
    @AUTADMMO,
    @MATPROFPC,
    @SERPROFPC,
    @AUTPROFPC,
    @MATPROFMO,
    @SERPROFMO,
    @AUTPROFMO,
    @GLOBAJUPC,
    @GLOBAJUMO,
    @GLOBEXPLIC,
    @GLOBAJU2PC,
    @GLOBAJU2MO,
    @GLOBEXPL2,
    @OPTIONSIMP,
    @OPIMPADJMA,
    @OPIMPADJLA,
    @OPIMPADJOT,
    @NOTEBAS,
    @MATTAXAB1,
    @MATTAXAB2,
    @MATTAXAB3,
    @MATTAXAB4,
    @MATTAXAB5,
    @MATTAXAB6,
    @SERTAXAB1,
    @SERTAXAB2,
    @SERTAXAB3,
    @SERTAXAB4,
    @SERTAXAB5,
    @SERTAXAB6,
    @AUTTAXAB1,
    @AUTTAXAB2,
    @AUTTAXAB3,
    @AUTTAXAB4,
    @AUTTAXAB5,
    @AUTTAXAB6,
    @TAXTYPCAL,
    @AJUTAXAB1,
    @AJUTAXAB2,
    @AJUTAXAB3,
    @AJUTAXAB4,
    @AJUTAXAB5,
    @TOTTAXFED,
    @TOTTAXPRV,
    @TAX_ID,
    @APPLIQUTVF,
    @APPLIQUTVP,
    @TVPSURCOUT,
    @TOTCALCULE,
    @CALCTIMSTP,
    @UMPLAN,
    @TYPEPROF,
    @MATPROFDEF,
    @TYPESRVPRO,
    @TAUXMD,
    @NUMLOTEXP,
    @SYSTEM,
    @USER1,
    @USER2,
    @EST_NAME,
    @ACCTRANSNO,
    @PRJTRANSNO,
    @STATUTLIBF, 
    @STATUTLIBE,  	
    @USER_ID,
    @BRANCH_ID, 
    @OWC,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACTURES
  SET
    [SOU_ID] = @SOU_ID,
    [ORIGIN] = @ORIGIN,       -- 2014-07-31 EMadore V6 - Ajout
    [ORIGINREF] = @ORIGINREF, -- 2014-07-31 EMadore V6 - Ajout
    [EXTAPP] = @EXTAPP,       -- 2014-07-31 EMadore V6 - Ajout
    [EXTFILE] = @EXTFILE,     -- 2014-07-31 EMadore V6 - Ajout
    [NODOC] = @NODOC,
    [DESCDOC] = @DESCDOC,
    [DATECREE] = @DATECREE,
    [DATEDOC] = @DATEDOC,
    [DATEEXP] = @DATEEXP,
    [REF_ID] = @REF_ID,
    [STATUT] = @STATUT,
    [NOCOMMANDE] = @NOCOMMANDE,
    [NOTEINTERN] = @NOTEINTERN,
    [CLIENTNO] = @CLIENTNO,
    [CLIENTCIE] = @CLIENTCIE,
    [CLIENTCNT] = @CLIENTCNT,
    [CLIENTRUE1] = @CLIENTRUE1,
    [CLIENTRUE2] = @CLIENTRUE2,
    [CLIENTVILL] = @CLIENTVILL,
    [CLIENTCP] = @CLIENTCP,
    [CLIENTPROV] = @CLIENTPROV,
    [CLIENTPAYS] = @CLIENTPAYS,
    [CLIENTBP] = @CLIENTBP,
    [CLIENTTEL1] = @CLIENTTEL1,
    [CLIENTTEL2] = @CLIENTTEL2,
    [CLIENTTEL3] = @CLIENTTEL3,
    [CLIENTFAX] = @CLIENTFAX,
    [CLIENTEMAI] = @CLIENTEMAI,  -- 2012-01-19 EMadore V3 : Ajout
    [MEMESITE] = @MEMESITE,
    [SITENO] = @SITENO,
    [SITECIE] = @SITECIE,
    [SITECNT] = @SITECNT,
    [SITERUE1] = @SITERUE1,
    [SITERUE2] = @SITERUE2,
    [SITEVILLE] = @SITEVILLE,
    [SITECP] = @SITECP,
    [SITEPROV] = @SITEPROV,
    [SITEPAYS] = @SITEPAYS,
    [SITEBP] = @SITEBP,
    [SITETEL1] = @SITETEL1,
    [SITETEL2] = @SITETEL2,
    [SITETEL3] = @SITETEL3,
    [SITEFAX] = @SITEFAX,
    [SITEEMAIL] = @SITEEMAIL,   -- 2012-01-19 EMadore V3 : Ajout
    [MATTOTALMD] = @MATTOTALMD,
    [NOTEPRINC] = @NOTEPRINC,
    [MATCOUTREL] = @MATCOUTREL,
    [MATCOUTLOT] = @MATCOUTLOT,
    [MATVENDCAL] = @MATVENDCAL,
    [MATPORTTVP] = @MATPORTTVP,
    [SERCOUTCAL] = @SERCOUTCAL,
    [SERVENDCAL] = @SERVENDCAL,
    [SERHRESCAL] = @SERHRESCAL,
    [SERPORTTVP] = @SERPORTTVP,
    [AUTCOUTCAL] = @AUTCOUTCAL,
    [AUTVENDCAL] = @AUTVENDCAL,
    [AUTPORTTVP] = @AUTPORTTVP,
    [OPTIONSSOM] = @OPTIONSSOM,
    [MATCOUTMO] = @MATCOUTMO,
    [SERCOUTMO] = @SERCOUTMO,
    [AUTCOUTMO] = @AUTCOUTMO,
    [MATADMPC] = @MATADMPC,
    [SERADMPC] = @SERADMPC,
    [AUTADMPC] = @AUTADMPC,
    [MATADMMO] = @MATADMMO,
    [SERADMMO] = @SERADMMO,
    [AUTADMMO] = @AUTADMMO,
    [MATPROFPC] = @MATPROFPC,
    [SERPROFPC] = @SERPROFPC,
    [AUTPROFPC] = @AUTPROFPC,
    [MATPROFMO] = @MATPROFMO,
    [SERPROFMO] = @SERPROFMO,
    [AUTPROFMO] = @AUTPROFMO,
    [GLOBAJUPC] = @GLOBAJUPC,
    [GLOBAJUMO] = @GLOBAJUMO,
    [GLOBEXPLIC] = @GLOBEXPLIC,
    [GLOBAJU2PC] = @GLOBAJU2PC,
    [GLOBAJU2MO] = @GLOBAJU2MO,
    [GLOBEXPL2] = @GLOBEXPL2,
    [OPTIONSIMP] = @OPTIONSIMP,
    [OPIMPADJMA] = @OPIMPADJMA,
    [OPIMPADJLA] = @OPIMPADJLA,
    [OPIMPADJOT] = @OPIMPADJOT,
    [NOTEBAS] = @NOTEBAS,
    [MATTAXAB1] = @MATTAXAB1,
    [MATTAXAB2] = @MATTAXAB2,
    [MATTAXAB3] = @MATTAXAB3,
    [MATTAXAB4] = @MATTAXAB4,
    [MATTAXAB5] = @MATTAXAB5,
    [MATTAXAB6] = @MATTAXAB6,
    [SERTAXAB1] = @SERTAXAB1,
    [SERTAXAB2] = @SERTAXAB2,
    [SERTAXAB3] = @SERTAXAB3,
    [SERTAXAB4] = @SERTAXAB4,
    [SERTAXAB5] = @SERTAXAB5,
    [SERTAXAB6] = @SERTAXAB6,
    [AUTTAXAB1] = @AUTTAXAB1,
    [AUTTAXAB2] = @AUTTAXAB2,
    [AUTTAXAB3] = @AUTTAXAB3,
    [AUTTAXAB4] = @AUTTAXAB4,
    [AUTTAXAB5] = @AUTTAXAB5,
    [AUTTAXAB6] = @AUTTAXAB6,
    [TAXTYPCAL] = @TAXTYPCAL,
    [AJUTAXAB1] = @AJUTAXAB1,
    [AJUTAXAB2] = @AJUTAXAB2,
    [AJUTAXAB3] = @AJUTAXAB3,
    [AJUTAXAB4] = @AJUTAXAB4,
    [AJUTAXAB5] = @AJUTAXAB5,
    [TOTTAXFED] = @TOTTAXFED,
    [TOTTAXPRV] = @TOTTAXPRV,
    [TAX_ID] = @TAX_ID,
    [APPLIQUTVF] = @APPLIQUTVF,
    [APPLIQUTVP] = @APPLIQUTVP,
    [TVPSURCOUT] = @TVPSURCOUT,
    [TOTCALCULE] = @TOTCALCULE,
    [CALCTIMSTP] = @CALCTIMSTP,
    [UMPLAN] = @UMPLAN,
    [TYPEPROF] = @TYPEPROF,
    [MATPROFDEF] = @MATPROFDEF,
    [TYPESRVPRO] = @TYPESRVPRO,
    [TAUXMD] = @TAUXMD,
    [NUMLOTEXP] = @NUMLOTEXP,
    [SYSTEM] = @SYSTEM,
    [USER1] = @USER1,
    [USER2] = @USER2,
    [EST_NAME] = @EST_NAME,
    [ACCTRANSNO] = @ACCTRANSNO,
    [PRJTRANSNO] = @PRJTRANSNO,
    [STATUTLIBF]  = @STATUTLIBF,
    [STATUTLIBE]  = @STATUTLIBE,	
    [USER_ID] = @USER_ID,
    [BRANCH_ID]  = @BRANCH_ID,
    [OWC]  = @OWC,	
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating FACTURES
  exec dbo.sp_Update_FacturesUserSession @SOU_ID	

  --Return updated ID
  RETURN @UniqueId
END
GO

-----------------------

IF OBJECT_ID(N'dbo.up_FACAMD_Delete', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_FACAMD_Delete ;
GO

CREATE PROCEDURE [dbo].[up_FACAMD_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM FACAMD D WHERE D.UniqueId = @UniqueId

DELETE FROM FACAMD WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating FACTURES
exec dbo.sp_Update_FacturesUserSession @SOU_ID	
GO


IF OBJECT_ID(N'dbo.up_FACBLO_Delete', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_FACBLO_Delete ;
GO

CREATE PROCEDURE [dbo].[up_FACBLO_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM FACBLO D WHERE D.UniqueId = @UniqueId

DELETE FROM FACBLO WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating FACTURES
exec dbo.sp_Update_FacturesUserSession @SOU_ID	
GO


IF OBJECT_ID(N'dbo.[up_FACDIV_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_FACDIV_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_FACDIV_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM FACDIV D WHERE D.UniqueId = @UniqueId

DELETE FROM FACDIV WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating FACTURES
exec dbo.sp_Update_FacturesUserSession @SOU_ID	
GO

IF OBJECT_ID(N'dbo.[up_FACENS_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_FACENS_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_FACENS_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM FACENS D WHERE D.UniqueId = @UniqueId

DELETE FROM FACENS WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating FACTURES
exec dbo.sp_Update_FacturesUserSession @SOU_ID	
GO


IF OBJECT_ID(N'dbo.[up_FACENSCO_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_FACENSCO_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_FACENSCO_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM FACENSCO D WHERE D.UniqueId = @UniqueId

DELETE FROM FACENSCO WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating FACTURES
exec dbo.sp_Update_FacturesUserSession @SOU_ID	
GO

IF OBJECT_ID(N'dbo.[up_FACLOTS_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_FACLOTS_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_FACLOTS_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM FACLOTS D WHERE D.UniqueId = @UniqueId

DELETE FROM FACLOTS WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating FACTURES
exec dbo.sp_Update_FacturesUserSession @SOU_ID	
GO

IF OBJECT_ID(N'dbo.[up_FACLOTSCO_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_FACLOTSCO_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_FACLOTSCO_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM FACLOTSCO D WHERE D.UniqueId = @UniqueId

DELETE FROM FACLOTSCO WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating FACTURES
exec dbo.sp_Update_FacturesUserSession @SOU_ID	
GO

IF OBJECT_ID(N'dbo.[up_FACPRO_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_FACPRO_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_FACPRO_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM FACPRO D WHERE D.UniqueId = @UniqueId

DELETE FROM FACPRO WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating FACTURES
exec dbo.sp_Update_FacturesUserSession @SOU_ID	
GO


IF OBJECT_ID(N'dbo.[up_FACREL_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_FACREL_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_FACREL_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM FACREL D WHERE D.UniqueId = @UniqueId

DELETE FROM FACREL WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating FACTURES
exec dbo.sp_Update_FacturesUserSession @SOU_ID	
GO

IF OBJECT_ID(N'dbo.[up_FACWEBLOGL_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_FACWEBLOGL_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_FACWEBLOGL_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM FACWEBLOG D WHERE D.UniqueId = @UniqueId

DELETE FROM FACWEBLOG WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating FACTURES
exec dbo.sp_Update_FacturesUserSession @SOU_ID	
GO



-------------- corriger le contenu des procedures apre avoir changer les noms


IF OBJECT_ID(N'dbo.sp_SOU_CalculQteTotalItem', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_SOU_CalculQteTotalItem ;
GO

CREATE PROCEDURE [dbo].sp_SOU_CalculQteTotalItem (@SOU_ID VARCHAR(20), @ITEM_ID VARCHAR(20), @TYPEITEM VARCHAR(1), @BLO_ID_REL VARCHAR(3), @QTE FLOAT, @QTEUM VARCHAR(2) , @UID VARCHAR(14))
AS BEGIN
  DECLARE @COUUM_SOUPRO   VARCHAR(2)
  DECLARE @QPP_SOUPRO     INT
  DECLARE @MULT_BLOC      INT
  DECLARE @QTE_TOTAL      FLOAT
  DECLARE @CALCTIMSTP     VARCHAR(14)
       
  SET @QTE_TOTAL = 0;


  SELECT @COUUM_SOUPRO = P.COUUM,  @QPP_SOUPRO = P.QPP , @CALCTIMSTP = P.CALCTIMSTP
    FROM SOUPRO P
   WHERE P.SOU_ID = @SOU_ID
     AND P.PRO_ID = @ITEM_ID

  SET @QTE_TOTAL = @QTE * DBO.fn_UM_GetRatioDeConversion  (@QTEUM, DBO.fn_UM_GetUniteDeBase(@COUUM_SOUPRO),  @QPP_SOUPRO)
     
  SELECT @MULT_BLOC = B.MULT
    FROM SOUBLO B
   WHERE B.BLO_ID = @BLO_ID_REL
     AND B.SOU_ID = @SOU_ID

  IF @MULT_BLOC IS NOT NULL 
  BEGIN
    SET @QTE_TOTAL = @QTE_TOTAL * @MULT_BLOC
  END


  IF @CALCTIMSTP <> @UID 
  BEGIN
    UPDATE SOUPRO
      SET   QTEOTH = 0, 
            QTEENS = 0,
            QTELOT = 0
    WHERE   SOU_ID = @SOU_ID
    AND     PRO_ID = @ITEM_ID 
  END

  IF ((@TYPEITEM = 'P') OR (@TYPEITEM = 'N'))
    EXEC dbo.sp_SOU_UpdateQteTotalOth @SOU_ID, @ITEM_ID, @CALCTIMSTP, @UID , @QTE_TOTAL  
  ELSE IF @TYPEITEM = 'A'
    EXEC dbo.sp_SOU_UpdateQteTotalEns @SOU_ID, @ITEM_ID, @CALCTIMSTP, @UID , @QTE_TOTAL  
  ELSE IF @TYPEITEM = 'L'
    EXEC dbo.sp_SOU_UpdateQteTotalLots @SOU_ID, @ITEM_ID, @CALCTIMSTP, @UID , @QTE_TOTAL  

END 
GO


-- procedure de calcule des quantités


IF OBJECT_ID(N'dbo.sp_SOUPRO_Quantity', N'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_SOUPRO_Quantity ;
GO


CREATE PROCEDURE [dbo].sp_SOUPRO_Quantity (@SOU_ID VARCHAR(20), @REPLACE_FILTER INT)
AS BEGIN

   DECLARE @UID            VARCHAR(14)
   DECLARE @QTE            FLOAT    
   DECLARE @QTEUM          VARCHAR(2)
    --
   DECLARE @TYPERELEVE_REL CHAR
   DECLARE @TYPEITEM_REL   CHAR
   DECLARE @QTE_REL        FLOAT 
   DECLARE @QTEUM_REL      VARCHAR(2)
   DECLARE @ITEM_ID_REL    VARCHAR(20)
   DECLARE @BLO_ID_REL     VARCHAR(3)
   DECLARE @SECTION_REL    FLOAT 
   DECLARE @CODEIMPR_REL   VARCHAR(36)
    --
   DECLARE @QPP_SOUPRO     INT
    --
   DECLARE @COUUM_ENS      VARCHAR(2)
   DECLARE @QTEUM_ENSCO    VARCHAR(2)
   DECLARE @TYPRATIO_ENSCO VARCHAR(1)
   DECLARE @QTE_ENSCO      FLOAT 
   DECLARE @ENS_ID_ENS     VARCHAR(20)
   DECLARE @PRO_ID_ENSCO   VARCHAR(20)
    --
   DECLARE @COUUM_LOT      VARCHAR(2)
   DECLARE @QTE_LOTCO      FLOAT
   DECLARE @QTEUM_LOTCO    VARCHAR(2)
   DECLARE @PRO_ID_LOTCO   VARCHAR(20)
    --
   DECLARE CUR_SOUREL CURSOR FOR 
      SELECT S.ITEM_ID , S.TYPERELEVE, S.TYPEITEM, S.QTE, S.QTEUM, S.BLO_ID, S.SECTION, S.CODEIMPR
   FROM SOUREL S
   WHERE S.SOU_ID = @SOU_ID
  
   SELECT @UID = DBO.fn_DateTime_GetTimeStampStr()

   ----------------------------------
   ---- Pour les codes d'impression : 0 Pour Ne pas traiter , 1 Pour Ajouter, 2 pour remplacer
   ----------------------------------

   IF @REPLACE_FILTER = 2 
   BEGIN
     UPDATE   SOUPRO
        SET CODEIMPR = ''
        WHERE   SOU_ID = @SOU_ID
   END
 
   -----------------------------------

   OPEN CUR_SOUREL
   FETCH NEXT FROM CUR_SOUREL
   INTO @ITEM_ID_REL, @TYPERELEVE_REL, @TYPEITEM_REL, @QTE_REL, @QTEUM_REL, @BLO_ID_REL, @SECTION_REL, @CODEIMPR_REL


   UPDATE SOUMIS 
      SET CALCTIMSTP = @UID
    WHERE SOU_ID = @SOU_ID 


   UPDATE SOUPRO 
      SET QTEOTH = 0,  
          QTEENS = 0, 
          QTELOT = 0  
    WHERE SOU_ID = @SOU_ID 


   WHILE @@FETCH_STATUS = 0
   BEGIN
     IF ((@TYPERELEVE_REL = 'P') AND (@TYPEITEM_REL <> 'T'))
     BEGIN
       --------------------------------------
       ---- Produits-------------------------
       --------------------------------------
       IF ((@TYPEITEM_REL = 'P') OR (@TYPEITEM_REL = 'N'))
       BEGIN

         SET @QTE   = @QTE_REL
         SET @QTEUM = @QTEUM_REL

         EXEC dbo.sp_SOU_CalculQteTotalItem @SOU_ID, 
                                            @ITEM_ID_REL, 
                                            @TYPEITEM_REL,
                                            @BLO_ID_REL, 
                                            @QTE, 
                                            @QTEUM, 
                                            @UID

         IF @REPLACE_FILTER > 0
         BEGIN
          EXEC dbo.sp_SOU_CalculCodeImpr @SOU_ID, @ITEM_ID_REL, @CODEIMPR_REL
         END

       END ELSE
       --------------------------------------
       ---- Ensembles------------------------
       --------------------------------------
       IF (@TYPEITEM_REL = 'A')
       BEGIN

         DECLARE CUR_PRODUITSENS CURSOR FOR
            SELECT E.COUUM, C.QTEUM, C.TYPRATIO,
                    CASE 
                      WHEN (C.TYPRATIO = 'L') AND (E.COUUM <> '') AND (DBO.fn_UM_GetNatureUnite(E.COUUM) = 'L') THEN 
                        CASE 
                          WHEN (C.DIV <> '')  THEN (C.QTE / C.DIV) * DBO.fn_UM_GetRatioDeConversion  (E.COUUM, C.DIVUM,  0)   
                          ELSE 0
                        END
                      ELSE C.QTE          
                    END AS QTE_ENSCO , E.ENS_ID, C.PRO_ID

            FROM SOUENS E, SOUENSCO C
            WHERE E.SOU_ID = C.SOU_ID
            AND   E.ENS_ID = C.ENS_ID
            AND   E.SOU_ID = @SOU_ID
            AND   E.ENS_ID = @ITEM_ID_REL               
        ----------------------------------


         OPEN CUR_PRODUITSENS

         FETCH NEXT FROM CUR_PRODUITSENS
         INTO @COUUM_ENS, @QTEUM_ENSCO, @TYPRATIO_ENSCO, @QTE_ENSCO, @ENS_ID_ENS, @PRO_ID_ENSCO

         WHILE @@FETCH_STATUS = 0
         BEGIN
           SET @QTE = 0;

           IF @TYPRATIO_ENSCO = 'L'
             SET @QTE = (@QTE_ENSCO * @QTE_REL * DBO.fn_UM_GetRatioDeConversion  (@QTEUM_REL, @COUUM_ENS,  0))
           ELSE
             SET @QTE = (@QTE_ENSCO * @SECTION_REL)

           SET @QTEUM = @QTEUM_ENSCO

           EXEC dbo.sp_SOU_CalculQteTotalItem @SOU_ID, 
                                              @PRO_ID_ENSCO, 
                                              @TYPEITEM_REL,
                                              @BLO_ID_REL, 
                                              @QTE, 
                                              @QTEUM, 
                                              @UID

           IF @REPLACE_FILTER > 0
           BEGIN
             EXEC dbo.sp_SOU_CalculCodeImpr @SOU_ID, @PRO_ID_ENSCO, @CODEIMPR_REL
           END

           FETCH NEXT FROM CUR_PRODUITSENS
           INTO @COUUM_ENS, @QTEUM_ENSCO, @TYPRATIO_ENSCO, @QTE_ENSCO, @ENS_ID_ENS, @PRO_ID_ENSCO
         END

         CLOSE CUR_PRODUITSENS;
         DEALLOCATE CUR_PRODUITSENS;
       END ELSE
       --------------------------------------
       ---- Lots-----------------------------
       --------------------------------------
       IF (@TYPEITEM_REL = 'L')
       BEGIN

       ----------------------------------

         DECLARE CUR_PRODUITSLOTS CURSOR FOR
            SELECT L.COUUM, C.QTE, C.QTEUM, C.PRO_ID
            FROM SOULOTS L, SOULOTSCO C
            WHERE L.LOTS_ID = C.LOTS_ID
            AND   L.SOU_ID = @SOU_ID

         OPEN CUR_PRODUITSLOTS

         FETCH NEXT FROM CUR_PRODUITSLOTS
         INTO @COUUM_LOT, @QTE_LOTCO, @QTEUM_LOTCO, @PRO_ID_LOTCO

         WHILE @@FETCH_STATUS = 0
         BEGIN

           SELECT @QPP_SOUPRO = P.QPP
            FROM SOUPRO P
           WHERE P.SOU_ID = @SOU_ID
             AND P.PRO_ID = @ITEM_ID_REL

           SET @QTE = (@QTE_LOTCO * @QTE_REL * DBO.fn_UM_GetRatioDeConversion  (@QTEUM_REL, @COUUM_LOT,  @QPP_SOUPRO))

           SET @QTEUM = @QTEUM_LOTCO

           EXEC dbo.sp_SOU_CalculQteTotalItem @SOU_ID, 
                                              @PRO_ID_LOTCO, 
                                              @TYPEITEM_REL,
                                              @BLO_ID_REL, 
                                              @QTE, 
                                              @QTEUM, 
                                              @UID

           IF @REPLACE_FILTER > 0
           BEGIN
             EXEC dbo.sp_SOU_CalculCodeImpr @SOU_ID, @PRO_ID_LOTCO, @CODEIMPR_REL
           END

           FETCH NEXT FROM CUR_PRODUITSLOTS
           INTO @COUUM_LOT, @QTE_LOTCO, @QTEUM_LOTCO, @PRO_ID_LOTCO 

         END

         CLOSE CUR_PRODUITSLOTS;
         DEALLOCATE CUR_PRODUITSLOTS;
       END
       --------------------------------------
     END
     FETCH NEXT FROM CUR_SOUREL
     INTO @ITEM_ID_REL, @TYPERELEVE_REL, @TYPEITEM_REL, @QTE_REL, @QTEUM_REL, @BLO_ID_REL, @SECTION_REL, @CODEIMPR_REL

   END
   CLOSE CUR_SOUREL;
   DEALLOCATE CUR_SOUREL;

END
GO


IF OBJECT_ID(N'dbo.sp_SOU_CalculProductUsageInAssemblies', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_SOU_CalculProductUsageInAssemblies ;
GO

CREATE PROCEDURE [dbo].sp_SOU_CalculProductUsageInAssemblies (@SOU_ID VARCHAR(20), @LANG INT)
AS BEGIN
  DECLARE  @TITLE  VARCHAR(60);
  DECLARE  @DESCR  VARCHAR(2000);  
  DECLARE  @SOUID  VARCHAR(20);
  DECLARE  @PRO_ID VARCHAR(20);



  IF @LANG = 1 
    SET @TITLE = 'Dans les ensembles'
  ELSE
    SET @TITLE = 'In assemblies '

  SET @TITLE =    @TITLE + CHAR(13) + CHAR(10) + REPLICATE('-', LEN(@TITLE))

  DECLARE CUR_1 CURSOR FOR 
   
   SELECT E.SOU_ID, C.PRO_ID , DESCR = @TITLE +  CHAR(13) + CHAR(10) + dbo.sp_SOU_GetAssemblyCompositionConcat(E.SOU_ID, C.PRO_ID)    
   FROM SOUENS E, SOUENSCO C , SOUREL L
      WHERE E.ENS_ID = C.ENS_ID
        AND E.SOU_ID = C.SOU_ID
        AND L.SOU_ID = E.SOU_ID
        AND L.ITEM_ID = E.ENS_ID
        AND C.SOU_ID = @SOU_ID    
  GROUP BY  E.SOU_ID, C.PRO_ID

  OPEN CUR_1
  FETCH NEXT FROM CUR_1
  INTO @SOUID, @PRO_ID, @DESCR

  WHILE @@FETCH_STATUS = 0
   BEGIN
     UPDATE SOUPRO
        SET INASSEMBLIE = @DESCR
      WHERE PRO_ID = @PRO_ID 
        AND SOU_ID = @SOUID 

     FETCH NEXT FROM CUR_1
     INTO @SOUID, @PRO_ID, @DESCR
   END
  CLOSE CUR_1;
  DEALLOCATE CUR_1;

END
GO

