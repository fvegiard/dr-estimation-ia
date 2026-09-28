
---------------------------------------------
--- CREER la colonne ORDRE POUR SOUDIV ET
--- INITIALISER L'ORDRE D'AFFICHAGE DES DIVISIONS POUR LES SOUMISSIONS
--- Ce script s'execute uniquement si la colonne ORDRE de la table SOUDIV existe
--------------------------------------------- 


IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUDIV'
    AND [COLUMN_NAME] = 'ORDRE' )

BEGIN
  ALTER TABLE
    SOUDIV
  ADD
    ORDRE varchar(6);

  EXECUTE ('
	  DECLARE @SOU_ID   VARCHAR(20)	  
	  DECLARE @ORDRE    VARCHAR(6)	    
	  DECLARE @UniqueId BIGINT;

	  DECLARE CUR_2 CURSOR FOR 
		  SELECT SOU_ID
		  FROM SOUDIV
		  GROUP BY SOU_ID 
      
	  OPEN CUR_2
	  FETCH NEXT FROM CUR_2
	  INTO @SOU_ID

	  WHILE @@FETCH_STATUS = 0
	  BEGIN
		  DECLARE CUR_3 CURSOR FOR 
		  SELECT  ROW_NUMBER() OVER(ORDER BY [DESC] ASC), UniqueId
		  FROM SOUDIV
		  WHERE SOU_ID = @SOU_ID

		  OPEN CUR_3
		  FETCH NEXT FROM CUR_3
		  INTO @ORDRE, @UniqueId

		  WHILE @@FETCH_STATUS = 0
		  BEGIN
			UPDATE SOUDIV 
			SET ORDRE = @ORDRE 
			WHERE SOU_ID = @SOU_ID  
			AND UniqueId = @UniqueId;  

			FETCH NEXT FROM CUR_3
			INTO @ORDRE, @UniqueId
		  END

		CLOSE CUR_3;
		DEALLOCATE CUR_3;

		FETCH NEXT FROM CUR_2
		INTO @SOU_ID
	
	  END
	  CLOSE CUR_2;
	  DEALLOCATE CUR_2');

END;
GO


  -- DROP PROCEDURE up_SOUDIV_Update
IF OBJECT_ID(N'dbo.up_SOUDIV_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOUDIV_Update;
GO

  -- CREATE PROCEDURE up_SOUDIV_Update
CREATE PROCEDURE [dbo].[up_SOUDIV_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @DIV_ID varchar(3),
  @DESC varchar(40),
  @ORDRE varchar(6)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUDIV (
    [SOU_ID],
    [DIV_ID],
    [DESC],
	[ORDRE],
    SysDate)
  VALUES (
    @SOU_ID,
    @DIV_ID,
    @DESC,
	@ORDRE,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUDIV
  SET
    [SOU_ID] = @SOU_ID,
    [DIV_ID] = @DIV_ID,
    [DESC] = @DESC,
    [ORDRE] = @ORDRE,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


---------------------------------------------
--- CREER la colonne ORDRE POUR SOUBLO ET
--- INITIALISER L'ORDRE D'AFFICHAGE DES DIVISIONS POUR LES SOUMISSIONS
--- Ce script s'execute uniquement si la colonne ORDRE de la table SOUBLO existe
--------------------------------------------- 


IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUBLO'
    AND [COLUMN_NAME] = 'ORDRE' )

BEGIN
  ALTER TABLE
    SOUBLO
  ADD
    ORDRE varchar(6);

  EXECUTE ('
	  DECLARE @SOU_ID   VARCHAR(20)	  
	  DECLARE @ORDRE    VARCHAR(6)	    
	  DECLARE @UniqueId BIGINT;

	  DECLARE CUR_2 CURSOR FOR 
		  SELECT SOU_ID
		  FROM SOUBLO
		  GROUP BY SOU_ID 
      
	  OPEN CUR_2
	  FETCH NEXT FROM CUR_2
	  INTO @SOU_ID

	  WHILE @@FETCH_STATUS = 0
	  BEGIN
		  DECLARE CUR_3 CURSOR FOR 
		  SELECT  ROW_NUMBER() OVER(ORDER BY [DESC] ASC), UniqueId
		  FROM SOUBLO
		  WHERE SOU_ID = @SOU_ID

		  OPEN CUR_3
		  FETCH NEXT FROM CUR_3
		  INTO @ORDRE, @UniqueId

		  WHILE @@FETCH_STATUS = 0
		  BEGIN
			UPDATE SOUBLO 
			SET ORDRE = @ORDRE 
			WHERE SOU_ID = @SOU_ID  
			AND UniqueId = @UniqueId;  

			FETCH NEXT FROM CUR_3
			INTO @ORDRE, @UniqueId
		  END

		CLOSE CUR_3;
		DEALLOCATE CUR_3;

		FETCH NEXT FROM CUR_2
		INTO @SOU_ID
	
	  END
	  CLOSE CUR_2;
	  DEALLOCATE CUR_2');

END;
GO

  -- DROP PROCEDURE up_SOUBLO_Update
IF OBJECT_ID(N'dbo.up_SOUBLO_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOUBLO_Update;
GO

  -- CREATE PROCEDURE up_SOUBLO_Update
CREATE PROCEDURE [dbo].[up_SOUBLO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DESC varchar(40),
  @MULT int,
  @ORDRE varchar(6)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUBLO (
    [SOU_ID],
    [BLO_ID],
    [DESC],
    [MULT],
	[ORDRE],
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DESC,
    @MULT,
	@ORDRE,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUBLO
  SET
    [SOU_ID] = @SOU_ID,
    [BLO_ID] = @BLO_ID,
    [DESC] = @DESC,
    [MULT] = @MULT,
    [ORDRE] = @ORDRE,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO
---------------------


---------------------------------------------
--- CREER la colonne ORDRE POUR FACDIV ET
--- INITIALISER L'ORDRE D'AFFICHAGE DES DIVISIONS POUR LES SOUMISSIONS
--- Ce script s'execute uniquement si la colonne ORDRE de la table FACDIV existe
--------------------------------------------- 


IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACDIV'
    AND [COLUMN_NAME] = 'ORDRE' )

BEGIN
  ALTER TABLE
    FACDIV
  ADD
    ORDRE varchar(6);

  EXECUTE ('
	  DECLARE @SOU_ID   VARCHAR(20)	  
	  DECLARE @ORDRE    VARCHAR(6)	    
	  DECLARE @UniqueId BIGINT;

	  DECLARE CUR_2 CURSOR FOR 
		  SELECT SOU_ID
		  FROM FACDIV
		  GROUP BY SOU_ID 
      
	  OPEN CUR_2
	  FETCH NEXT FROM CUR_2
	  INTO @SOU_ID

	  WHILE @@FETCH_STATUS = 0
	  BEGIN
		  DECLARE CUR_3 CURSOR FOR 
		  SELECT  ROW_NUMBER() OVER(ORDER BY [DESC] ASC), UniqueId
		  FROM FACDIV
		  WHERE SOU_ID = @SOU_ID

		  OPEN CUR_3
		  FETCH NEXT FROM CUR_3
		  INTO @ORDRE, @UniqueId

		  WHILE @@FETCH_STATUS = 0
		  BEGIN
			UPDATE FACDIV 
			SET ORDRE = @ORDRE 
			WHERE SOU_ID = @SOU_ID  
			AND UniqueId = @UniqueId;  

			FETCH NEXT FROM CUR_3
			INTO @ORDRE, @UniqueId
		  END

		CLOSE CUR_3;
		DEALLOCATE CUR_3;

		FETCH NEXT FROM CUR_2
		INTO @SOU_ID
	
	  END
	  CLOSE CUR_2;
	  DEALLOCATE CUR_2');

END;
GO

  -- DROP PROCEDURE up_FACDIV_Update
IF OBJECT_ID(N'dbo.up_FACDIV_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_FACDIV_Update;
GO

  -- CREATE PROCEDURE up_FACDIV_Update
CREATE PROCEDURE [dbo].[up_FACDIV_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @DIV_ID varchar(3),
  @DESC varchar(40),
  @ORDRE varchar(6)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACDIV (
    [SOU_ID],
    [DIV_ID],
    [DESC],
	[ORDRE],
    SysDate)
  VALUES (
    @SOU_ID,
    @DIV_ID,
    @DESC,
	@ORDRE,
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
    [DESC] = @DESC,
    [ORDRE] = @ORDRE,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


---------------------------------------------
--- CREER la colonne ORDRE POUR FACBLO ET
--- INITIALISER L'ORDRE D'AFFICHAGE DES DIVISIONS POUR LES SOUMISSIONS
--- Ce script s'execute uniquement si la colonne ORDRE de la table FACBLO existe
--------------------------------------------- 


IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACBLO'
    AND [COLUMN_NAME] = 'ORDRE' )

BEGIN
  ALTER TABLE
    FACBLO
  ADD
    ORDRE varchar(6);

  EXECUTE ('
	  DECLARE @SOU_ID   VARCHAR(20)	  
	  DECLARE @ORDRE    VARCHAR(6)	    
	  DECLARE @UniqueId BIGINT;

	  DECLARE CUR_2 CURSOR FOR 
		  SELECT SOU_ID
		  FROM FACBLO
		  GROUP BY SOU_ID 
      
	  OPEN CUR_2
	  FETCH NEXT FROM CUR_2
	  INTO @SOU_ID

	  WHILE @@FETCH_STATUS = 0
	  BEGIN
		  DECLARE CUR_3 CURSOR FOR 
		  SELECT  ROW_NUMBER() OVER(ORDER BY [DESC] ASC), UniqueId
		  FROM FACBLO
		  WHERE SOU_ID = @SOU_ID

		  OPEN CUR_3
		  FETCH NEXT FROM CUR_3
		  INTO @ORDRE, @UniqueId

		  WHILE @@FETCH_STATUS = 0
		  BEGIN
			UPDATE FACBLO 
			SET ORDRE = @ORDRE 
			WHERE SOU_ID = @SOU_ID  
			AND UniqueId = @UniqueId;  

			FETCH NEXT FROM CUR_3
			INTO @ORDRE, @UniqueId
		  END

		CLOSE CUR_3;
		DEALLOCATE CUR_3;

		FETCH NEXT FROM CUR_2
		INTO @SOU_ID
	
	  END
	  CLOSE CUR_2;
	  DEALLOCATE CUR_2');

END;
GO

  -- DROP PROCEDURE up_FACBLO_Update
IF OBJECT_ID(N'dbo.up_FACBLO_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_FACBLO_Update;
GO

  -- CREATE PROCEDURE up_FACBLO_Update
CREATE PROCEDURE [dbo].[up_FACBLO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DESC varchar(40),
  @MULT int,
  @ORDRE varchar(6)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACBLO (
    [SOU_ID],
    [BLO_ID],
    [DESC],
    [MULT],
	[ORDRE],
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DESC,
    @MULT,
	@ORDRE,
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
    [MULT] = @MULT,
    [ORDRE] = @ORDRE,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


