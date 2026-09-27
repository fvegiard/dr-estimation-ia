  -- New fields - Nouvelle licence
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'BDEE'
    AND [COLUMN_NAME] = 'LVERSION' )
BEGIN
  ALTER TABLE
    BDEE
  ADD
    [LVERSION] [int] NULL CONSTRAINT [DF_BDEE_LVERSION] DEFAULT ((1)),
    [NODIST] [varchar] (6) NULL,
    [NOEEWIN] [varchar] (6) NULL,
    [NOGEM] [varchar] (6) NULL,
    [ISINT] [bit] NULL,
    [DIVISIONPX] [varchar] (2) NULL,
    [DIVISION] [varchar] (3) NULL,
    [ISDEMO] [bit] NULL,
    [DEMOEND] [datetime] NULL,
    [SUPPORTEND] [datetime] NULL,
    [MAXUSERS] [int] NULL,
    [ISSQL] [bit] NULL,
    [ISACOMBA] [bit] NULL,
    [ISAVANTAGE] [bit] NULL,
    [ISSAGE50] [bit] NULL,
    [ISQUICKBK] [bit] NULL,
    [KVERSION] [int] NULL CONSTRAINT [DF_BDEE_KVERSION] DEFAULT ((1)),
    [LICENCEKEY] [varchar] (128) NULL
END
GO

ALTER PROCEDURE [dbo].[up_BDEE_Update] (
  @UniqueId bigint,
  @LVERSION	  int,
  @CODEVER	  varchar(20),
  @DATA       varchar(30),
  @NODIST	    varchar(6),
  @NOEEWIN	  varchar(6),
  @NOGEM	    varchar(6),
  @ISINT      bit,
  @DIVISIONPX varchar(2),
  @DIVISION	  varchar(3),
  @DESCR	    varchar(40),
  @URLFR	    varchar(100),
  @URLEN	    varchar(100),
  @ISDEMO	    bit,
  @DEMOEND	  datetime,
  @SUPPORTEND	datetime,
  @MAXUSERS	  int,
  @ISSQL	    bit,
  @ISACOMBA	  bit,
  @ISAVANTAGE	bit,
  @ISSAGE50	  bit,
  @ISQUICKBK	bit,
  @KVERSION	  int,
  @LICENCEKEY	varchar(128)
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
    ISDEMO, 
    DEMOEND, 
    SUPPORTEND, 
    MAXUSERS, 
    ISSQL, 
    ISACOMBA, 
    ISAVANTAGE, 
    ISSAGE50, 
    ISQUICKBK, 
    KVERSION, 
    LICENCEKEY, 
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
    @ISDEMO, 
    @DEMOEND, 
    @SUPPORTEND, 
    @MAXUSERS, 
    @ISSQL, 
    @ISACOMBA, 
    @ISAVANTAGE, 
    @ISSAGE50, 
    @ISQUICKBK, 
    @KVERSION, 
    @LICENCEKEY, 
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
    ISDEMO      = @ISDEMO,
    DEMOEND     = @DEMOEND,
    SUPPORTEND  = @SUPPORTEND,
    MAXUSERS    = @MAXUSERS,
    ISSQL       = @ISSQL,
    ISACOMBA    = @ISACOMBA,
    ISAVANTAGE  = @ISAVANTAGE,
    ISSAGE50    = @ISSAGE50,
    ISQUICKBK   = @ISQUICKBK,
    KVERSION    = @KVERSION,
    LICENCEKEY  = @LICENCEKEY,
    SysDate     = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END

GO
