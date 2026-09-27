-- SP -- UPDATE -- [up_CopySoumis_Full] -- START --

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_CopySoumis_Full')
  DROP PROCEDURE up_CopySoumis_Full
GO

CREATE PROCEDURE [dbo].[up_CopySoumis_Full] (
    @CopySOU_ID		varchar(20),	-- SOU_ID de la soumission à copy/paster 
	@PasteSOU_ID	varchar(20)		-- SOU_ID de la soumission pasté. Doit être fournir car logique dans EE
									-- Retourne : L'identité du record pasté dans la table soumis
)
AS
BEGIN
	SET NOCOUNT ON;

		-- Clone tous les records details ayant le SOU_ID reçu de la table soumission
	EXEC up_CloneRecords 'SOUREL',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOUBLO',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOUDIV',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOUAMD',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOUWEBLOG',	'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOUPRO',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOUENS',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOUENSCO',	'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOULOTS',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOULOTSCO',	'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'

		-- Clone le record d'entête et retourne l'identité du nouveau record
		-- Si ca saute avant, on vas simplement avoir un tas de détails sans entête, facile à cleaner au besoin
	EXEC up_CloneRecords 'SOUMIS',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_SOU_ID'

		-- Met à jour les informations d'entêtes
			--WEXPORTED	= 0, -- EM : Pour la version Interne, Assigner
    UPDATE 
      SOUMIS 
		SET 
      ORIGIN    = 'C',    -- TO_CopyPaste en Delphi
      ORIGINREF = @PasteSOU_ID,
      NODOC		  = '', 
			DESCDOC		= SUBSTRING('+ ' + DESCDOC, 1, 200), -- 2019-06-04 EE-???? EMadore - Doit tronquer si plus de 200 char sinon saute
			DATECREE	= GetDate(), 
			DATEDOC		= NULL
		WHERE 
      SOU_ID = @PasteSOU_ID

		-- Retounre l'identité du record de soumission d'entête
    DECLARE @TempResult INT

	SELECT	@TempResult = UniqueID 
		FROM  SOUMIS
		WHERE SOU_ID = @PasteSOU_ID

	RETURN @TempResult
END
GO

-- SP -- UPDATE -- [up_CopySoumis_Full] -- END --


-- SP -- UPDATE -- [up_CopyFactures_Full] -- START --


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_CopyFactures_Full')
  DROP PROCEDURE up_CopyFactures_Full
GO

CREATE PROCEDURE [dbo].[up_CopyFactures_Full] (
    @CopySOU_ID		varchar(20),	-- SOU_ID de la facture à copy/paster 
    @PasteSOU_ID	varchar(20)	-- SOU_ID de la facture pasté. Doit être fournir car logique dans EE
									-- Retourne : L'identité du record pasté dans la table soumis
)
AS
BEGIN
	SET NOCOUNT ON;

		-- Clone tous les records details ayant le SOU_ID reçu de la table soumission
	EXEC up_CloneRecords 'FACREL',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACBLO',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACDIV',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACAMD',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACWEBLOG',	'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACPRO',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACENS',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACENSCO',	'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACLOTS',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACLOTSCO',	'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'

		-- Clone le record d'entête et retourne l'identité du nouveau record
		-- Si ca saute avant, on vas simplement avoir un tas de détails sans entête, facile à cleaner au besoin
	EXEC up_CloneRecords 'FACTURES',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_SOU_ID'

		-- Met à jour les informations d'entêtes
			--WEXPORTED	= 0, -- EM : Pour la version Interne, Assigner
    UPDATE 
      FACTURES 
		SET 
      ORIGIN    = 'C',          -- TO_CopyPaste en Delphi
      ORIGINREF = @CopySOU_ID,  
      NODOC		  = '', 
			DESCDOC		= SUBSTRING('+ ' + DESCDOC, 1, 200), -- 2019-06-04 EE-???? EMadore - Doit tronquer si plus de 200 char sinon saute
			DATECREE	= GetDate(), 
			DATEDOC		= NULL
		WHERE 
      SOU_ID = @PasteSOU_ID
	
		-- Retounre l'identité du record de soumission d'entête
    DECLARE @TempResult INT

	SELECT	@TempResult = UniqueID 
		FROM  FACTURES
		WHERE SOU_ID = @PasteSOU_ID

	RETURN @TempResult
END
GO

-- SP -- UPDATE -- [up_CopyFactures_Full] -- END --
