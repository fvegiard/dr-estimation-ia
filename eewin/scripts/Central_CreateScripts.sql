IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_UM_USERS_Update')
  DROP PROCEDURE up_UM_USERS_Update
GO

CREATE PROCEDURE [dbo].[up_UM_USERS_Update] (
  @UniqueId bigint,
  @USER_ID varchar(20),
  @NAME varchar(30),
  @EMAIL varchar(30),
  @BRANCH_ID varchar(20),
  @ROLE_ID INT,
  @VALIDATEFROM INT,
  @PSW varchar(12),
  @ACTIVE bit,
  @SORTBRANCH_CODE varchar(20),
  @OWC varchar(2)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO UM_USERS (
    [USER_ID],
    [NAME],
    [EMAIL],
    [BRANCH_ID],
    [ROLE_ID],
    [VALIDATEFROM],
    [PSW],
    [ACTIVE],
    [SORTBRANCH_CODE],
    [OWC],
    SysDate)
  VALUES (
    @USER_ID,
    @NAME,
    @EMAIL,
    @BRANCH_ID,
    @ROLE_ID,
    @VALIDATEFROM,
    @PSW,
    @ACTIVE,
    @SORTBRANCH_CODE,
    @OWC,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    UM_USERS
  SET
    [USER_ID] = @USER_ID,
    [NAME] = @NAME,
    [EMAIL] = @EMAIL,
    [BRANCH_ID] = @BRANCH_ID,
    [ROLE_ID] = @ROLE_ID,
    [VALIDATEFROM] = @VALIDATEFROM,
    [PSW] = @PSW,
    [ACTIVE] = @ACTIVE,
    [SORTBRANCH_CODE] = @SORTBRANCH_CODE,
    [OWC] = @OWC,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_UM_REGIONS_Update')
  DROP PROCEDURE up_UM_REGIONS_Update
GO
    
  
CREATE PROCEDURE [dbo].[up_UM_REGIONS_Update] (
  @UniqueId bigint,
  @REGION_ID varchar(20),
  @REGION_CODE varchar(20),
  @DIV_ID      varchar(3),
  @WOL_ID  varchar(20),  
  @NAME varchar(30),
  @ORDRE varchar(6)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO UM_REGIONS (
    [REGION_ID],
    [REGION_CODE],
    [DIV_ID],
    [WOL_ID],
    [NAME],    
    [ORDRE],    
    SysDate)
  VALUES (
    @REGION_ID,
    @REGION_CODE,
    @DIV_ID,
    @WOL_ID,
    @NAME,    
    @ORDRE,    
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    UM_REGIONS
  SET
    [REGION_ID] = @REGION_ID,  
    [REGION_CODE] = @REGION_CODE,  
    [DIV_ID] = @DIV_ID,  
    [WOL_ID] = @WOL_ID,
    [NAME] = @NAME,
    [ORDRE] = @ORDRE,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_UM_AREAS_Update')
  DROP PROCEDURE up_UM_AREAS_Update
GO  

CREATE PROCEDURE [dbo].[up_UM_AREAS_Update] (
  @UniqueId bigint,
  @AREA_ID  varchar(20),  
  @AREA_CODE  varchar(20),  
  @NAME varchar(30),
  @REGION_ID varchar(20) ,
  @ORDRE varchar(6)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO UM_AREAS (
    [AREA_ID],
    [AREA_CODE],
    [NAME],  
    [REGION_ID],
    [ORDRE],
    SysDate)
  VALUES (
    @AREA_ID,
    @AREA_CODE,
    @NAME,  
    @REGION_ID,
    @ORDRE,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    UM_AREAS
  SET
    [AREA_ID] = @AREA_ID,
    [AREA_CODE] = @AREA_CODE,
    [NAME] = @NAME,
    [REGION_ID] = @REGION_ID,    
    [ORDRE] = @ORDRE,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_UM_BUSINESSUNIT_Update')
  DROP PROCEDURE up_UM_BUSINESSUNIT_Update
GO  

CREATE PROCEDURE [dbo].[up_UM_BUSINESSUNIT_Update] (
  @UniqueId bigint,
  @BU_ID  varchar(20),  
  @BU_CODE  varchar(20), 
  @NAME varchar(30),
  @ORDRE varchar(6)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO UM_BUSINESSUNIT (
    [BU_ID],
    [BU_CODE],
    [NAME],  
    [ORDRE],
    SysDate)
  VALUES (
    @BU_ID,
    @BU_CODE,
    @NAME,  
    @ORDRE,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    UM_BUSINESSUNIT
  SET
    [BU_ID] = @BU_ID,
    [BU_CODE] = @BU_CODE,
    [NAME] = @NAME,
    [ORDRE] = @ORDRE,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_UM_BRANCHS_Update')
  DROP PROCEDURE up_UM_BRANCHS_Update
GO

CREATE PROCEDURE [dbo].[up_UM_BRANCHS_Update] (
  @UniqueId bigint,
  @BRANCH_ID varchar(20),
  @BRANCH_CODE varchar(20),
  @AREA_ID  varchar(20),
  @NAME varchar(30),
  @BU_ID varchar(20),
  @LOGOPATH  varchar(200), 
  @PROFITC_NO  varchar(1), 
  @CLIENT_NO  varchar(20), 
  @ACTIVE   bit,    
  @ORDRE varchar(6)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO UM_BRANCHS (
    
  [BRANCH_ID],  
  [BRANCH_CODE],  
  [AREA_ID],
  [NAME],
  [BU_ID],
  [LOGOPATH],
  [PROFITC_NO],
  [CLIENT_NO],
  [ACTIVE],    
  [ORDRE],
    SysDate)
  VALUES (
  @BRANCH_ID,  
  @BRANCH_CODE,  
  @AREA_ID,
  @NAME,
  @BU_ID,
  @LOGOPATH,
  @PROFITC_NO,
  @CLIENT_NO,
  @ACTIVE,
  @ORDRE,
  GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    UM_BRANCHS
  SET
    [BRANCH_ID] = @BRANCH_ID,
    [BRANCH_CODE] = @BRANCH_CODE,
    [AREA_ID] = @AREA_ID,
    [NAME] = @NAME,
    [BU_ID] = @BU_ID,
    [LOGOPATH] = @LOGOPATH,
    [PROFITC_NO] = @PROFITC_NO,
    [CLIENT_NO] = @CLIENT_NO,
    [ACTIVE] = @ACTIVE,
    [ORDRE] = @ORDRE,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_UM_USERREGIONS_Update')
  DROP PROCEDURE up_UM_USERREGIONS_Update
GO

CREATE PROCEDURE [dbo].[up_UM_USERREGIONS_Update] (
  @UniqueId bigint,
  @USER_ID  varchar(20),  
  @TERITORY_ID varchar(20),
  @TERITORY_TYPE varchar(1),
  @ORDRE  varchar(6)    
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO UM_USERREGIONS (
    [USER_ID],
    [TERITORY_ID],  
    [TERITORY_TYPE],
    [ORDRE],  
    SysDate)
  VALUES (
    @USER_ID,
    @TERITORY_ID,  
    @TERITORY_TYPE,
    @ORDRE,  
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    UM_USERREGIONS
  SET
    [USER_ID] = @USER_ID,
    [TERITORY_TYPE] = @TERITORY_TYPE,
    [TERITORY_ID] = @TERITORY_ID,
    [ORDRE] = @ORDRE,  
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_UM_USERREGIONS_Delete')
  DROP PROCEDURE up_UM_USERREGIONS_Delete
GO

CREATE PROCEDURE [dbo].[up_UM_USERREGIONS_Delete] (
  @UniqueId bigint
) AS
BEGIN
  DELETE FROM UM_USERREGIONS WHERE UniqueId = @UniqueId
END
GO  


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_UM_USERS_Delete')
  DROP PROCEDURE up_UM_USERS_Delete
GO

CREATE PROCEDURE [dbo].[up_UM_USERS_Delete] (
  @UniqueId bigint
) AS
BEGIN
  DELETE FROM UM_USERS WHERE UniqueId = @UniqueId
END
GO    
  
IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_UM_AREAS_Delete')
  DROP PROCEDURE up_UM_AREAS_Delete
GO

CREATE PROCEDURE [dbo].[up_UM_AREAS_Delete] (
  @UniqueId bigint
) AS
BEGIN
  DELETE FROM UM_AREAS WHERE UniqueId = @UniqueId
END
GO  

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_UM_REGIONS_Delete')
  DROP PROCEDURE up_UM_REGIONS_Delete
GO

CREATE PROCEDURE [dbo].[up_UM_REGIONS_Delete] (
  @UniqueId bigint
) AS
BEGIN
  DELETE FROM UM_REGIONS WHERE UniqueId = @UniqueId
END
GO  


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_UM_BRANCHS_Delete')
  DROP PROCEDURE up_UM_BRANCHS_Delete
GO

CREATE PROCEDURE [dbo].up_UM_BRANCHS_Delete (
  @UniqueId bigint
) AS
BEGIN
  DELETE FROM UM_BRANCHS WHERE UniqueId = @UniqueId
END
GO  


IF OBJECT_ID(N'dbo.sp_UpdateToSortCols', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_UpdateToSortCols ;
GO

CREATE PROCEDURE [dbo].sp_UpdateToSortCols
AS BEGIN

  DECLARE  @BRANCH_ID  VARCHAR(20);
  DECLARE  @BRANCH_CODE VARCHAR(20);

  DECLARE CUR_1 CURSOR FOR 

   SELECT A.BRANCH_ID, A.BRANCH_CODE
   FROM UM_BRANCHS A
      
  OPEN CUR_1
  FETCH NEXT FROM CUR_1
  INTO @BRANCH_ID, @BRANCH_CODE

  WHILE @@FETCH_STATUS = 0
   BEGIN
     UPDATE UM_USERS
        SET SORTBRANCH_CODE = @BRANCH_CODE
      WHERE BRANCH_ID = @BRANCH_ID

     FETCH NEXT FROM CUR_1
     INTO @BRANCH_ID, @BRANCH_CODE
   END
  CLOSE CUR_1;
  DEALLOCATE CUR_1;

END
GO

