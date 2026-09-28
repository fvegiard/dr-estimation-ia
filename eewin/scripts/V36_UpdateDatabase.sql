  -- DROP PROCEDURE
IF OBJECT_ID(N'dbo.sp_SOU_GetAssemblyCompositionConcat', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_SOU_GetAssemblyCompositionConcat;
GO

  -- DROP PROCEDURE
IF OBJECT_ID(N'dbo.sp_FAC_GetAssemblyCompositionConcat', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_FAC_GetAssemblyCompositionConcat;
GO

  -- DROP PROCEDURE
IF OBJECT_ID(N'dbo.sp_GetAssemblyCompositionConcat', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_GetAssemblyCompositionConcat;
GO

  -- DROP PROCEDURE
IF OBJECT_ID(N'dbo.sp_SOU_CalculProductUsageInAssemblies_V2', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_SOU_CalculProductUsageInAssemblies_V2;
GO

  -- DROP PROCEDURE
IF OBJECT_ID(N'dbo.sp_FAC_CalculProductUsageInAssemblies_V2', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_FAC_CalculProductUsageInAssemblies_V2;
GO


  -- DROP field - SOUPRO.INASSEMBLIE
IF EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUPRO'
    AND [COLUMN_NAME] = 'INASSEMBLIE' )
BEGIN
  ALTER TABLE
    SOUPRO
  DROP COLUMN
    INASSEMBLIE;
END
GO

  -- DROP field - FACPRO.INASSEMBLIE
IF EXISTS (
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
  DROP COLUMN
    INASSEMBLIE;
END
GO

  -- New field - SOUPRO.UnitSelling
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUPRO'
    AND [COLUMN_NAME] = 'UnitSelling' )
BEGIN
  ALTER TABLE
    SOUPRO
  ADD
    UnitSelling  FLOAT
END
GO

  -- New field - FACPRO.UnitSelling
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACPRO'
    AND [COLUMN_NAME] = 'UnitSelling' )
BEGIN
  ALTER TABLE
    FACPRO
  ADD
    UnitSelling  FLOAT
END
GO

------------
IF OBJECT_ID(N'dbo.sp_SOU_CalculTotaux', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_SOU_CalculTotaux;
GO

 CREATE PROCEDURE [dbo].[sp_SOU_CalculTotaux] (@SOU_ID                          VARCHAR(20),                                              
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

  DECLARE @ccVendantUnitaire            DECIMAL(18,6)
  DECLARE @ccVendantUnitaireIncluantTVP DECIMAL(18,6)
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
		            AND SEC.SOU_ID = SP.SOU_ID COLLATE DATABASE_DEFAULT
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
				AND SLC.SOU_ID = SP.SOU_ID COLLATE DATABASE_DEFAULT
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
					  WHEN SL.COUTANTSEL = 4 THEN SL.COUTANT4
					  ELSE @CoutantNetReel
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

	   ---------------------------------------------
	   --- Traitement des UnitSelling
	   ---------------------------------------------   
  DECLARE CUR_2 CURSOR FOR     
  SELECT ITEM_ID, MAX(VendantUnitaire) as ccVendantUnitaire , MAX(VendantUnitaireIncluantTVP) as ccVendantUnitaireIncluantTVP
  FROM @Log 
  GROUP BY ITEM_ID; 

  OPEN CUR_2
  FETCH NEXT FROM CUR_2
  INTO @ITEM_ID, @ccVendantUnitaire, @ccVendantUnitaireIncluantTVP

  WHILE @@FETCH_STATUS = 0
  BEGIN
      IF NOT EXISTS (
     	  SELECT 1 FROM SOUPRO 
	      WHERE SOU_ID = @SOU_ID  
	      AND PRO_ID = @ITEM_ID) 
      BEGIN
		  UPDATE SOUPRO 
		  SET UnitSelling = -1 
		  WHERE SOU_ID = @SOU_ID  
			AND PRO_ID = @ITEM_ID;  

	  END ELSE
	  BEGIN
		  UPDATE SOUPRO 
		  SET UnitSelling =  CASE WHEN (@TVPSurCoutPermise = 1) 
								THEN @ccVendantUnitaireIncluantTVP      
								ELSE @ccVendantUnitaire
							 END  
		  WHERE SOU_ID = @SOU_ID  
			AND PRO_ID = @ITEM_ID;  
      END

	FETCH NEXT FROM CUR_2
	INTO @ITEM_ID, @ccVendantUnitaire, @ccVendantUnitaireIncluantTVP
	
  END
  CLOSE CUR_2;
  DEALLOCATE CUR_2;

  ------------------------
  -- Retour des resultats
  ------------------------

  SELECT @fCoutantTotal           AS fCoutantTotal, 
	     @fCoutantTotalPortionTVP AS fCoutantTotalPortionTVP, 
	     @fVendantTotal           AS fVendantTotal, 
	     @fLaborTotal             AS fLaborTotal


  END
GO
------------------


IF OBJECT_ID(N'dbo.sp_FAC_CalculTotaux', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_FAC_CalculTotaux;
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

  DECLARE @ccVendantUnitaire            DECIMAL(18,6)
  DECLARE @ccVendantUnitaireIncluantTVP DECIMAL(18,6)
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

	   ---------------------------------------------
	   --- Traitement des UnitSelling
	   ---------------------------------------------   
  DECLARE CUR_2 CURSOR FOR     
  SELECT ITEM_ID, MAX(VendantUnitaire) as ccVendantUnitaire , MAX(VendantUnitaireIncluantTVP) as ccVendantUnitaireIncluantTVP
  FROM @Log 
  GROUP BY ITEM_ID; 

  OPEN CUR_2
  FETCH NEXT FROM CUR_2
  INTO @ITEM_ID, @ccVendantUnitaire, @ccVendantUnitaireIncluantTVP

  WHILE @@FETCH_STATUS = 0
  BEGIN
      IF NOT EXISTS (
     	  SELECT 1 FROM FACPRO 
	      WHERE SOU_ID = @SOU_ID  
	      AND PRO_ID = @ITEM_ID) 
      BEGIN
		  UPDATE FACPRO 
		  SET UnitSelling = -1 
		  WHERE SOU_ID = @SOU_ID  
			AND PRO_ID = @ITEM_ID;  

	  END ELSE
	  BEGIN
		  UPDATE FACPRO 
		  SET UnitSelling =  CASE WHEN (@TVPSurCoutPermise = 1) 
								THEN @ccVendantUnitaireIncluantTVP      
								ELSE @ccVendantUnitaire
							 END  
		  WHERE SOU_ID = @SOU_ID  
			AND PRO_ID = @ITEM_ID;  
      END

	FETCH NEXT FROM CUR_2
	INTO @ITEM_ID, @ccVendantUnitaire, @ccVendantUnitaireIncluantTVP
	
  END
  CLOSE CUR_2;
  DEALLOCATE CUR_2;

  ------------------------
  -- Retour des resultats
  ------------------------

  SELECT @fCoutantTotal           AS fCoutantTotal, 
	     @fCoutantTotalPortionTVP AS fCoutantTotalPortionTVP, 
	     @fVendantTotal           AS fVendantTotal, 
	     @fLaborTotal             AS fLaborTotal


  END
GO
-------------


IF OBJECT_ID(N'dbo.fn_CompositionConcat', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.fn_CompositionConcat;
GO

 CREATE FUNCTION  [dbo].[fn_CompositionConcat]  
( @SFMode VARCHAR(3), 
  @TYPEITEM VARCHAR(1),
  @SOU_ID   VARCHAR(20),
  @PRO_ID   VARCHAR(20))

RETURNS VARCHAR(2000)
AS 
BEGIN
  DECLARE @sEspace VARCHAR(30);
  SET @sEspace = '     ';

  IF (@SFMode ='SOU')
  BEGIN
	  IF @TYPEITEM = 'A' 
	  BEGIN
		  DECLARE @s VARCHAR(2000);  
		  SELECT @s = COALESCE(@s , N'') 
					  + CHAR(13) + CHAR(10) 
					  + E.[DESC] + CHAR(13) +  CHAR(10) + @sEspace +  '> ' + LTRIM(STR(C.QTE, 10, 2)) + ' ' + C.QTEUM + ' / 1.00 '+ DBO.fn_UM_GetUniteDeBase(E.COUUM)
			FROM SOUENS E, SOUENSCO C , SOUREL L
		   WHERE E.ENS_ID = C.ENS_ID
			 AND E.SOU_ID = C.SOU_ID
			 AND L.SOU_ID = E.SOU_ID
			 AND L.ITEM_ID = E.ENS_ID
			 AND C.SOU_ID = @SOU_ID
			 AND C.PRO_ID = @PRO_ID;
	  END ELSE
	  IF @TYPEITEM = 'L' 
	  BEGIN
		  SELECT @s = COALESCE(@s , N'') + 
					  E.[DESC] + CHAR(13) +  CHAR(10) + @sEspace + '> ' + LTRIM(STR(C.QTE, 10, 2)) + ' ' + C.QTEUM + ' / 1.00 '+ DBO.fn_UM_GetUniteDeBase(E.COUUM)
					  + CHAR(13) + CHAR(10) 
			FROM SOULOTS E, SOULOTSCO C , SOUREL L
		   WHERE E.LOTS_ID = C.LOTS_ID
			 AND E.SOU_ID = C.SOU_ID
			 AND L.SOU_ID = E.SOU_ID
			 AND L.ITEM_ID = E.LOTS_ID
			 AND C.SOU_ID = @SOU_ID
			 AND C.PRO_ID = @PRO_ID;
	  END 

  END ELSE
  IF (@SFMode ='FAC')
  BEGIN
	  IF @TYPEITEM = 'A' 
	  BEGIN
		  SELECT @s = COALESCE(@s , N'') + 
					  E.[DESC] + CHAR(13) +  CHAR(10) + @sEspace + '> ' + LTRIM(STR(C.QTE, 10, 2)) + ' ' + C.QTEUM + ' / 1.00 '+ DBO.fn_UM_GetUniteDeBase(E.COUUM)
					  + CHAR(13) + CHAR(10) 
			FROM FACENS E, FACENSCO C , FACREL L
		   WHERE E.ENS_ID = C.ENS_ID
			 AND E.SOU_ID = C.SOU_ID
			 AND L.SOU_ID = E.SOU_ID
			 AND L.ITEM_ID = E.ENS_ID
			 AND C.SOU_ID = @SOU_ID
			 AND C.PRO_ID = @PRO_ID;
	  END ELSE
	  IF @TYPEITEM = 'L' 
	  BEGIN
		  SELECT @s = COALESCE(@s , N'') + 
					  E.[DESC] + CHAR(13) +  CHAR(10) +  @sEspace + '> ' + LTRIM(STR(C.QTE, 10, 2)) + ' ' + C.QTEUM + ' / 1.00 '+ DBO.fn_UM_GetUniteDeBase(E.COUUM)
					  + CHAR(13) + CHAR(10) 
			FROM FACLOTS E, FACLOTSCO C , FACREL L
		   WHERE E.LOTS_ID = C.LOTS_ID
			 AND E.SOU_ID = C.SOU_ID
			 AND L.SOU_ID = E.SOU_ID
			 AND L.ITEM_ID = E.LOTS_ID
			 AND C.SOU_ID = @SOU_ID
			 AND C.PRO_ID = @PRO_ID;
	  END 
  END;

  RETURN (@s);
END
GO
-------------------

IF OBJECT_ID(N'dbo.fn_GetProductComposition', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.fn_GetProductComposition;
GO

 CREATE FUNCTION [dbo].fn_GetProductComposition  
( @TypeReleve VARCHAR(1), 
  @SFMode VARCHAR(3),
  @SOU_ID VARCHAR(20),
  @PRO_ID VARCHAR(20),
  @COUUM VARCHAR(2))

RETURNS VARCHAR(2000)
AS 
BEGIN

  DECLARE @s VARCHAR(2000);  
  DECLARE @v VARCHAR(2000);  
  DECLARE @r VARCHAR(2000);  
  
  IF @TypeReleve = 'P' 
  BEGIN
	  IF (@SFMode ='SOU')
	  BEGIN
			 -- Ajouter les produits simple
		  SELECT  @s = COALESCE(@s , N'') + 
					 [dbo].fn_GetProductCompositionConcat(@TypeReleve, 'SOU', R.SOU_ID, R.ITEM_ID, R.BLO_ID, R.DIV_ID, @PRO_ID, @COUUM, R.TYPEITEM) 
				 -- +  CHAR(13) + CHAR(10) 
			FROM SOUBLO B, SOUDIV D , 
			   (SELECT RR.SOU_ID, RR.BLO_ID, RR.DIV_ID, RR.ITEM_ID, RR.TYPEITEM             
				  FROM SOUREL RR
				 WHERE RR.SOU_ID = @SOU_ID
				   AND RR.ITEM_ID = @PRO_ID
				   AND RR.TYPEITEM IN('P','N')
				   AND RR.TYPERELEVE = @TypeReleve
			  GROUP BY RR.SOU_ID, RR.BLO_ID, RR.DIV_ID , RR.ITEM_ID	, RR.TYPEITEM  
				) AS R
		   WHERE R.SOU_ID = B.SOU_ID
			 AND R.BLO_ID = B.BLO_ID
			 AND R.SOU_ID = D.SOU_ID
			 AND R.DIV_ID = D.DIV_ID
			 AND R.SOU_ID = @SOU_ID;
		 
		   -- Ajouter les produits d'ensemble
		  SELECT  @v = COALESCE(@v , N'') + 
				  [dbo].fn_GetProductCompositionConcat(@TypeReleve, 'SOU', R.SOU_ID, R.ITEM_ID, R.BLO_ID, R.DIV_ID, @PRO_ID, @COUUM, R.TYPEITEM) 
			--	   CHAR(13) + CHAR(10) 
			FROM SOUBLO B, SOUDIV D , 
			   (SELECT RR.SOU_ID, RR.BLO_ID, RR.DIV_ID, RR.ITEM_ID, RR.TYPEITEM             
				  FROM SOUREL RR
				 WHERE RR.SOU_ID = @SOU_ID
				   AND RR.TYPEITEM = 'A'
				   AND RR.TYPERELEVE = @TypeReleve
			  GROUP BY RR.SOU_ID, RR.BLO_ID, RR.DIV_ID , RR.ITEM_ID	, RR.TYPEITEM  
				) AS R
		   WHERE R.SOU_ID = B.SOU_ID
			 AND R.BLO_ID = B.BLO_ID
			 AND R.SOU_ID = D.SOU_ID
			 AND R.DIV_ID = D.DIV_ID
			 AND R.SOU_ID = @SOU_ID;

		   -- Ajouter les produits de Lot
		  SELECT  @v = COALESCE(@v , N'') + 
				  [dbo].fn_GetProductCompositionConcat(@TypeReleve, 'SOU', R.SOU_ID, R.ITEM_ID, R.BLO_ID, R.DIV_ID, @PRO_ID, @COUUM, R.TYPEITEM) 
			--	   CHAR(13) + CHAR(10)
			FROM SOUBLO B, SOUDIV D , 
			   (SELECT RR.SOU_ID, RR.BLO_ID, RR.DIV_ID, RR.ITEM_ID, RR.TYPEITEM             
				  FROM SOUREL RR
				 WHERE RR.SOU_ID = @SOU_ID
				   AND RR.TYPEITEM = 'L'
				   AND RR.TYPERELEVE = @TypeReleve
			  GROUP BY RR.SOU_ID, RR.BLO_ID, RR.DIV_ID , RR.ITEM_ID	, RR.TYPEITEM  
				) AS R
		   WHERE R.SOU_ID = B.SOU_ID
			 AND R.BLO_ID = B.BLO_ID
			 AND R.SOU_ID = D.SOU_ID
			 AND R.DIV_ID = D.DIV_ID
			 AND R.SOU_ID = @SOU_ID;
		
	  END ELSE

	  IF (@SFMode ='FAC')
	  BEGIN
			 -- Ajouter les produits simple
		  SELECT  @s = COALESCE(@s , N'') + 
					 [dbo].fn_GetProductCompositionConcat(@TypeReleve, 'FAC', R.SOU_ID, R.ITEM_ID, R.BLO_ID, R.DIV_ID, @PRO_ID, @COUUM, R.TYPEITEM) 
				--  +  CHAR(13) + CHAR(10) 
			FROM FACBLO B, FACDIV D , 
			   (SELECT RR.SOU_ID, RR.BLO_ID, RR.DIV_ID, RR.ITEM_ID, RR.TYPEITEM             
				  FROM FACREL RR
				 WHERE RR.SOU_ID = @SOU_ID
				   AND RR.ITEM_ID = @PRO_ID
				   AND RR.TYPEITEM IN('P','N')
				   AND RR.TYPERELEVE = @TypeReleve
			  GROUP BY RR.SOU_ID, RR.BLO_ID, RR.DIV_ID , RR.ITEM_ID	, RR.TYPEITEM  
				) AS R
		   WHERE R.SOU_ID = B.SOU_ID
			 AND R.BLO_ID = B.BLO_ID
			 AND R.SOU_ID = D.SOU_ID
			 AND R.DIV_ID = D.DIV_ID
			 AND R.SOU_ID = @SOU_ID;
		 
		   -- Ajouter les produits d'ensemble
		  SELECT  @v = COALESCE(@v , N'') + 
				  [dbo].fn_GetProductCompositionConcat(@TypeReleve, 'FAC', R.SOU_ID, R.ITEM_ID, R.BLO_ID, R.DIV_ID, @PRO_ID, @COUUM, R.TYPEITEM) 
			--	   CHAR(13) + CHAR(10) 
			FROM FACBLO B, FACDIV D , 
			   (SELECT RR.SOU_ID, RR.BLO_ID, RR.DIV_ID, RR.ITEM_ID, RR.TYPEITEM             
				  FROM FACREL RR
				 WHERE RR.SOU_ID = @SOU_ID
				   AND RR.TYPEITEM = 'A'
				   AND RR.TYPERELEVE = @TypeReleve
			  GROUP BY RR.SOU_ID, RR.BLO_ID, RR.DIV_ID , RR.ITEM_ID	, RR.TYPEITEM  
				) AS R
		   WHERE R.SOU_ID = B.SOU_ID
			 AND R.BLO_ID = B.BLO_ID
			 AND R.SOU_ID = D.SOU_ID
			 AND R.DIV_ID = D.DIV_ID
			 AND R.SOU_ID = @SOU_ID;

		   -- Ajouter les produits de Lot
		  SELECT  @v = COALESCE(@v , N'') + 
				  [dbo].fn_GetProductCompositionConcat(@TypeReleve, 'FAC', R.SOU_ID, R.ITEM_ID, R.BLO_ID, R.DIV_ID, @PRO_ID, @COUUM, R.TYPEITEM) 
			--	   CHAR(13) + CHAR(10)
			FROM FACBLO B, FACDIV D , 
			   (SELECT RR.SOU_ID, RR.BLO_ID, RR.DIV_ID, RR.ITEM_ID, RR.TYPEITEM             
				  FROM FACREL RR
				 WHERE RR.SOU_ID = @SOU_ID
				   AND RR.TYPEITEM = 'L'
				   AND RR.TYPERELEVE = @TypeReleve
			  GROUP BY RR.SOU_ID, RR.BLO_ID, RR.DIV_ID , RR.ITEM_ID	, RR.TYPEITEM  
				) AS R
		   WHERE R.SOU_ID = B.SOU_ID
			 AND R.BLO_ID = B.BLO_ID
			 AND R.SOU_ID = D.SOU_ID
			 AND R.DIV_ID = D.DIV_ID
			 AND R.SOU_ID = @SOU_ID;
	  END;

  END ELSE
  IF @TypeReleve = 'U'  -------------- UnitaryPrices
  BEGIN
	  IF (@SFMode ='SOU')
	  BEGIN
			 -- Ajouter les produits simple
		  SELECT  @s = COALESCE(@s , N'') + 
					 [dbo].fn_GetProductCompositionConcat(@TypeReleve, 'SOU', RR.SOU_ID, RR.ITEM_ID, RR.BLO_ID, RR.DIV_ID, @PRO_ID, @COUUM, RR.TYPEITEM) 
				--  +  CHAR(13) + CHAR(10)           
				  FROM SOUREL RR
				 WHERE RR.SOU_ID = @SOU_ID
				   AND RR.ITEM_ID = @PRO_ID
				   AND RR.TYPEITEM IN('P','N')
				   AND RR.TYPERELEVE = @TypeReleve
			GROUP BY RR.SOU_ID, RR.BLO_ID, RR.DIV_ID , RR.ITEM_ID, RR.TYPEITEM;  

		 
		   -- Ajouter les produits d'ensemble
		  SELECT  @v = COALESCE(@v , N'') + 
				  [dbo].fn_GetProductCompositionConcat(@TypeReleve, 'SOU', RR.SOU_ID, RR.ITEM_ID, RR.BLO_ID, RR.DIV_ID, @PRO_ID, @COUUM, RR.TYPEITEM) 
			--	   CHAR(13) + CHAR(10)   
				  FROM SOUREL RR
				 WHERE RR.SOU_ID = @SOU_ID
				   AND RR.TYPEITEM = 'A'
				   AND RR.TYPERELEVE = @TypeReleve
			GROUP BY RR.SOU_ID, RR.BLO_ID, RR.DIV_ID , RR.ITEM_ID, RR.TYPEITEM;  

		   -- Ajouter les produits de Lot
		  SELECT  @v = COALESCE(@v , N'') + 
				  [dbo].fn_GetProductCompositionConcat(@TypeReleve, 'SOU', RR.SOU_ID, RR.ITEM_ID, RR.BLO_ID, RR.DIV_ID, @PRO_ID, @COUUM, RR.TYPEITEM) 
			--	   CHAR(13) + CHAR(10)  
				  FROM SOUREL RR
				 WHERE RR.SOU_ID = @SOU_ID
				   AND RR.TYPEITEM = 'L'
				   AND RR.TYPERELEVE = @TypeReleve
			GROUP BY RR.SOU_ID, RR.BLO_ID, RR.DIV_ID , RR.ITEM_ID, RR.TYPEITEM;  
		
	  END ELSE

	  IF (@SFMode ='FAC')
	  BEGIN
			 -- Ajouter les produits simple
		  SELECT  @s = COALESCE(@s , N'') + 
					 [dbo].fn_GetProductCompositionConcat(@TypeReleve, 'FAC', RR.SOU_ID, RR.ITEM_ID, RR.BLO_ID, RR.DIV_ID, @PRO_ID, @COUUM, RR.TYPEITEM) 
				--  +  CHAR(13) + CHAR(10)         
				  FROM FACREL RR
				 WHERE RR.SOU_ID = @SOU_ID
				   AND RR.ITEM_ID = @PRO_ID
				   AND RR.TYPEITEM IN('P','N')
				   AND RR.TYPERELEVE = @TypeReleve
			GROUP BY RR.SOU_ID, RR.BLO_ID, RR.DIV_ID , RR.ITEM_ID, RR.TYPEITEM;  
		 
		   -- Ajouter les produits d'ensemble
		  SELECT  @v = COALESCE(@v , N'') + 
				  [dbo].fn_GetProductCompositionConcat(@TypeReleve, 'FAC', RR.SOU_ID, RR.ITEM_ID, RR.BLO_ID, RR.DIV_ID, @PRO_ID, @COUUM, RR.TYPEITEM) 
			--	   CHAR(13) + CHAR(10)      
				  FROM FACREL RR
				 WHERE RR.SOU_ID = @SOU_ID
				   AND RR.TYPEITEM = 'A'
				   AND RR.TYPERELEVE = @TypeReleve
			GROUP BY RR.SOU_ID, RR.BLO_ID, RR.DIV_ID , RR.ITEM_ID, RR.TYPEITEM;  

		   -- Ajouter les produits de Lot
		  SELECT  @v = COALESCE(@v , N'') + 
				  [dbo].fn_GetProductCompositionConcat(@TypeReleve, 'FAC', RR.SOU_ID, RR.ITEM_ID, RR.BLO_ID, RR.DIV_ID, @PRO_ID, @COUUM, RR.TYPEITEM) 
			--	   CHAR(13) + CHAR(10)         
				  FROM FACREL RR
				 WHERE RR.SOU_ID = @SOU_ID
				   AND RR.TYPEITEM = 'L'
				   AND RR.TYPERELEVE = @TypeReleve
			GROUP BY RR.SOU_ID, RR.BLO_ID, RR.DIV_ID , RR.ITEM_ID, RR.TYPEITEM;  
	  END;
  END

  SET @r = '';
  IF (ISNULL(@s,'') != '')
    SET @r = @s;

  IF (ISNULL(@v,'') != '')
    SET @r = @r + CHAR(13) + CHAR(10)  +  ISNULL(@v,'');
  	 
  RETURN @r;
    
END
GO

--------------------------

IF OBJECT_ID(N'dbo.fn_GetProductCompositionConcat', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.fn_GetProductCompositionConcat ;
GO

 CREATE FUNCTION [dbo].fn_GetProductCompositionConcat  
( @TypeReleve VARCHAR(1), 
  @SFMode   VARCHAR(3),
  @SOU_ID   VARCHAR(20),
  @ITEM_ID  VARCHAR(20),  
  @BLO_ID   VARCHAR(3),
  @DIV_ID   VARCHAR(3),
  @PRO_ID   VARCHAR(20),
  @COUUM    VARCHAR(2),
  @TYPEITEM VARCHAR(1)
  )
RETURNS VARCHAR(2000)
AS 
BEGIN
  DECLARE @s         VARCHAR(2000);  
  DECLARE @sBlock    VARCHAR(200);  
  DECLARE @sDivision VARCHAR(200);  
  DECLARE @sMult     VARCHAR(30);  
  DECLARE @sTitre    VARCHAR(250);  
  DECLARE @SECTION   DECIMAL(18,6);
  DECLARE @QTEUM     VARCHAR(2)
  DECLARE @QTE       DECIMAL(18,6)
  DECLARE @sEspace   VARCHAR(30);  

  SET @sEspace = '        ';

  IF @TypeReleve = 'P'
  BEGIN
	  SELECT @sBlock = B.[DESC] , 
			 @sMult  = CASE WHEN B.MULT = 1 THEN ' ' ELSE ' x ' + LTRIM(STR(B.MULT)) END 
		FROM SOUBLO B 
	   WHERE B.SOU_ID = @SOU_ID
		 AND  B.BLO_ID = @BLO_ID;

	  SELECT @sDivision = D.[DESC] FROM SOUDIV D 
	   WHERE D.SOU_ID = @SOU_ID
		 AND  D.DIV_ID = @DIV_ID;
	
	  SET @sTitre = @sBlock +  '/ ' + @sDivision + @sMult;

  END ELSE
  IF @TypeReleve = 'U'
  BEGIN
		SET @BLO_ID    = 'U';
		SET @DIV_ID    = 'U';
		SET @sBlock    = '';
		SET @sDivision = '';
		SET @sTitre    = '';
  END;


  IF (@SFMode ='SOU')
  BEGIN
         -- Produits simple
	  IF (@TYPEITEM ='P')
	  BEGIN
		  SELECT @s = COALESCE(@s , N'') + 
					  @sEspace + LTRIM(STR(R.QTE, 10, 2)) + ' ' + R.QTEUM +
					  CHAR(13) + CHAR(10) 
			FROM SOUREL R
			WHERE R.SOU_ID  = @SOU_ID
			  AND R.BLO_ID  = @BLO_ID
			  AND R.DIV_ID  = @DIV_ID
			  AND R.ITEM_ID = @ITEM_ID
			  AND R.TYPERELEVE = @TypeReleve;
	  END ELSE
	  -- Produits d'ensemble
	  IF (@TYPEITEM ='A')
	  BEGIN
	    SELECT @QTE = RR.QTE, @QTEUM = RR.QTEUM , @SECTION = RR.SECTION
			FROM SOUREL RR
			WHERE RR.SOU_ID = @SOU_ID
			AND RR.ITEM_ID = @ITEM_ID
			AND RR.TYPERELEVE = @TypeReleve;

        SELECT   @s = COALESCE(@S , N'') + @sEspace + 
           
		   CASE WHEN SEC.TYPRATIO = 'L' 
		   THEN
		     LTRIM(STR([dbo].fn_GetQuantyProductIn(@SFMode, 'A', @SOU_ID, @ITEM_ID, @PRO_ID) * @QTE * DBO.fn_UM_GetRatioDeConversion(@QTEUM, SE.COUUM, 0),25,2)) 			
		   ELSE 
		     LTRIM(STR([dbo].fn_GetQuantyProductIn(@SFMode, 'A', @SOU_ID, @ITEM_ID, @PRO_ID) * @SECTION,25,2)) 			
		   END  

 		 	+ ' ' + SEC.QTEUM  + ' ->  ' + SE.[DESC] + ' (' +   + LTRIM(STR(SEC.QTE,25,2))   + ' ' +   @COUUM   + ')' + 
		   CHAR(13) + CHAR(10) 

		FROM SOUENS SE, SOUENSCO SEC
		WHERE SE.SOU_ID  = SEC.SOU_ID
		AND SE.ENS_ID  = SEC.ENS_ID
		AND SE.SOU_ID  = @SOU_ID
		AND SE.ENS_ID  = @ITEM_ID
		AND SEC.PRO_ID = @PRO_ID;
	  END ELSE
	  -- Produits de Lots
	  IF (@TYPEITEM ='L')
	  BEGIN
	    SELECT @QTE = RR.QTE, @QTEUM = RR.QTEUM , @SECTION = RR.SECTION
			FROM SOUREL RR
			WHERE RR.SOU_ID = @SOU_ID
			AND RR.ITEM_ID = @ITEM_ID
			AND RR.TYPERELEVE = @TypeReleve;

        SELECT   @s = COALESCE(@S , N'') + @sEspace +          		   
		     LTRIM(STR([dbo].fn_GetQuantyProductIn(@SFMode, 'L', @SOU_ID, @ITEM_ID, @PRO_ID) * @QTE * DBO.fn_UM_GetRatioDeConversion(@QTEUM, SE.COUUM, 0),25,2)) 			
 		 	+ ' ' + SEC.QTEUM  + ' ->  ' + SE.[DESC] + ' (' +   + LTRIM(STR(SEC.QTE,25,2))   + ' ' +   @COUUM   + ')' + 
		   CHAR(13) + CHAR(10) 

		FROM SOULOTS SE, SOULOTSCO SEC
		WHERE SE.SOU_ID = SEC.SOU_ID
		AND SE.LOTS_ID  = SEC.LOTS_ID
		AND SE.SOU_ID   = @SOU_ID
		AND SE.LOTS_ID  = @ITEM_ID
		AND SEC.PRO_ID  = @PRO_ID;
	  END
  END ELSE

  IF (@SFMode ='FAC')
  BEGIN
         -- Produits simple
	  IF (@TYPEITEM ='P')
	  BEGIN
		  SELECT @s = COALESCE(@s , N'') + 
					  @sEspace + LTRIM(STR(R.QTE, 10, 2)) + ' ' + R.QTEUM +
					  CHAR(13) + CHAR(10) 
			FROM FACREL R
			WHERE R.SOU_ID  = @SOU_ID
			  AND  R.BLO_ID = @BLO_ID
			  AND R.DIV_ID  = @DIV_ID
			  AND R.ITEM_ID = @ITEM_ID
			  AND R.TYPERELEVE = @TypeReleve;
	  END ELSE
	  -- Produits d'ensemble
	  IF (@TYPEITEM ='A')
	  BEGIN

	    SELECT @QTE = RR.QTE, @QTEUM = RR.QTEUM , @SECTION = RR.SECTION
			FROM FACREL RR
			WHERE RR.SOU_ID = @SOU_ID
			AND RR.ITEM_ID = @ITEM_ID
			AND RR.TYPERELEVE = @TypeReleve;

        SELECT   @s = COALESCE(@S , N'') + @sEspace + 
           
		   CASE WHEN SEC.TYPRATIO = 'L' 
		   THEN
		     LTRIM(STR([dbo].fn_GetQuantyProductIn(@SFMode, 'A', @SOU_ID, @ITEM_ID, @PRO_ID) * @QTE * DBO.fn_UM_GetRatioDeConversion(@QTEUM, SE.COUUM, 0),25,2)) 			
		   ELSE 
		     LTRIM(STR([dbo].fn_GetQuantyProductIn(@SFMode, 'A', @SOU_ID, @ITEM_ID, @PRO_ID) * @SECTION,25,2)) 			
		   END  

 		 	+ ' ' + SEC.QTEUM  + ' ->  ' + SE.[DESC] + ' (' +   + LTRIM(STR(SEC.QTE,25,2))   + ' ' +   @COUUM   + ')' + 
		   CHAR(13) + CHAR(10) 

		FROM FACENS SE, FACENSCO SEC
		WHERE SE.SOU_ID  = SEC.SOU_ID
		AND SE.ENS_ID  = SEC.ENS_ID
		AND SE.SOU_ID  = @SOU_ID
		AND SE.ENS_ID  = @ITEM_ID
		AND SEC.PRO_ID = @PRO_ID;
	  END ELSE
	  -- Produits de Lots
	  IF (@TYPEITEM ='L')
	  BEGIN
	    SELECT @QTE = RR.QTE, @QTEUM = RR.QTEUM , @SECTION = RR.SECTION
			FROM FACREL RR
			WHERE RR.SOU_ID = @SOU_ID
			AND RR.ITEM_ID = @ITEM_ID
			AND RR.TYPERELEVE = @TypeReleve;

        SELECT   @s = COALESCE(@s , N'') + @sEspace +          		   
		     LTRIM(STR([dbo].fn_GetQuantyProductIn(@SFMode, 'L', @SOU_ID, @ITEM_ID, @PRO_ID) * @QTE * DBO.fn_UM_GetRatioDeConversion(@QTEUM, SE.COUUM, 0),25,2)) 			
 		 	+ ' ' + SEC.QTEUM  + ' ->  ' + SE.[DESC] + ' (' +   + LTRIM(STR(SEC.QTE,25,2))   + ' ' +   @COUUM   + ')' + 
		   CHAR(13) + CHAR(10) 

		FROM FACLOTS SE, FACLOTSCO SEC
		WHERE SE.SOU_ID = SEC.SOU_ID
		AND SE.LOTS_ID  = SEC.LOTS_ID
		AND SE.SOU_ID   = @SOU_ID
		AND SE.LOTS_ID  = @ITEM_ID
		AND SEC.PRO_ID  = @PRO_ID;
	  END
  END;


  IF ISNULL(@s,'') != '' 
  BEGIN  
	SET @s = @sTitre  + CHAR(13) + CHAR(10) +  @s;
  END

  RETURN (ISNULL(@s,''));

END
GO

-----------------------------

IF OBJECT_ID(N'dbo.fn_GetQuantyProductIn', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.fn_GetQuantyProductIn ;
GO

 CREATE FUNCTION [dbo].fn_GetQuantyProductIn  
( @SFMode VARCHAR(3),
  @TYPEITEM VARCHAR(1),
  @SOU_ID VARCHAR(20),
  @ITEM_ID VARCHAR(20),  
  @PRO_ID VARCHAR(20)
  )
RETURNS VARCHAR(2000)
AS 
BEGIN
  DECLARE @R DECIMAL(18,6)

  IF (@SFMode ='SOU')
  BEGIN    
	IF (@TYPEITEM = 'A')
	BEGIN
		SELECT @R = CASE WHEN (SEC.TYPRATIO = 'L') AND (SE.COUUM != '' ) AND ([dbo].[fn_UM_GetNatureUnite](SE.COUUM) = 'L') 
					THEN CASE 
							WHEN (ISNULL(SEC.DIV,0.0) != 0) 
							THEN (ISNULL(SEC.QTE,0.0) / SEC.DIV) * DBO.fn_UM_GetRatioDeConversion (SE.COUUM , SEC.DIVUM,  0)
							ELSE 0 
						END
					ELSE SEC.QTE
					END

		FROM SOUENS SE, SOUENSCO SEC
		WHERE SE.SOU_ID  = SEC.SOU_ID
		AND SE.ENS_ID  = SEC.ENS_ID
		AND SE.SOU_ID  = @SOU_ID
		AND SE.ENS_ID  = @ITEM_ID
		AND SEC.PRO_ID = @PRO_ID;
    END ELSE
	IF (@TYPEITEM = 'L')
	BEGIN
		SELECT @R = SEC.QTE
		FROM SOULOTS SE, SOULOTSCO SEC
		WHERE SE.SOU_ID = SEC.SOU_ID
		AND SE.LOTS_ID  = SEC.LOTS_ID
		AND SE.SOU_ID   = @SOU_ID
		AND SE.LOTS_ID  = @ITEM_ID
		AND SEC.PRO_ID  = @PRO_ID;
	END

  END ELSE
  IF (@SFMode ='FAC')
  BEGIN
	IF (@TYPEITEM = 'A')
	BEGIN
		SELECT @R = CASE WHEN (SEC.TYPRATIO = 'L') AND (SE.COUUM != '' ) AND ([dbo].[fn_UM_GetNatureUnite](SE.COUUM) = 'L') 
					THEN CASE 
							WHEN (ISNULL(SEC.DIV,0.0) != 0) 
							THEN (ISNULL(SEC.QTE,0.0) / SEC.DIV) * DBO.fn_UM_GetRatioDeConversion (SE.COUUM , SEC.DIVUM,  0)
							ELSE 0 
						END
					ELSE SEC.QTE
					END

		FROM FACENS SE, FACENSCO SEC
		WHERE SE.SOU_ID  = SEC.SOU_ID
		AND SE.ENS_ID  = SEC.ENS_ID
		AND SE.SOU_ID  = @SOU_ID
		AND SE.ENS_ID  = @ITEM_ID
		AND SEC.PRO_ID = @PRO_ID;
    END ELSE
	IF (@TYPEITEM = 'L')
	BEGIN
		SELECT @R = SEC.QTE
		FROM FACLOTS SE, FACLOTSCO SEC
		WHERE SE.SOU_ID = SEC.SOU_ID
		AND SE.LOTS_ID  = SEC.LOTS_ID
		AND SE.SOU_ID   = @SOU_ID
		AND SE.LOTS_ID  = @ITEM_ID
		AND SEC.PRO_ID  = @PRO_ID;
	END
  END

  RETURN @R
END
GO

---------------------------

IF OBJECT_ID(N'dbo.sp_CalculUsage_Assembly', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_CalculUsage_Assembly ;
GO

 CREATE PROCEDURE [dbo].[sp_CalculUsage_Assembly] 
 (@SFMode VARCHAR(3), 
  @SOU_ID VARCHAR(20))
AS BEGIN

  DECLARE  @TITLE       VARCHAR(60);
  DECLARE  @DESCR       VARCHAR(2000);  
  DECLARE  @SOUID       VARCHAR(20);
  DECLARE  @PRO_ID      VARCHAR(20);
  DECLARE  @INASSEMBLIE VARCHAR(2000);  

  IF (@SFMode ='SOU')
  BEGIN
  	  SELECT SP.UniqueId, SP.SOU_ID , SP.PRO_ID, AA.DESCR FROM SOUPRO SP LEFT JOIN  --SP.INASSEMBLIE
		   (SELECT E.SOU_ID, 
				   C.PRO_ID , 
				   DESCR = dbo.fn_CompositionConcat('SOU', 'A' , E.SOU_ID, C.PRO_ID) 
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
			AND (AA.DESCR IS NOT NULL) 
  END ELSE
  IF (@SFMode ='FAC')
  BEGIN
	  SELECT SP.UniqueId, SP.SOU_ID , SP.PRO_ID, AA.DESCR FROM FACPRO SP LEFT JOIN  --SP.INASSEMBLIE
		   (SELECT E.SOU_ID, 
				   C.PRO_ID , 
				   DESCR = dbo.fn_CompositionConcat('FAC', 'A', E.SOU_ID, C.PRO_ID) 
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
			AND (AA.DESCR IS NOT NULL) 

  END;


END
GO

------------------------------

IF OBJECT_ID(N'dbo.sp_CalculUsage_Lot', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_CalculUsage_Lot ;
GO

 CREATE PROCEDURE [dbo].[sp_CalculUsage_Lot] 
 (@SFMode VARCHAR(3), 
  @SOU_ID VARCHAR(20))
AS BEGIN

  DECLARE  @TITLE       VARCHAR(60);
  DECLARE  @DESCR       VARCHAR(2000);  
  DECLARE  @SOUID       VARCHAR(20);
  DECLARE  @PRO_ID      VARCHAR(20);

  IF (@SFMode ='SOU')
  BEGIN
  	  SELECT SP.UniqueId, SP.SOU_ID , SP.PRO_ID, AA.DESCR FROM SOUPRO SP LEFT JOIN  --SP.INASSEMBLIE
		   (SELECT E.SOU_ID, 
				   C.PRO_ID , 
				   DESCR = dbo.fn_CompositionConcat('SOU', 'L', E.SOU_ID, C.PRO_ID) 
			FROM SOULOTS E, SOULOTSCO C , SOUREL L
			WHERE E.LOTS_ID = C.LOTS_ID
			  AND E.SOU_ID  = C.SOU_ID
			  AND L.SOU_ID  = E.SOU_ID
			  AND L.ITEM_ID = E.LOTS_ID
			  AND C.SOU_ID  = @SOU_ID
			GROUP BY  E.SOU_ID, C.PRO_ID
			) AA

			ON  SP.SOU_ID = AA.SOU_ID 
			AND SP.PRO_ID = AA.PRO_ID
			WHERE  SP.SOU_ID =  @SOU_ID
			AND (AA.DESCR IS NOT NULL) 
  END ELSE
  IF (@SFMode ='FAC')
  BEGIN
	  SELECT SP.UniqueId, SP.SOU_ID , SP.PRO_ID, AA.DESCR FROM FACPRO SP LEFT JOIN  --SP.INASSEMBLIE
		   (SELECT E.SOU_ID, 
				   C.PRO_ID , 
				   DESCR = dbo.fn_CompositionConcat('FAC', 'L', E.SOU_ID, C.PRO_ID) 
			FROM FACLOTS E, FACLOTSCO C , FACREL L
			WHERE E.LOTS_ID = C.LOTS_ID
			  AND E.SOU_ID  = C.SOU_ID
			  AND L.SOU_ID  = E.SOU_ID
			  AND L.ITEM_ID = E.LOTS_ID
			  AND C.SOU_ID  = @SOU_ID
			GROUP BY  E.SOU_ID, C.PRO_ID
			) AA

			ON  SP.SOU_ID = AA.SOU_ID 
			AND SP.PRO_ID = AA.PRO_ID
			WHERE  SP.SOU_ID =  @SOU_ID
			AND (AA.DESCR IS NOT NULL) 

  END;
END
GO

-------------------------

IF OBJECT_ID(N'dbo.sp_CalculUsage_Product', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_CalculUsage_Product ;
GO

 CREATE PROCEDURE [dbo].[sp_CalculUsage_Product]
 (@TypeReleve VARCHAR(1), 
  @SFMode VARCHAR(3), 
  @SOU_ID VARCHAR(20))
AS BEGIN

  DECLARE  @TITLE       VARCHAR(60);
  DECLARE  @DESCR       VARCHAR(2000);  
  DECLARE  @SOUID       VARCHAR(20);
  DECLARE  @PRO_ID      VARCHAR(20);
  
  IF (@SFMode ='SOU')
  BEGIN     
    SELECT SP2.UniqueId, SP2.SOU_ID , SP2.PRO_ID, 
		DESCR = dbo.fn_GetProductComposition(@TypeReleve, 'SOU', SP2.SOU_ID, SP2.PRO_ID, SP2.COUUM)               
	FROM SOUPRO SP2
    WHERE SP2.SOU_ID =  @SOU_ID
  
  END ELSE

  IF (@SFMode ='FAC')
  BEGIN
    SELECT SP2.UniqueId, SP2.SOU_ID , SP2.PRO_ID, 
		DESCR = dbo.fn_GetProductComposition(@TypeReleve, 'FAC', SP2.SOU_ID, SP2.PRO_ID, SP2.COUUM)               
	FROM FACPRO SP2
    WHERE SP2.SOU_ID =  @SOU_ID
  END;
END
GO

----------------------------



