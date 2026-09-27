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
  @STATUT int,
  @STATUTLIBF varchar(30), 
  @STATUTLIBE varchar(30), 
  @ORIGIN varchar(1), 
  @ORIGINREF varchar(200),
  @CONFIRMNO varchar(60),  
  @EXPORTCOUNT int,
  @CLIENTCIE   varchar(50) ,
  @CLIENTCNT   varchar(50) ,
  @CLIENTRUE1  varchar(50) ,
  @CLIENTRUE2  varchar(50) ,
  @CLIENTVILL  varchar(40) ,
  @CLIENTCP    varchar(7)  ,
  @CLIENTPROV  varchar(40) ,
  @CLIENTPAYS  varchar(40) ,
  @CLIENTBP    varchar(30) ,
  @CLIENTTEL1  varchar(20) ,
  @CLIENTTEL2  varchar(20) ,
  @CLIENTTEL3  varchar(20) ,
  @CLIENTFAX   varchar(20) ,
  @CLIENTEMAIL varchar(80) ,    
  @SITECIE   varchar(50) ,
  @SITECNT   varchar(50) ,
  @SITERUE1  varchar(50) ,
  @SITERUE2  varchar(50) ,
  @SITEVILL  varchar(40) ,
  @SITECP    varchar(7)  ,
  @SITEPROV  varchar(40) ,
  @SITEPAYS  varchar(40) ,
  @SITEBP    varchar(30) ,
  @SITETEL1  varchar(20) ,
  @SITETEL2  varchar(20) ,
  @SITETEL3  varchar(20) ,
  @SITEFAX   varchar(20) ,
  @SITEEMAIL varchar(80) ,    
  @SUPPCIE   varchar(50) ,
  @SUPPCNT   varchar(50) ,
  @SUPPRUE1  varchar(50) ,
  @SUPPRUE2  varchar(50) ,
  @SUPPVILL  varchar(40) ,
  @SUPPCP    varchar(7)  ,
  @SUPPPROV  varchar(40) ,
  @SUPPPAYS  varchar(40) ,
  @SUPPBP    varchar(30) ,
  @SUPPTEL1  varchar(20) ,
  @SUPPTEL2  varchar(20) ,
  @SUPPTEL3  varchar(20) ,
  @SUPPFAX   varchar(20) ,
  @SUPPEMAIL varchar(80)    
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
    [STATUTLIBF], 
    [STATUTLIBE],  
    [ORIGIN], 
    [ORIGINREF],  
    [CONFIRMNO],      
    [EXPORTCOUNT],     
    [CLIENTCIE],
    [CLIENTCNT],
    [CLIENTRUE1],
    [CLIENTRUE2],
    [CLIENTVILL],
    [CLIENTCP],
    [CLIENTPROV],
    [CLIENTPAYS],
    [CLIENTBP],
    [CLIENTTEL1],
    [CLIENTTEL2],
    [CLIENTTEL3],
    [CLIENTFAX],
    [CLIENTEMAIL],
    [SITECIE],
    [SITECNT],
    [SITERUE1],
    [SITERUE2],
    [SITEVILL],
    [SITECP],
    [SITEPROV],
    [SITEPAYS],
    [SITEBP],
    [SITETEL1],
    [SITETEL2],
    [SITETEL3],
    [SITEFAX],
    [SITEEMAIL],
    [SUPPCIE],
    [SUPPCNT],
    [SUPPRUE1],
    [SUPPRUE2],
    [SUPPVILL],
    [SUPPCP],
    [SUPPPROV],
    [SUPPPAYS],
    [SUPPBP],
    [SUPPTEL1],
    [SUPPTEL2],
    [SUPPTEL3],
    [SUPPFAX],
    [SUPPEMAIL],    
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
    @STATUTLIBF, 
    @STATUTLIBE,  
    @ORIGIN, 
    @ORIGINREF,     
    @CONFIRMNO,  
    @EXPORTCOUNT,   
    @CLIENTCIE  ,
    @CLIENTCNT  ,
    @CLIENTRUE1 ,
    @CLIENTRUE2 ,
    @CLIENTVILL ,
    @CLIENTCP   ,
    @CLIENTPROV ,
    @CLIENTPAYS ,
    @CLIENTBP   ,
    @CLIENTTEL1 ,
    @CLIENTTEL2 ,
    @CLIENTTEL3 ,
    @CLIENTFAX  ,
    @CLIENTEMAIL ,
    @SITECIE  ,
    @SITECNT  ,
    @SITERUE1 ,
    @SITERUE2 ,
    @SITEVILL ,
    @SITECP   ,
    @SITEPROV ,
    @SITEPAYS ,
    @SITEBP   ,
    @SITETEL1 ,
    @SITETEL2 ,
    @SITETEL3 ,
    @SITEFAX  ,
    @SITEEMAIL ,
    @SUPPCIE  ,
    @SUPPCNT  ,
    @SUPPRUE1 ,
    @SUPPRUE2 ,
    @SUPPVILL ,
    @SUPPCP   ,
    @SUPPPROV ,
    @SUPPPAYS ,
    @SUPPBP   ,
    @SUPPTEL1 ,
    @SUPPTEL2 ,
    @SUPPTEL3 ,
    @SUPPFAX  ,
    @SUPPEMAIL ,
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
    [STATUTLIBF]  = @STATUTLIBF,
    [STATUTLIBE]  = @STATUTLIBE,
    [ORIGIN]      = @ORIGIN, 
    [ORIGINREF]   = @ORIGINREF,  
    [CONFIRMNO]   = @CONFIRMNO,      
    [EXPORTCOUNT]   = @EXPORTCOUNT,      
    [CLIENTCIE]   = @CLIENTCIE,
    [CLIENTCNT]   = @CLIENTCNT,
    [CLIENTRUE1]  = @CLIENTRUE1,
    [CLIENTRUE2]  = @CLIENTRUE2,
    [CLIENTVILL]  = @CLIENTVILL,
    [CLIENTCP]    = @CLIENTCP,
    [CLIENTPROV]  = @CLIENTPROV,
    [CLIENTPAYS]  = @CLIENTPAYS,
    [CLIENTBP]    = @CLIENTBP,
    [CLIENTTEL1]  = @CLIENTTEL1,
    [CLIENTTEL2]  = @CLIENTTEL2,
    [CLIENTTEL3]  = @CLIENTTEL3,
    [CLIENTFAX]   = @CLIENTFAX,
    [CLIENTEMAIL] = @CLIENTEMAIL,
    [SITECIE]   = @SITECIE,
    [SITECNT]   = @SITECNT,
    [SITERUE1]  = @SITERUE1,
    [SITERUE2]  = @SITERUE2,
    [SITEVILL]  = @SITEVILL,
    [SITECP]    = @SITECP,
    [SITEPROV]  = @SITEPROV,
    [SITEPAYS]  = @SITEPAYS,
    [SITEBP]    = @SITEBP,
    [SITETEL1]  = @SITETEL1,
    [SITETEL2]  = @SITETEL2,
    [SITETEL3]  = @SITETEL3,
    [SITEFAX]   = @SITEFAX,
    [SITEEMAIL] = @SITEEMAIL,
    [SUPPCIE]   = @SUPPCIE,
    [SUPPCNT]   = @SUPPCNT,
    [SUPPRUE1]  = @SUPPRUE1,
    [SUPPRUE2]  = @SUPPRUE2,
    [SUPPVILL]  = @SUPPVILL,
    [SUPPCP]    = @SUPPCP,
    [SUPPPROV]  = @SUPPPROV,
    [SUPPPAYS]  = @SUPPPAYS,
    [SUPPBP]    = @SUPPBP,
    [SUPPTEL1]  = @SUPPTEL1,
    [SUPPTEL2]  = @SUPPTEL2,
    [SUPPTEL3]  = @SUPPTEL3,
    [SUPPFAX]   = @SUPPFAX,
    [SUPPEMAIL] = @SUPPEMAIL,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- Field Resize to 80 - Bug script 27 : field - COMMANDE.CLIENTEMAIL
IF EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'COMMANDE'
    AND [COLUMN_NAME] = 'CLIENTEMAIL' 
    AND [CHARACTER_MAXIMUM_LENGTH] < 80 )
BEGIN
  ALTER TABLE
    COMMANDE
  ALTER COLUMN
    CLIENTEMAIL VARCHAR(80);
END
GO

  -- Field Resize to 80 - Bug script 27 : field - COMMANDE.SITEEMAIL
IF EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'COMMANDE'
    AND [COLUMN_NAME] = 'SITEEMAIL' 
    AND [CHARACTER_MAXIMUM_LENGTH] < 80 )
BEGIN
  ALTER TABLE
    COMMANDE
  ALTER COLUMN
    SITEEMAIL VARCHAR(80);
END
GO

  -- Field Resize to 80 - Bug script 27 : field - COMMANDE.SUPPEMAIL
IF EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'COMMANDE'
    AND [COLUMN_NAME] = 'SUPPEMAIL' 
    AND [CHARACTER_MAXIMUM_LENGTH] < 80 )
BEGIN
  ALTER TABLE
    COMMANDE
  ALTER COLUMN
    SUPPEMAIL VARCHAR(80);
END
GO