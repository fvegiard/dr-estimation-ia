
  -- colonnes des vue user
IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE Table_Name = 'USR_GRIDVIEW')
BEGIN
  DROP TABLE USR_GRIDVIEW
END
GO


  CREATE TABLE [dbo].USR_GRIDVIEW (
  UniqueId          bigint       IDENTITY(1,1) NOT NULL,
  [ORDRE]           varchar(6),
  [VIEW_ID]         [varchar](20),     
  [DESCR]           [varchar](40),     
  [LIST_ID]         [varchar](8),         
  [SysDate]         datetime     NOT NULL DEFAULT (getdate()),
    )

GO

IF OBJECT_ID(N'dbo.up_USR_GRIDVIEW_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_USR_GRIDVIEW_Update ;
GO

CREATE PROCEDURE [dbo].[up_USR_GRIDVIEW_Update] (
  @UniqueId     bigint,
  @ORDRE        varchar(6),
  @VIEW_ID      [varchar](20),    
  @DESCR        varchar(40),  
  @LIST_ID      [varchar](8),   
  @SysDate      datetime
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO USR_GRIDVIEW (    
    [ORDRE],
    [VIEW_ID],
    [DESCR],
    [LIST_ID],
    SysDate)
  VALUES (
    @ORDRE,
    @VIEW_ID,
    @DESCR,
    @LIST_ID,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    USR_GRIDVIEW
  SET
    [ORDRE] = @ORDRE,
    [VIEW_ID] = @VIEW_ID,
    [DESCR] = @DESCR,
    [LIST_ID] = @LIST_ID,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.[up_USR_GRIDVIEW_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_USR_GRIDVIEW_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_USR_GRIDVIEW_Delete] (
  @UniqueId bigint
) AS
BEGIN
   DELETE FROM USR_GRIDVIEW WHERE UniqueId = @UniqueId
END
GO


----------


  -- colonnes des vue user
IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE Table_Name = 'USR_GRIDVIEWCOL')
BEGIN
  DROP TABLE USR_GRIDVIEWCOL
END
GO

  -- colonnes des vue user

  CREATE TABLE [dbo].USR_GRIDVIEWCOL (
  UniqueId          bigint       IDENTITY(1,1) NOT NULL,
  [ORDRE]           varchar(6),
  [VIEW_ID]         [varchar](20),     
  [COLNAME]         [varchar](35),
  [SIZE]            int,
  [SysDate]         datetime     NOT NULL DEFAULT (getdate()),
    )

GO

IF OBJECT_ID(N'dbo.up_USR_GRIDVIEWCOL_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_USR_GRIDVIEWCOL_Update ;
GO

CREATE PROCEDURE [dbo].[up_USR_GRIDVIEWCOL_Update] (
  @UniqueId     bigint,
  @ORDRE        varchar(6),
  @VIEW_ID      [varchar](20),    
  @COLNAME      varchar(35),    
  @SIZE         int,   
  @SysDate      datetime
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO USR_GRIDVIEWCOL (    
    [ORDRE],
    [VIEW_ID],
    [COLNAME],    
    [SIZE],
    SysDate)
  VALUES (
    @ORDRE,
    @VIEW_ID,
    @COLNAME,
    @SIZE,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    USR_GRIDVIEWCOL
  SET
    [ORDRE] = @ORDRE,
    [VIEW_ID] = @VIEW_ID,
    [COLNAME] = @COLNAME,    
    [SIZE] = @SIZE,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.[up_USR_GRIDVIEWCOL_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_USR_GRIDVIEWCOL_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_USR_GRIDVIEWCOL_Delete] (
  @UniqueId bigint
) AS
BEGIN
   DELETE FROM USR_GRIDVIEWCOL WHERE UniqueId = @UniqueId
END
GO



