  -- New field - COMMITEM.CLECLIENT
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'COMMITEM'
    AND [COLUMN_NAME] = 'CLECLIENT' )
BEGIN
  ALTER TABLE
    COMMITEM
  ADD
    CLECLIENT  varchar(30);
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_COMMITEM_Update')
  DROP PROCEDURE up_COMMITEM_Update
GO

CREATE PROCEDURE [dbo].[up_COMMITEM_Update] (
  @UniqueId bigint,
  @COM_ID varchar(20),
  @ORDRE varchar(6),
  @PRO_ID varchar(20),
  @CLEMANU varchar(30),
  @CLEDIST varchar(20),
  @CLEPERS varchar(20),
  @PRO_TYPE varchar(1),
  @DESCR varchar(60),
  @QTE_TOT float,
  @COUBRUTUNI float,
  @COUUM varchar(2),
  @COUESC float,
  @PROMCOUNET float,
  @QPP float,
  @MULCOM float,
  @CODEIMPR varchar(2),
  @WEBADDED bit,
  @CLECLIENT  varchar(30),
  @NOTES      text        = '' -- Update V2.#0001
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO COMMITEM (
    [COM_ID],
    [ORDRE],
    [PRO_ID],
    [CLEMANU],
    [CLEDIST],
    [CLEPERS],
    [PRO_TYPE],
    [DESCR],
    [QTE_TOT],
    [COUBRUTUNI],
    [COUUM],
    [COUESC],
    [PROMCOUNET],
    [QPP],
    [MULCOM],
    [CODEIMPR],
    [WEBADDED],
    [CLECLIENT],	
    [NOTES],      -- Update V2.#0001
    SysDate)
  VALUES (
    @COM_ID,
    @ORDRE,
    @PRO_ID,
    @CLEMANU,
    @CLEDIST,
    @CLEPERS,
    @PRO_TYPE,
    @DESCR,
    @QTE_TOT,
    @COUBRUTUNI,
    @COUUM,
    @COUESC,
    @PROMCOUNET,
    @QPP,
    @MULCOM,
    @CODEIMPR,
    @WEBADDED,
    @CLECLIENT,	
    @NOTES,     -- Update V2.#0001
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    COMMITEM
  SET
    [COM_ID] = @COM_ID,
    [ORDRE] = @ORDRE,
    [PRO_ID] = @PRO_ID,
    [CLEMANU] = @CLEMANU,
    [CLEDIST] = @CLEDIST,
    [CLEPERS] = @CLEPERS,
    [PRO_TYPE] = @PRO_TYPE,
    [DESCR] = @DESCR,
    [QTE_TOT] = @QTE_TOT,
    [COUBRUTUNI] = @COUBRUTUNI,
    [COUUM] = @COUUM,
    [COUESC] = @COUESC,
    [PROMCOUNET] = @PROMCOUNET,
    [QPP] = @QPP,
    [MULCOM] = @MULCOM,
    [CODEIMPR] = @CODEIMPR,
    [WEBADDED] = @WEBADDED,
    [CLECLIENT] = @CLECLIENT,	
    [NOTES] = @NOTES,           -- Update V2.#0001
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO