-- PRODUIT PROJECT MAN ADJUST START --------------------------------------------------------------------------

  -- New field - PRODUITS.ACC_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'PRODUITS'
    AND [COLUMN_NAME] = 'ACC_NO' )
BEGIN
  ALTER TABLE
    PRODUITS
  ADD
    ACC_NO  varchar(20);
END
GO

  -- New field - PRODUITS.ACH_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'PRODUITS'
    AND [COLUMN_NAME] = 'ACH_NO' )
BEGIN
  ALTER TABLE
    PRODUITS
  ADD
    ACH_NO  varchar(20);
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_PRODUITS_Update')
  DROP PROCEDURE up_PRODUITS_Update
GO

CREATE PROCEDURE [dbo].[up_PRODUITS_Update] (
  @UniqueId bigint,
  @PRO_ID varchar(20),
  @PRO_ID_OLD varchar(20), -- V9 EE-682 Supercedes
  @PRO_ID_NEW varchar(20), -- V9 EE-682 Supercedes
  @PRO_ID_Parent varchar(20), 
  @CLEMANU varchar(30),
  @CLEPERS varchar(20),
  @CLEDIST varchar(20),
  @CODEUPC varchar(12),
  @CODECAT varchar(3),
  @DESCDIST varchar(60),
  @DESC varchar(60),
  @COUBRUTUNI float,
  @COUUM varchar(2),
  @QPP float,
  @COUESC float,
  @PROMCOUNET float,
  @PROFIT float,
  @MULCOM float,
  @TEMPUNI float,
  @TEMPUM varchar(2),
  @CODEFOUR varchar(2),
  @NOUVEAU varchar(1),
  @DNR varchar(1),
  @DATECOUT datetime,
  @DATECOUNET datetime,   -- V7 EE-222 - Prix net Rexel
  @RESCOUNET int,         -- V7 EE-222 - Prix net Rexel
  @DATECREE datetime,
  @PATHPICT varchar(60),
  @PATHSPEC varchar(60),
  @IMAGE varchar(1),
  @USER1 varchar(20),
  @USER2 varchar(20),
  @PREFERED varchar(1),    -- V8 EE-263 - Prix net Rexel Phase 2
  @ACC_NO varchar(20),
  @ACH_NO varchar(20)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO PRODUITS (
    [PRO_ID],
    [PRO_ID_OLD],   -- V9 EE-682 Supercedes
    [PRO_ID_NEW],   -- V9 EE-682 Supercedes
    [PRO_ID_Parent],
    [CLEMANU],
    [CLEPERS],
    [CLEDIST],
    [CODEUPC],
    [CODECAT],
    [DESCDIST],
    [DESC],
    [COUBRUTUNI],
    [COUUM],
    [QPP],
    [COUESC],
    [PROMCOUNET],
    [PROFIT],
    [MULCOM],
    [TEMPUNI],
    [TEMPUM],
    [CODEFOUR],
    [NOUVEAU],
    [DNR],
    [DATECOUT],
    [DATECOUNET],   -- V7 EE-222 - Prix net Rexel
    [RESCOUNET],    -- V7 EE-222 - Prix net Rexel
    [DATECREE],
    [PATHPICT],
    [PATHSPEC],
    [IMAGE],
    [USER1],
    [USER2],
    [PREFERED],     -- V8 EE-263 - Prix net Rexel Phase 2
    [ACC_NO],
    [ACH_NO],
    SysDate)
  VALUES (
    @PRO_ID,
    @PRO_ID_OLD,   -- V9 EE-682 Supercedes
    @PRO_ID_NEW,   -- V9 EE-682 Supercedes
    @PRO_ID_Parent,
    @CLEMANU,
    @CLEPERS,
    @CLEDIST,
    @CODEUPC,
    @CODECAT,
    @DESCDIST,
    @DESC,
    @COUBRUTUNI,
    @COUUM,
    @QPP,
    @COUESC,
    @PROMCOUNET,
    @PROFIT,
    @MULCOM,
    @TEMPUNI,
    @TEMPUM,
    @CODEFOUR,
    @NOUVEAU,
    @DNR,
    @DATECOUT,
    @DATECOUNET,  -- V7 EE-222 - Prix net Rexel
    @RESCOUNET,   -- V7 EE-222 - Prix net Rexel
    @DATECREE,
    @PATHPICT,
    @PATHSPEC,
    @IMAGE,
    @USER1,
    @USER2,
    @PREFERED,    -- V8 EE-263 - Prix net Rexel Phase 2
    @ACC_NO,
    @ACH_NO,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    PRODUITS
  SET
    [PRO_ID] = @PRO_ID,
    [PRO_ID_OLD] = @PRO_ID_OLD,   -- V9 EE-682 Supercedes
    [PRO_ID_NEW] = @PRO_ID_NEW,   -- V9 EE-682 Supercedes
    [PRO_ID_Parent] = @PRO_ID_Parent,
    [CLEMANU] = @CLEMANU,
    [CLEPERS] = @CLEPERS,
    [CLEDIST] = @CLEDIST,
    [CODEUPC] = @CODEUPC,
    [CODECAT] = @CODECAT,
    [DESCDIST] = @DESCDIST,
    [DESC] = @DESC,
    [COUBRUTUNI] = @COUBRUTUNI,
    [COUUM] = @COUUM,
    [QPP] = @QPP,
    [COUESC] = @COUESC,
    [PROMCOUNET] = @PROMCOUNET,
    [PROFIT] = @PROFIT,
    [MULCOM] = @MULCOM,
    [TEMPUNI] = @TEMPUNI,
    [TEMPUM] = @TEMPUM,
    [CODEFOUR] = @CODEFOUR,
    [NOUVEAU] = @NOUVEAU,
    [DNR] = @DNR,
    [DATECOUT] = @DATECOUT,
    [DATECOUNET] = @DATECOUNET,   -- V7 EE-222 - Prix net Rexel
    [RESCOUNET] = @RESCOUNET,     -- V7 EE-222 - Prix net Rexel
    [DATECREE] = @DATECREE,
    [PATHPICT] = @PATHPICT,
    [PATHSPEC] = @PATHSPEC,
    [IMAGE] = @IMAGE,
    [USER1] = @USER1,
    [USER2] = @USER2,
    [PREFERED] = CASE WHEN @PREFERED IS NULL THEN [PREFERED] ELSE @PREFERED END,  -- V8 EE-263 - Prix net Rexel Phase 2
    [ACC_NO] = @ACC_NO,
    [ACH_NO] = @ACH_NO,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


-- PRODUIT - PROJECT MAN ADJUST END --------------------------------------------------------------------------
