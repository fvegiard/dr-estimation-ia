IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'TOOLSQLSCRIPT')
BEGIN

CREATE TABLE [dbo].[TOOLSQLSCRIPT](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[EXECDATE] [datetime] NOT NULL, 
	[EXECNAME] VARCHAR(30) NOT NULL,
	[EXECSUCCES] bit DEFAULT (0),
	[EXECBLOCERR] int DEFAULT (0),
	[SysDate] [datetime] NOT NULL DEFAULT (getdate())
)

END
GO

IF OBJECT_ID(N'dbo.up_TOOLSQLSCRIPT_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_TOOLSQLSCRIPT_Update ;
GO

CREATE PROCEDURE [dbo].[up_TOOLSQLSCRIPT_Update] (
  @UniqueId bigint,
  @EXECDATE datetime,
  @EXECNAME VARCHAR(30),
  @EXECSUCCES bit,
  @EXECBLOCERR int
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO TOOLSQLSCRIPT (
    [EXECDATE],
    [EXECNAME],
    [EXECSUCCES],
    [EXECBLOCERR],
    SysDate)
  VALUES (
    @EXECDATE,
    @EXECNAME,
    @EXECSUCCES,
	@EXECBLOCERR,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    TOOLSQLSCRIPT
  SET
    [EXECDATE] = @EXECDATE,
    [EXECNAME] = @EXECNAME,
    [EXECSUCCES] = @EXECSUCCES,
    [EXECBLOCERR] = @EXECBLOCERR,
     SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

IF OBJECT_ID(N'dbo.up_TOOLSQLSCRIPT_Delete', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_TOOLSQLSCRIPT_Delete ;
GO

CREATE PROCEDURE [dbo].[up_TOOLSQLSCRIPT_Delete] (
  @UniqueId bigint
) AS
BEGIN
  DELETE FROM TOOLSQLSCRIPT WHERE UniqueId = @UniqueId
END
GO
  
----------------------

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'sp_SOU_UpdateQteTotalEns_v2')
  DROP PROCEDURE sp_SOU_UpdateQteTotalEns_v2
GO

CREATE PROCEDURE [dbo].[sp_SOU_UpdateQteTotalEns_v2] (@SOU_ID VARCHAR(20), @REPLACE_FILTER INT, @UID VARCHAR(14), @DoLog BIT, @SOUPROLOG VARCHAR(20))
AS BEGIN
   
  DECLARE @CODEIMPR       VARCHAR(36)
  DECLARE @PROD_ID        VARCHAR(20)
  DECLARE @QTE_NEW        FLOAT

  DECLARE @SqlTable       VARCHAR(100)
  DECLARE @Sql1           NVARCHAR(1000)
  -----------------------------------

    DECLARE CUR_1 CURSOR FOR 

    SELECT BB.PRO_ID, BB.New_QTE  -- , SPP.QTEENS  --, BB.New_QTE - SPP.QTEENS 
    FROM SOUPRO SPP LEFT JOIN 
         ( SELECT SP.PRO_ID  AS PRO_ID ,  
			     SUM(SR2.QTE_cmp * DBO.fn_UM_GetRatioDeConversion(SR2.QTEUM_cmp, DBO.fn_UM_GetUniteDeBase(SP.COUUM), SP.QPP)) AS New_QTE
  		     FROM SOUPRO SP, (
							  SELECT 
								CMP1.PRO_ID as ITEM_ID_cmp, 
								SR.BLO_ID   as BLO_ID_cmp, 									  
								CMP1.QTEUM  as QTEUM_cmp, 
								SUM(
									(CASE 
										WHEN CMP1.TYPRATIO = 'L'											
											THEN CAST( CMP1.QTE_ENSCO * DBO.fn_UM_GetRatioDeConversion  (SR.QTEUM, CMP1.COUUM,  0) AS NUMERIC(18,3)) * SR.QTE
											ELSE CMP1.QTE_ENSCO * SR.SECTION
										END ) * dbo.fn_MultBlock(SR.SOU_ID, SR.BLO_ID) 
									) as QTE_cmp

						      FROM SOUREL SR ,
								( SELECT E.COUUM, C.QTEUM, C.TYPRATIO,
										CASE 
										  WHEN (C.TYPRATIO = 'L') AND (E.COUUM <> '') AND (DBO.fn_UM_GetNatureUnite(E.COUUM) = 'L') THEN 
											CASE 
											  WHEN (C.DIV <> 0)  THEN (C.QTE / C.DIV) * DBO.fn_UM_GetRatioDeConversion  (E.COUUM, C.DIVUM,  0)   
											  ELSE 0
											END
										  ELSE C.QTE          
										END AS QTE_ENSCO , 
										E.ENS_ID, 
										C.PRO_ID

										FROM SOUENS E, SOUENSCO C
										WHERE E.SOU_ID = C.SOU_ID
										AND   E.ENS_ID = C.ENS_ID
										AND   E.SOU_ID = @SOU_ID
								 ) AS CMP1

						      WHERE SR.SOU_ID     = @SOU_ID	
							    AND SR.TYPEITEM = 'A'
							    AND SR.ITEM_ID  = CMP1.ENS_ID
						      GROUP BY SR.BLO_ID, CMP1.PRO_ID , CMP1.QTEUM
							  ) AS SR2
   		     
  		     WHERE SP.PRO_ID = SR2.ITEM_ID_cmp
					 AND SP.SOU_ID  = @SOU_ID	
  		     GROUP BY SP.PRO_ID
         ) AS BB

    ON SPP.PRO_ID = BB.PRO_ID
    WHERE SPP.SOU_ID  = @SOU_ID	
	AND ((@DoLog=1) OR 
	     ((((BB.New_QTE IS NOT NULL) AND (CAST(SPP.QTEENS AS NUMERIC(18,2)) != CAST(BB.New_QTE AS NUMERIC(18,2)))) OR
           ((BB.New_QTE IS NULL)     AND (SPP.QTEENS  != 0)))));

  -----------------------------------
	IF @DoLog = 0 
	BEGIN
	  SET @SqlTable = 'SOUPRO'
	END ELSE 
	BEGIN
	  SET @SqlTable = @SOUPROLOG	
	END
  ----------------------------------- 

    OPEN CUR_1
    FETCH NEXT FROM CUR_1
    INTO @PROD_ID, @QTE_NEW

	WHILE @@FETCH_STATUS = 0
	BEGIN
 	  -- On modifie les produits dont la quantité total a changé, les autres forcer a zero
	  IF (@QTE_NEW IS NOT NULL) AND (@QTE_NEW <> 0)
	  BEGIN
	    SET @sql1 =  'UPDATE ' + @SqlTable +'  SET QTEENS = ' + STR( @QTE_NEW, 18, 5) + ' , CALCTIMSTP = ' + '''' + @UID + '''' +  ' WHERE SOU_ID = ' + '''' + @SOU_ID + '''' +  ' AND PRO_ID = ' + '''' + @PROD_ID + '''';
	  END ELSE 
	  BEGIN
        SET @sql1 =  'UPDATE ' + @SqlTable +'  SET QTEENS = 0                             , CALCTIMSTP = ' + '''' + @UID + '''' +  ' WHERE SOU_ID = ' + '''' + @SOU_ID + '''' +  ' AND PRO_ID = ' + '''' + @PROD_ID + '''';
	  END;
		
      EXECUTE sp_executeSQL @Sql1;

    
	  FETCH NEXT FROM CUR_1
	  INTO @PROD_ID, @QTE_NEW
	END

   CLOSE CUR_1;
   DEALLOCATE CUR_1;

    ----- Calcul du code d'impresion

   IF @REPLACE_FILTER > 0
   BEGIN
	 DECLARE CUR_2 CURSOR FOR 
	
	 SELECT DISTINCT SEC.PRO_ID , SR.CODEIMPR
     FROM SOUREL SR, SOUENS SE, SOUENSCO SEC
     WHERE SR.SOU_ID   =  @SOU_ID
       AND SR.TYPEITEM = 'A'
	   AND SR.SOU_ID   = SE.SOU_ID
	   AND SR.ITEM_ID  = SE.ENS_ID
	   AND SE.SOU_ID   = SEC.SOU_ID
	   AND SE.ENS_ID   = SEC.ENS_ID  
	   AND SR.CODEIMPR != '';

	 OPEN CUR_2
	 FETCH NEXT FROM CUR_2
	 INTO @PROD_ID, @CODEIMPR

	 WHILE @@FETCH_STATUS = 0
	 BEGIN
	   IF @CODEIMPR != ''
	   BEGIN
	     EXEC dbo.sp_SOU_CalculCodeImpr @SOU_ID, @PROD_ID, @CODEIMPR
	   END

	   FETCH NEXT FROM CUR_2
	   INTO @PROD_ID, @CODEIMPR

	 END 
   END

   CLOSE CUR_2;
   DEALLOCATE CUR_2;
		    			    
END
GO


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'sp_FAC_UpdateQteTotalEns_v2')
  DROP PROCEDURE sp_FAC_UpdateQteTotalEns_v2
GO

CREATE PROCEDURE [dbo].[sp_FAC_UpdateQteTotalEns_v2] (@SOU_ID VARCHAR(20), @REPLACE_FILTER INT, @UID VARCHAR(14), @DoLog BIT, @FACPROLOG VARCHAR(20))
AS BEGIN
   
  DECLARE @CODEIMPR       VARCHAR(36)
  DECLARE @PROD_ID        VARCHAR(20)
  DECLARE @QTE_NEW        FLOAT

  DECLARE @SqlTable       VARCHAR(100)
  DECLARE @Sql1           NVARCHAR(1000)
  -----------------------------------

    DECLARE CUR_1 CURSOR FOR 

    SELECT BB.PRO_ID, BB.New_QTE  -- , SPP.QTEENS  --, BB.New_QTE - SPP.QTEENS 
    FROM FACPRO SPP LEFT JOIN 
         ( SELECT SP.PRO_ID  AS PRO_ID ,  
			     SUM(SR2.QTE_cmp * DBO.fn_UM_GetRatioDeConversion(SR2.QTEUM_cmp, DBO.fn_UM_GetUniteDeBase(SP.COUUM), SP.QPP)) AS New_QTE
  		     FROM FACPRO SP, (
							  SELECT 
								CMP1.PRO_ID as ITEM_ID_cmp, 
								SR.BLO_ID   as BLO_ID_cmp, 									  
								CMP1.QTEUM  as QTEUM_cmp, 
								SUM(
									(CASE 
										WHEN CMP1.TYPRATIO = 'L'
											THEN CAST( CMP1.QTE_ENSCO * DBO.fn_UM_GetRatioDeConversion  (SR.QTEUM, CMP1.COUUM,  0) AS NUMERIC(18,3)) * SR.QTE
											ELSE CMP1.QTE_ENSCO * SR.SECTION
										END ) * dbo.fn_MultBlock(SR.SOU_ID, SR.BLO_ID) 
									) as QTE_cmp

						      FROM FACREL SR ,
								( SELECT E.COUUM, C.QTEUM, C.TYPRATIO,
										CASE 
										  WHEN (C.TYPRATIO = 'L') AND (E.COUUM <> '') AND (DBO.fn_UM_GetNatureUnite(E.COUUM) = 'L') THEN 
											CASE 
											  WHEN (C.DIV <> 0)  THEN (C.QTE / C.DIV) * DBO.fn_UM_GetRatioDeConversion  (E.COUUM, C.DIVUM,  0)   
											  ELSE 0
											END
										  ELSE C.QTE          
										END AS QTE_ENSCO , 
										E.ENS_ID, 
										C.PRO_ID

										FROM FACENS E, FACENSCO C
										WHERE E.SOU_ID = C.SOU_ID
										AND   E.ENS_ID = C.ENS_ID
										AND   E.SOU_ID = @SOU_ID
								 ) AS CMP1

						      WHERE SR.SOU_ID     = @SOU_ID	
							    AND SR.TYPEITEM = 'A'
							    AND SR.ITEM_ID  = CMP1.ENS_ID
						      GROUP BY SR.BLO_ID, CMP1.PRO_ID , CMP1.QTEUM
							  ) AS SR2
   		     
  		     WHERE SP.PRO_ID = SR2.ITEM_ID_cmp
					 AND SP.SOU_ID  = @SOU_ID	
  		     GROUP BY SP.PRO_ID
         ) AS BB

    ON SPP.PRO_ID = BB.PRO_ID
    WHERE SPP.SOU_ID  = @SOU_ID	
	AND ((@DoLog=1) OR 
	     ((((BB.New_QTE IS NOT NULL) AND (CAST(SPP.QTEENS AS NUMERIC(18,2)) != CAST(BB.New_QTE AS NUMERIC(18,2)))) OR
           ((BB.New_QTE IS NULL)     AND (SPP.QTEENS  != 0)))));

  -----------------------------------
	IF @DoLog = 0 
	BEGIN
	  SET @SqlTable = 'FACPRO'
	END ELSE 
	BEGIN
	  SET @SqlTable = @FACPROLOG	
	END
  ----------------------------------- 

    OPEN CUR_1
    FETCH NEXT FROM CUR_1
    INTO @PROD_ID, @QTE_NEW

	WHILE @@FETCH_STATUS = 0
	BEGIN
 	  -- On modifie les produits dont la quantité total a changé, les autres forcer a zero
	  IF (@QTE_NEW IS NOT NULL) AND (@QTE_NEW <> 0)
	  BEGIN
	    SET @sql1 =  'UPDATE ' + @SqlTable +'  SET QTEENS = ' + STR( @QTE_NEW, 18, 5) + ' , CALCTIMSTP = ' + '''' + @UID + '''' +  ' WHERE SOU_ID = ' + '''' + @SOU_ID + '''' +  ' AND PRO_ID = ' + '''' + @PROD_ID + '''';
	  END ELSE 
	  BEGIN
        SET @sql1 =  'UPDATE ' + @SqlTable +'  SET QTEENS = 0                             , CALCTIMSTP = ' + '''' + @UID + '''' +  ' WHERE SOU_ID = ' + '''' + @SOU_ID + '''' +  ' AND PRO_ID = ' + '''' + @PROD_ID + '''';
	  END;
		
      EXECUTE sp_executeSQL @Sql1;

    
	  FETCH NEXT FROM CUR_1
	  INTO @PROD_ID, @QTE_NEW
	END

   CLOSE CUR_1;
   DEALLOCATE CUR_1;

    ----- Calcul du code d'impresion

   IF @REPLACE_FILTER > 0
   BEGIN
	 DECLARE CUR_2 CURSOR FOR 
	
	 SELECT DISTINCT SEC.PRO_ID , SR.CODEIMPR
     FROM FACREL SR, FACENS SE, FACENSCO SEC
     WHERE SR.SOU_ID   =  @SOU_ID
       AND SR.TYPEITEM = 'A'
	   AND SR.SOU_ID   = SE.SOU_ID
	   AND SR.ITEM_ID  = SE.ENS_ID
	   AND SE.SOU_ID   = SEC.SOU_ID
	   AND SE.ENS_ID   = SEC.ENS_ID  
	   AND SR.CODEIMPR != '';

	 OPEN CUR_2
	 FETCH NEXT FROM CUR_2
	 INTO @PROD_ID, @CODEIMPR

	 WHILE @@FETCH_STATUS = 0
	 BEGIN
	   IF @CODEIMPR != ''
	   BEGIN
	     EXEC dbo.sp_FAC_CalculCodeImpr @SOU_ID, @PROD_ID, @CODEIMPR
	   END

	   FETCH NEXT FROM CUR_2
	   INTO @PROD_ID, @CODEIMPR

	 END 
   END

   CLOSE CUR_2;
   DEALLOCATE CUR_2;
		    			    
END
GO

  