IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '_DBVersion')
BEGIN
  DROP TABLE _DBVersion
END
GO


IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE Table_Name = '_DBVersion')
BEGIN
  CREATE TABLE [dbo].[_DBVersion]
  (
  [DBV_VersionNo] [int] NULL,
  [DBV_VersionFrom] [int] NULL,
  [DBV_DataPath] [varchar] (256) NULL,
  [DBV_MachineID] [varchar] (128) NULL,
  [DBV_UserID] [varchar] (128) NULL,
  [DBV_SessionID] [bigint] NULL,
  [DBV_DateTimeStart] [datetime] NULL,
  [DBV_DateTimeEnd] [datetime] NULL,
  [DBV_Success] [bit] NULL,
  [DBV_Error] [varchar] (256) NOT NULL
  )
END
GO


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'UM_USERS')
BEGIN
  DROP TABLE UM_USERS
END
GO


IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'UM_USERS')
BEGIN
  CREATE TABLE [dbo].UM_USERS (
  UniqueId          bigint       IDENTITY(1,1) NOT NULL,
  [USER_ID]         [varchar](20) NOT NULL,  
  [NAME]            [varchar](30) NOT NULL,  
  [EMAIL]           [varchar](30)  NOT NULL,    
  [BRANCH_ID]       [varchar](30),  
  [ROLE_ID]         INT,
  [VALIDATEFROM]    INT,
  [PSW]             [varchar](12),  
  [ACTIVE]          bit,  
  [SORTBRANCH_CODE] [varchar](20),       
  [OWC]             [varchar](2),    
  [SysDate]         datetime     NOT NULL DEFAULT (getdate()),
    )
END
GO


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'UM_REGIONS')
BEGIN
  DROP TABLE UM_REGIONS
END
GO


IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'UM_REGIONS')
BEGIN
  CREATE TABLE [dbo].UM_REGIONS (
  UniqueId    bigint  IDENTITY(1,1) NOT NULL,
  [REGION_ID]    [varchar](20)  NOT NULL,      
  [REGION_CODE]  [varchar](20)  NOT NULL,      
  [DIV_ID]       [varchar](3)   NOT NULL,     
  [WOL_ID]       [varchar](20 ),  
  [NAME]         [varchar](30 ),  
  [ORDRE]        [varchar](6), 
  [SysDate]      datetime     NOT NULL DEFAULT (getdate()),
    )
END
GO


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'UM_AREAS')
BEGIN
  DROP TABLE UM_AREAS
END
GO


IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'UM_AREAS')
BEGIN
  CREATE TABLE [dbo].UM_AREAS (
  UniqueId    bigint  IDENTITY(1,1) NOT NULL,
  [AREA_ID]      [varchar](20)  NOT NULL,
  [AREA_CODE]    [varchar](20)  NOT NULL,
  [NAME]         [varchar](30 ),  
  [REGION_ID]    [varchar](20)  NOT NULL,  
  [ORDRE]        [varchar](6),         
  [SysDate]   datetime     NOT NULL DEFAULT (getdate()),
    )
END
GO



IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'UM_BUSINESSUNIT')
BEGIN
  DROP TABLE UM_BUSINESSUNIT
END
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'UM_BUSINESSUNIT')
BEGIN
  CREATE TABLE [dbo].UM_BUSINESSUNIT (
  UniqueId    bigint  IDENTITY(1,1) NOT NULL,
  [BU_ID]        [varchar](20)  NOT NULL,    
  [BU_CODE]      [varchar](20)  NOT NULL,    
  [NAME]         [varchar](30),    
  [ORDRE]        [varchar](6),    
  [SysDate]      datetime     NOT NULL DEFAULT (getdate()),
    )
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'UM_BRANCHS')
BEGIN
  DROP TABLE UM_BRANCHS
END
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'UM_BRANCHS')
BEGIN
  CREATE TABLE [dbo].UM_BRANCHS (
  UniqueId    bigint  IDENTITY(1,1) NOT NULL,
  [BRANCH_ID]    [varchar](20)  NOT NULL,    
  [BRANCH_CODE]  [varchar](20)  NOT NULL,    
  [NAME]         [varchar](30 ),  
  [AREA_ID]      [varchar](20)  NOT NULL,  
  [BU_ID]        [varchar](20),    
  [LOGOPATH]     [varchar](200),
  [PROFITC_NO]   [varchar](1),
  [CLIENT_NO]    [varchar](20),
  [ACTIVE]       bit,    
  [ORDRE]        [varchar](6),          
  [SysDate]   datetime     NOT NULL DEFAULT (getdate()),
    )
END
GO


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'UM_USERREGIONS')
BEGIN
  DROP TABLE UM_USERREGIONS
END
GO


IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'UM_USERREGIONS')
BEGIN
  CREATE TABLE [dbo].UM_USERREGIONS (
  UniqueId         bigint   IDENTITY(1,1) NOT NULL,
  [USER_ID]        [varchar](20 ) NOT NULL,  
  [TERITORY_ID]    [varchar](30)  NOT NULL,    
  [TERITORY_TYPE]  [varchar](1),  
  [ORDRE]          [varchar](6),
  [SysDate]        datetime     NOT NULL DEFAULT (getdate()),
    )
END
GO
