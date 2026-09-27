
------- Procedures communes a Soumissions et factures

-- Dans le cas ou on voudrait changer la facon d"arrondir , on aura qu"'a le changer ici
IF OBJECT_ID(N'dbo.fn_CastAE', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.fn_CastAE ;
GO

  
CREATE FUNCTION dbo.fn_CastAE (@Input DECIMAL(18,6), @Precision INT)
RETURNS DECIMAL(18,6)
AS
BEGIN

  DECLARE @Output DECIMAL(18,6)
  Select @Output = ROUND(@Input, @Precision);
  Return @Output

END;
GO


IF OBJECT_ID(N'dbo.fn_MultBlock', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.fn_MultBlock ;
GO

CREATE FUNCTION [dbo].[fn_MultBlock](@SOU_ID VARCHAR(20), @BLO_ID_REL INT)
RETURNS float
AS BEGIN
   DECLARE @RES  FLOAT

   SELECT @RES = B.MULT
   FROM SOUBLO B
   WHERE B.BLO_ID = @BLO_ID_REL
     AND B.SOU_ID = @SOU_ID
   
   if @RES is null set @RES = 1;
   
   RETURN @RES;

END
GO

IF OBJECT_ID(N'dbo.fn_STR_Alphaorder', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.fn_STR_Alphaorder ;
GO

CREATE FUNCTION [dbo].[fn_STR_Alphaorder](@str VARCHAR(50))
returns VARCHAR(50)
BEGIN
    DECLARE @len    INT,
            @cnt    INT,
            @str1   VARCHAR(50),
            @output VARCHAR(50)
    set @cnt    = 1
    set @str1   =''
    set @output =''

    SELECT @len = Len(@str)
    IF @len > 0 
    BEGIN
        WHILE @cnt <= @len
        BEGIN
            SELECT @str1 = @str1 + Substring(@str, @cnt, 1) + ','

            SET @cnt = @cnt + 1
        END

        SELECT @str1 = LEFT(@str1, Len(@str1) - 1)

        SELECT @output = @output + Sp_data
        FROM  (SELECT Split.a.value('.', 'VARCHAR(100)') Sp_data
                FROM   (SELECT Cast ('<M>' + Replace(@str1, ',', '</M><M>') + '</M>' AS XML) AS Data) AS A
                    CROSS APPLY Data.nodes ('/M') AS Split(a)) A
        ORDER  BY Sp_data

    END;

    RETURN @output
END
GO

------- Procedures pour Soumissions

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'sp_SOU_UpdateQteTotalOth_v2')
  DROP PROCEDURE sp_SOU_UpdateQteTotalOth_v2
GO


CREATE PROCEDURE [dbo].[sp_SOU_UpdateQteTotalOth_v2] (@SOU_ID VARCHAR(20), @REPLACE_FILTER INT, @UID VARCHAR(14), @DoLog BIT, @SOUPROLOG VARCHAR(20))
AS BEGIN   
  DECLARE @CODEIMPR       VARCHAR(36)
  DECLARE @PROD_ID        VARCHAR(20)
  DECLARE @QTE_NEW        FLOAT

  DECLARE @SqlTable       VARCHAR(100)
  DECLARE @Sql1           NVARCHAR(1000)
  -----------------------------------

  DECLARE CUR_1 CURSOR FOR 
 	
  SELECT BB.PRO_ID, BB.New_QTE -- , SPP.QTEOTH 
    FROM SOUPRO SPP LEFT JOIN 
         (   
		   SELECT SP.PRO_ID  AS PRO_ID ,  
			  SUM( SR2.QTE_cmp * DBO.fn_UM_GetRatioDeConversion(SR2.QTEUM_cmp, DBO.fn_UM_GetUniteDeBase(SP.COUUM), SP.QPP)) AS New_QTE
   
		   FROM SOUPRO SP,  (	
	                        SELECT 
								   SR.ITEM_ID as ITEM_ID_cmp, 
								   SR.BLO_ID  as BLO_ID_cmp, 
								   SR.QTEUM   as QTEUM_cmp,  
								   SUM(SR.QTE * dbo.fn_MultBlock(SR.SOU_ID, SR.BLO_ID) ) as QTE_cmp
							FROM SOUREL SR
							WHERE SR.SOU_ID = @SOU_ID
							and ((SR.TYPEITEM = 'P') OR (SR.TYPEITEM = 'N'))
							GROUP BY SR.BLO_ID, SR.ITEM_ID , SR.QTEUM 

						   ) AS SR2
   		     
		   WHERE SP.PRO_ID = SR2.ITEM_ID_cmp
			 AND SP.SOU_ID  = @SOU_ID
		   GROUP BY SP.PRO_ID

         ) AS BB
    ON SPP.PRO_ID = BB.PRO_ID
    WHERE SPP.SOU_ID  = @SOU_ID
	AND ((@DoLog=1) OR 
	     ((((BB.New_QTE IS NOT NULL) AND (CAST(SPP.QTEOTH AS NUMERIC(18,2)) != CAST(BB.New_QTE AS NUMERIC(18,2)))) OR
           ((BB.New_QTE IS NULL)     AND (SPP.QTEOTH  != 0)))));

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
	    SET @sql1 =  'UPDATE ' + @SqlTable +'  SET QTEOTH = ' + STR( @QTE_NEW, 18, 5) + ' , CALCTIMSTP = ' + '''' + @UID + '''' +  ' WHERE SOU_ID = ' + '''' + @SOU_ID + '''' +  ' AND PRO_ID = ' + '''' + @PROD_ID + '''';
	  END ELSE 
	  BEGIN
        SET @sql1 =  'UPDATE ' + @SqlTable +'  SET QTEOTH = 0                             , CALCTIMSTP = ' + '''' + @UID + '''' +  ' WHERE SOU_ID = ' + '''' + @SOU_ID + '''' +  ' AND PRO_ID = ' + '''' + @PROD_ID + '''';
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
	
	 SELECT DISTINCT S.ITEM_ID , S.CODEIMPR
	 FROM SOUREL S
	 WHERE S.SOU_ID = @SOU_ID
	   AND ((S.TYPEITEM = 'P') OR (S.TYPEITEM = 'N'))
	   AND S.CODEIMPR != '';

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
											THEN CMP1.QTE_ENSCO * SR.QTE * DBO.fn_UM_GetRatioDeConversion  (SR.QTEUM, CMP1.COUUM,  0)
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

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'sp_SOU_UpdateQteTotalLots_v2')
  DROP PROCEDURE sp_SOU_UpdateQteTotalLots_v2
GO

CREATE PROCEDURE [dbo].[sp_SOU_UpdateQteTotalLots_v2] (@SOU_ID VARCHAR(20), @REPLACE_FILTER INT, @UID VARCHAR(14), @DoLog BIT, @SOUPROLOG VARCHAR(20))
AS BEGIN
   
  DECLARE @CODEIMPR       VARCHAR(36)
  DECLARE @PROD_ID        VARCHAR(20)
  DECLARE @QTE_NEW        FLOAT

  DECLARE @SqlTable       VARCHAR(100)
  DECLARE @Sql1           NVARCHAR(1000)
  -----------------------------------

  DECLARE CUR_1 CURSOR FOR 

    SELECT BB.PRO_ID, BB.New_QTE  -- , SPP.QTELOTS  --, BB.New_QTE - SPP.QTELOTS 
    FROM SOUPRO SPP LEFT JOIN 
         ( SELECT SP.PRO_ID  AS PRO_ID ,  
			     SUM(SR2.QTE_cmp * DBO.fn_UM_GetRatioDeConversion(SR2.QTEUM_cmp, DBO.fn_UM_GetUniteDeBase(SP.COUUM), SP.QPP)) AS New_QTE
  		     FROM SOUPRO SP, (
							  SELECT 
								CMP1.PRO_ID as ITEM_ID_cmp, 
								SR.BLO_ID   as BLO_ID_cmp, 									  
								CMP1.QTEUM  as QTEUM_cmp, 
								SUM((CMP1.QTE * SR.QTE * DBO.fn_UM_GetRatioDeConversion(SR.QTEUM, CMP1.COUUM, 0)) * dbo.fn_MultBlock(SR.SOU_ID, SR.BLO_ID) ) as QTE_cmp
						      FROM SOUREL SR ,
								( SELECT L.COUUM,
								         L.LOTS_ID,
								         C.QTEUM, 								     
										 C.QTE, 
										 C.PRO_ID

										FROM SOULOTS L, SOULOTSCO C
										WHERE L.SOU_ID = C.SOU_ID
										AND   L.LOTS_ID = C.LOTS_ID
										AND   L.SOU_ID = @SOU_ID
								 ) AS CMP1

						      WHERE SR.SOU_ID     = @SOU_ID	
							    AND SR.TYPEITEM = 'L'
							    AND SR.ITEM_ID  = CMP1.LOTS_ID
						      GROUP BY SR.BLO_ID, CMP1.PRO_ID , CMP1.QTEUM
							  
							  ) AS SR2
   		     
  		     WHERE SP.PRO_ID = SR2.ITEM_ID_cmp
					 AND SP.SOU_ID  = @SOU_ID	
  		     GROUP BY SP.PRO_ID
         ) AS BB

    ON SPP.PRO_ID = BB.PRO_ID
    WHERE SPP.SOU_ID  = @SOU_ID	
	AND ((@DoLog=1) OR 
	     ((((BB.New_QTE IS NOT NULL) AND (CAST(SPP.QTELOT AS NUMERIC(18,2)) != CAST(BB.New_QTE AS NUMERIC(18,2)))) OR
           ((BB.New_QTE IS NULL)     AND (SPP.QTELOT  != 0)))));

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
	    SET @sql1 =  'UPDATE ' + @SqlTable +'  SET QTELOT = ' + STR( @QTE_NEW, 18, 5) + ' , CALCTIMSTP = ' + '''' + @UID + '''' +  ' WHERE SOU_ID = ' + '''' + @SOU_ID + '''' +  ' AND PRO_ID = ' + '''' + @PROD_ID + '''';
	  END ELSE 
	  BEGIN
        SET @sql1 =  'UPDATE ' + @SqlTable +'  SET QTELOT = 0                             , CALCTIMSTP = ' + '''' + @UID + '''' +  ' WHERE SOU_ID = ' + '''' + @SOU_ID + '''' +  ' AND PRO_ID = ' + '''' + @PROD_ID + '''';
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
	
	 SELECT DISTINCT SLC.PRO_ID , SR.CODEIMPR
     FROM SOUREL SR, SOULOTS SL, SOULOTSCO SLC
     WHERE SR.SOU_ID   =  @SOU_ID
       AND SR.TYPEITEM = 'L'
	   AND SR.SOU_ID   = SL.SOU_ID
	   AND SR.ITEM_ID  = SL.LOTS_ID
	   AND SL.SOU_ID   = SLC.SOU_ID
	   AND SL.LOTS_ID  = SLC.LOTS_ID  
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

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'sp_SOUPRO_Quantity_V2')
  DROP PROCEDURE sp_SOUPRO_Quantity_V2
GO


CREATE PROCEDURE [dbo].[sp_SOUPRO_Quantity_V2] (@SOU_ID VARCHAR(20), @REPLACE_FILTER INT, @DoLog BIT, @SOUPROLOG VARCHAR(20))
AS BEGIN
 
  ----------------------------------
   -- Normalement cette procedure est appelée uniquement pour :  (TYPERELEVE = 'P') 
   ----------------------------------

   DECLARE @UID  VARCHAR(14)

   SELECT @UID = DBO.fn_DateTime_GetTimeStampStr()

   ----------------------------------
   ---- Pour les codes d'impression : 0 Pour Ne pas traiter , 1 Pour Ajouter, 2 pour remplacer
   ----------------------------------

   IF @REPLACE_FILTER = 2 
   BEGIN
     UPDATE   SOUPRO
        SET CODEIMPR = ''
      WHERE SOU_ID   = @SOU_ID
   END 
   -----------------------------------
   -- le meme @UID est partagé entre SOUMIS est les produits correspondants recalculés (en dernier) dans SOUPRO
   -----------------------------------
   UPDATE SOUMIS 
      SET CALCTIMSTP = @UID
    WHERE SOU_ID     = @SOU_ID 
   -----------------------------------
   --  Traitement 
   -----------------------------------

    EXEC dbo.sp_SOU_UpdateQteTotalOth_v2  @SOU_ID, @REPLACE_FILTER, @UID, @DoLog, @SOUPROLOG;
    EXEC dbo.sp_SOU_UpdateQteTotalEns_v2  @SOU_ID, @REPLACE_FILTER, @UID, @DoLog, @SOUPROLOG;
    EXEC dbo.sp_SOU_UpdateQteTotalLots_v2 @SOU_ID, @REPLACE_FILTER, @UID, @DoLog, @SOUPROLOG;

   -----------------------------------
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'sp_SOU_CalculTotaux')
  DROP PROCEDURE sp_SOU_CalculTotaux
GO

CREATE PROCEDURE [dbo].[sp_SOU_CalculTotaux] (@SOU_ID                           VARCHAR(20),                                              
                                              @TypeReleve                       VARCHAR(1),
                                              @EE_CALGARY                       bit, 
								              @ModeCalcul                       VARCHAR(1),
								              @VendantUAvantVendantT            bit,
											  @VPM                              int,								            
								              @DoLog                            bit)
AS 
BEGIN
  DECLARE @fCout                      DECIMAL(18,6)
  DECLARE @fCoutantTotal              DECIMAL(18,6)
  DECLARE @fCoutPortionTVP            DECIMAL(18,6)
  DECLARE @fCoutantTotalPortionTVP    DECIMAL(18,6)
  DECLARE @CoutantNetReel             DECIMAL(18,6)
  DECLARE @CoutantNetSpecial          DECIMAL(18,6)
  DECLARE @CoutantUnitaire            DECIMAL(18,7) -- 7 decimal car n'est jamais arrondi
  DECLARE @CoutantTotal               DECIMAL(18,6)
  DECLARE @CoutantNetSection          DECIMAL(18,6)
  DECLARE @fVendant                   DECIMAL(18,6)
  DECLARE @fVendantTotal              DECIMAL(18,6)
  DECLARE @TempsInstallationSection   DECIMAL(18,6)
  DECLARE @TempsInstallationTotal     DECIMAL(18,6)
  DECLARE @TempsInstallationUnitaire  DECIMAL(18,6)
  DECLARE @VendantUnitaire            DECIMAL(18,6)
  DECLARE @VendantTotal               DECIMAL(18,6)
  DECLARE @VendantTotalIncluantTVP    DECIMAL(18,6)
  DECLARE @VendantUnitaireIncluantTVP DECIMAL(18,6)
  DECLARE @LandedCost                 DECIMAL(18,6)
  DECLARE @DivisibleEnSections        int
  ---------------------------------------------
  DECLARE @ITEM_ID                    VARCHAR(20)
  DECLARE @BLO_ID                     VARCHAR(3)
  DECLARE @DIV_ID                     VARCHAR(3)
  DECLARE @MULT_BLOC                  INT
  DECLARE @LaborFactor                INT
  DECLARE @TypeItem                   VARCHAR(1)
  DECLARE @QTE                        DECIMAL(18,6)
  DECLARE @QTEUM                      VARCHAR(2)
  DECLARE @COUUM                      VARCHAR(2)  
  DECLARE @COUBRUTUNI                 DECIMAL(18,6)
  DECLARE @COUESC                     DECIMAL(18,6)
  DECLARE @QPP                        INT
  DECLARE @TempsUM                    VARCHAR(2)
  DECLARE @COUTANBRUT                 DECIMAL(18,6)
  DECLARE @SECTION                    DECIMAL(18,6)
  DECLARE @TYPRATIO                   VARCHAR(1)
  DECLARE @PROFIT                     DECIMAL(18,6)
  DECLARE @fLaborTotal                DECIMAL(18,6)
  ---------------------------------------------

  -- POUR LES TAXES TPGSX
  DECLARE @TAX_ID                     VARCHAR(20)
  DECLARE @TYPETAXE                   VARCHAR(1)
  DECLARE @TaxeProv                   DECIMAL(18,6)
  DECLARE @INDEXTAX                   INT
  DECLARE @TVPSurCoutPermise          bit
  DECLARE @MontantTax1                DECIMAL(18,6)
  DECLARE @MontantTax2                DECIMAL(18,6)
  DECLARE @MontantTax3                DECIMAL(18,6)
  DECLARE @MontantTax4                DECIMAL(18,6)
  DECLARE @MontantTax5                DECIMAL(18,6)
  
  	   ---------------------------------------------
       --- Pour produir un log si @DoLog = 1
	   ---------------------------------------------

  DECLARE @log table 
   ( 
   ITEM_ID                    varchar(20), 
   BLO_ID                     VARCHAR(3),
   DIV_ID                     VARCHAR(3),
   TypeItem                   VARCHAR(1),
   QTE                        DECIMAL(18,6),      
   QTEUM                      VARCHAR(2),
   COUTANBRUT                 DECIMAL(18,6), 
   SECTION                    DECIMAL(18,6),        
   PROFIT                     DECIMAL(18,6),
   TYPETAXE                   VARCHAR(1),
   MULT_BLOC                  int,       
   fCout                      DECIMAL(18,6),
   fCoutPortionTVP            DECIMAL(18,6),
   fVendant                   DECIMAL(18,6),
   fCoutantTotal              DECIMAL(18,6),
   fCoutantTotalPortionTVP    DECIMAL(18,6),
   fVendantTotal              DECIMAL(18,6),
   fLaborTotal                DECIMAL(18,6),
   CoutantNetReel             DECIMAL(18,6), 
   CoutantNetSection          DECIMAL(18,6),
   TempsUnitaireApprox        DECIMAL(18,6), 
   LandedCost                 DECIMAL(18,6),
   CoutantUnitaire            DECIMAL(18,6),
   CoutantTotal               DECIMAL(18,6),
   VendantUnitaire            DECIMAL(18,6),
   VendantTotal               DECIMAL(18,6),
   TaxeProv                   DECIMAL(18,6),
   VendantUnitaireIncluantTVP DECIMAL(18,6),
   VendantTotalIncluantTVP    DECIMAL(18,6),
   TempsInstallationSection   DECIMAL(18,6),
   TempsInstallationTotal     DECIMAL(18,6)
   )
       
	   ---------------------------------------------
       -- On remplace la table Soupro par #SOUPRO_TEMP pour inclure la colonne LC dans le cas de @EE_CALGARY = 0
	   ---------------------------------------------

  IF OBJECT_ID('tempdb..#SOUPRO_TEMP') IS NOT NULL 
  begin 
    DROP TABLE #SOUPRO_TEMP
  end

  select sp.* into #SOUPRO_TEMP from SOUPRO sp
   where sp.SOU_ID = @SOU_ID

  if @EE_CALGARY = 0 
  begin
    ALTER TABLE #SOUPRO_TEMP ADD LC FLOAT
  end

	   ---------------------------------------------
	   --- Initialiser les resultats finaux
	   ---------------------------------------------
  
  SET @fCoutantTotal           = 0.0  
  SET @fCoutantTotalPortionTVP = 0.0
  SET @fVendantTotal           = 0.0
  SET @fLaborTotal             = 0.0	

  -- Les tax

  SET @MontantTax1             = 0.0  
  SET @MontantTax2             = 0.0  
  SET @MontantTax3             = 0.0  
  SET @MontantTax4             = 0.0  
  SET @MontantTax5             = 0.0  

	   ---------------------------------------------
	   --- Recuperer le numero de tax
	   ---------------------------------------------    

  SELECT @TAX_ID = s.TAX_ID from SOUMIS s WHERE SOU_ID = @SOU_ID

	   ---------------------------------------------
	   --- Debut des Calcules
	   ---------------------------------------------   

  DECLARE CUR_1 CURSOR FOR   
  SELECT  SR.ITEM_ID, SR.BLO_ID, SR.DIV_ID, SR.TYPEITEM,  
          ISNULL(SR.QTE,0.0), SR.QTEUM, ISNULL(SR.COUTANBRUT,0.0) , ISNULL(SR.SECTION,0.0) , ISNULL(SR.PROFIT,0.0), SR.TYPETAXE          
    FROM  SOUREL SR 
    WHERE SR.SOU_ID = @SOU_ID
	  AND SR.TYPERELEVE = @TypeReleve
	
	ORDER BY SOU_ID, TYPERELEVE, BLO_ID, DIV_ID, ORDRE

  OPEN CUR_1
  FETCH NEXT FROM CUR_1
  INTO @ITEM_ID, @BLO_ID, @DIV_ID, @TypeItem, @QTE, @QTEUM, @COUTANBRUT, @SECTION, @PROFIT, @TYPETAXE

  WHILE @@FETCH_STATUS = 0
  BEGIN
		SET @fCout                    = 0.0
		SET @fCoutPortionTVP          = 0.0
		SET @fVendant                 = 0.0 		
		SET @DivisibleEnSections      = 0
		SET @TempsInstallationSection = 0.0
		SET @TempsInstallationTotal   = 0.0


		SELECT @MULT_BLOC = SB.MULT  FROM SOUBLO SB
		 WHERE SB.SOU_ID = @SOU_ID
		   AND SB.BLO_ID = @BLO_ID

		IF @MULT_BLOC IS NULL SET @MULT_BLOC = 1; 


		SELECT @LaborFactor = SA.FACTMD  FROM SOUAMD SA
		 WHERE SA.SOU_ID = @SOU_ID
		   AND SA.BLO_ID = @BLO_ID
		   AND SA.DIV_ID = @DIV_ID

		IF @LaborFactor IS NULL SET @LaborFactor = 1.0; 


	    -----------------------------------------------------------------------------------------
		IF (@TypeReleve = 'P') AND ((@TypeItem = 'P') OR (@TypeItem = 'N'))
		BEGIN

			SELECT @CoutantNetSpecial         = SP.PROMCOUNET, 
			       @COUBRUTUNI                = ISNULL(SP.COUBRUTUNI, 0.0), 
				   @COUESC                    = ISNULL(SP.COUESC, 0.0), 
				   @QPP                       = ISNULL(SP.QPP, 0.0),
				   @COUUM                     = SP.COUUM COLLATE DATABASE_DEFAULT , 
				   @LandedCost                = ISNULL(SP.LC, 0.0),
			       @TempsInstallationUnitaire = ISNULL(SP.TEMPUNI, 0.0),
				   @TempsUM                   = SP.TEMPUM COLLATE DATABASE_DEFAULT 
			  FROM #SOUPRO_TEMP SP
			 WHERE SP.SOU_ID = @SOU_ID COLLATE DATABASE_DEFAULT 
			   AND SP.PRO_ID = @ITEM_ID COLLATE DATABASE_DEFAULT 

			IF @CoutantNetSpecial > 0 
			  SET @CoutantNetReel = @CoutantNetSpecial
			ELSE 
	  		  SET @CoutantNetReel = @COUBRUTUNI - (@COUBRUTUNI * (@COUESC / 100.0)); 


			SET @TempsInstallationTotal = @QTE *  @TempsInstallationUnitaire * DBO.fn_UM_GetRatioDeConversion (@QTEUM, @TempsUM, @QPP);
		          
	    END ELSE 

	    -----------------------------------------------------------------------------------------
		IF (@TypeReleve = 'P') AND (@TypeItem = 'A') 
		BEGIN

			WITH ComposanteEnsemble(QTE_cmp, CoutantNetReel_cmp, CoutantNetSection_cmp, QTEUM_cmp, COUUM_cmp, QPP_cmp, TEMPUM_cmp, LANDEDCOST_cmp, DivisibleSection_cmp) AS

	   	   (SELECT   CASE WHEN (SEC.TYPRATIO = 'L') AND (SE.COUUM != '' ) AND ([dbo].[fn_UM_GetNatureUnite](SE.COUUM) = 'L') 
					   THEN CASE 
							  WHEN (ISNULL(SEC.DIV,0.0) != 0) 
								THEN (ISNULL(SEC.QTE,0.0) / SEC.DIV) * DBO.fn_UM_GetRatioDeConversion (SE.COUUM , SEC.DIVUM,  0)
							  ELSE 0 
							END
					   ELSE SEC.QTE
					 END AS QTE_cmp					 
					 	
					, CASE WHEN (SEC.TYPRATIO = 'L') 
					    THEN CASE WHEN ISNULL(SP.PROMCOUNET,0.0) > 0 
						       THEN  SP.PROMCOUNET
							   ELSE  ISNULL(SP.COUBRUTUNI,0.0) - (ISNULL(SP.COUBRUTUNI,0.0) * (ISNULL(SP.COUESC,0.0) / 100.0)) 	
							 END				 
					   ELSE 0
					  END AS CoutantNetReel_cmp

				    , CASE WHEN (SEC.TYPRATIO = 'L') 
					    THEN 0
					    ELSE CASE WHEN ISNULL(SP.PROMCOUNET,0.0) > 0 
						       THEN  SP.PROMCOUNET
							   ELSE  ISNULL(SP.COUBRUTUNI,0.0) - (ISNULL(SP.COUBRUTUNI,0.0) * (ISNULL(SP.COUESC,0.0) / 100.0)) 	
							 END				 
					  END AS CoutantNetSection_cmp

					, SEC.QTEUM         as QTEUM_cmp
					, SP.COUUM COLLATE DATABASE_DEFAULT         as COUUM_cmp 
					, ISNULL(SP.QPP,0.0)  as QPP_cmp
					, SP.TEMPUM COLLATE DATABASE_DEFAULT        as TEMPUM_cmp

					, CASE WHEN @EE_CALGARY = 1
					    THEN ISNULL(SP.LC,0.0) 
						ELSE 0 
				      END AS LANDEDCOST_cmp

					, CASE WHEN (SEC.TYPRATIO = 'L')
					    THEN 0
					    ELSE 1
					  END AS DivisibleSection_cmp
								 
			  FROM SOUENS SE, SOUENSCO SEC, #SOUPRO_TEMP  sp
			  WHERE SE.SOU_ID  = SEC.SOU_ID
			    AND SE.ENS_ID  = SEC.ENS_ID
			    AND SEC.PRO_ID = SP.PRO_ID COLLATE DATABASE_DEFAULT
			    AND SEC.SOU_ID = @SOU_ID
			    and SE.ENS_ID  = @ITEM_ID
	       )  
		   select  @CoutantNetReel      = ISNULL(SUM(dbo.fn_CastAE(QTE_cmp * CoutantNetReel_cmp * DBO.fn_UM_GetRatioDeConversion(QTEUM_cmp, COUUM_cmp,  QPP_cmp) , 2)),0.0),		
                   @CoutantNetSection   = ISNULL(SUM(QTE_cmp * CoutantNetSection_cmp    * DBO.fn_UM_GetRatioDeConversion(QTEUM_cmp, COUUM_cmp,  QPP_cmp)),0.0),		           
                   @LandedCost          = ISNULL(SUM(QTE_cmp * LANDEDCOST_cmp           * DBO.fn_UM_GetRatioDeConversion(QTEUM_cmp, TEMPUM_cmp, QPP_cmp)),0.0),
				   @DivisibleEnSections = ISNULL(SUM(DivisibleSection_cmp),0.0)   
		   from ComposanteEnsemble
	       
		   SET @QPP = 0;	   

		   select @COUUM = SE.COUUM , 
		          @TempsInstallationSection  = SE.TEMPSEC, 
				  @TempsInstallationTotal    = @QTE *  SE.TEMPUNI * DBO.fn_UM_GetRatioDeConversion (@QTEUM, SE.TEMPUM, @QPP) 
		     from SOUENS  SE
 		    where SE.SOU_ID = @SOU_ID
		      and SE.ENS_ID = @ITEM_ID

            -- 
			IF  (@DivisibleEnSections > 0)
			  SET @TempsInstallationTotal = @TempsInstallationTotal + (@TempsInstallationSection * @SECTION);

		END  ELSE-- Fin @TypeItem = 'A'

	    -----------------------------------------------------------------------------------------
        IF (@TypeReleve = 'P') AND (@TypeItem = 'L') 
		BEGIN
		   WITH ComposanteLot(CoutantNetReel_cmp, QTE_cmp, QTEUM_cmp, COUUM_cmp, QPP_cmp, TEMPUM_cmp, LANDEDCOST_cmp) AS

	   	   (SELECT   
		    	     CASE WHEN ISNULL(SP.PROMCOUNET,0.0) > 0 
				        THEN  SP.PROMCOUNET
					    ELSE  ISNULL(SP.COUBRUTUNI,0.0) - (ISNULL(SP.COUBRUTUNI,0.0) * (ISNULL(SP.COUESC,0.0) / 100.0)) 							 
					  END AS CoutantNetReel_cmp
		   
		            , ISNULL(SLC.QTE,0.0) as QTE_cmp					 					 	
					, SLC.QTEUM           as QTEUM_cmp
					, SP.COUUM COLLATE DATABASE_DEFAULT           as COUUM_cmp
					, ISNULL(SP.QPP,0.0)  as QPP_cmp
					, SP.TEMPUM COLLATE DATABASE_DEFAULT          as TEMPUM_cmp

					, CASE WHEN @EE_CALGARY = 1
					    THEN ISNULL(SP.LC,0.0) 
						ELSE 0 
				      END AS LANDEDCOST_cmp
								 
			  FROM SOULOTS SL, SOULOTSCO SLC, #SOUPRO_TEMP sp
			  WHERE SL.SOU_ID  = SLC.SOU_ID
			    AND SL.LOTS_ID = SLC.LOTS_ID
			    AND SLC.PRO_ID = SP.PRO_ID COLLATE DATABASE_DEFAULT
			    AND SLC.SOU_ID = @SOU_ID
			    and SL.LOTS_ID = @ITEM_ID
	       )  
		   select  @CoutantNetReel = ISNULL(SUM(dbo.fn_CastAE(QTE_cmp * CoutantNetReel_cmp * DBO.fn_UM_GetRatioDeConversion(QTEUM_cmp, COUUM_cmp,  QPP_cmp) , 2)),0.0),				           
                   @LandedCost     = ISNULL(SUM(QTE_cmp * LANDEDCOST_cmp        * DBO.fn_UM_GetRatioDeConversion (QTEUM_cmp, TEMPUM_cmp, QPP_cmp)),0.0)			   
		   from ComposanteLot
	   
		   SET @QPP = 0.0;	   

		   select   @COUUM = SL.COUUM  		          
				  , @TempsInstallationTotal  = @QTE *  SL.TEMPUNI * DBO.fn_UM_GetRatioDeConversion (@QTEUM, SL.TEMPUM, @QPP) 
				  , @CoutantNetReel = 
				    CASE 
					  WHEN SL.COUTANTSEL = 1 THEN SL.COUTANT1
					  WHEN SL.COUTANTSEL = 2 THEN SL.COUTANT2
					  WHEN SL.COUTANTSEL = 3 THEN SL.COUTANT3
					  WHEN SL.COUTANTSEL = 4 THEN SL.COUTANT3
					  --ELSE @CoutantNetReel
					END

		     from SOULOTS SL
 		    where SL.SOU_ID  = @SOU_ID
		      and SL.LOTS_ID = @ITEM_ID

		END  -- Fin @TypeItem = 'L'
	

       IF (@TypeItem != 'T')
	   BEGIN 

	   ---------------------------------------------
	   --- Calculer le CoutantTotal / CoutantUnitaire
	   ---------------------------------------------

	       SET @CoutantUnitaire   = 0.0;
		   SET @CoutantTotal      = 0.0;

		   IF ((@TypeReleve = 'S') AND (@TypeItem = 'S')) OR  ((@TypeReleve = 'O') AND (@TypeItem = 'O'))
		   BEGIN

			   SET @CoutantUnitaire = @COUTANBRUT;		  

		   END ELSE
           BEGIN
			   IF @EE_CALGARY = 1 
			   BEGIN
				 SET @CoutantUnitaire = @LandedCost     * DBO.fn_UM_GetRatioDeConversion (@QTEUM, @COUUM,  @QPP)
			   END ELSE 
			   BEGIN
				 SET @CoutantUnitaire = @CoutantNetReel * DBO.fn_UM_GetRatioDeConversion (@QTEUM, @COUUM,  @QPP);
			   END
		   END
 			
		   SET @CoutantTotal   = dbo.fn_CastAE(@QTE * @CoutantUnitaire , 2);

		   if ((@TypeReleve = 'P') AND (@TypeItem = 'A')) and (@DivisibleEnSections > 0)
		     SET @CoutantTotal = dbo.fn_CastAE(@CoutantTotal  + (@SECTION * @CoutantNetSection) , 2)


	   ---------------------------------------------
	    --- Calculer le VendantUnitaire /  VendantTotal
	   ---------------------------------------------

		   SET @VendantUnitaire = 0.0;
		   SET @VendantTotal    = 0.0;
		   
		   IF (@DivisibleEnSections = 0) and
		     ((@VendantUAvantVendantT = 1) or (@QTE = 0)) 
		   BEGIN
		   		   		
		     SELECT @VendantUnitaire = 
		          CASE WHEN (@ModeCalcul = 'C')
		                 THEN  dbo.fn_CastAE(@CoutantUnitaire * (1.0 + (@PROFIT / 100.0)), @VPM)
				       WHEN (@ModeCalcul = 'G') AND (@PROFIT < 100)
					     THEN  dbo.fn_CastAE(@CoutantUnitaire / (1.0 - (@PROFIT / 100.0)), @VPM)
					   ELSE 0
		          END
				  		 
			 SET @VendantTotal    =  dbo.fn_CastAE(@QTE * @VendantUnitaire , 2);

		   END ELSE
		   BEGIN

		     SELECT @VendantTotal  = 
		          CASE WHEN (@ModeCalcul = 'C')
		                 THEN dbo.fn_CastAE(@CoutantTotal * (1.0 + (@PROFIT / 100.0)) , 2)
				       WHEN (@ModeCalcul = 'G') AND (@PROFIT < 100)
					     THEN dbo.fn_CastAE(@CoutantTotal / (1.0 - (@PROFIT / 100.0)) , 2)
					   ELSE 0
		          END

			 SET @VendantUnitaire = dbo.fn_CastAE(@VendantTotal / @QTE , 2);
		   END;     

	   ---------------------------------------------
	   --- Calculer la TaxProv
	   ---------------------------------------------
	      
	      with TaxeProvincial(CODETAX, TAUXPRV, INDEXTAX) as
			(select [CODETAX1], [TAUXPRV1], 1  FROM [TAXDEF] where TAX_ID = @TAX_ID  UNION
			 select [CODETAX2], [TAUXPRV2], 2  FROM [TAXDEF] where TAX_ID = @TAX_ID  UNION
			 select [CODETAX3], [TAUXPRV3], 3  FROM [TAXDEF] where TAX_ID = @TAX_ID  UNION
			 select [CODETAX4], [TAUXPRV4], 4  FROM [TAXDEF] where TAX_ID = @TAX_ID  UNION
			 select [CODETAX5], [TAUXPRV5], 5  FROM [TAXDEF] where TAX_ID = @TAX_ID
			) 
			select @TaxeProv = S.TAUXPRV,
			       @INDEXTAX = S.INDEXTAX
			from TaxeProvincial S where S.CODETAX = @TYPETAXE; 

		if @TaxeProv is null SET @TaxeProv = 0.0;

		SELECT @TVPSurCoutPermise = TVPSURCPER FROM [TAXDEF] S  WHERE S.TAX_ID = @TAX_ID 

	   ---------------------------------------------
	   --- Calculer le VendantTotalIncluantTVP / VendantUnitaireIncluantTVP
	   ---------------------------------------------
	       
		SET @VendantUnitaireIncluantTVP = 0.0;
		SET @VendantTotalIncluantTVP    = 0.0;

	    IF (@TVPSurCoutPermise = 1) 
		BEGIN
			IF  (@TypeReleve = 'P') AND (@TypeItem = 'A') AND (@DivisibleEnSections > 0)  
			BEGIN
			  SET @VendantUnitaireIncluantTVP    = 0;
			  SET @VendantTotalIncluantTVP       = dbo.fn_CastAE(@VendantTotal +  (@CoutantTotal *  (@TaxeProv / 100.0)) , 2);   
			END ELSE 
			BEGIN
			  IF (@VendantUAvantVendantT = 1 ) OR (@QTE = 0)
			  BEGIN
 				SET @VendantUnitaireIncluantTVP = dbo.fn_CastAE(@VendantUnitaire +  (@CoutantUnitaire *  (@TaxeProv / 100.0)), @VPM);
				SET @VendantTotalIncluantTVP    = dbo.fn_CastAE(@QTE * @VendantUnitaireIncluantTVP , 2);   
			  END ELSE
			  BEGIN
				SET @VendantTotalIncluantTVP    = dbo.fn_CastAE(@VendantTotal +  (@CoutantTotal *  (@TaxeProv / 100.0)) , 2);   
				SET @VendantUnitaireIncluantTVP = dbo.fn_CastAE(@VendantTotalIncluantTVP / @QTE , @VPM);
			  END
			END;
		END;

	   ---------------------------------------------
	   --- Calcul des totaux 
	   ---------------------------------------------
	   IF (@TypeReleve = 'P') AND ((@TypeItem = 'P') OR (@TypeItem = 'N') OR (@TypeItem = 'A') OR (@TypeItem = 'L'))
		BEGIN	     
			SET @fCout           =  @CoutantTotal * @MULT_BLOC;
			SET @fCoutPortionTVP = (@VendantTotalIncluantTVP - @VendantTotal) * @MULT_BLOC;
			SET @fVendant        =  @VendantTotal * @MULT_BLOC;
			SET @fLaborTotal     =  @fLaborTotal + (@TempsInstallationTotal * @LaborFactor * @MULT_BLOC);
		END ELSE
		IF (@TypeReleve = 'S') AND (@TypeItem = 'S')
		BEGIN 
            SET @fCout           =  @CoutantTotal;
			SET @fVendant        =  @VendantTotal;
			SET @fLaborTotal     =  @fLaborTotal + @QTE;
		END ELSE
		IF (@TypeReleve = 'O') AND (@TypeItem = 'O')
		BEGIN
            SET @fCout           =  @CoutantTotal;
			SET @fVendant        =  @VendantTotal;
			SET @fCoutPortionTVP = (@VendantTotalIncluantTVP - @VendantTotal);
		END
	   ---------------------------------------------
		SET @fCoutantTotal           = @fCoutantTotal           + @fCout;
		SET @fCoutantTotalPortionTVP = @fCoutantTotalPortionTVP + @fCoutPortionTVP
		SET @fVendantTotal           = @fVendantTotal           + @fVendant
	    

       ---------------------------------------------
	   -- AddMontantTaxable
       ---------------------------------------------

	     IF @INDEXTAX = 1 BEGIN SET @MontantTax1 = @MontantTax1 + @fVendant END ELSE
		 IF @INDEXTAX = 2 BEGIN SET @MontantTax2 = @MontantTax2 + @fVendant END ELSE
		 IF @INDEXTAX = 3 BEGIN SET @MontantTax3 = @MontantTax3 + @fVendant END ELSE
		 IF @INDEXTAX = 4 BEGIN SET @MontantTax4 = @MontantTax4 + @fVendant END ELSE
		 IF @INDEXTAX = 5 BEGIN SET @MontantTax5 = @MontantTax5 + @fVendant END;
	   
	   ---------------------------------------------
	   -- Log
    IF @DoLog = 1
	BEGIN
		insert into @Log  ( ITEM_ID, BLO_ID, DIV_ID, TypeItem, QTE , QTEUM , COUTANBRUT, SECTION , PROFIT  , TYPETAXE, MULT_BLOC, 
							fCout, fCoutPortionTVP, fVendant , fCoutantTotal, fCoutantTotalPortionTVP , fVendantTotal, 
							CoutantNetReel ,  CoutantNetSection,  LandedCost,                
							CoutantUnitaire , CoutantTotal  ,  VendantUnitaire, VendantTotal , fLaborTotal, TaxeProv , VendantUnitaireIncluantTVP, VendantTotalIncluantTVP ,
							TempsInstallationSection , TempsInstallationTotal     
						  ) Values
						  ( @ITEM_ID, @BLO_ID, @DIV_ID, @TypeItem, @QTE , @QTEUM , @COUTANBRUT, @SECTION , @PROFIT  , @TYPETAXE, @MULT_BLOC,
							@fCout  , @fCoutPortionTVP, @fVendant , @fCoutantTotal, @fCoutantTotalPortionTVP , @fVendantTotal, 
							@CoutantNetReel ,  @CoutantNetSection,  @LandedCost,                
							@CoutantUnitaire , @CoutantTotal  ,  @VendantUnitaire, @VendantTotal , @fLaborTotal, @TaxeProv , @VendantUnitaireIncluantTVP, @VendantTotalIncluantTVP ,
							@TempsInstallationSection , @TempsInstallationTotal     
						  );
	END;
	   ---------------------------------------------

	END


	FETCH NEXT FROM CUR_1
	INTO @ITEM_ID, @BLO_ID, @DIV_ID, @TypeItem, @QTE, @QTEUM, @COUTANBRUT, @SECTION, @PROFIT, @TYPETAXE
  END
  CLOSE CUR_1;
  DEALLOCATE CUR_1;


  ------------------------
  -- M.A.J des tax dans soumissions
  ------------------------
  IF @TypeReleve = 'P' 
  BEGIN
   UPDATE SOUMIS 
    SET MATTAXAB1 = @MontantTax1, 
	    MATTAXAB2 = @MontantTax2, 
		MATTAXAB3 = @MontantTax3, 
		MATTAXAB4 = @MontantTax4, 
		MATTAXAB5 = @MontantTax5
   WHERE SOU_ID = @SOU_ID;
  END ELSE
  IF @TypeReleve = 'S' 
  BEGIN
   UPDATE SOUMIS 
    SET SERTAXAB1 = @MontantTax1, 
	    SERTAXAB2 = @MontantTax2, 
		SERTAXAB3 = @MontantTax3, 
		SERTAXAB4 = @MontantTax4, 
		SERTAXAB5 = @MontantTax5
   WHERE SOU_ID = @SOU_ID;
  END ELSE
  IF @TypeReleve = 'O' 
  BEGIN
   UPDATE SOUMIS 
    SET AUTTAXAB1 = @MontantTax1, 
	    AUTTAXAB2 = @MontantTax2, 
		AUTTAXAB3 = @MontantTax3, 
		AUTTAXAB4 = @MontantTax4, 
		AUTTAXAB5 = @MontantTax5
   WHERE SOU_ID = @SOU_ID;
  END; 
  ------------------------
  IF @DoLog = 1
  BEGIN  
	  select * from @Log
  END;

  ------------------------
  -- Retour des resultats
  ------------------------

  SELECT @fCoutantTotal           AS fCoutantTotal, 
	     @fCoutantTotalPortionTVP AS fCoutantTotalPortionTVP, 
	     @fVendantTotal           AS fVendantTotal, 
	     @fLaborTotal             AS fLaborTotal


  END
  GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'sp_SOU_CalculProductUsageInAssemblies_V2')
  DROP PROCEDURE sp_SOU_CalculProductUsageInAssemblies_V2
GO


CREATE PROCEDURE [dbo].[sp_SOU_CalculProductUsageInAssemblies_V2] (@SOU_ID VARCHAR(20), @LANG INT)
AS BEGIN

  DECLARE  @TITLE       VARCHAR(60);
  DECLARE  @DESCR       VARCHAR(2000);  
  DECLARE  @SOUID       VARCHAR(20);
  DECLARE  @PRO_ID      VARCHAR(20);
  DECLARE  @INASSEMBLIE VARCHAR(2000);  

  IF @LANG = 1 
    SET @TITLE = 'Dans les ensembles'
  ELSE
    SET @TITLE = 'In assemblies '

  SET @TITLE =    @TITLE + CHAR(13) + CHAR(10) + REPLICATE('-', LEN(@TITLE))
	DECLARE CUR_1 CURSOR FOR 

  SELECT SP.SOU_ID , SP.PRO_ID, AA.DESCR FROM SOUPRO SP LEFT JOIN  --SP.INASSEMBLIE
	   (SELECT E.SOU_ID, 
			   C.PRO_ID , 
			   DESCR = @TITLE +  CHAR(13) + CHAR(10) + dbo.sp_SOU_GetAssemblyCompositionConcat(E.SOU_ID, C.PRO_ID) 
	    FROM SOUENS E, SOUENSCO C , SOUREL L
	    WHERE E.ENS_ID = C.ENS_ID
		  AND E.SOU_ID = C.SOU_ID
		  AND L.SOU_ID = E.SOU_ID
		  AND L.ITEM_ID = E.ENS_ID
		  AND C.SOU_ID = @SOU_ID
		GROUP BY  E.SOU_ID, C.PRO_ID
		) AA

		ON  SP.SOU_ID = AA.SOU_ID 
		AND SP.PRO_ID = AA.PRO_ID
		WHERE  SP.SOU_ID =  @SOU_ID
		AND (AA.DESCR IS NOT NULL) AND (SP.INASSEMBLIE != AA.DESCR)

  OPEN CUR_1
  FETCH NEXT FROM CUR_1
  INTO @SOUID, @PRO_ID, @DESCR

  WHILE @@FETCH_STATUS = 0
   BEGIN
     UPDATE SOUPRO -- TEMPSOUPRODESCR
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



------- Procedures pour factures


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'sp_FAC_UpdateQteTotalOth_v2')
  DROP PROCEDURE sp_FAC_UpdateQteTotalOth_v2
GO


CREATE PROCEDURE [dbo].[sp_FAC_UpdateQteTotalOth_v2] (@SOU_ID VARCHAR(20), @REPLACE_FILTER INT, @UID VARCHAR(14), @DoLog BIT, @FACPROLOG VARCHAR(20))
AS BEGIN   
  DECLARE @CODEIMPR       VARCHAR(36)
  DECLARE @PROD_ID        VARCHAR(20)
  DECLARE @QTE_NEW        FLOAT

  DECLARE @SqlTable       VARCHAR(100)
  DECLARE @Sql1           NVARCHAR(1000)
  -----------------------------------

  DECLARE CUR_1 CURSOR FOR 
 	
  SELECT BB.PRO_ID, BB.New_QTE -- , SPP.QTEOTH 
    FROM FACPRO SPP LEFT JOIN 
         (   
		   SELECT SP.PRO_ID  AS PRO_ID ,  
			  SUM( SR2.QTE_cmp * DBO.fn_UM_GetRatioDeConversion(SR2.QTEUM_cmp, DBO.fn_UM_GetUniteDeBase(SP.COUUM), SP.QPP)) AS New_QTE
   
		   FROM FACPRO SP,  (	
	                        SELECT 
								   SR.ITEM_ID as ITEM_ID_cmp, 
								   SR.BLO_ID  as BLO_ID_cmp, 
								   SR.QTEUM   as QTEUM_cmp,  
								   SUM(SR.QTE * dbo.fn_MultBlock(SR.SOU_ID, SR.BLO_ID) ) as QTE_cmp
							FROM FACREL SR
							WHERE SR.SOU_ID = @SOU_ID
							and ((SR.TYPEITEM = 'P') OR (SR.TYPEITEM = 'N'))
							GROUP BY SR.BLO_ID, SR.ITEM_ID , SR.QTEUM 

						   ) AS SR2
   		     
		   WHERE SP.PRO_ID = SR2.ITEM_ID_cmp
			 AND SP.SOU_ID  = @SOU_ID
		   GROUP BY SP.PRO_ID

         ) AS BB
    ON SPP.PRO_ID = BB.PRO_ID
    WHERE SPP.SOU_ID  = @SOU_ID
	AND ((@DoLog=1) OR 
	     ((((BB.New_QTE IS NOT NULL) AND (CAST(SPP.QTEOTH AS NUMERIC(18,2)) != CAST(BB.New_QTE AS NUMERIC(18,2)))) OR
           ((BB.New_QTE IS NULL)     AND (SPP.QTEOTH  != 0)))));

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
	    SET @sql1 =  'UPDATE ' + @SqlTable +'  SET QTEOTH = ' + STR( @QTE_NEW, 18, 5) + ' , CALCTIMSTP = ' + '''' + @UID + '''' +  ' WHERE SOU_ID = ' + '''' + @SOU_ID + '''' +  ' AND PRO_ID = ' + '''' + @PROD_ID + '''';
	  END ELSE 
	  BEGIN
        SET @sql1 =  'UPDATE ' + @SqlTable +'  SET QTEOTH = 0                             , CALCTIMSTP = ' + '''' + @UID + '''' +  ' WHERE SOU_ID = ' + '''' + @SOU_ID + '''' +  ' AND PRO_ID = ' + '''' + @PROD_ID + '''';
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
	
	 SELECT DISTINCT S.ITEM_ID , S.CODEIMPR
	 FROM FACREL S
	 WHERE S.SOU_ID = @SOU_ID
	   AND ((S.TYPEITEM = 'P') OR (S.TYPEITEM = 'N'))
	   AND S.CODEIMPR != '';

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
											THEN CMP1.QTE_ENSCO * SR.QTE * DBO.fn_UM_GetRatioDeConversion  (SR.QTEUM, CMP1.COUUM,  0)
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

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'sp_FAC_UpdateQteTotalLots_v2')
  DROP PROCEDURE sp_FAC_UpdateQteTotalLots_v2
GO

CREATE PROCEDURE [dbo].[sp_FAC_UpdateQteTotalLots_v2] (@SOU_ID VARCHAR(20), @REPLACE_FILTER INT, @UID VARCHAR(14), @DoLog BIT, @FACPROLOG VARCHAR(20))
AS BEGIN
   
  DECLARE @CODEIMPR       VARCHAR(36)
  DECLARE @PROD_ID        VARCHAR(20)
  DECLARE @QTE_NEW        FLOAT

  DECLARE @SqlTable       VARCHAR(100)
  DECLARE @Sql1           NVARCHAR(1000)
  -----------------------------------

  DECLARE CUR_1 CURSOR FOR 

    SELECT BB.PRO_ID, BB.New_QTE  -- , SPP.QTELOTS  --, BB.New_QTE - SPP.QTELOTS 
    FROM FACPRO SPP LEFT JOIN 
         ( SELECT SP.PRO_ID  AS PRO_ID ,  
			     SUM(SR2.QTE_cmp * DBO.fn_UM_GetRatioDeConversion(SR2.QTEUM_cmp, DBO.fn_UM_GetUniteDeBase(SP.COUUM), SP.QPP)) AS New_QTE
  		     FROM FACPRO SP, (
							  SELECT 
								CMP1.PRO_ID as ITEM_ID_cmp, 
								SR.BLO_ID   as BLO_ID_cmp, 									  
								CMP1.QTEUM  as QTEUM_cmp, 
								SUM((CMP1.QTE * SR.QTE * DBO.fn_UM_GetRatioDeConversion(SR.QTEUM, CMP1.COUUM, 0)) * dbo.fn_MultBlock(SR.SOU_ID, SR.BLO_ID) ) as QTE_cmp
						      FROM FACREL SR ,
								( SELECT L.COUUM,
								         L.LOTS_ID,
								         C.QTEUM, 								     
										 C.QTE, 
										 C.PRO_ID

										FROM FACLOTS L, FACLOTSCO C
										WHERE L.SOU_ID = C.SOU_ID
										AND   L.LOTS_ID = C.LOTS_ID
										AND   L.SOU_ID = @SOU_ID
								 ) AS CMP1

						      WHERE SR.SOU_ID     = @SOU_ID	
							    AND SR.TYPEITEM = 'L'
							    AND SR.ITEM_ID  = CMP1.LOTS_ID
						      GROUP BY SR.BLO_ID, CMP1.PRO_ID , CMP1.QTEUM
							  
							  ) AS SR2
   		     
  		     WHERE SP.PRO_ID = SR2.ITEM_ID_cmp
					 AND SP.SOU_ID  = @SOU_ID	
  		     GROUP BY SP.PRO_ID
         ) AS BB

    ON SPP.PRO_ID = BB.PRO_ID
    WHERE SPP.SOU_ID  = @SOU_ID	
	AND ((@DoLog=1) OR 
	     ((((BB.New_QTE IS NOT NULL) AND (CAST(SPP.QTELOT AS NUMERIC(18,2)) != CAST(BB.New_QTE AS NUMERIC(18,2)))) OR
           ((BB.New_QTE IS NULL)     AND (SPP.QTELOT  != 0)))));

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
	    SET @sql1 =  'UPDATE ' + @SqlTable +'  SET QTELOT = ' + STR( @QTE_NEW, 18, 5) + ' , CALCTIMSTP = ' + '''' + @UID + '''' +  ' WHERE SOU_ID = ' + '''' + @SOU_ID + '''' +  ' AND PRO_ID = ' + '''' + @PROD_ID + '''';
	  END ELSE 
	  BEGIN
        SET @sql1 =  'UPDATE ' + @SqlTable +'  SET QTELOT = 0                             , CALCTIMSTP = ' + '''' + @UID + '''' +  ' WHERE SOU_ID = ' + '''' + @SOU_ID + '''' +  ' AND PRO_ID = ' + '''' + @PROD_ID + '''';
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
	
	 SELECT DISTINCT SLC.PRO_ID , SR.CODEIMPR
     FROM FACREL SR, FACLOTS SL, FACLOTSCO SLC
     WHERE SR.SOU_ID   =  @SOU_ID
       AND SR.TYPEITEM = 'L'
	   AND SR.SOU_ID   = SL.SOU_ID
	   AND SR.ITEM_ID  = SL.LOTS_ID
	   AND SL.SOU_ID   = SLC.SOU_ID
	   AND SL.LOTS_ID  = SLC.LOTS_ID  
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

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'sp_FACPRO_Quantity_V2')
  DROP PROCEDURE sp_FACPRO_Quantity_V2
GO


CREATE PROCEDURE [dbo].[sp_FACPRO_Quantity_V2] (@SOU_ID VARCHAR(20), @REPLACE_FILTER INT, @DoLog BIT, @FACPROLOG VARCHAR(20))
AS BEGIN
 
  ----------------------------------
   -- Normalement cette procedure est appelée uniquement pour :  (TYPERELEVE = 'P') 
   ----------------------------------

   DECLARE @UID  VARCHAR(14)

   SELECT @UID = DBO.fn_DateTime_GetTimeStampStr()

   ----------------------------------
   ---- Pour les codes d'impression : 0 Pour Ne pas traiter , 1 Pour Ajouter, 2 pour remplacer
   ----------------------------------

   IF @REPLACE_FILTER = 2 
   BEGIN
     UPDATE   FACPRO
        SET CODEIMPR = ''
      WHERE SOU_ID   = @SOU_ID
   END 
   -----------------------------------
   -- le meme @UID est partagé entre SOUMIS est les produits correspondants recalculés (en dernier) dans FACPRO
   -----------------------------------
   UPDATE SOUMIS 
      SET CALCTIMSTP = @UID
    WHERE SOU_ID     = @SOU_ID 
   -----------------------------------
   --  Traitement 
   -----------------------------------

    EXEC dbo.sp_FAC_UpdateQteTotalOth_v2  @SOU_ID, @REPLACE_FILTER, @UID, @DoLog, @FACPROLOG;
    EXEC dbo.sp_FAC_UpdateQteTotalEns_v2  @SOU_ID, @REPLACE_FILTER, @UID, @DoLog, @FACPROLOG;
    EXEC dbo.sp_FAC_UpdateQteTotalLots_v2 @SOU_ID, @REPLACE_FILTER, @UID, @DoLog, @FACPROLOG;

   -----------------------------------
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'sp_FAC_CalculTotaux')
  DROP PROCEDURE sp_FAC_CalculTotaux
GO

CREATE PROCEDURE [dbo].[sp_FAC_CalculTotaux] (@SOU_ID                           VARCHAR(20),                                              
                                              @TypeReleve                       VARCHAR(1),
                                              @EE_CALGARY                       bit, 
								              @ModeCalcul                       VARCHAR(1),
								              @VendantUAvantVendantT            bit,
											  @VPM                              int,								            
								              @DoLog                            bit)
AS 
BEGIN
  DECLARE @fCout                      DECIMAL(18,6)
  DECLARE @fCoutantTotal              DECIMAL(18,6)
  DECLARE @fCoutPortionTVP            DECIMAL(18,6)
  DECLARE @fCoutantTotalPortionTVP    DECIMAL(18,6)
  DECLARE @CoutantNetReel             DECIMAL(18,6)
  DECLARE @CoutantNetSpecial          DECIMAL(18,6)
  DECLARE @CoutantUnitaire            DECIMAL(18,7) -- 7 decimal car n'est jamais arrondi
  DECLARE @CoutantTotal               DECIMAL(18,6)
  DECLARE @CoutantNetSection          DECIMAL(18,6)
  DECLARE @fVendant                   DECIMAL(18,6)
  DECLARE @fVendantTotal              DECIMAL(18,6)
  DECLARE @TempsInstallationSection   DECIMAL(18,6)
  DECLARE @TempsInstallationTotal     DECIMAL(18,6)
  DECLARE @TempsInstallationUnitaire  DECIMAL(18,6)
  DECLARE @VendantUnitaire            DECIMAL(18,6)
  DECLARE @VendantTotal               DECIMAL(18,6)
  DECLARE @VendantTotalIncluantTVP    DECIMAL(18,6)
  DECLARE @VendantUnitaireIncluantTVP DECIMAL(18,6)
  DECLARE @LandedCost                 DECIMAL(18,6)
  DECLARE @DivisibleEnSections        int
  ---------------------------------------------
  DECLARE @ITEM_ID                    VARCHAR(20)
  DECLARE @BLO_ID                     VARCHAR(3)
  DECLARE @DIV_ID                     VARCHAR(3)
  DECLARE @MULT_BLOC                  INT
  DECLARE @LaborFactor                INT
  DECLARE @TypeItem                   VARCHAR(1)
  DECLARE @QTE                        DECIMAL(18,6)
  DECLARE @QTEUM                      VARCHAR(2)
  DECLARE @COUUM                      VARCHAR(2)  
  DECLARE @COUBRUTUNI                 DECIMAL(18,6)
  DECLARE @COUESC                     DECIMAL(18,6)
  DECLARE @QPP                        INT
  DECLARE @TempsUM                    VARCHAR(2)
  DECLARE @COUTANBRUT                 DECIMAL(18,6)
  DECLARE @SECTION                    DECIMAL(18,6)
  DECLARE @TYPRATIO                   VARCHAR(1)
  DECLARE @PROFIT                     DECIMAL(18,6)
  DECLARE @fLaborTotal                DECIMAL(18,6)
  ---------------------------------------------

  -- POUR LES TAXES TPGSX
  DECLARE @TAX_ID                     VARCHAR(20)
  DECLARE @TYPETAXE                   VARCHAR(1)
  DECLARE @TaxeProv                   DECIMAL(18,6)
  DECLARE @INDEXTAX                   INT
  DECLARE @TVPSurCoutPermise          bit
  DECLARE @MontantTax1                DECIMAL(18,6)
  DECLARE @MontantTax2                DECIMAL(18,6)
  DECLARE @MontantTax3                DECIMAL(18,6)
  DECLARE @MontantTax4                DECIMAL(18,6)
  DECLARE @MontantTax5                DECIMAL(18,6)
  
  	   ---------------------------------------------
       --- Pour produir un log si @DoLog = 1
	   ---------------------------------------------

  DECLARE @log table 
   ( 
   ITEM_ID                    varchar(20), 
   BLO_ID                     VARCHAR(3),
   DIV_ID                     VARCHAR(3),
   TypeItem                   VARCHAR(1),
   QTE                        DECIMAL(18,6),      
   QTEUM                      VARCHAR(2),
   COUTANBRUT                 DECIMAL(18,6), 
   SECTION                    DECIMAL(18,6),        
   PROFIT                     DECIMAL(18,6),
   TYPETAXE                   VARCHAR(1),
   MULT_BLOC                  int,       
   fCout                      DECIMAL(18,6),
   fCoutPortionTVP            DECIMAL(18,6),
   fVendant                   DECIMAL(18,6),
   fCoutantTotal              DECIMAL(18,6),
   fCoutantTotalPortionTVP    DECIMAL(18,6),
   fVendantTotal              DECIMAL(18,6),
   fLaborTotal                DECIMAL(18,6),
   CoutantNetReel             DECIMAL(18,6), 
   CoutantNetSection          DECIMAL(18,6),
   TempsUnitaireApprox        DECIMAL(18,6), 
   LandedCost                 DECIMAL(18,6),
   CoutantUnitaire            DECIMAL(18,6),
   CoutantTotal               DECIMAL(18,6),
   VendantUnitaire            DECIMAL(18,6),
   VendantTotal               DECIMAL(18,6),
   TaxeProv                   DECIMAL(18,6),
   VendantUnitaireIncluantTVP DECIMAL(18,6),
   VendantTotalIncluantTVP    DECIMAL(18,6),
   TempsInstallationSection   DECIMAL(18,6),
   TempsInstallationTotal     DECIMAL(18,6)
   )
       
	   ---------------------------------------------
       -- On remplace la table FACPRO par #FACPRO_TEMP pour inclure la colonne LC dans le cas de @EE_CALGARY = 0
	   ---------------------------------------------

  IF OBJECT_ID('tempdb..#FACPRO_TEMP') IS NOT NULL 
  begin 
    DROP TABLE #FACPRO_TEMP
  end

  select sp.* into #FACPRO_TEMP from FACPRO sp
   where sp.SOU_ID = @SOU_ID

  if @EE_CALGARY = 0 
  begin
    ALTER TABLE #FACPRO_TEMP ADD LC FLOAT
  end

	   ---------------------------------------------
	   --- Initialiser les resultats finaux
	   ---------------------------------------------
  
  SET @fCoutantTotal           = 0.0  
  SET @fCoutantTotalPortionTVP = 0.0
  SET @fVendantTotal           = 0.0
  SET @fLaborTotal             = 0.0	

  -- Les tax

  SET @MontantTax1             = 0.0  
  SET @MontantTax2             = 0.0  
  SET @MontantTax3             = 0.0  
  SET @MontantTax4             = 0.0  
  SET @MontantTax5             = 0.0  

	   ---------------------------------------------
	   --- Recuperer le numero de tax
	   ---------------------------------------------    

  SELECT @TAX_ID = s.TAX_ID from FACTURES s WHERE SOU_ID = @SOU_ID

	   ---------------------------------------------
	   --- Debut des Calcules
	   ---------------------------------------------   

  DECLARE CUR_1 CURSOR FOR   
  SELECT  SR.ITEM_ID, SR.BLO_ID, SR.DIV_ID, SR.TYPEITEM,  
          ISNULL(SR.QTE,0.0), SR.QTEUM, ISNULL(SR.COUTANBRUT,0.0) , ISNULL(SR.SECTION,0.0) , ISNULL(SR.PROFIT,0.0), SR.TYPETAXE          
    FROM  FACREL SR 
    WHERE SR.SOU_ID = @SOU_ID
	  AND SR.TYPERELEVE = @TypeReleve
	
	ORDER BY SOU_ID, TYPERELEVE, BLO_ID, DIV_ID, ORDRE

  OPEN CUR_1
  FETCH NEXT FROM CUR_1
  INTO @ITEM_ID, @BLO_ID, @DIV_ID, @TypeItem, @QTE, @QTEUM, @COUTANBRUT, @SECTION, @PROFIT, @TYPETAXE

  WHILE @@FETCH_STATUS = 0
  BEGIN
		SET @fCout                    = 0.0
		SET @fCoutPortionTVP          = 0.0
		SET @fVendant                 = 0.0 		
		SET @DivisibleEnSections      = 0
		SET @TempsInstallationSection = 0.0
		SET @TempsInstallationTotal   = 0.0


		SELECT @MULT_BLOC = SB.MULT  FROM FACBLO SB
		 WHERE SB.SOU_ID = @SOU_ID
		   AND SB.BLO_ID = @BLO_ID

		IF @MULT_BLOC IS NULL SET @MULT_BLOC = 1; 


		SELECT @LaborFactor = SA.FACTMD  FROM FACAMD SA
		 WHERE SA.SOU_ID = @SOU_ID
		   AND SA.BLO_ID = @BLO_ID
		   AND SA.DIV_ID = @DIV_ID

		IF @LaborFactor IS NULL SET @LaborFactor = 1.0; 


	    -----------------------------------------------------------------------------------------
		IF (@TypeReleve = 'P') AND ((@TypeItem = 'P') OR (@TypeItem = 'N'))
		BEGIN

			SELECT @CoutantNetSpecial         = SP.PROMCOUNET, 
			       @COUBRUTUNI                = ISNULL(SP.COUBRUTUNI, 0.0), 
				   @COUESC                    = ISNULL(SP.COUESC, 0.0), 
				   @QPP                       = ISNULL(SP.QPP, 0.0),
				   @COUUM                     = SP.COUUM COLLATE DATABASE_DEFAULT, 
				   @LandedCost                = ISNULL(SP.LC, 0.0),
			       @TempsInstallationUnitaire = ISNULL(SP.TEMPUNI, 0.0),
				   @TempsUM                   = SP.TEMPUM COLLATE DATABASE_DEFAULT
			  FROM #FACPRO_TEMP SP
			 WHERE SP.SOU_ID = @SOU_ID COLLATE DATABASE_DEFAULT  
			   AND SP.PRO_ID = @ITEM_ID COLLATE DATABASE_DEFAULT

			IF @CoutantNetSpecial > 0 
			  SET @CoutantNetReel = @CoutantNetSpecial
			ELSE 
	  		  SET @CoutantNetReel = @COUBRUTUNI - (@COUBRUTUNI * (@COUESC / 100.0)); 


			SET @TempsInstallationTotal = @QTE *  @TempsInstallationUnitaire * DBO.fn_UM_GetRatioDeConversion (@QTEUM, @TempsUM, @QPP);
		          
	    END ELSE 

	    -----------------------------------------------------------------------------------------
		IF (@TypeReleve = 'P') AND (@TypeItem = 'A') 
		BEGIN

			WITH ComposanteEnsemble(QTE_cmp, CoutantNetReel_cmp, CoutantNetSection_cmp, QTEUM_cmp, COUUM_cmp, QPP_cmp, TEMPUM_cmp, LANDEDCOST_cmp, DivisibleSection_cmp) AS

	   	   (SELECT   CASE WHEN (SEC.TYPRATIO = 'L') AND (SE.COUUM != '' ) AND ([dbo].[fn_UM_GetNatureUnite](SE.COUUM) = 'L') 
					   THEN CASE 
							  WHEN (ISNULL(SEC.DIV,0.0) != 0) 
								THEN (ISNULL(SEC.QTE,0.0) / SEC.DIV) * DBO.fn_UM_GetRatioDeConversion (SE.COUUM , SEC.DIVUM,  0)
							  ELSE 0 
							END
					   ELSE SEC.QTE
					 END AS QTE_cmp					 
					 	
					, CASE WHEN (SEC.TYPRATIO = 'L') 
					    THEN CASE WHEN ISNULL(SP.PROMCOUNET,0.0) > 0 
						       THEN  SP.PROMCOUNET
							   ELSE  ISNULL(SP.COUBRUTUNI,0.0) - (ISNULL(SP.COUBRUTUNI,0.0) * (ISNULL(SP.COUESC,0.0) / 100.0)) 	
							 END				 
					   ELSE 0
					  END AS CoutantNetReel_cmp

				    , CASE WHEN (SEC.TYPRATIO = 'L') 
					    THEN 0
					    ELSE CASE WHEN ISNULL(SP.PROMCOUNET,0.0) > 0 
						       THEN  SP.PROMCOUNET
							   ELSE  ISNULL(SP.COUBRUTUNI,0.0) - (ISNULL(SP.COUBRUTUNI,0.0) * (ISNULL(SP.COUESC,0.0) / 100.0)) 	
							 END				 
					  END AS CoutantNetSection_cmp

					, SEC.QTEUM         as QTEUM_cmp
					, SP.COUUM          as COUUM_cmp
					, ISNULL(SP.QPP,0.0)  as QPP_cmp
					, SP.TEMPUM         as TEMPUM_cmp

					, CASE WHEN @EE_CALGARY = 1
					    THEN ISNULL(SP.LC,0.0) 
						ELSE 0 
				      END AS LANDEDCOST_cmp

					, CASE WHEN (SEC.TYPRATIO = 'L')
					    THEN 0
					    ELSE 1
					  END AS DivisibleSection_cmp
								 
			  FROM FACENS SE, FACENSCO SEC, #FACPRO_TEMP  sp
			  WHERE SE.SOU_ID  = SEC.SOU_ID
			    AND SE.ENS_ID  = SEC.ENS_ID
			    AND SEC.PRO_ID = SP.PRO_ID COLLATE DATABASE_DEFAULT
			    AND SEC.SOU_ID = @SOU_ID
			    and SE.ENS_ID  = @ITEM_ID
	       )  
		   select  @CoutantNetReel      = ISNULL(SUM(dbo.fn_CastAE(QTE_cmp * CoutantNetReel_cmp * DBO.fn_UM_GetRatioDeConversion(QTEUM_cmp, COUUM_cmp,  QPP_cmp) , 2)),0.0),		
                   @CoutantNetSection   = ISNULL(SUM(QTE_cmp * CoutantNetSection_cmp    * DBO.fn_UM_GetRatioDeConversion(QTEUM_cmp, COUUM_cmp,  QPP_cmp)),0.0),		           
                   @LandedCost          = ISNULL(SUM(QTE_cmp * LANDEDCOST_cmp           * DBO.fn_UM_GetRatioDeConversion(QTEUM_cmp, TEMPUM_cmp, QPP_cmp)),0.0),
				   @DivisibleEnSections = ISNULL(SUM(DivisibleSection_cmp),0.0)   
		   from ComposanteEnsemble
	       
		   SET @QPP = 0;	   

		   select @COUUM = SE.COUUM , 
		          @TempsInstallationSection  = SE.TEMPSEC, 
				  @TempsInstallationTotal    = @QTE *  SE.TEMPUNI * DBO.fn_UM_GetRatioDeConversion (@QTEUM, SE.TEMPUM, @QPP) 
		     from FACENS  SE
 		    where SE.SOU_ID = @SOU_ID
		      and SE.ENS_ID = @ITEM_ID

            -- 
			IF  (@DivisibleEnSections > 0)
			  SET @TempsInstallationTotal = @TempsInstallationTotal + (@TempsInstallationSection * @SECTION);

		END  ELSE-- Fin @TypeItem = 'A'

	    -----------------------------------------------------------------------------------------
        IF (@TypeReleve = 'P') AND (@TypeItem = 'L') 
		BEGIN
		   WITH ComposanteLot(CoutantNetReel_cmp, QTE_cmp, QTEUM_cmp, COUUM_cmp, QPP_cmp, TEMPUM_cmp, LANDEDCOST_cmp) AS

	   	   (SELECT   
		    	     CASE WHEN ISNULL(SP.PROMCOUNET,0.0) > 0 
				        THEN  SP.PROMCOUNET
					    ELSE  ISNULL(SP.COUBRUTUNI,0.0) - (ISNULL(SP.COUBRUTUNI,0.0) * (ISNULL(SP.COUESC,0.0) / 100.0)) 							 
					  END AS CoutantNetReel_cmp
		   
		            , ISNULL(SLC.QTE,0.0) as QTE_cmp					 					 	
					, SLC.QTEUM           as QTEUM_cmp
					, SP.COUUM  COLLATE DATABASE_DEFAULT          as COUUM_cmp
					, ISNULL(SP.QPP,0.0)  as QPP_cmp
					, SP.TEMPUM COLLATE DATABASE_DEFAULT          as TEMPUM_cmp

					, CASE WHEN @EE_CALGARY = 1
					    THEN ISNULL(SP.LC,0.0) 
						ELSE 0 
				      END AS LANDEDCOST_cmp
								 
			  FROM FACLOTS SL, FACLOTSCO SLC, #FACPRO_TEMP sp
			  WHERE SL.SOU_ID  = SLC.SOU_ID
			    AND SL.LOTS_ID = SLC.LOTS_ID
			    AND SLC.PRO_ID = SP.PRO_ID COLLATE DATABASE_DEFAULT
			    AND SLC.SOU_ID = @SOU_ID
			    and SL.LOTS_ID = @ITEM_ID
	       )  
		   select  @CoutantNetReel = ISNULL(SUM(dbo.fn_CastAE(QTE_cmp * CoutantNetReel_cmp * DBO.fn_UM_GetRatioDeConversion(QTEUM_cmp, COUUM_cmp,  QPP_cmp) , 2)),0.0),				           
                   @LandedCost     = ISNULL(SUM(QTE_cmp * LANDEDCOST_cmp        * DBO.fn_UM_GetRatioDeConversion (QTEUM_cmp, TEMPUM_cmp, QPP_cmp)),0.0)			   
		   from ComposanteLot
	   
		   SET @QPP = 0.0;	   

		   select   @COUUM = SL.COUUM  		          
				  , @TempsInstallationTotal  = @QTE *  SL.TEMPUNI * DBO.fn_UM_GetRatioDeConversion (@QTEUM, SL.TEMPUM, @QPP) 
				  , @CoutantNetReel = 
				    CASE 
					  WHEN SL.COUTANTSEL = 1 THEN SL.COUTANT1
					  WHEN SL.COUTANTSEL = 2 THEN SL.COUTANT2
					  WHEN SL.COUTANTSEL = 3 THEN SL.COUTANT3
					  WHEN SL.COUTANTSEL = 4 THEN SL.COUTANT3
					  --ELSE @CoutantNetReel
					END

		     from FACLOTS SL
 		    where SL.SOU_ID  = @SOU_ID
		      and SL.LOTS_ID = @ITEM_ID

		END  -- Fin @TypeItem = 'L'
	

       IF (@TypeItem != 'T')
	   BEGIN 

	   ---------------------------------------------
	   --- Calculer le CoutantTotal / CoutantUnitaire
	   ---------------------------------------------

	       SET @CoutantUnitaire   = 0.0;
		   SET @CoutantTotal      = 0.0;

		   IF ((@TypeReleve = 'S') AND (@TypeItem = 'S')) OR  ((@TypeReleve = 'O') AND (@TypeItem = 'O'))
		   BEGIN

			   SET @CoutantUnitaire = @COUTANBRUT;		  

		   END ELSE
           BEGIN
			   IF @EE_CALGARY = 1 
			   BEGIN
				 SET @CoutantUnitaire = @LandedCost     * DBO.fn_UM_GetRatioDeConversion (@QTEUM, @COUUM,  @QPP)
			   END ELSE 
			   BEGIN
				 SET @CoutantUnitaire = @CoutantNetReel * DBO.fn_UM_GetRatioDeConversion (@QTEUM, @COUUM,  @QPP);
			   END
		   END
 			
		   SET @CoutantTotal   = dbo.fn_CastAE(@QTE * @CoutantUnitaire , 2);

		   if ((@TypeReleve = 'P') AND (@TypeItem = 'A')) and (@DivisibleEnSections > 0)
		     SET @CoutantTotal = dbo.fn_CastAE(@CoutantTotal  + (@SECTION * @CoutantNetSection) , 2)


	   ---------------------------------------------
	    --- Calculer le VendantUnitaire /  VendantTotal
	   ---------------------------------------------

		   SET @VendantUnitaire = 0.0;
		   SET @VendantTotal    = 0.0;
		   
		   IF (@DivisibleEnSections = 0) and
		     ((@VendantUAvantVendantT = 1) or (@QTE = 0)) 
		   BEGIN
		   		   		
		     SELECT @VendantUnitaire = 
		          CASE WHEN (@ModeCalcul = 'C')
		                 THEN  dbo.fn_CastAE(@CoutantUnitaire * (1.0 + (@PROFIT / 100.0)), @VPM)
				       WHEN (@ModeCalcul = 'G') AND (@PROFIT < 100)
					     THEN  dbo.fn_CastAE(@CoutantUnitaire / (1.0 - (@PROFIT / 100.0)), @VPM)
					   ELSE 0
		          END
				  		 
			 SET @VendantTotal    =  dbo.fn_CastAE(@QTE * @VendantUnitaire , 2);

		   END ELSE
		   BEGIN

		     SELECT @VendantTotal  = 
		          CASE WHEN (@ModeCalcul = 'C')
		                 THEN dbo.fn_CastAE(@CoutantTotal * (1.0 + (@PROFIT / 100.0)) , 2)
				       WHEN (@ModeCalcul = 'G') AND (@PROFIT < 100)
					     THEN dbo.fn_CastAE(@CoutantTotal / (1.0 - (@PROFIT / 100.0)) , 2)
					   ELSE 0
		          END

			 SET @VendantUnitaire = dbo.fn_CastAE(@VendantTotal / @QTE , 2);
		   END;     

	   ---------------------------------------------
	   --- Calculer la TaxProv
	   ---------------------------------------------
	      
	      with TaxeProvincial(CODETAX, TAUXPRV, INDEXTAX) as
			(select [CODETAX1], [TAUXPRV1], 1  FROM [TAXDEF] where TAX_ID = @TAX_ID  UNION
			 select [CODETAX2], [TAUXPRV2], 2  FROM [TAXDEF] where TAX_ID = @TAX_ID  UNION
			 select [CODETAX3], [TAUXPRV3], 3  FROM [TAXDEF] where TAX_ID = @TAX_ID  UNION
			 select [CODETAX4], [TAUXPRV4], 4  FROM [TAXDEF] where TAX_ID = @TAX_ID  UNION
			 select [CODETAX5], [TAUXPRV5], 5  FROM [TAXDEF] where TAX_ID = @TAX_ID
			) 
			select @TaxeProv = S.TAUXPRV,
			       @INDEXTAX = S.INDEXTAX
			from TaxeProvincial S where S.CODETAX = @TYPETAXE; 

		if @TaxeProv is null SET @TaxeProv = 0.0;

		SELECT @TVPSurCoutPermise = TVPSURCPER FROM [TAXDEF] S  WHERE S.TAX_ID = @TAX_ID 

	   ---------------------------------------------
	   --- Calculer le VendantTotalIncluantTVP / VendantUnitaireIncluantTVP
	   ---------------------------------------------
	       
		SET @VendantUnitaireIncluantTVP = 0.0;
		SET @VendantTotalIncluantTVP    = 0.0;

	    IF (@TVPSurCoutPermise = 1) 
		BEGIN
			IF  (@TypeReleve = 'P') AND (@TypeItem = 'A') AND (@DivisibleEnSections > 0)  
			BEGIN
			  SET @VendantUnitaireIncluantTVP    = 0;
			  SET @VendantTotalIncluantTVP       = dbo.fn_CastAE(@VendantTotal +  (@CoutantTotal *  (@TaxeProv / 100.0)) , 2);   
			END ELSE 
			BEGIN
			  IF (@VendantUAvantVendantT = 1 ) OR (@QTE = 0)
			  BEGIN
 				SET @VendantUnitaireIncluantTVP = dbo.fn_CastAE(@VendantUnitaire +  (@CoutantUnitaire *  (@TaxeProv / 100.0)), @VPM);
				SET @VendantTotalIncluantTVP    = dbo.fn_CastAE(@QTE * @VendantUnitaireIncluantTVP , 2);   
			  END ELSE
			  BEGIN
				SET @VendantTotalIncluantTVP    = dbo.fn_CastAE(@VendantTotal +  (@CoutantTotal *  (@TaxeProv / 100.0)) , 2);   
				SET @VendantUnitaireIncluantTVP = dbo.fn_CastAE(@VendantTotalIncluantTVP / @QTE , @VPM);
			  END
			END;
		END;

	   ---------------------------------------------
	   --- Calcul des totaux 
	   ---------------------------------------------
	   IF (@TypeReleve = 'P') AND ((@TypeItem = 'P') OR (@TypeItem = 'N') OR (@TypeItem = 'A') OR (@TypeItem = 'L'))
		BEGIN	     
			SET @fCout           =  @CoutantTotal * @MULT_BLOC;
			SET @fCoutPortionTVP = (@VendantTotalIncluantTVP - @VendantTotal) * @MULT_BLOC;
			SET @fVendant        =  @VendantTotal * @MULT_BLOC;
			SET @fLaborTotal     =  @fLaborTotal + (@TempsInstallationTotal * @LaborFactor * @MULT_BLOC);
		END ELSE
		IF (@TypeReleve = 'S') AND (@TypeItem = 'S')
		BEGIN 
            SET @fCout           =  @CoutantTotal;
			SET @fVendant        =  @VendantTotal;
			SET @fLaborTotal     =  @fLaborTotal + @QTE;
		END ELSE
		IF (@TypeReleve = 'O') AND (@TypeItem = 'O')
		BEGIN
            SET @fCout           =  @CoutantTotal;
			SET @fVendant        =  @VendantTotal;
			SET @fCoutPortionTVP = (@VendantTotalIncluantTVP - @VendantTotal);
		END
	   ---------------------------------------------
		SET @fCoutantTotal           = @fCoutantTotal           + @fCout;
		SET @fCoutantTotalPortionTVP = @fCoutantTotalPortionTVP + @fCoutPortionTVP
		SET @fVendantTotal           = @fVendantTotal           + @fVendant
	    

       ---------------------------------------------
	   -- AddMontantTaxable
       ---------------------------------------------

	     IF @INDEXTAX = 1 BEGIN SET @MontantTax1 = @MontantTax1 + @fVendant END ELSE
		 IF @INDEXTAX = 2 BEGIN SET @MontantTax2 = @MontantTax2 + @fVendant END ELSE
		 IF @INDEXTAX = 3 BEGIN SET @MontantTax3 = @MontantTax3 + @fVendant END ELSE
		 IF @INDEXTAX = 4 BEGIN SET @MontantTax4 = @MontantTax4 + @fVendant END ELSE
		 IF @INDEXTAX = 5 BEGIN SET @MontantTax5 = @MontantTax5 + @fVendant END;
	   
	   ---------------------------------------------
	   -- Log
    IF @DoLog = 1
	BEGIN
		insert into @Log  ( ITEM_ID, BLO_ID, DIV_ID, TypeItem, QTE , QTEUM , COUTANBRUT, SECTION , PROFIT  , TYPETAXE, MULT_BLOC, 
							fCout, fCoutPortionTVP, fVendant , fCoutantTotal, fCoutantTotalPortionTVP , fVendantTotal, 
							CoutantNetReel ,  CoutantNetSection,  LandedCost,                
							CoutantUnitaire , CoutantTotal  ,  VendantUnitaire, VendantTotal , fLaborTotal, TaxeProv , VendantUnitaireIncluantTVP, VendantTotalIncluantTVP ,
							TempsInstallationSection , TempsInstallationTotal     
						  ) Values
						  ( @ITEM_ID, @BLO_ID, @DIV_ID, @TypeItem, @QTE , @QTEUM , @COUTANBRUT, @SECTION , @PROFIT  , @TYPETAXE, @MULT_BLOC,
							@fCout  , @fCoutPortionTVP, @fVendant , @fCoutantTotal, @fCoutantTotalPortionTVP , @fVendantTotal, 
							@CoutantNetReel ,  @CoutantNetSection,  @LandedCost,                
							@CoutantUnitaire , @CoutantTotal  ,  @VendantUnitaire, @VendantTotal , @fLaborTotal, @TaxeProv , @VendantUnitaireIncluantTVP, @VendantTotalIncluantTVP ,
							@TempsInstallationSection , @TempsInstallationTotal     
						  );
	END;
	   ---------------------------------------------

	END


	FETCH NEXT FROM CUR_1
	INTO @ITEM_ID, @BLO_ID, @DIV_ID, @TypeItem, @QTE, @QTEUM, @COUTANBRUT, @SECTION, @PROFIT, @TYPETAXE
  END
  CLOSE CUR_1;
  DEALLOCATE CUR_1;


  ------------------------
  -- M.A.J des tax dans FACTURES
  ------------------------
  IF @TypeReleve = 'P' 
  BEGIN
   UPDATE FACTURES 
    SET MATTAXAB1 = @MontantTax1, 
	    MATTAXAB2 = @MontantTax2, 
		MATTAXAB3 = @MontantTax3, 
		MATTAXAB4 = @MontantTax4, 
		MATTAXAB5 = @MontantTax5
   WHERE SOU_ID = @SOU_ID;
  END ELSE
  IF @TypeReleve = 'S' 
  BEGIN
   UPDATE FACTURES 
    SET SERTAXAB1 = @MontantTax1, 
	    SERTAXAB2 = @MontantTax2, 
		SERTAXAB3 = @MontantTax3, 
		SERTAXAB4 = @MontantTax4, 
		SERTAXAB5 = @MontantTax5
   WHERE SOU_ID = @SOU_ID;
  END ELSE
  IF @TypeReleve = 'O' 
  BEGIN
   UPDATE FACTURES 
    SET AUTTAXAB1 = @MontantTax1, 
	    AUTTAXAB2 = @MontantTax2, 
		AUTTAXAB3 = @MontantTax3, 
		AUTTAXAB4 = @MontantTax4, 
		AUTTAXAB5 = @MontantTax5
   WHERE SOU_ID = @SOU_ID;
  END; 
  ------------------------
  IF @DoLog = 1
  BEGIN  
	  select * from @Log
  END;

  ------------------------
  -- Retour des resultats
  ------------------------

  SELECT @fCoutantTotal           AS fCoutantTotal, 
	     @fCoutantTotalPortionTVP AS fCoutantTotalPortionTVP, 
	     @fVendantTotal           AS fVendantTotal, 
	     @fLaborTotal             AS fLaborTotal


  END
  GO


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'sp_FAC_CalculProductUsageInAssemblies_V2')
  DROP PROCEDURE sp_FAC_CalculProductUsageInAssemblies_V2
GO


CREATE PROCEDURE [dbo].[sp_FAC_CalculProductUsageInAssemblies_V2] (@SOU_ID VARCHAR(20), @LANG INT)
AS BEGIN

  DECLARE  @TITLE       VARCHAR(60);
  DECLARE  @DESCR       VARCHAR(2000);  
  DECLARE  @SOUID       VARCHAR(20);
  DECLARE  @PRO_ID      VARCHAR(20);
  DECLARE  @INASSEMBLIE VARCHAR(2000);  

  IF @LANG = 1 
    SET @TITLE = 'Dans les ensembles'
  ELSE
    SET @TITLE = 'In assemblies '

  SET @TITLE =    @TITLE + CHAR(13) + CHAR(10) + REPLICATE('-', LEN(@TITLE))
	DECLARE CUR_1 CURSOR FOR 

  SELECT SP.SOU_ID , SP.PRO_ID, AA.DESCR FROM FACPRO SP LEFT JOIN  --SP.INASSEMBLIE
	   (SELECT E.SOU_ID, 
			   C.PRO_ID , 
			   DESCR = @TITLE +  CHAR(13) + CHAR(10) + dbo.sp_FAC_GetAssemblyCompositionConcat(E.SOU_ID, C.PRO_ID) 
	    FROM FACENS E, FACENSCO C , FACREL L
	    WHERE E.ENS_ID = C.ENS_ID
		  AND E.SOU_ID = C.SOU_ID
		  AND L.SOU_ID = E.SOU_ID
		  AND L.ITEM_ID = E.ENS_ID
		  AND C.SOU_ID = @SOU_ID
		GROUP BY  E.SOU_ID, C.PRO_ID
		) AA

		ON  SP.SOU_ID = AA.SOU_ID 
		AND SP.PRO_ID = AA.PRO_ID
		WHERE  SP.SOU_ID =  @SOU_ID
		AND (AA.DESCR IS NOT NULL) AND (SP.INASSEMBLIE != AA.DESCR)

  OPEN CUR_1
  FETCH NEXT FROM CUR_1
  INTO @SOUID, @PRO_ID, @DESCR

  WHILE @@FETCH_STATUS = 0
   BEGIN
     UPDATE FACPRO -- TEMPFACPRODESCR
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




