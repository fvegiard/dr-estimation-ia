-- New field - COMMANDE.STATUT  -- START
  
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'COMMANDE'
    AND [COLUMN_NAME] = 'STATUT' )
BEGIN
  ALTER TABLE
    COMMANDE
  ADD
    STATUT INT
END
GO

-- SP -- UPDATE -- [up_COMMANDE_Update] -- START --

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_COMMANDE_Update')
  DROP PROCEDURE up_COMMANDE_Update
GO

CREATE PROCEDURE [dbo].[up_COMMANDE_Update] (
  @UniqueId bigint,
  @COM_ID varchar(20),
  @COM_NO varchar(12),
  @SOU_ID varchar(20),
  @JOB_NO varchar(12),
  @DESCR varchar(60),
  @DATE_CREE datetime,
  @DATE_COM datetime,
  @DATE_LIVR datetime,
  @INSTRUCT text,
  @NOTES text,
  @ORDERED_ID varchar(20),
  @ORDERED_NO varchar(20),
  @BILLEDIDX int,
  @BILLED_ID varchar(20),
  @BILLED_NO varchar(20),
  @DELIVERIDX int,
  @DELIVER_ID varchar(20),
  @DELIVER_NO varchar(20),
  @COMTOTAL float,
  @ACCTRANSNO varchar(12),
  @STATUT int
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO COMMANDE (
    [COM_ID],
    [COM_NO],
    [SOU_ID],
    [JOB_NO],
    [DESCR],
    [DATE_CREE],
    [DATE_COM],
    [DATE_LIVR],
    [INSTRUCT],
    [NOTES],
    [ORDERED_ID],
    [ORDERED_NO],
    [BILLEDIDX],
    [BILLED_ID],
    [BILLED_NO],
    [DELIVERIDX],
    [DELIVER_ID],
    [DELIVER_NO],
    [COMTOTAL],
    [ACCTRANSNO],
	[STATUT],
    SysDate)
  VALUES (
    @COM_ID,
    @COM_NO,
    @SOU_ID,
    @JOB_NO,
    @DESCR,
    @DATE_CREE,
    @DATE_COM,
    @DATE_LIVR,
    @INSTRUCT,
    @NOTES,
    @ORDERED_ID,
    @ORDERED_NO,
    @BILLEDIDX,
    @BILLED_ID,
    @BILLED_NO,
    @DELIVERIDX,
    @DELIVER_ID,
    @DELIVER_NO,
    @COMTOTAL,
    @ACCTRANSNO,
	@STATUT,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    COMMANDE
  SET
    [COM_ID] = @COM_ID,
    [COM_NO] = @COM_NO,
    [SOU_ID] = @SOU_ID,
    [JOB_NO] = @JOB_NO,
    [DESCR] = @DESCR,
    [DATE_CREE] = @DATE_CREE,
    [DATE_COM] = @DATE_COM,
    [DATE_LIVR] = @DATE_LIVR,
    [INSTRUCT] = @INSTRUCT,
    [NOTES] = @NOTES,
    [ORDERED_ID] = @ORDERED_ID,
    [ORDERED_NO] = @ORDERED_NO,
    [BILLEDIDX] = @BILLEDIDX,
    [BILLED_ID] = @BILLED_ID,
    [BILLED_NO] = @BILLED_NO,
    [DELIVERIDX] = @DELIVERIDX,
    [DELIVER_ID] = @DELIVER_ID,
    [DELIVER_NO] = @DELIVER_NO,
    [COMTOTAL] = @COMTOTAL,
    [ACCTRANSNO] = @ACCTRANSNO,
    [STATUT] = @STATUT,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
