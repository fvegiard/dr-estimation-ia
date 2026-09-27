/******************************************************************************/
/* Création des stored procedures propre à la version standard de EE          */
/* Ces stored procs. doivents être en tout temps identique à ceux déclarés    */
/* dans le fichier CreateScripts_Calgary.sql SAUF pour les scripts ayant des  */
/* champs exclusifs à la version interne. Ces champs ne doivent JAMAIS a      */  
/* paraitre dans ce fichier. Utiliser Beyond Compare au besoin pour s'assurer */
/* de l'exactitude des tables                                                 */ 
/******************************************************************************/

CREATE PROCEDURE [dbo].[up_BDEE_Update] (
  @UniqueId bigint,
  @CODEVER varchar(20),
  @DATA varchar(30),
  @DESCR varchar(40),
  @URLFR varchar(100),
  @URLEN varchar(100)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO BDEE (
    [CODEVER],
    [DATA],
    [DESCR],
    [URLFR],
    [URLEN],
    SysDate)
  VALUES (
    @CODEVER,
    @DATA,
    @DESCR,
    @URLFR,
    @URLEN,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    BDEE
  SET
    [CODEVER] = @CODEVER,
    [DATA] = @DATA,
    [DESCR] = @DESCR,
    [URLFR] = @URLFR,
    [URLEN] = @URLEN,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_BDEE_Delete] (
  @UniqueId bigint
) AS

DELETE FROM BDEE WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_CLIENTS_Update] (
  @UniqueId bigint,
  @CLI_ID varchar(20),
  @TYPEFICHE varchar(1),
  @NUMERO varchar(20),
  @NOMCIE varchar(50),
  @CONTACT varchar(50),
  @RUE1 varchar(50),
  @RUE2 varchar(50),
  @VILLE varchar(40),
  @CODEPOSTAL varchar(7),
  @PROVINCE varchar(40),
  @PAYS varchar(40),
  @BOITEPOSTA varchar(30),
  @TEL1 varchar(20),
  @TEL2 varchar(20),
  @TEL3 varchar(20),
  @FAX varchar(20),
  @PROFIT float,
  @TVFAPPL bit,
  @TVPAPPL bit,
  @NOTES text,
  @EMAIL varchar(80),
  @SITEWEB varchar(80),
  @SYSTEM bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO CLIENTS (
    [CLI_ID],
    [TYPEFICHE],
    [NUMERO],
    [NOMCIE],
    [CONTACT],
    [RUE1],
    [RUE2],
    [VILLE],
    [CODEPOSTAL],
    [PROVINCE],
    [PAYS],
    [BOITEPOSTA],
    [TEL1],
    [TEL2],
    [TEL3],
    [FAX],
    [PROFIT],
    [TVFAPPL],
    [TVPAPPL],
    [NOTES],
    [EMAIL],
    [SITEWEB],
    [SYSTEM],
    SysDate)
  VALUES (
    @CLI_ID,
    @TYPEFICHE,
    @NUMERO,
    @NOMCIE,
    @CONTACT,
    @RUE1,
    @RUE2,
    @VILLE,
    @CODEPOSTAL,
    @PROVINCE,
    @PAYS,
    @BOITEPOSTA,
    @TEL1,
    @TEL2,
    @TEL3,
    @FAX,
    @PROFIT,
    @TVFAPPL,
    @TVPAPPL,
    @NOTES,
    @EMAIL,
    @SITEWEB,
    @SYSTEM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    CLIENTS
  SET
    [CLI_ID] = @CLI_ID,
    [TYPEFICHE] = @TYPEFICHE,
    [NUMERO] = @NUMERO,
    [NOMCIE] = @NOMCIE,
    [CONTACT] = @CONTACT,
    [RUE1] = @RUE1,
    [RUE2] = @RUE2,
    [VILLE] = @VILLE,
    [CODEPOSTAL] = @CODEPOSTAL,
    [PROVINCE] = @PROVINCE,
    [PAYS] = @PAYS,
    [BOITEPOSTA] = @BOITEPOSTA,
    [TEL1] = @TEL1,
    [TEL2] = @TEL2,
    [TEL3] = @TEL3,
    [FAX] = @FAX,
    [PROFIT] = @PROFIT,
    [TVFAPPL] = @TVFAPPL,
    [TVPAPPL] = @TVPAPPL,
    [NOTES] = @NOTES,
    [EMAIL] = @EMAIL,
    [SITEWEB] = @SITEWEB,
    [SYSTEM] = @SYSTEM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_CLIENTS_Delete] (
  @UniqueId bigint
) AS

DELETE FROM CLIENTS WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_CLITAUX_Update] (
  @UniqueId bigint,
  @CLI_ID varchar(20),
  @ORDRE varchar(6),
  @DESCTAUX varchar(50),
  @COUTUNI float,
  @PROFIT float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO CLITAUX (
    [CLI_ID],
    [ORDRE],
    [DESCTAUX],
    [COUTUNI],
    [PROFIT],
    SysDate)
  VALUES (
    @CLI_ID,
    @ORDRE,
    @DESCTAUX,
    @COUTUNI,
    @PROFIT,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    CLITAUX
  SET
    [CLI_ID] = @CLI_ID,
    [ORDRE] = @ORDRE,
    [DESCTAUX] = @DESCTAUX,
    [COUTUNI] = @COUTUNI,
    [PROFIT] = @PROFIT,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_CLITAUX_Delete] (
  @UniqueId bigint
) AS

DELETE FROM CLITAUX WHERE UniqueId = @UniqueId
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
  @COMTOTAL float
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_COMMANDE_Delete] (
  @UniqueId bigint
) AS

DELETE FROM COMMANDE WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_COMMITEM_Update] (
  @UniqueId bigint,
  @COM_ID varchar(20),
  @ORDRE varchar(6),
  @PRO_ID varchar(20),
  @CLEMANU varchar(20),
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
    [NOTES] = @NOTES,           -- Update V2.#0001
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_COMMITEM_Delete] (
  @UniqueId bigint
) AS

DELETE FROM COMMITEM WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_DEFBLO_Update] (
  @UniqueId bigint,
  @ORDRE varchar(6),
  @DESC varchar(40),
  @MULT int,
  @INCLSOU bit,
  @INCLFAC bit,
  @SYSTEM bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO DEFBLO (
    [ORDRE],
    [DESC],
    [MULT],
    [INCLSOU],
    [INCLFAC],
    [SYSTEM],
    SysDate)
  VALUES (
    @ORDRE,
    @DESC,
    @MULT,
    @INCLSOU,
    @INCLFAC,
    @SYSTEM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    DEFBLO
  SET
    [ORDRE] = @ORDRE,
    [DESC] = @DESC,
    [MULT] = @MULT,
    [INCLSOU] = @INCLSOU,
    [INCLFAC] = @INCLFAC,
    [SYSTEM] = @SYSTEM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_DEFBLO_Delete] (
  @UniqueId bigint
) AS

DELETE FROM DEFBLO WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_DEFDIV_Update] (
  @UniqueId bigint,
  @ORDRE varchar(6),
  @DESC varchar(40),
  @INCLSOU bit,
  @INCLFAC bit,
  @SYSTEM bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO DEFDIV (
    [ORDRE],
    [DESC],
    [INCLSOU],
    [INCLFAC],
    [SYSTEM],
    SysDate)
  VALUES (
    @ORDRE,
    @DESC,
    @INCLSOU,
    @INCLFAC,
    @SYSTEM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    DEFDIV
  SET
    [ORDRE] = @ORDRE,
    [DESC] = @DESC,
    [INCLSOU] = @INCLSOU,
    [INCLFAC] = @INCLFAC,
    [SYSTEM] = @SYSTEM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_DEFDIV_Delete] (
  @UniqueId bigint
) AS

DELETE FROM DEFDIV WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_ENSCOMPO_Update] (
  @UniqueId bigint,
  @ENS_ID varchar(20),
  @ORDRE varchar(6),
  @PRO_ID varchar(20),
  @QTE float,
  @QTEUM varchar(2),
  @TYPRATIO varchar(1),
  @DIV float,
  @DIVUM varchar(2)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO ENSCOMPO (
    [ENS_ID],
    [ORDRE],
    [PRO_ID],
    [QTE],
    [QTEUM],
    [TYPRATIO],
    [DIV],
    [DIVUM],
    SysDate)
  VALUES (
    @ENS_ID,
    @ORDRE,
    @PRO_ID,
    @QTE,
    @QTEUM,
    @TYPRATIO,
    @DIV,
    @DIVUM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    ENSCOMPO
  SET
    [ENS_ID] = @ENS_ID,
    [ORDRE] = @ORDRE,
    [PRO_ID] = @PRO_ID,
    [QTE] = @QTE,
    [QTEUM] = @QTEUM,
    [TYPRATIO] = @TYPRATIO,
    [DIV] = @DIV,
    [DIVUM] = @DIVUM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_ENSCOMPO_Delete] (
  @UniqueId bigint
) AS

DELETE FROM ENSCOMPO WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_ENSEMBLE_Update] (
  @UniqueId bigint,
  @ENS_ID varchar(20),
  @CLEPERS varchar(20),
  @DESC varchar(40),
  @COUUM varchar(2),
  @PROFIT float,
  @TEMPSEC float,
  @TEMPUNI float,
  @TEMPUM varchar(2),
  @DATECREE datetime,
  @OLDESTPROD datetime,
  @SYSTEM bit,
  @USES_DISC bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO ENSEMBLE (
    [ENS_ID],
    [CLEPERS],
    [DESC],
    [COUUM],
    [PROFIT],
    [TEMPSEC],
    [TEMPUNI],
    [TEMPUM],
    [DATECREE],
    [OLDESTPROD],
    [SYSTEM],
    [USES_DISC],
    SysDate)
  VALUES (
    @ENS_ID,
    @CLEPERS,
    @DESC,
    @COUUM,
    @PROFIT,
    @TEMPSEC,
    @TEMPUNI,
    @TEMPUM,
    @DATECREE,
    @OLDESTPROD,
    @SYSTEM,
    @USES_DISC,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    ENSEMBLE
  SET
    [ENS_ID] = @ENS_ID,
    [CLEPERS] = @CLEPERS,
    [DESC] = @DESC,
    [COUUM] = @COUUM,
    [PROFIT] = @PROFIT,
    [TEMPSEC] = @TEMPSEC,
    [TEMPUNI] = @TEMPUNI,
    [TEMPUM] = @TEMPUM,
    [DATECREE] = @DATECREE,
    [OLDESTPROD] = @OLDESTPROD,
    [SYSTEM] = @SYSTEM,
    [USES_DISC] = @USES_DISC,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_ENSEMBLE_Delete] (
  @UniqueId bigint
) AS

DELETE FROM ENSEMBLE WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_FACAMD_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DIV_ID varchar(3),
  @FACTMD float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACAMD (
    [SOU_ID],
    [BLO_ID],
    [DIV_ID],
    [FACTMD],
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DIV_ID,
    @FACTMD,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACAMD
  SET
    [SOU_ID] = @SOU_ID,
    [BLO_ID] = @BLO_ID,
    [DIV_ID] = @DIV_ID,
    [FACTMD] = @FACTMD,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_FACAMD_Delete] (
  @UniqueId bigint
) AS

DELETE FROM FACAMD WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_FACBLO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DESC varchar(40),
  @MULT int
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACBLO (
    [SOU_ID],
    [BLO_ID],
    [DESC],
    [MULT],
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DESC,
    @MULT,
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_FACBLO_Delete] (
  @UniqueId bigint
) AS

DELETE FROM FACBLO WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_FACDIV_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @DIV_ID varchar(3),
  @DESC varchar(40)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACDIV (
    [SOU_ID],
    [DIV_ID],
    [DESC],
    SysDate)
  VALUES (
    @SOU_ID,
    @DIV_ID,
    @DESC,
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_FACDIV_Delete] (
  @UniqueId bigint
) AS

DELETE FROM FACDIV WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_FACENS_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @ENS_ID varchar(20),
  @DESC varchar(40),
  @QTETOT float,
  @QTETOTSECT float,
  @CALCTIMSTP varchar(14),
  @COUUM varchar(2),
  @TEMPUNI float,
  @TEMPSEC float,
  @TEMPUM varchar(2),
  @DATECREE datetime,
  @OLDESTPROD datetime,
  @CLEPERS varchar(40),
  @PROFIT float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACENS (
    [SOU_ID],
    [ENS_ID],
    [DESC],
    [QTETOT],
    [QTETOTSECT],
    [CALCTIMSTP],
    [COUUM],
    [TEMPUNI],
    [TEMPSEC],
    [TEMPUM],
    [DATECREE],
    [OLDESTPROD],
    [CLEPERS],
    [PROFIT],
    SysDate)
  VALUES (
    @SOU_ID,
    @ENS_ID,
    @DESC,
    @QTETOT,
    @QTETOTSECT,
    @CALCTIMSTP,
    @COUUM,
    @TEMPUNI,
    @TEMPSEC,
    @TEMPUM,
    @DATECREE,
    @OLDESTPROD,
    @CLEPERS,
    @PROFIT,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACENS
  SET
    [SOU_ID] = @SOU_ID,
    [ENS_ID] = @ENS_ID,
    [DESC] = @DESC,
    [QTETOT] = @QTETOT,
    [QTETOTSECT] = @QTETOTSECT,
    [CALCTIMSTP] = @CALCTIMSTP,
    [COUUM] = @COUUM,
    [TEMPUNI] = @TEMPUNI,
    [TEMPSEC] = @TEMPSEC,
    [TEMPUM] = @TEMPUM,
    [DATECREE] = @DATECREE,
    [OLDESTPROD] = @OLDESTPROD,
    [CLEPERS] = @CLEPERS,
    [PROFIT] = @PROFIT,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_FACENS_Delete] (
  @UniqueId bigint
) AS

DELETE FROM FACENS WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_FACENSCO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @ENS_ID varchar(20),
  @PRO_ID varchar(20),
  @ORDRE varchar(6),
  @QTE float,
  @QTEUM varchar(2),
  @TYPRATIO varchar(1),
  @DIV float,
  @DIVUM varchar(2)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACENSCO (
    [SOU_ID],
    [ENS_ID],
    [PRO_ID],
    [ORDRE],
    [QTE],
    [QTEUM],
    [TYPRATIO],
    [DIV],
    [DIVUM],
    SysDate)
  VALUES (
    @SOU_ID,
    @ENS_ID,
    @PRO_ID,
    @ORDRE,
    @QTE,
    @QTEUM,
    @TYPRATIO,
    @DIV,
    @DIVUM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACENSCO
  SET
    [SOU_ID] = @SOU_ID,
    [ENS_ID] = @ENS_ID,
    [PRO_ID] = @PRO_ID,
    [ORDRE] = @ORDRE,
    [QTE] = @QTE,
    [QTEUM] = @QTEUM,
    [TYPRATIO] = @TYPRATIO,
    [DIV] = @DIV,
    [DIVUM] = @DIVUM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_FACENSCO_Delete] (
  @UniqueId bigint
) AS

DELETE FROM FACENSCO WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_FACLOTS_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @LOTS_ID varchar(20),
  @DESC varchar(40),
  @QTETOT float,
  @QTETOTSECT float,
  @CALCTIMSTP varchar(14),
  @COUUM varchar(2),
  @TEMPUNI float,
  @TEMPUM varchar(2),
  @DATECREE datetime,
  @OLDESTPROD datetime,
  @CLEPERS varchar(40),
  @PROFIT float,
  @COUTANTSEL int,
  @COUTANT1 float,
  @COUTANT2 float,
  @COUTANT3 float,
  @COUTANT4 float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACLOTS (
    [SOU_ID],
    [LOTS_ID],
    [DESC],
    [QTETOT],
    [QTETOTSECT],
    [CALCTIMSTP],
    [COUUM],
    [TEMPUNI],
    [TEMPUM],
    [DATECREE],
    [OLDESTPROD],
    [CLEPERS],
    [PROFIT],
    [COUTANTSEL],
    [COUTANT1],
    [COUTANT2],
    [COUTANT3],
    [COUTANT4],
    SysDate)
  VALUES (
    @SOU_ID,
    @LOTS_ID,
    @DESC,
    @QTETOT,
    @QTETOTSECT,
    @CALCTIMSTP,
    @COUUM,
    @TEMPUNI,
    @TEMPUM,
    @DATECREE,
    @OLDESTPROD,
    @CLEPERS,
    @PROFIT,
    @COUTANTSEL,
    @COUTANT1,
    @COUTANT2,
    @COUTANT3,
    @COUTANT4,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACLOTS
  SET
    [SOU_ID] = @SOU_ID,
    [LOTS_ID] = @LOTS_ID,
    [DESC] = @DESC,
    [QTETOT] = @QTETOT,
    [QTETOTSECT] = @QTETOTSECT,
    [CALCTIMSTP] = @CALCTIMSTP,
    [COUUM] = @COUUM,
    [TEMPUNI] = @TEMPUNI,
    [TEMPUM] = @TEMPUM,
    [DATECREE] = @DATECREE,
    [OLDESTPROD] = @OLDESTPROD,
    [CLEPERS] = @CLEPERS,
    [PROFIT] = @PROFIT,
    [COUTANTSEL] = @COUTANTSEL,
    [COUTANT1] = @COUTANT1,
    [COUTANT2] = @COUTANT2,
    [COUTANT3] = @COUTANT3,
    [COUTANT4] = @COUTANT4,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_FACLOTS_Delete] (
  @UniqueId bigint
) AS

DELETE FROM FACLOTS WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_FACLOTSCO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @LOTS_ID varchar(20),
  @PRO_ID varchar(20),
  @ORDRE varchar(6),
  @QTE float,
  @QTEUM varchar(2)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACLOTSCO (
    [SOU_ID],
    [LOTS_ID],
    [PRO_ID],
    [ORDRE],
    [QTE],
    [QTEUM],
    SysDate)
  VALUES (
    @SOU_ID,
    @LOTS_ID,
    @PRO_ID,
    @ORDRE,
    @QTE,
    @QTEUM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACLOTSCO
  SET
    [SOU_ID] = @SOU_ID,
    [LOTS_ID] = @LOTS_ID,
    [PRO_ID] = @PRO_ID,
    [ORDRE] = @ORDRE,
    [QTE] = @QTE,
    [QTEUM] = @QTEUM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_FACLOTSCO_Delete] (
  @UniqueId bigint
) AS

DELETE FROM FACLOTSCO WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_FACPRO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @PRO_ID varchar(20),
  @CLEMANU varchar(20),
  @CLEDIST varchar(20),
  @CLEPERS varchar(20),
  @DESC varchar(60),
  @QTEENS float,
  @QTELOT float,
  @QTEOTH float,
  @CALCTIMSTP varchar(14),
  @COUBRUTUNI float,
  @COUUM varchar(2),
  @QPP float,
  @COUESC float,
  @PROMCOUNET float,
  @TEMPUNI float,
  @TEMPUM varchar(2),
  @MULCOM float,
  @CODEIMPR varchar(20),
  @CODEFOUR varchar(2),
  @CODECAT varchar(3),
  @DATECOUT datetime,
  @QTECOM float,
  @QTEACOM float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACPRO (
    [SOU_ID],
    [PRO_ID],
    [CLEMANU],
    [CLEDIST],
    [CLEPERS],
    [DESC],
    [QTEENS],
    [QTELOT],
    [QTEOTH],
    [CALCTIMSTP],
    [COUBRUTUNI],
    [COUUM],
    [QPP],
    [COUESC],
    [PROMCOUNET],
    [TEMPUNI],
    [TEMPUM],
    [MULCOM],
    [CODEIMPR],
    [CODEFOUR],
    [CODECAT],
    [DATECOUT],
    [QTECOM],
    [QTEACOM],
    SysDate)
  VALUES (
    @SOU_ID,
    @PRO_ID,
    @CLEMANU,
    @CLEDIST,
    @CLEPERS,
    @DESC,
    @QTEENS,
    @QTELOT,
    @QTEOTH,
    @CALCTIMSTP,
    @COUBRUTUNI,
    @COUUM,
    @QPP,
    @COUESC,
    @PROMCOUNET,
    @TEMPUNI,
    @TEMPUM,
    @MULCOM,
    @CODEIMPR,
    @CODEFOUR,
    @CODECAT,
    @DATECOUT,
    @QTECOM,
    @QTEACOM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACPRO
  SET
    [SOU_ID] = @SOU_ID,
    [PRO_ID] = @PRO_ID,
    [CLEMANU] = @CLEMANU,
    [CLEDIST] = @CLEDIST,
    [CLEPERS] = @CLEPERS,
    [DESC] = @DESC,
    [QTEENS] = @QTEENS,
    [QTELOT] = @QTELOT,
    [QTEOTH] = @QTEOTH,
    [CALCTIMSTP] = @CALCTIMSTP,
    [COUBRUTUNI] = @COUBRUTUNI,
    [COUUM] = @COUUM,
    [QPP] = @QPP,
    [COUESC] = @COUESC,
    [PROMCOUNET] = @PROMCOUNET,
    [TEMPUNI] = @TEMPUNI,
    [TEMPUM] = @TEMPUM,
    [MULCOM] = @MULCOM,
    [CODEIMPR] = @CODEIMPR,
    [CODEFOUR] = @CODEFOUR,
    [CODECAT] = @CODECAT,
    [DATECOUT] = @DATECOUT,
    [QTECOM] = @QTECOM,
    [QTEACOM] = @QTEACOM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_FACPRO_Delete] (
  @UniqueId bigint
) AS

DELETE FROM FACPRO WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_FACREL_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DIV_ID varchar(3),
  @TYPERELEVE varchar(1),
  @ORDRE varchar(6),
  @TYPEITEM varchar(1),
  @ITEM_ID varchar(20),
  @DESCR varchar(60),
  @QTE float,
  @SECTION float,
  @QTEUM varchar(2),
  @PROFIT float,
  @TYPETAXE varchar(1),
  @CODEIMPR varchar(2),
  @COUTANBRUT float,
  @TEMPSUNIT float,
  @TEMPSSEC float,
  @TEMPSUM varchar(2),
  @PROFITPLUS float,
  @PROFITMOIN float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACREL (
    [SOU_ID],
    [BLO_ID],
    [DIV_ID],
    [TYPERELEVE],
    [ORDRE],
    [TYPEITEM],
    [ITEM_ID],
    [DESCR],
    [QTE],
    [SECTION],
    [QTEUM],
    [PROFIT],
    [TYPETAXE],
    [CODEIMPR],
    [COUTANBRUT],
    [TEMPSUNIT],
    [TEMPSSEC],
    [TEMPSUM],
    [PROFITPLUS],
    [PROFITMOIN],
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DIV_ID,
    @TYPERELEVE,
    @ORDRE,
    @TYPEITEM,
    @ITEM_ID,
    @DESCR,
    @QTE,
    @SECTION,
    @QTEUM,
    @PROFIT,
    @TYPETAXE,
    @CODEIMPR,
    @COUTANBRUT,
    @TEMPSUNIT,
    @TEMPSSEC,
    @TEMPSUM,
    @PROFITPLUS,
    @PROFITMOIN,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACREL
  SET
    [SOU_ID] = @SOU_ID,
    [BLO_ID] = @BLO_ID,
    [DIV_ID] = @DIV_ID,
    [TYPERELEVE] = @TYPERELEVE,
    [ORDRE] = @ORDRE,
    [TYPEITEM] = @TYPEITEM,
    [ITEM_ID] = @ITEM_ID,
    [DESCR] = @DESCR,
    [QTE] = @QTE,
    [SECTION] = @SECTION,
    [QTEUM] = @QTEUM,
    [PROFIT] = @PROFIT,
    [TYPETAXE] = @TYPETAXE,
    [CODEIMPR] = @CODEIMPR,
    [COUTANBRUT] = @COUTANBRUT,
    [TEMPSUNIT] = @TEMPSUNIT,
    [TEMPSSEC] = @TEMPSSEC,
    [TEMPSUM] = @TEMPSUM,
    [PROFITPLUS] = @PROFITPLUS,
    [PROFITMOIN] = @PROFITMOIN,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_FACREL_Delete] (
  @UniqueId bigint
) AS

DELETE FROM FACREL WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_FACTURES_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @NODOC varchar(12),
  @DESCDOC varchar(200),
  @DATECREE datetime,
  @DATEDOC datetime,
  @DATEEXP datetime,
  @REF_ID varchar(20),
  @STATUT int,
  @NOCOMMANDE varchar(20),
  @NOTEINTERN text,
  @CLIENTNO varchar(20),
  @CLIENTCIE varchar(50),
  @CLIENTCNT varchar(50),
  @CLIENTRUE1 varchar(50),
  @CLIENTRUE2 varchar(50),
  @CLIENTVILL varchar(40),
  @CLIENTCP varchar(7),
  @CLIENTPROV varchar(40),
  @CLIENTPAYS varchar(40),
  @CLIENTBP varchar(30),
  @CLIENTTEL1 varchar(20),
  @CLIENTTEL2 varchar(20),
  @CLIENTTEL3 varchar(20),
  @CLIENTFAX varchar(20),
  @MEMESITE bit,
  @SITENO varchar(20),
  @SITECIE varchar(50),
  @SITECNT varchar(50),
  @SITERUE1 varchar(50),
  @SITERUE2 varchar(50),
  @SITEVILLE varchar(40),
  @SITECP varchar(7),
  @SITEPROV varchar(40),
  @SITEPAYS varchar(40),
  @SITEBP varchar(30),
  @SITETEL1 varchar(20),
  @SITETEL2 varchar(20),
  @SITETEL3 varchar(20),
  @SITEFAX varchar(20),
  @MATTOTALMD float,
  @NOTEPRINC text,
  @MATCOUTREL float,
  @MATCOUTLOT float,
  @MATVENDCAL float,
  @MATPORTTVP float,
  @SERCOUTCAL float,
  @SERVENDCAL float,
  @SERHRESCAL float,
  @SERPORTTVP float,
  @AUTCOUTCAL float,
  @AUTVENDCAL float,
  @AUTPORTTVP float,
  @OPTIONSSOM varchar(40),
  @MATCOUTMO float,
  @SERCOUTMO float,
  @AUTCOUTMO float,
  @MATADMPC float,
  @SERADMPC float,
  @AUTADMPC float,
  @MATADMMO float,
  @SERADMMO float,
  @AUTADMMO float,
  @MATPROFPC float,
  @SERPROFPC float,
  @AUTPROFPC float,
  @MATPROFMO float,
  @SERPROFMO float,
  @AUTPROFMO float,
  @GLOBAJUPC float,
  @GLOBAJUMO float,
  @GLOBEXPLIC varchar(40),
  @GLOBAJU2PC float,
  @GLOBAJU2MO float,
  @GLOBEXPL2 varchar(40),
  @OPTIONSIMP varchar(50),
  @OPIMPADJMA varchar(40),
  @OPIMPADJLA varchar(40),
  @OPIMPADJOT varchar(40),
  @NOTEBAS text,
  @MATTAXAB1 float,
  @MATTAXAB2 float,
  @MATTAXAB3 float,
  @MATTAXAB4 float,
  @MATTAXAB5 float,
  @MATTAXAB6 float,
  @SERTAXAB1 float,
  @SERTAXAB2 float,
  @SERTAXAB3 float,
  @SERTAXAB4 float,
  @SERTAXAB5 float,
  @SERTAXAB6 float,
  @AUTTAXAB1 float,
  @AUTTAXAB2 float,
  @AUTTAXAB3 float,
  @AUTTAXAB4 float,
  @AUTTAXAB5 float,
  @AUTTAXAB6 float,
  @TAXTYPCAL int,
  @AJUTAXAB1 float,
  @AJUTAXAB2 float,
  @AJUTAXAB3 float,
  @AJUTAXAB4 float,
  @AJUTAXAB5 float,
  @TOTTAXFED float,
  @TOTTAXPRV float,
  @TAX_ID varchar(20),
  @APPLIQUTVF bit,
  @APPLIQUTVP bit,
  @TVPSURCOUT bit,
  @TOTCALCULE bit,
  @CALCTIMSTP varchar(14),
  @UMPLAN varchar(2),
  @TYPEPROF varchar(1),
  @MATPROFDEF float,
  @TYPESRVPRO varchar(1),
  @TAUXMD float,
  @NUMLOTEXP float,
  @SYSTEM bit,
  @USER1 varchar(20),
  @USER2 varchar(20),
  @EST_NAME varchar(50)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACTURES (
    [SOU_ID],
    [NODOC],
    [DESCDOC],
    [DATECREE],
    [DATEDOC],
    [DATEEXP],
    [REF_ID],
    [STATUT],
    [NOCOMMANDE],
    [NOTEINTERN],
    [CLIENTNO],
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
    [MEMESITE],
    [SITENO],
    [SITECIE],
    [SITECNT],
    [SITERUE1],
    [SITERUE2],
    [SITEVILLE],
    [SITECP],
    [SITEPROV],
    [SITEPAYS],
    [SITEBP],
    [SITETEL1],
    [SITETEL2],
    [SITETEL3],
    [SITEFAX],
    [MATTOTALMD],
    [NOTEPRINC],
    [MATCOUTREL],
    [MATCOUTLOT],
    [MATVENDCAL],
    [MATPORTTVP],
    [SERCOUTCAL],
    [SERVENDCAL],
    [SERHRESCAL],
    [SERPORTTVP],
    [AUTCOUTCAL],
    [AUTVENDCAL],
    [AUTPORTTVP],
    [OPTIONSSOM],
    [MATCOUTMO],
    [SERCOUTMO],
    [AUTCOUTMO],
    [MATADMPC],
    [SERADMPC],
    [AUTADMPC],
    [MATADMMO],
    [SERADMMO],
    [AUTADMMO],
    [MATPROFPC],
    [SERPROFPC],
    [AUTPROFPC],
    [MATPROFMO],
    [SERPROFMO],
    [AUTPROFMO],
    [GLOBAJUPC],
    [GLOBAJUMO],
    [GLOBEXPLIC],
    [GLOBAJU2PC],
    [GLOBAJU2MO],
    [GLOBEXPL2],
    [OPTIONSIMP],
    [OPIMPADJMA],
    [OPIMPADJLA],
    [OPIMPADJOT],
    [NOTEBAS],
    [MATTAXAB1],
    [MATTAXAB2],
    [MATTAXAB3],
    [MATTAXAB4],
    [MATTAXAB5],
    [MATTAXAB6],
    [SERTAXAB1],
    [SERTAXAB2],
    [SERTAXAB3],
    [SERTAXAB4],
    [SERTAXAB5],
    [SERTAXAB6],
    [AUTTAXAB1],
    [AUTTAXAB2],
    [AUTTAXAB3],
    [AUTTAXAB4],
    [AUTTAXAB5],
    [AUTTAXAB6],
    [TAXTYPCAL],
    [AJUTAXAB1],
    [AJUTAXAB2],
    [AJUTAXAB3],
    [AJUTAXAB4],
    [AJUTAXAB5],
    [TOTTAXFED],
    [TOTTAXPRV],
    [TAX_ID],
    [APPLIQUTVF],
    [APPLIQUTVP],
    [TVPSURCOUT],
    [TOTCALCULE],
    [CALCTIMSTP],
    [UMPLAN],
    [TYPEPROF],
    [MATPROFDEF],
    [TYPESRVPRO],
    [TAUXMD],
    [NUMLOTEXP],
    [SYSTEM],
    [USER1],
    [USER2],
    [EST_NAME],
    SysDate)
  VALUES (
    @SOU_ID,
    @NODOC,
    @DESCDOC,
    @DATECREE,
    @DATEDOC,
    @DATEEXP,
    @REF_ID,
    @STATUT,
    @NOCOMMANDE,
    @NOTEINTERN,
    @CLIENTNO,
    @CLIENTCIE,
    @CLIENTCNT,
    @CLIENTRUE1,
    @CLIENTRUE2,
    @CLIENTVILL,
    @CLIENTCP,
    @CLIENTPROV,
    @CLIENTPAYS,
    @CLIENTBP,
    @CLIENTTEL1,
    @CLIENTTEL2,
    @CLIENTTEL3,
    @CLIENTFAX,
    @MEMESITE,
    @SITENO,
    @SITECIE,
    @SITECNT,
    @SITERUE1,
    @SITERUE2,
    @SITEVILLE,
    @SITECP,
    @SITEPROV,
    @SITEPAYS,
    @SITEBP,
    @SITETEL1,
    @SITETEL2,
    @SITETEL3,
    @SITEFAX,
    @MATTOTALMD,
    @NOTEPRINC,
    @MATCOUTREL,
    @MATCOUTLOT,
    @MATVENDCAL,
    @MATPORTTVP,
    @SERCOUTCAL,
    @SERVENDCAL,
    @SERHRESCAL,
    @SERPORTTVP,
    @AUTCOUTCAL,
    @AUTVENDCAL,
    @AUTPORTTVP,
    @OPTIONSSOM,
    @MATCOUTMO,
    @SERCOUTMO,
    @AUTCOUTMO,
    @MATADMPC,
    @SERADMPC,
    @AUTADMPC,
    @MATADMMO,
    @SERADMMO,
    @AUTADMMO,
    @MATPROFPC,
    @SERPROFPC,
    @AUTPROFPC,
    @MATPROFMO,
    @SERPROFMO,
    @AUTPROFMO,
    @GLOBAJUPC,
    @GLOBAJUMO,
    @GLOBEXPLIC,
    @GLOBAJU2PC,
    @GLOBAJU2MO,
    @GLOBEXPL2,
    @OPTIONSIMP,
    @OPIMPADJMA,
    @OPIMPADJLA,
    @OPIMPADJOT,
    @NOTEBAS,
    @MATTAXAB1,
    @MATTAXAB2,
    @MATTAXAB3,
    @MATTAXAB4,
    @MATTAXAB5,
    @MATTAXAB6,
    @SERTAXAB1,
    @SERTAXAB2,
    @SERTAXAB3,
    @SERTAXAB4,
    @SERTAXAB5,
    @SERTAXAB6,
    @AUTTAXAB1,
    @AUTTAXAB2,
    @AUTTAXAB3,
    @AUTTAXAB4,
    @AUTTAXAB5,
    @AUTTAXAB6,
    @TAXTYPCAL,
    @AJUTAXAB1,
    @AJUTAXAB2,
    @AJUTAXAB3,
    @AJUTAXAB4,
    @AJUTAXAB5,
    @TOTTAXFED,
    @TOTTAXPRV,
    @TAX_ID,
    @APPLIQUTVF,
    @APPLIQUTVP,
    @TVPSURCOUT,
    @TOTCALCULE,
    @CALCTIMSTP,
    @UMPLAN,
    @TYPEPROF,
    @MATPROFDEF,
    @TYPESRVPRO,
    @TAUXMD,
    @NUMLOTEXP,
    @SYSTEM,
    @USER1,
    @USER2,
    @EST_NAME,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACTURES
  SET
    [SOU_ID] = @SOU_ID,
    [NODOC] = @NODOC,
    [DESCDOC] = @DESCDOC,
    [DATECREE] = @DATECREE,
    [DATEDOC] = @DATEDOC,
    [DATEEXP] = @DATEEXP,
    [REF_ID] = @REF_ID,
    [STATUT] = @STATUT,
    [NOCOMMANDE] = @NOCOMMANDE,
    [NOTEINTERN] = @NOTEINTERN,
    [CLIENTNO] = @CLIENTNO,
    [CLIENTCIE] = @CLIENTCIE,
    [CLIENTCNT] = @CLIENTCNT,
    [CLIENTRUE1] = @CLIENTRUE1,
    [CLIENTRUE2] = @CLIENTRUE2,
    [CLIENTVILL] = @CLIENTVILL,
    [CLIENTCP] = @CLIENTCP,
    [CLIENTPROV] = @CLIENTPROV,
    [CLIENTPAYS] = @CLIENTPAYS,
    [CLIENTBP] = @CLIENTBP,
    [CLIENTTEL1] = @CLIENTTEL1,
    [CLIENTTEL2] = @CLIENTTEL2,
    [CLIENTTEL3] = @CLIENTTEL3,
    [CLIENTFAX] = @CLIENTFAX,
    [MEMESITE] = @MEMESITE,
    [SITENO] = @SITENO,
    [SITECIE] = @SITECIE,
    [SITECNT] = @SITECNT,
    [SITERUE1] = @SITERUE1,
    [SITERUE2] = @SITERUE2,
    [SITEVILLE] = @SITEVILLE,
    [SITECP] = @SITECP,
    [SITEPROV] = @SITEPROV,
    [SITEPAYS] = @SITEPAYS,
    [SITEBP] = @SITEBP,
    [SITETEL1] = @SITETEL1,
    [SITETEL2] = @SITETEL2,
    [SITETEL3] = @SITETEL3,
    [SITEFAX] = @SITEFAX,
    [MATTOTALMD] = @MATTOTALMD,
    [NOTEPRINC] = @NOTEPRINC,
    [MATCOUTREL] = @MATCOUTREL,
    [MATCOUTLOT] = @MATCOUTLOT,
    [MATVENDCAL] = @MATVENDCAL,
    [MATPORTTVP] = @MATPORTTVP,
    [SERCOUTCAL] = @SERCOUTCAL,
    [SERVENDCAL] = @SERVENDCAL,
    [SERHRESCAL] = @SERHRESCAL,
    [SERPORTTVP] = @SERPORTTVP,
    [AUTCOUTCAL] = @AUTCOUTCAL,
    [AUTVENDCAL] = @AUTVENDCAL,
    [AUTPORTTVP] = @AUTPORTTVP,
    [OPTIONSSOM] = @OPTIONSSOM,
    [MATCOUTMO] = @MATCOUTMO,
    [SERCOUTMO] = @SERCOUTMO,
    [AUTCOUTMO] = @AUTCOUTMO,
    [MATADMPC] = @MATADMPC,
    [SERADMPC] = @SERADMPC,
    [AUTADMPC] = @AUTADMPC,
    [MATADMMO] = @MATADMMO,
    [SERADMMO] = @SERADMMO,
    [AUTADMMO] = @AUTADMMO,
    [MATPROFPC] = @MATPROFPC,
    [SERPROFPC] = @SERPROFPC,
    [AUTPROFPC] = @AUTPROFPC,
    [MATPROFMO] = @MATPROFMO,
    [SERPROFMO] = @SERPROFMO,
    [AUTPROFMO] = @AUTPROFMO,
    [GLOBAJUPC] = @GLOBAJUPC,
    [GLOBAJUMO] = @GLOBAJUMO,
    [GLOBEXPLIC] = @GLOBEXPLIC,
    [GLOBAJU2PC] = @GLOBAJU2PC,
    [GLOBAJU2MO] = @GLOBAJU2MO,
    [GLOBEXPL2] = @GLOBEXPL2,
    [OPTIONSIMP] = @OPTIONSIMP,
    [OPIMPADJMA] = @OPIMPADJMA,
    [OPIMPADJLA] = @OPIMPADJLA,
    [OPIMPADJOT] = @OPIMPADJOT,
    [NOTEBAS] = @NOTEBAS,
    [MATTAXAB1] = @MATTAXAB1,
    [MATTAXAB2] = @MATTAXAB2,
    [MATTAXAB3] = @MATTAXAB3,
    [MATTAXAB4] = @MATTAXAB4,
    [MATTAXAB5] = @MATTAXAB5,
    [MATTAXAB6] = @MATTAXAB6,
    [SERTAXAB1] = @SERTAXAB1,
    [SERTAXAB2] = @SERTAXAB2,
    [SERTAXAB3] = @SERTAXAB3,
    [SERTAXAB4] = @SERTAXAB4,
    [SERTAXAB5] = @SERTAXAB5,
    [SERTAXAB6] = @SERTAXAB6,
    [AUTTAXAB1] = @AUTTAXAB1,
    [AUTTAXAB2] = @AUTTAXAB2,
    [AUTTAXAB3] = @AUTTAXAB3,
    [AUTTAXAB4] = @AUTTAXAB4,
    [AUTTAXAB5] = @AUTTAXAB5,
    [AUTTAXAB6] = @AUTTAXAB6,
    [TAXTYPCAL] = @TAXTYPCAL,
    [AJUTAXAB1] = @AJUTAXAB1,
    [AJUTAXAB2] = @AJUTAXAB2,
    [AJUTAXAB3] = @AJUTAXAB3,
    [AJUTAXAB4] = @AJUTAXAB4,
    [AJUTAXAB5] = @AJUTAXAB5,
    [TOTTAXFED] = @TOTTAXFED,
    [TOTTAXPRV] = @TOTTAXPRV,
    [TAX_ID] = @TAX_ID,
    [APPLIQUTVF] = @APPLIQUTVF,
    [APPLIQUTVP] = @APPLIQUTVP,
    [TVPSURCOUT] = @TVPSURCOUT,
    [TOTCALCULE] = @TOTCALCULE,
    [CALCTIMSTP] = @CALCTIMSTP,
    [UMPLAN] = @UMPLAN,
    [TYPEPROF] = @TYPEPROF,
    [MATPROFDEF] = @MATPROFDEF,
    [TYPESRVPRO] = @TYPESRVPRO,
    [TAUXMD] = @TAUXMD,
    [NUMLOTEXP] = @NUMLOTEXP,
    [SYSTEM] = @SYSTEM,
    [USER1] = @USER1,
    [USER2] = @USER2,
    [EST_NAME] = @EST_NAME,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_FACTURES_Delete] (
  @UniqueId bigint
) AS

DELETE FROM FACTURES WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_FACWEBLOG_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @WEB_ID varchar(15),
  @TRF_DATE varchar(25),
  @RESULT varchar(10),
  @MESSAGE varchar(60)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACWEBLOG (
    [SOU_ID],
    [WEB_ID],
    [TRF_DATE],
    [RESULT],
    [MESSAGE],
    SysDate)
  VALUES (
    @SOU_ID,
    @WEB_ID,
    @TRF_DATE,
    @RESULT,
    @MESSAGE,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACWEBLOG
  SET
    [SOU_ID] = @SOU_ID,
    [WEB_ID] = @WEB_ID,
    [TRF_DATE] = @TRF_DATE,
    [RESULT] = @RESULT,
    [MESSAGE] = @MESSAGE,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_FACWEBLOG_Delete] (
  @UniqueId bigint
) AS

DELETE FROM FACWEBLOG WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_FRAIS_Update] (
  @UniqueId bigint,
  @ORDRE varchar(6),
  @DESCFRAIS varchar(50),
  @COUTUNI float,
  @FRAISUM varchar(2),
  @PROFIT float,
  @INCLSOU bit,
  @INCLFAC bit,
  @SYSTEM bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FRAIS (
    [ORDRE],
    [DESCFRAIS],
    [COUTUNI],
    [FRAISUM],
    [PROFIT],
    [INCLSOU],
    [INCLFAC],
    [SYSTEM],
    SysDate)
  VALUES (
    @ORDRE,
    @DESCFRAIS,
    @COUTUNI,
    @FRAISUM,
    @PROFIT,
    @INCLSOU,
    @INCLFAC,
    @SYSTEM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FRAIS
  SET
    [ORDRE] = @ORDRE,
    [DESCFRAIS] = @DESCFRAIS,
    [COUTUNI] = @COUTUNI,
    [FRAISUM] = @FRAISUM,
    [PROFIT] = @PROFIT,
    [INCLSOU] = @INCLSOU,
    [INCLFAC] = @INCLFAC,
    [SYSTEM] = @SYSTEM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_FRAIS_Delete] (
  @UniqueId bigint
) AS

DELETE FROM FRAIS WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_IMPRIMER_Update] (
  @UniqueId bigint,
  @NOMCONFIG varchar(30),
  @TYPECONFIG varchar(20),
  @NOMIMPRIM varchar(30),
  @LANGUE int,
  @OBJECT text,
  @SYSTEM bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO IMPRIMER (
    [NOMCONFIG],
    [TYPECONFIG],
    [NOMIMPRIM],
    [LANGUE],
    [OBJECT],
    [SYSTEM],
    SysDate)
  VALUES (
    @NOMCONFIG,
    @TYPECONFIG,
    @NOMIMPRIM,
    @LANGUE,
    @OBJECT,
    @SYSTEM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    IMPRIMER
  SET
    [NOMCONFIG] = @NOMCONFIG,
    [TYPECONFIG] = @TYPECONFIG,
    [NOMIMPRIM] = @NOMIMPRIM,
    [LANGUE] = @LANGUE,
    [OBJECT] = @OBJECT,
    [SYSTEM] = @SYSTEM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_IMPRIMER_Delete] (
  @UniqueId bigint
) AS

DELETE FROM IMPRIMER WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_NOTES_Update] (
  @UniqueId bigint,
  @NOTE_ID varchar(20),
  @DESCR varchar(40),
  @NOTE text,
  @NOTETYPE varchar(2),
  @DEFAULT bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO NOTES (
    [NOTE_ID],
    [DESCR],
    [NOTE],
    [NOTETYPE],
    [DEFAULT],
    SysDate)
  VALUES (
    @NOTE_ID,
    @DESCR,
    @NOTE,
    @NOTETYPE,
    @DEFAULT,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    NOTES
  SET
    [NOTE_ID] = @NOTE_ID,
    [DESCR] = @DESCR,
    [NOTE] = @NOTE,
    [NOTETYPE] = @NOTETYPE,
    [DEFAULT] = @DEFAULT,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_NOTES_Delete] (
  @UniqueId bigint
) AS

DELETE FROM NOTES WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_PROCAT_Update] (
  @UniqueId bigint,
  @CODECAT varchar(3),
  @DESC varchar(40)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO PROCAT (
    [CODECAT],
    [DESC],
    SysDate)
  VALUES (
    @CODECAT,
    @DESC,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    PROCAT
  SET
    [CODECAT] = @CODECAT,
    [DESC] = @DESC,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_PROCAT_Delete] (
  @UniqueId bigint
) AS

DELETE FROM PROCAT WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_PRODUITS_Update] (
  @UniqueId bigint,
  @PRO_ID varchar(20),
  @CLEMANU varchar(20),
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
  @DATECREE datetime,
  @PATHPICT varchar(60),
  @PATHSPEC varchar(60),
  @IMAGE varchar(1),
  @USER1 varchar(20),
  @USER2 varchar(20)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO PRODUITS (
    [PRO_ID],
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
    [DATECREE],
    [PATHPICT],
    [PATHSPEC],
    [IMAGE],
    [USER1],
    [USER2],
    SysDate)
  VALUES (
    @PRO_ID,
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
    @DATECREE,
    @PATHPICT,
    @PATHSPEC,
    @IMAGE,
    @USER1,
    @USER2,
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
    [DATECREE] = @DATECREE,
    [PATHPICT] = @PATHPICT,
    [PATHSPEC] = @PATHSPEC,
    [IMAGE] = @IMAGE,
    [USER1] = @USER1,
    [USER2] = @USER2,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_PRODUITS_Delete] (
  @UniqueId bigint
) AS

DELETE FROM PRODUITS WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_PROFGRID_Update] (
  @UniqueId bigint,
  @UM varchar(2),
  @PRIXBAS float,
  @PRIXHAUT float,
  @PROFIT float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO PROFGRID (
    [UM],
    [PRIXBAS],
    [PRIXHAUT],
    [PROFIT],
    SysDate)
  VALUES (
    @UM,
    @PRIXBAS,
    @PRIXHAUT,
    @PROFIT,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    PROFGRID
  SET
    [UM] = @UM,
    [PRIXBAS] = @PRIXBAS,
    [PRIXHAUT] = @PRIXHAUT,
    [PROFIT] = @PROFIT,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_PROFGRID_Delete] (
  @UniqueId bigint
) AS

DELETE FROM PROFGRID WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_PROGLOSS_Update] (
  @UniqueId bigint,
  @TYPEGLOSS varchar(2),
  @CATEGORIE varchar(30),
  @SOUSCAT varchar(30),
  @CODE varchar(20),
  @DESCRIPTIO varchar(50),
  @CODEBANK varchar(3)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO PROGLOSS (
    [TYPEGLOSS],
    [CATEGORIE],
    [SOUSCAT],
    [CODE],
    [DESCRIPTIO],
    [CODEBANK],
    SysDate)
  VALUES (
    @TYPEGLOSS,
    @CATEGORIE,
    @SOUSCAT,
    @CODE,
    @DESCRIPTIO,
    @CODEBANK,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    PROGLOSS
  SET
    [TYPEGLOSS] = @TYPEGLOSS,
    [CATEGORIE] = @CATEGORIE,
    [SOUSCAT] = @SOUSCAT,
    [CODE] = @CODE,
    [DESCRIPTIO] = @DESCRIPTIO,
    [CODEBANK] = @CODEBANK,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_PROGLOSS_Delete] (
  @UniqueId bigint
) AS

DELETE FROM PROGLOSS WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_SOUAMD_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DIV_ID varchar(3),
  @FACTMD float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUAMD (
    [SOU_ID],
    [BLO_ID],
    [DIV_ID],
    [FACTMD],
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DIV_ID,
    @FACTMD,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUAMD
  SET
    [SOU_ID] = @SOU_ID,
    [BLO_ID] = @BLO_ID,
    [DIV_ID] = @DIV_ID,
    [FACTMD] = @FACTMD,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_SOUAMD_Delete] (
  @UniqueId bigint
) AS

DELETE FROM SOUAMD WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_SOUBLO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DESC varchar(40),
  @MULT int
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUBLO (
    [SOU_ID],
    [BLO_ID],
    [DESC],
    [MULT],
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DESC,
    @MULT,
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_SOUBLO_Delete] (
  @UniqueId bigint
) AS

DELETE FROM SOUBLO WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_SOUDIV_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @DIV_ID varchar(3),
  @DESC varchar(40)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUDIV (
    [SOU_ID],
    [DIV_ID],
    [DESC],
    SysDate)
  VALUES (
    @SOU_ID,
    @DIV_ID,
    @DESC,
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_SOUDIV_Delete] (
  @UniqueId bigint
) AS

DELETE FROM SOUDIV WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_SOUENS_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @ENS_ID varchar(20),
  @DESC varchar(40),
  @QTETOT float,
  @QTETOTSECT float,
  @CALCTIMSTP varchar(14),
  @COUUM varchar(2),
  @TEMPUNI float,
  @TEMPSEC float,
  @TEMPUM varchar(2),
  @DATECREE datetime,
  @OLDESTPROD datetime,
  @CLEPERS varchar(40),
  @PROFIT float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUENS (
    [SOU_ID],
    [ENS_ID],
    [DESC],
    [QTETOT],
    [QTETOTSECT],
    [CALCTIMSTP],
    [COUUM],
    [TEMPUNI],
    [TEMPSEC],
    [TEMPUM],
    [DATECREE],
    [OLDESTPROD],
    [CLEPERS],
    [PROFIT],
    SysDate)
  VALUES (
    @SOU_ID,
    @ENS_ID,
    @DESC,
    @QTETOT,
    @QTETOTSECT,
    @CALCTIMSTP,
    @COUUM,
    @TEMPUNI,
    @TEMPSEC,
    @TEMPUM,
    @DATECREE,
    @OLDESTPROD,
    @CLEPERS,
    @PROFIT,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUENS
  SET
    [SOU_ID] = @SOU_ID,
    [ENS_ID] = @ENS_ID,
    [DESC] = @DESC,
    [QTETOT] = @QTETOT,
    [QTETOTSECT] = @QTETOTSECT,
    [CALCTIMSTP] = @CALCTIMSTP,
    [COUUM] = @COUUM,
    [TEMPUNI] = @TEMPUNI,
    [TEMPSEC] = @TEMPSEC,
    [TEMPUM] = @TEMPUM,
    [DATECREE] = @DATECREE,
    [OLDESTPROD] = @OLDESTPROD,
    [CLEPERS] = @CLEPERS,
    [PROFIT] = @PROFIT,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_SOUENS_Delete] (
  @UniqueId bigint
) AS

DELETE FROM SOUENS WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_SOUENSCO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @ENS_ID varchar(20),
  @PRO_ID varchar(20),
  @ORDRE varchar(6),
  @QTE float,
  @QTEUM varchar(2),
  @TYPRATIO varchar(1),
  @DIV float,
  @DIVUM varchar(2)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUENSCO (
    [SOU_ID],
    [ENS_ID],
    [PRO_ID],
    [ORDRE],
    [QTE],
    [QTEUM],
    [TYPRATIO],
    [DIV],
    [DIVUM],
    SysDate)
  VALUES (
    @SOU_ID,
    @ENS_ID,
    @PRO_ID,
    @ORDRE,
    @QTE,
    @QTEUM,
    @TYPRATIO,
    @DIV,
    @DIVUM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUENSCO
  SET
    [SOU_ID] = @SOU_ID,
    [ENS_ID] = @ENS_ID,
    [PRO_ID] = @PRO_ID,
    [ORDRE] = @ORDRE,
    [QTE] = @QTE,
    [QTEUM] = @QTEUM,
    [TYPRATIO] = @TYPRATIO,
    [DIV] = @DIV,
    [DIVUM] = @DIVUM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_SOUENSCO_Delete] (
  @UniqueId bigint
) AS

DELETE FROM SOUENSCO WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_SOULOTS_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @LOTS_ID varchar(20),
  @DESC varchar(40),
  @QTETOT float,
  @QTETOTSECT float,
  @CALCTIMSTP varchar(14),
  @COUUM varchar(2),
  @TEMPUNI float,
  @TEMPUM varchar(2),
  @DATECREE datetime,
  @OLDESTPROD datetime,
  @CLEPERS varchar(40),
  @PROFIT float,
  @COUTANTSEL int,
  @COUTANT1 float,
  @COUTANT2 float,
  @COUTANT3 float,
  @COUTANT4 float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOULOTS (
    [SOU_ID],
    [LOTS_ID],
    [DESC],
    [QTETOT],
    [QTETOTSECT],
    [CALCTIMSTP],
    [COUUM],
    [TEMPUNI],
    [TEMPUM],
    [DATECREE],
    [OLDESTPROD],
    [CLEPERS],
    [PROFIT],
    [COUTANTSEL],
    [COUTANT1],
    [COUTANT2],
    [COUTANT3],
    [COUTANT4],
    SysDate)
  VALUES (
    @SOU_ID,
    @LOTS_ID,
    @DESC,
    @QTETOT,
    @QTETOTSECT,
    @CALCTIMSTP,
    @COUUM,
    @TEMPUNI,
    @TEMPUM,
    @DATECREE,
    @OLDESTPROD,
    @CLEPERS,
    @PROFIT,
    @COUTANTSEL,
    @COUTANT1,
    @COUTANT2,
    @COUTANT3,
    @COUTANT4,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOULOTS
  SET
    [SOU_ID] = @SOU_ID,
    [LOTS_ID] = @LOTS_ID,
    [DESC] = @DESC,
    [QTETOT] = @QTETOT,
    [QTETOTSECT] = @QTETOTSECT,
    [CALCTIMSTP] = @CALCTIMSTP,
    [COUUM] = @COUUM,
    [TEMPUNI] = @TEMPUNI,
    [TEMPUM] = @TEMPUM,
    [DATECREE] = @DATECREE,
    [OLDESTPROD] = @OLDESTPROD,
    [CLEPERS] = @CLEPERS,
    [PROFIT] = @PROFIT,
    [COUTANTSEL] = @COUTANTSEL,
    [COUTANT1] = @COUTANT1,
    [COUTANT2] = @COUTANT2,
    [COUTANT3] = @COUTANT3,
    [COUTANT4] = @COUTANT4,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_SOULOTS_Delete] (
  @UniqueId bigint
) AS

DELETE FROM SOULOTS WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_SOULOTSCO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @LOTS_ID varchar(20),
  @PRO_ID varchar(20),
  @ORDRE varchar(6),
  @QTE float,
  @QTEUM varchar(2)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOULOTSCO (
    [SOU_ID],
    [LOTS_ID],
    [PRO_ID],
    [ORDRE],
    [QTE],
    [QTEUM],
    SysDate)
  VALUES (
    @SOU_ID,
    @LOTS_ID,
    @PRO_ID,
    @ORDRE,
    @QTE,
    @QTEUM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOULOTSCO
  SET
    [SOU_ID] = @SOU_ID,
    [LOTS_ID] = @LOTS_ID,
    [PRO_ID] = @PRO_ID,
    [ORDRE] = @ORDRE,
    [QTE] = @QTE,
    [QTEUM] = @QTEUM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_SOULOTSCO_Delete] (
  @UniqueId bigint
) AS

DELETE FROM SOULOTSCO WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_SOUMIS_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @NODOC varchar(12),
  @DESCDOC varchar(200),
  @DATECREE datetime,
  @DATEDOC datetime,
  @DATEEXP datetime,
  @REF_ID varchar(20),
  @STATUT int,
  @NOCOMMANDE varchar(20),
  @NOTEINTERN text,
  @CLIENTNO varchar(20),
  @CLIENTCIE varchar(50),
  @CLIENTCNT varchar(50),
  @CLIENTRUE1 varchar(50),
  @CLIENTRUE2 varchar(50),
  @CLIENTVILL varchar(40),
  @CLIENTCP varchar(7),
  @CLIENTPROV varchar(40),
  @CLIENTPAYS varchar(40),
  @CLIENTBP varchar(30),
  @CLIENTTEL1 varchar(20),
  @CLIENTTEL2 varchar(20),
  @CLIENTTEL3 varchar(20),
  @CLIENTFAX varchar(20),
  @MEMESITE bit,
  @SITENO varchar(20),
  @SITECIE varchar(50),
  @SITECNT varchar(50),
  @SITERUE1 varchar(50),
  @SITERUE2 varchar(50),
  @SITEVILLE varchar(40),
  @SITECP varchar(7),
  @SITEPROV varchar(40),
  @SITEPAYS varchar(40),
  @SITEBP varchar(30),
  @SITETEL1 varchar(20),
  @SITETEL2 varchar(20),
  @SITETEL3 varchar(20),
  @SITEFAX varchar(20),
  @MATTOTALMD float,
  @NOTEPRINC text,
  @MATCOUTREL float,
  @MATCOUTLOT float,
  @MATVENDCAL float,
  @MATPORTTVP float,
  @SERCOUTCAL float,
  @SERVENDCAL float,
  @SERHRESCAL float,
  @SERPORTTVP float,
  @AUTCOUTCAL float,
  @AUTVENDCAL float,
  @AUTPORTTVP float,
  @OPTIONSSOM varchar(40),
  @MATCOUTMO float,
  @SERCOUTMO float,
  @AUTCOUTMO float,
  @MATADMPC float,
  @SERADMPC float,
  @AUTADMPC float,
  @MATADMMO float,
  @SERADMMO float,
  @AUTADMMO float,
  @MATPROFPC float,
  @SERPROFPC float,
  @AUTPROFPC float,
  @MATPROFMO float,
  @SERPROFMO float,
  @AUTPROFMO float,
  @GLOBAJUPC float,
  @GLOBAJUMO float,
  @GLOBEXPLIC varchar(40),
  @GLOBAJU2PC float,
  @GLOBAJU2MO float,
  @GLOBEXPL2 varchar(40),
  @OPTIONSIMP varchar(50),
  @OPIMPADJMA varchar(40),
  @OPIMPADJLA varchar(40),
  @OPIMPADJOT varchar(40),
  @NOTEBAS text,
  @MATTAXAB1 float,
  @MATTAXAB2 float,
  @MATTAXAB3 float,
  @MATTAXAB4 float,
  @MATTAXAB5 float,
  @MATTAXAB6 float,
  @SERTAXAB1 float,
  @SERTAXAB2 float,
  @SERTAXAB3 float,
  @SERTAXAB4 float,
  @SERTAXAB5 float,
  @SERTAXAB6 float,
  @AUTTAXAB1 float,
  @AUTTAXAB2 float,
  @AUTTAXAB3 float,
  @AUTTAXAB4 float,
  @AUTTAXAB5 float,
  @AUTTAXAB6 float,
  @TAXTYPCAL int,
  @AJUTAXAB1 float,
  @AJUTAXAB2 float,
  @AJUTAXAB3 float,
  @AJUTAXAB4 float,
  @AJUTAXAB5 float,
  @TOTTAXFED float,
  @TOTTAXPRV float,
  @TAX_ID varchar(20),
  @APPLIQUTVF bit,
  @APPLIQUTVP bit,
  @TVPSURCOUT bit,
  @TOTCALCULE bit,
  @CALCTIMSTP varchar(14),
  @UMPLAN varchar(2),
  @TYPEPROF varchar(1),
  @MATPROFDEF float,
  @TYPESRVPRO varchar(1),
  @TAUXMD float,
  @NUMLOTEXP float,
  @SYSTEM bit,
  @USER1 varchar(20),
  @USER2 varchar(20),
  @EST_NAME varchar(50)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUMIS (
    [SOU_ID],
    [NODOC],
    [DESCDOC],
    [DATECREE],
    [DATEDOC],
    [DATEEXP],
    [REF_ID],
    [STATUT],
    [NOCOMMANDE],
    [NOTEINTERN],
    [CLIENTNO],
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
    [MEMESITE],
    [SITENO],
    [SITECIE],
    [SITECNT],
    [SITERUE1],
    [SITERUE2],
    [SITEVILLE],
    [SITECP],
    [SITEPROV],
    [SITEPAYS],
    [SITEBP],
    [SITETEL1],
    [SITETEL2],
    [SITETEL3],
    [SITEFAX],
    [MATTOTALMD],
    [NOTEPRINC],
    [MATCOUTREL],
    [MATCOUTLOT],
    [MATVENDCAL],
    [MATPORTTVP],
    [SERCOUTCAL],
    [SERVENDCAL],
    [SERHRESCAL],
    [SERPORTTVP],
    [AUTCOUTCAL],
    [AUTVENDCAL],
    [AUTPORTTVP],
    [OPTIONSSOM],
    [MATCOUTMO],
    [SERCOUTMO],
    [AUTCOUTMO],
    [MATADMPC],
    [SERADMPC],
    [AUTADMPC],
    [MATADMMO],
    [SERADMMO],
    [AUTADMMO],
    [MATPROFPC],
    [SERPROFPC],
    [AUTPROFPC],
    [MATPROFMO],
    [SERPROFMO],
    [AUTPROFMO],
    [GLOBAJUPC],
    [GLOBAJUMO],
    [GLOBEXPLIC],
    [GLOBAJU2PC],
    [GLOBAJU2MO],
    [GLOBEXPL2],
    [OPTIONSIMP],
    [OPIMPADJMA],
    [OPIMPADJLA],
    [OPIMPADJOT],
    [NOTEBAS],
    [MATTAXAB1],
    [MATTAXAB2],
    [MATTAXAB3],
    [MATTAXAB4],
    [MATTAXAB5],
    [MATTAXAB6],
    [SERTAXAB1],
    [SERTAXAB2],
    [SERTAXAB3],
    [SERTAXAB4],
    [SERTAXAB5],
    [SERTAXAB6],
    [AUTTAXAB1],
    [AUTTAXAB2],
    [AUTTAXAB3],
    [AUTTAXAB4],
    [AUTTAXAB5],
    [AUTTAXAB6],
    [TAXTYPCAL],
    [AJUTAXAB1],
    [AJUTAXAB2],
    [AJUTAXAB3],
    [AJUTAXAB4],
    [AJUTAXAB5],
    [TOTTAXFED],
    [TOTTAXPRV],
    [TAX_ID],
    [APPLIQUTVF],
    [APPLIQUTVP],
    [TVPSURCOUT],
    [TOTCALCULE],
    [CALCTIMSTP],
    [UMPLAN],
    [TYPEPROF],
    [MATPROFDEF],
    [TYPESRVPRO],
    [TAUXMD],
    [NUMLOTEXP],
    [SYSTEM],
    [USER1],
    [USER2],
    [EST_NAME],
    SysDate)
  VALUES (
    @SOU_ID,
    @NODOC,
    @DESCDOC,
    @DATECREE,
    @DATEDOC,
    @DATEEXP,
    @REF_ID,
    @STATUT,
    @NOCOMMANDE,
    @NOTEINTERN,
    @CLIENTNO,
    @CLIENTCIE,
    @CLIENTCNT,
    @CLIENTRUE1,
    @CLIENTRUE2,
    @CLIENTVILL,
    @CLIENTCP,
    @CLIENTPROV,
    @CLIENTPAYS,
    @CLIENTBP,
    @CLIENTTEL1,
    @CLIENTTEL2,
    @CLIENTTEL3,
    @CLIENTFAX,
    @MEMESITE,
    @SITENO,
    @SITECIE,
    @SITECNT,
    @SITERUE1,
    @SITERUE2,
    @SITEVILLE,
    @SITECP,
    @SITEPROV,
    @SITEPAYS,
    @SITEBP,
    @SITETEL1,
    @SITETEL2,
    @SITETEL3,
    @SITEFAX,
    @MATTOTALMD,
    @NOTEPRINC,
    @MATCOUTREL,
    @MATCOUTLOT,
    @MATVENDCAL,
    @MATPORTTVP,
    @SERCOUTCAL,
    @SERVENDCAL,
    @SERHRESCAL,
    @SERPORTTVP,
    @AUTCOUTCAL,
    @AUTVENDCAL,
    @AUTPORTTVP,
    @OPTIONSSOM,
    @MATCOUTMO,
    @SERCOUTMO,
    @AUTCOUTMO,
    @MATADMPC,
    @SERADMPC,
    @AUTADMPC,
    @MATADMMO,
    @SERADMMO,
    @AUTADMMO,
    @MATPROFPC,
    @SERPROFPC,
    @AUTPROFPC,
    @MATPROFMO,
    @SERPROFMO,
    @AUTPROFMO,
    @GLOBAJUPC,
    @GLOBAJUMO,
    @GLOBEXPLIC,
    @GLOBAJU2PC,
    @GLOBAJU2MO,
    @GLOBEXPL2,
    @OPTIONSIMP,
    @OPIMPADJMA,
    @OPIMPADJLA,
    @OPIMPADJOT,
    @NOTEBAS,
    @MATTAXAB1,
    @MATTAXAB2,
    @MATTAXAB3,
    @MATTAXAB4,
    @MATTAXAB5,
    @MATTAXAB6,
    @SERTAXAB1,
    @SERTAXAB2,
    @SERTAXAB3,
    @SERTAXAB4,
    @SERTAXAB5,
    @SERTAXAB6,
    @AUTTAXAB1,
    @AUTTAXAB2,
    @AUTTAXAB3,
    @AUTTAXAB4,
    @AUTTAXAB5,
    @AUTTAXAB6,
    @TAXTYPCAL,
    @AJUTAXAB1,
    @AJUTAXAB2,
    @AJUTAXAB3,
    @AJUTAXAB4,
    @AJUTAXAB5,
    @TOTTAXFED,
    @TOTTAXPRV,
    @TAX_ID,
    @APPLIQUTVF,
    @APPLIQUTVP,
    @TVPSURCOUT,
    @TOTCALCULE,
    @CALCTIMSTP,
    @UMPLAN,
    @TYPEPROF,
    @MATPROFDEF,
    @TYPESRVPRO,
    @TAUXMD,
    @NUMLOTEXP,
    @SYSTEM,
    @USER1,
    @USER2,
    @EST_NAME,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUMIS
  SET
    [SOU_ID] = @SOU_ID,
    [NODOC] = @NODOC,
    [DESCDOC] = @DESCDOC,
    [DATECREE] = @DATECREE,
    [DATEDOC] = @DATEDOC,
    [DATEEXP] = @DATEEXP,
    [REF_ID] = @REF_ID,
    [STATUT] = @STATUT,
    [NOCOMMANDE] = @NOCOMMANDE,
    [NOTEINTERN] = @NOTEINTERN,
    [CLIENTNO] = @CLIENTNO,
    [CLIENTCIE] = @CLIENTCIE,
    [CLIENTCNT] = @CLIENTCNT,
    [CLIENTRUE1] = @CLIENTRUE1,
    [CLIENTRUE2] = @CLIENTRUE2,
    [CLIENTVILL] = @CLIENTVILL,
    [CLIENTCP] = @CLIENTCP,
    [CLIENTPROV] = @CLIENTPROV,
    [CLIENTPAYS] = @CLIENTPAYS,
    [CLIENTBP] = @CLIENTBP,
    [CLIENTTEL1] = @CLIENTTEL1,
    [CLIENTTEL2] = @CLIENTTEL2,
    [CLIENTTEL3] = @CLIENTTEL3,
    [CLIENTFAX] = @CLIENTFAX,
    [MEMESITE] = @MEMESITE,
    [SITENO] = @SITENO,
    [SITECIE] = @SITECIE,
    [SITECNT] = @SITECNT,
    [SITERUE1] = @SITERUE1,
    [SITERUE2] = @SITERUE2,
    [SITEVILLE] = @SITEVILLE,
    [SITECP] = @SITECP,
    [SITEPROV] = @SITEPROV,
    [SITEPAYS] = @SITEPAYS,
    [SITEBP] = @SITEBP,
    [SITETEL1] = @SITETEL1,
    [SITETEL2] = @SITETEL2,
    [SITETEL3] = @SITETEL3,
    [SITEFAX] = @SITEFAX,
    [MATTOTALMD] = @MATTOTALMD,
    [NOTEPRINC] = @NOTEPRINC,
    [MATCOUTREL] = @MATCOUTREL,
    [MATCOUTLOT] = @MATCOUTLOT,
    [MATVENDCAL] = @MATVENDCAL,
    [MATPORTTVP] = @MATPORTTVP,
    [SERCOUTCAL] = @SERCOUTCAL,
    [SERVENDCAL] = @SERVENDCAL,
    [SERHRESCAL] = @SERHRESCAL,
    [SERPORTTVP] = @SERPORTTVP,
    [AUTCOUTCAL] = @AUTCOUTCAL,
    [AUTVENDCAL] = @AUTVENDCAL,
    [AUTPORTTVP] = @AUTPORTTVP,
    [OPTIONSSOM] = @OPTIONSSOM,
    [MATCOUTMO] = @MATCOUTMO,
    [SERCOUTMO] = @SERCOUTMO,
    [AUTCOUTMO] = @AUTCOUTMO,
    [MATADMPC] = @MATADMPC,
    [SERADMPC] = @SERADMPC,
    [AUTADMPC] = @AUTADMPC,
    [MATADMMO] = @MATADMMO,
    [SERADMMO] = @SERADMMO,
    [AUTADMMO] = @AUTADMMO,
    [MATPROFPC] = @MATPROFPC,
    [SERPROFPC] = @SERPROFPC,
    [AUTPROFPC] = @AUTPROFPC,
    [MATPROFMO] = @MATPROFMO,
    [SERPROFMO] = @SERPROFMO,
    [AUTPROFMO] = @AUTPROFMO,
    [GLOBAJUPC] = @GLOBAJUPC,
    [GLOBAJUMO] = @GLOBAJUMO,
    [GLOBEXPLIC] = @GLOBEXPLIC,
    [GLOBAJU2PC] = @GLOBAJU2PC,
    [GLOBAJU2MO] = @GLOBAJU2MO,
    [GLOBEXPL2] = @GLOBEXPL2,
    [OPTIONSIMP] = @OPTIONSIMP,
    [OPIMPADJMA] = @OPIMPADJMA,
    [OPIMPADJLA] = @OPIMPADJLA,
    [OPIMPADJOT] = @OPIMPADJOT,
    [NOTEBAS] = @NOTEBAS,
    [MATTAXAB1] = @MATTAXAB1,
    [MATTAXAB2] = @MATTAXAB2,
    [MATTAXAB3] = @MATTAXAB3,
    [MATTAXAB4] = @MATTAXAB4,
    [MATTAXAB5] = @MATTAXAB5,
    [MATTAXAB6] = @MATTAXAB6,
    [SERTAXAB1] = @SERTAXAB1,
    [SERTAXAB2] = @SERTAXAB2,
    [SERTAXAB3] = @SERTAXAB3,
    [SERTAXAB4] = @SERTAXAB4,
    [SERTAXAB5] = @SERTAXAB5,
    [SERTAXAB6] = @SERTAXAB6,
    [AUTTAXAB1] = @AUTTAXAB1,
    [AUTTAXAB2] = @AUTTAXAB2,
    [AUTTAXAB3] = @AUTTAXAB3,
    [AUTTAXAB4] = @AUTTAXAB4,
    [AUTTAXAB5] = @AUTTAXAB5,
    [AUTTAXAB6] = @AUTTAXAB6,
    [TAXTYPCAL] = @TAXTYPCAL,
    [AJUTAXAB1] = @AJUTAXAB1,
    [AJUTAXAB2] = @AJUTAXAB2,
    [AJUTAXAB3] = @AJUTAXAB3,
    [AJUTAXAB4] = @AJUTAXAB4,
    [AJUTAXAB5] = @AJUTAXAB5,
    [TOTTAXFED] = @TOTTAXFED,
    [TOTTAXPRV] = @TOTTAXPRV,
    [TAX_ID] = @TAX_ID,
    [APPLIQUTVF] = @APPLIQUTVF,
    [APPLIQUTVP] = @APPLIQUTVP,
    [TVPSURCOUT] = @TVPSURCOUT,
    [TOTCALCULE] = @TOTCALCULE,
    [CALCTIMSTP] = @CALCTIMSTP,
    [UMPLAN] = @UMPLAN,
    [TYPEPROF] = @TYPEPROF,
    [MATPROFDEF] = @MATPROFDEF,
    [TYPESRVPRO] = @TYPESRVPRO,
    [TAUXMD] = @TAUXMD,
    [NUMLOTEXP] = @NUMLOTEXP,
    [SYSTEM] = @SYSTEM,
    [USER1] = @USER1,
    [USER2] = @USER2,
    [EST_NAME] = @EST_NAME,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_SOUMIS_Delete] (
  @UniqueId bigint
) AS

DELETE FROM SOUMIS WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_SOUPRO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @PRO_ID varchar(20),
  @CLEMANU varchar(20),
  @CLEDIST varchar(20),
  @CLEPERS varchar(20),
  @DESC varchar(60),
  @QTEENS float,
  @QTELOT float,
  @QTEOTH float,
  @CALCTIMSTP varchar(14),
  @COUBRUTUNI float,
  @COUUM varchar(2),
  @QPP float,
  @COUESC float,
  @PROMCOUNET float,
  @TEMPUNI float,
  @TEMPUM varchar(2),
  @MULCOM float,
  @CODEIMPR varchar(20),
  @CODEFOUR varchar(2),
  @CODECAT varchar(3),
  @DATECOUT datetime,
  @QTECOM float,
  @QTEACOM float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUPRO (
    [SOU_ID],
    [PRO_ID],
    [CLEMANU],
    [CLEDIST],
    [CLEPERS],
    [DESC],
    [QTEENS],
    [QTELOT],
    [QTEOTH],
    [CALCTIMSTP],
    [COUBRUTUNI],
    [COUUM],
    [QPP],
    [COUESC],
    [PROMCOUNET],
    [TEMPUNI],
    [TEMPUM],
    [MULCOM],
    [CODEIMPR],
    [CODEFOUR],
    [CODECAT],
    [DATECOUT],
    [QTECOM],
    [QTEACOM],
    SysDate)
  VALUES (
    @SOU_ID,
    @PRO_ID,
    @CLEMANU,
    @CLEDIST,
    @CLEPERS,
    @DESC,
    @QTEENS,
    @QTELOT,
    @QTEOTH,
    @CALCTIMSTP,
    @COUBRUTUNI,
    @COUUM,
    @QPP,
    @COUESC,
    @PROMCOUNET,
    @TEMPUNI,
    @TEMPUM,
    @MULCOM,
    @CODEIMPR,
    @CODEFOUR,
    @CODECAT,
    @DATECOUT,
    @QTECOM,
    @QTEACOM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUPRO
  SET
    [SOU_ID] = @SOU_ID,
    [PRO_ID] = @PRO_ID,
    [CLEMANU] = @CLEMANU,
    [CLEDIST] = @CLEDIST,
    [CLEPERS] = @CLEPERS,
    [DESC] = @DESC,
    [QTEENS] = @QTEENS,
    [QTELOT] = @QTELOT,
    [QTEOTH] = @QTEOTH,
    [CALCTIMSTP] = @CALCTIMSTP,
    [COUBRUTUNI] = @COUBRUTUNI,
    [COUUM] = @COUUM,
    [QPP] = @QPP,
    [COUESC] = @COUESC,
    [PROMCOUNET] = @PROMCOUNET,
    [TEMPUNI] = @TEMPUNI,
    [TEMPUM] = @TEMPUM,
    [MULCOM] = @MULCOM,
    [CODEIMPR] = @CODEIMPR,
    [CODEFOUR] = @CODEFOUR,
    [CODECAT] = @CODECAT,
    [DATECOUT] = @DATECOUT,
    [QTECOM] = @QTECOM,
    [QTEACOM] = @QTEACOM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_SOUPRO_Delete] (
  @UniqueId bigint
) AS

DELETE FROM SOUPRO WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_SOUREL_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DIV_ID varchar(3),
  @TYPERELEVE varchar(1),
  @ORDRE varchar(6),
  @TYPEITEM varchar(1),
  @ITEM_ID varchar(20),
  @DESCR varchar(60),
  @QTE float,
  @SECTION float,
  @QTEUM varchar(2),
  @PROFIT float,
  @TYPETAXE varchar(1),
  @CODEIMPR varchar(2),
  @COUTANBRUT float,
  @TEMPSUNIT float,
  @TEMPSSEC float,
  @TEMPSUM varchar(2),
  @PROFITPLUS float,
  @PROFITMOIN float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUREL (
    [SOU_ID],
    [BLO_ID],
    [DIV_ID],
    [TYPERELEVE],
    [ORDRE],
    [TYPEITEM],
    [ITEM_ID],
    [DESCR],
    [QTE],
    [SECTION],
    [QTEUM],
    [PROFIT],
    [TYPETAXE],
    [CODEIMPR],
    [COUTANBRUT],
    [TEMPSUNIT],
    [TEMPSSEC],
    [TEMPSUM],
    [PROFITPLUS],
    [PROFITMOIN],
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DIV_ID,
    @TYPERELEVE,
    @ORDRE,
    @TYPEITEM,
    @ITEM_ID,
    @DESCR,
    @QTE,
    @SECTION,
    @QTEUM,
    @PROFIT,
    @TYPETAXE,
    @CODEIMPR,
    @COUTANBRUT,
    @TEMPSUNIT,
    @TEMPSSEC,
    @TEMPSUM,
    @PROFITPLUS,
    @PROFITMOIN,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUREL
  SET
    [SOU_ID] = @SOU_ID,
    [BLO_ID] = @BLO_ID,
    [DIV_ID] = @DIV_ID,
    [TYPERELEVE] = @TYPERELEVE,
    [ORDRE] = @ORDRE,
    [TYPEITEM] = @TYPEITEM,
    [ITEM_ID] = @ITEM_ID,
    [DESCR] = @DESCR,
    [QTE] = @QTE,
    [SECTION] = @SECTION,
    [QTEUM] = @QTEUM,
    [PROFIT] = @PROFIT,
    [TYPETAXE] = @TYPETAXE,
    [CODEIMPR] = @CODEIMPR,
    [COUTANBRUT] = @COUTANBRUT,
    [TEMPSUNIT] = @TEMPSUNIT,
    [TEMPSSEC] = @TEMPSSEC,
    [TEMPSUM] = @TEMPSUM,
    [PROFITPLUS] = @PROFITPLUS,
    [PROFITMOIN] = @PROFITMOIN,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_SOUREL_Delete] (
  @UniqueId bigint
) AS

DELETE FROM SOUREL WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_SOUWEBLOG_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @WEB_ID varchar(15),
  @TRF_DATE varchar(25),
  @RESULT varchar(10),
  @MESSAGE varchar(60)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUWEBLOG (
    [SOU_ID],
    [WEB_ID],
    [TRF_DATE],
    [RESULT],
    [MESSAGE],
    SysDate)
  VALUES (
    @SOU_ID,
    @WEB_ID,
    @TRF_DATE,
    @RESULT,
    @MESSAGE,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUWEBLOG
  SET
    [SOU_ID] = @SOU_ID,
    [WEB_ID] = @WEB_ID,
    [TRF_DATE] = @TRF_DATE,
    [RESULT] = @RESULT,
    [MESSAGE] = @MESSAGE,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_SOUWEBLOG_Delete] (
  @UniqueId bigint
) AS

DELETE FROM SOUWEBLOG WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_TAUX_Update] (
  @UniqueId bigint,
  @ORDRE varchar(6),
  @DESCTAUX varchar(50),
  @COUTUNI float,
  @PROFIT float,
  @INCLSOU bit,
  @INCLFAC bit,
  @SYSTEM bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO TAUX (
    [ORDRE],
    [DESCTAUX],
    [COUTUNI],
    [PROFIT],
    [INCLSOU],
    [INCLFAC],
    [SYSTEM],
    SysDate)
  VALUES (
    @ORDRE,
    @DESCTAUX,
    @COUTUNI,
    @PROFIT,
    @INCLSOU,
    @INCLFAC,
    @SYSTEM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    TAUX
  SET
    [ORDRE] = @ORDRE,
    [DESCTAUX] = @DESCTAUX,
    [COUTUNI] = @COUTUNI,
    [PROFIT] = @PROFIT,
    [INCLSOU] = @INCLSOU,
    [INCLFAC] = @INCLFAC,
    [SYSTEM] = @SYSTEM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_TAUX_Delete] (
  @UniqueId bigint
) AS

DELETE FROM TAUX WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_TAXDEF_Update] (
  @UniqueId bigint,
  @TAX_ID varchar(20),
  @PROVINCE varchar(2),
  @ABRFEDA varchar(6),
  @ABRPRVA varchar(6),
  @ABRFEDF varchar(6),
  @ABRPRVF varchar(6),
  @FEDINCL bit,
  @TVPSURCPER bit,
  @TVPSURCDEF bit,
  @CODESERV varchar(1),
  @CODEMATE varchar(1),
  @CODEAUTRE varchar(1),
  @CODEAJUST varchar(1),
  @DATEDEB datetime,
  @CODETAX1 varchar(1),
  @CODETAX2 varchar(1),
  @CODETAX3 varchar(1),
  @CODETAX4 varchar(1),
  @CODETAX5 varchar(1),
  @DESCA1 varchar(20),
  @DESCA2 varchar(20),
  @DESCA3 varchar(20),
  @DESCA4 varchar(20),
  @DESCA5 varchar(20),
  @DESCF1 varchar(20),
  @DESCF2 varchar(20),
  @DESCF3 varchar(20),
  @DESCF4 varchar(20),
  @DESCF5 varchar(20),
  @TAUXFED1 float,
  @TAUXFED2 float,
  @TAUXFED3 float,
  @TAUXFED4 float,
  @TAUXFED5 float,
  @TAUXPRV1 float,
  @TAUXPRV2 float,
  @TAUXPRV3 float,
  @TAUXPRV4 float,
  @TAUXPRV5 float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO TAXDEF (
    [TAX_ID],
    [PROVINCE],
    [ABRFEDA],
    [ABRPRVA],
    [ABRFEDF],
    [ABRPRVF],
    [FEDINCL],
    [TVPSURCPER],
    [TVPSURCDEF],
    [CODESERV],
    [CODEMATE],
    [CODEAUTRE],
    [CODEAJUST],
    [DATEDEB],
    [CODETAX1],
    [CODETAX2],
    [CODETAX3],
    [CODETAX4],
    [CODETAX5],
    [DESCA1],
    [DESCA2],
    [DESCA3],
    [DESCA4],
    [DESCA5],
    [DESCF1],
    [DESCF2],
    [DESCF3],
    [DESCF4],
    [DESCF5],
    [TAUXFED1],
    [TAUXFED2],
    [TAUXFED3],
    [TAUXFED4],
    [TAUXFED5],
    [TAUXPRV1],
    [TAUXPRV2],
    [TAUXPRV3],
    [TAUXPRV4],
    [TAUXPRV5],
    SysDate)
  VALUES (
    @TAX_ID,
    @PROVINCE,
    @ABRFEDA,
    @ABRPRVA,
    @ABRFEDF,
    @ABRPRVF,
    @FEDINCL,
    @TVPSURCPER,
    @TVPSURCDEF,
    @CODESERV,
    @CODEMATE,
    @CODEAUTRE,
    @CODEAJUST,
    @DATEDEB,
    @CODETAX1,
    @CODETAX2,
    @CODETAX3,
    @CODETAX4,
    @CODETAX5,
    @DESCA1,
    @DESCA2,
    @DESCA3,
    @DESCA4,
    @DESCA5,
    @DESCF1,
    @DESCF2,
    @DESCF3,
    @DESCF4,
    @DESCF5,
    @TAUXFED1,
    @TAUXFED2,
    @TAUXFED3,
    @TAUXFED4,
    @TAUXFED5,
    @TAUXPRV1,
    @TAUXPRV2,
    @TAUXPRV3,
    @TAUXPRV4,
    @TAUXPRV5,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    TAXDEF
  SET
    [TAX_ID] = @TAX_ID,
    [PROVINCE] = @PROVINCE,
    [ABRFEDA] = @ABRFEDA,
    [ABRPRVA] = @ABRPRVA,
    [ABRFEDF] = @ABRFEDF,
    [ABRPRVF] = @ABRPRVF,
    [FEDINCL] = @FEDINCL,
    [TVPSURCPER] = @TVPSURCPER,
    [TVPSURCDEF] = @TVPSURCDEF,
    [CODESERV] = @CODESERV,
    [CODEMATE] = @CODEMATE,
    [CODEAUTRE] = @CODEAUTRE,
    [CODEAJUST] = @CODEAJUST,
    [DATEDEB] = @DATEDEB,
    [CODETAX1] = @CODETAX1,
    [CODETAX2] = @CODETAX2,
    [CODETAX3] = @CODETAX3,
    [CODETAX4] = @CODETAX4,
    [CODETAX5] = @CODETAX5,
    [DESCA1] = @DESCA1,
    [DESCA2] = @DESCA2,
    [DESCA3] = @DESCA3,
    [DESCA4] = @DESCA4,
    [DESCA5] = @DESCA5,
    [DESCF1] = @DESCF1,
    [DESCF2] = @DESCF2,
    [DESCF3] = @DESCF3,
    [DESCF4] = @DESCF4,
    [DESCF5] = @DESCF5,
    [TAUXFED1] = @TAUXFED1,
    [TAUXFED2] = @TAUXFED2,
    [TAUXFED3] = @TAUXFED3,
    [TAUXFED4] = @TAUXFED4,
    [TAUXFED5] = @TAUXFED5,
    [TAUXPRV1] = @TAUXPRV1,
    [TAUXPRV2] = @TAUXPRV2,
    [TAUXPRV3] = @TAUXPRV3,
    [TAUXPRV4] = @TAUXPRV4,
    [TAUXPRV5] = @TAUXPRV5,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

CREATE PROCEDURE [dbo].[up_TAXDEF_Delete] (
  @UniqueId bigint
) AS

DELETE FROM TAXDEF WHERE UniqueId = @UniqueId
GO

CREATE PROCEDURE [dbo].[up_PriceUpdate_ClearProducts] AS

--Vider la table temp avant de commencer
TRUNCATE TABLE PriceUpdate_Products
GO

CREATE PROCEDURE [dbo].[up_PriceUpdate_SaveProduct](
  @PRO_ID     varchar(20), 
  @DESC       varchar(60), 
  @CODECAT    varchar(3),
  @COUUM      varchar(2), 
  @TEMPUM     varchar(2),
  @CLEMANU    varchar(20), 
  @CLEDIST    varchar(20), 
  @DESCDIST   varchar(60),
  @QPP        float, 
  @MULCOM     float,
  @COUBRUTUNI float, 
  @COUESC     float, 
  @PROMCOUNET float, 
  @NOUVEAU    varchar(1), 
  @DATECOUT   datetime
) AS

INSERT INTO PriceUpdate_Products(
  PRO_ID, 
  [DESC], 
  CODECAT,
  COUUM, 
  TEMPUM,
  CLEMANU, 
  CLEDIST, 
  DESCDIST,
  QPP, 
  MULCOM,
  COUBRUTUNI, 
  COUESC, 
  PROMCOUNET, 
  NOUVEAU, 
  DATECOUT)
VALUES (
  @PRO_ID, 
  @DESC, 
  @CODECAT,
  @COUUM, 
  @TEMPUM,
  @CLEMANU, 
  @CLEDIST, 
  @DESCDIST,
  @QPP, 
  @MULCOM,
  @COUBRUTUNI, 
  @COUESC, 
  @PROMCOUNET, 
  @NOUVEAU, 
  @DATECOUT)
GO

CREATE PROCEDURE [dbo].[up_PriceUpdate_UpdateProducts] AS

-- Insérer tous les produits inexistants
INSERT INTO PRODUITS (
  PRO_ID, 
  TEMPUM, 
  DATECREE)
SELECT
  PriceUpdate_Products.PRO_ID, 
  PriceUpdate_Products.TEMPUM,
  getdate()
FROM
  PriceUpdate_Products 
  LEFT JOIN PRODUITS 
  ON PriceUpdate_Products.PRO_ID = PRODUITS.PRO_ID
WHERE
  -- Produits qui n'existent pas déja
  PRODUITS.PRO_ID IS NULL


-- Updater tous les produits
UPDATE
  PRODUITS
SET 
  --Si la description personnelle n'a jamais été modifiée alors on peut se permettre de la mettre à jour
  PRODUITS.[DESC] = CASE WHEN PRODUITS.[DESC] IS NULL OR PRODUITS.[DESC] = '' OR PRODUITS.[DESC] = PRODUITS.DESCDIST THEN PriceUpdate_Products.[DESC] ELSE PRODUITS.[DESC] END,
  --Si la catégorie du produit est une catégorie système, alors on peut l'écraser sans souci 
  PRODUITS.CODECAT = CASE WHEN PRODUITS.CODECAT IS NULL OR PRODUITS.CODECAT = '' OR LEFT(PRODUITS.CODECAT, 1) = '+' OR LEFT(PRODUITS.CODECAT, 1) = '#' THEN PriceUpdate_Products.CODECAT ELSE PRODUITS.CODECAT END,
  --Les autres champs sont communs aux inserts et aux updates
  PRODUITS.CLEMANU    = PriceUpdate_Products.CLEMANU,
  PRODUITS.CLEDIST    = PriceUpdate_Products.CLEDIST,
  PRODUITS.DESCDIST   = PriceUpdate_Products.DESCDIST,
  PRODUITS.COUUM      = PriceUpdate_Products.COUUM,
  PRODUITS.QPP        = PriceUpdate_Products.QPP,
  PRODUITS.MULCOM     = PriceUpdate_Products.MULCOM,
  PRODUITS.CODEFOUR   = CASE WHEN LEFT(PRODUITS.PRO_ID, 1) = 'N' THEN 'NE' ELSE 'WE' END,
  PRODUITS.COUBRUTUNI = PriceUpdate_Products.COUBRUTUNI,
  PRODUITS.COUESC     = PriceUpdate_Products.COUESC,
  PRODUITS.PROMCOUNET = PriceUpdate_Products.PROMCOUNET,
  PRODUITS.DNR        = 'N',
  PRODUITS.NOUVEAU    = PriceUpdate_Products.NOUVEAU,
  PRODUITS.DATECOUT   = PriceUpdate_Products.DATECOUT
FROM
  PRODUITS 
  INNER JOIN PriceUpdate_Products
  ON PRODUITS.PRO_ID = PriceUpdate_Products.PRO_ID


--Vider la table temp maintenant qu'on a fini  
--TRUNCATE TABLE PriceUpdate_Products
GO

CREATE PROCEDURE [dbo].[up_PriceUpdate_DiscontinueProducts] (
  @Division varchar(3),
  @UpdateDate datetime
) AS

UPDATE 
  PRODUITS
SET 
  DNR = 'Y',
  NOUVEAU = 'N'
WHERE
  PRO_ID LIKE @Division + '%'
  AND DATECOUT <> @UpdateDate
GO

CREATE PROCEDURE [dbo].[up_PriceUpdate_ClearGlossary](
  @Division varchar(3)
) AS

DELETE FROM PROGLOSS WHERE CODEBANK = @Division
GO

CREATE PROCEDURE [dbo].[up_PriceUpdate_InsertGlossary](
  @TYPEGLOSS varchar(2),
  @CODEBANK varchar(3),
  @CATEGORIE varchar(30),
  @SOUSCAT varchar(30),
  @CODE varchar(20),
  @DESCRIPTIO varchar(50)
) AS

INSERT INTO PROGLOSS (
  TYPEGLOSS,
  CODEBANK,
  CATEGORIE,
  SOUSCAT,
  CODE,
  DESCRIPTIO)
VALUES (
  @TYPEGLOSS,
  @CODEBANK,
  @CATEGORIE,
  @SOUSCAT,
  @CODE,
  @DESCRIPTIO)
GO

   -- V2.#0002
   -- up_CopySouBlocDiv - Stored proc de copy de block / division dans soumission
CREATE PROCEDURE [dbo].up_CopySouBlocDiv (
  @OldSouID     varchar(20), 
  @NewSouID     varchar(20),
  @OldBloc      varchar(3),  
  @NewBloc      varchar(3),
  @OldDivision  varchar(3),  
  @NewDivision  varchar(3)
) AS

   --Trouver le prochain ORDRE dans SOUREL
DECLARE @LastSouRelOrdre varchar(6)
SELECT @LastSouRelOrdre = ISNULL(MAX(ORDRE), '000000') 
  FROM SOUREL 
  WHERE SOU_ID = @NewSouID AND TYPERELEVE = 'P' AND BLO_ID = @NewBloc AND DIV_ID = @NewDivision

DECLARE @UniqueId int
DECLARE CopySouRel CURSOR FOR
  
SELECT UniqueId 
  FROM SOUREL 
  WHERE SOU_ID = @OldSouID 
    AND TYPERELEVE = 'P' 
    AND BLO_ID = @OldBloc 
    AND DIV_ID = @OldDivision 
  ORDER BY ORDRE

OPEN CopySouRel

FETCH NEXT FROM CopySouRel INTO @UniqueId

WHILE @@FETCH_STATUS = 0
BEGIN
    --Augmenter le prochain ORDRE
  SELECT @LastSouRelOrdre = RIGHT('000000' + CAST(CAST(@LastSouRelOrdre as int) + 1000 as varchar), 6)

    --Copier ce SOUREL...
  INSERT INTO SOUREL (
    SOU_ID, 
    BLO_ID, 
    DIV_ID, 
    TYPERELEVE, 
    ORDRE,
    TYPEITEM, 
    ITEM_ID, 
    DESCR, 
    QTE, 
    SECTION, 
    QTEUM,
    PROFIT, 
    TYPETAXE, 
    CODEIMPR, 
    COUTANBRUT,
    TEMPSUNIT, 
    TEMPSSEC, 
    TEMPSUM, 
    PROFITPLUS, 
    PROFITMOIN
  )
  SELECT
    @NewSouID, 
    @NewBloc, 
    @NewDivision, 
    TYPERELEVE, 
    @LastSouRelOrdre,
    TYPEITEM, 
    ITEM_ID, 
    DESCR, 
    QTE, 
    SECTION, 
    QTEUM,
    PROFIT, 
    TYPETAXE, 
    CODEIMPR, 
    COUTANBRUT,
    TEMPSUNIT, 
    TEMPSSEC, 
    TEMPSUM, 
    PROFITPLUS, 
    PROFITMOIN
    FROM SOUREL
    WHERE UniqueId = @UniqueId

    -- This is executed as long as the previous fetch succeeds.
  FETCH NEXT FROM CopySouRel INTO @UniqueId
END

CLOSE CopySouRel
DEALLOCATE CopySouRel

  --Liste des ensembles à copier
IF OBJECT_ID('tempdb..#AssembliesToCopy') IS NOT NULL
  DROP TABLE #AssembliesToCopy

SELECT ITEM_ID AS ENS_ID
  INTO #AssembliesToCopy
  FROM SOUREL
  WHERE TYPEITEM = 'A'
    AND SOU_ID = @OldSouID
    AND BLO_ID = @OldBloc
    AND DIV_ID = @OldDivision
    AND ITEM_ID NOT IN (SELECT ENS_ID FROM SOUENS WHERE SOU_ID = @NewSouID)
  GROUP BY ITEM_ID

 --Copier les SOUENS
INSERT INTO SOUENS (
  SOU_ID, 
  ENS_ID, 
  [DESC],
  QTETOT, 
  QTETOTSECT, 
  CALCTIMSTP, 
  COUUM,
  TEMPUNI, 
  TEMPSEC, 
  TEMPUM,
  DATECREE, 
  OLDESTPROD, 
  CLEPERS, 
  PROFIT
)
SELECT DISTINCT
  @NewSouID, 
  ENS_ID, 
  [DESC],
  QTETOT, 
  QTETOTSECT, 
  CALCTIMSTP, 
  COUUM,
  TEMPUNI, 
  TEMPSEC, 
  TEMPUM,
  DATECREE, 
  OLDESTPROD, 
  CLEPERS, 
  PROFIT
  FROM SOUENS
  WHERE ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy)

  --Copier les SOUENSCO
INSERT INTO SOUENSCO (
  SOU_ID, 
  ENS_ID, 
  PRO_ID,
  ORDRE, 
  QTE, 
  QTEUM,
  TYPRATIO, 
  DIV, 
  DIVUM
)
SELECT
  @NewSouID, 
  ENS_ID, 
  PRO_ID,
  ORDRE, 
  QTE, 
  QTEUM,
  TYPRATIO, 
  DIV, 
  DIVUM
  FROM SOUENSCO
  WHERE ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy)

  --Liste des lots à copier
IF OBJECT_ID('tempdb..#LotsToCopy') IS NOT NULL
  DROP TABLE #LotsToCopy

SELECT ITEM_ID AS LOTS_ID
  INTO #LotsToCopy
  FROM SOUREL
  WHERE TYPEITEM = 'L'
    AND SOU_ID = @OldSouID
    AND BLO_ID = @OldBloc
    AND DIV_ID = @OldDivision
    AND ITEM_ID NOT IN (SELECT LOTS_ID FROM SOULOTS WHERE SOU_ID = @NewSouID)
  GROUP BY ITEM_ID

  --Copier les SOULOTS
INSERT INTO SOULOTS (
  SOU_ID, 
  LOTS_ID, 
  [DESC],
  QTETOT, 
  QTETOTSECT, 
  CALCTIMSTP, 
  COUUM,
  TEMPUNI, 
  TEMPUM, 
  DATECREE, 
  OLDESTPROD,
  CLEPERS, 
  PROFIT, 
  COUTANTSEL,
  COUTANT1, 
  COUTANT2, 
  COUTANT3, 
  COUTANT4
)
SELECT DISTINCT
  @NewSouID, 
  LOTS_ID, 
  [DESC],
  QTETOT, 
  QTETOTSECT, 
  CALCTIMSTP, 
  COUUM,
  TEMPUNI, 
  TEMPUM, 
  DATECREE, 
  OLDESTPROD,
  CLEPERS, 
  PROFIT, 
  COUTANTSEL,
  COUTANT1, 
  COUTANT2, 
  COUTANT3, 
  COUTANT4
FROM SOULOTS
WHERE LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy)

  --Copier les SOULOTSCO
INSERT INTO SOULOTSCO (
  SOU_ID, 
  LOTS_ID, 
  PRO_ID, 
  ORDRE, 
  QTE, 
  QTEUM
)
SELECT
  @NewSouID, 
  LOTS_ID, 
  PRO_ID, 
  ORDRE, 
  QTE, 
  QTEUM
FROM SOULOTSCO
WHERE LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy)

  --Liste des produits à copier
IF OBJECT_ID('tempdb..#ProductsToCopy') IS NOT NULL
  DROP TABLE #ProductsToCopy

  --Produits à copier...
SELECT ITEM_ID AS PRO_ID
  INTO #ProductsToCopy
  FROM SOUREL
  WHERE TYPEITEM NOT IN ('A', 'L', 'T')
    AND SOU_ID = @OldSouID
    AND BLO_ID = @OldBloc
    AND DIV_ID = @OldDivision
    AND ITEM_ID NOT IN (SELECT PRO_ID FROM SOUPRO WHERE SOU_ID = @NewSouID)
  GROUP BY ITEM_ID

  --Produits à copier (ensembles)
INSERT INTO #ProductsToCopy (PRO_ID)
  SELECT PRO_ID
  FROM SOUENSCO
  WHERE ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy)
    AND PRO_ID NOT IN (SELECT PRO_ID FROM SOUPRO WHERE SOU_ID = @NewSouID)

  --Produits à copier (lots)
INSERT INTO #ProductsToCopy (PRO_ID)
  SELECT PRO_ID
  FROM SOULOTSCO
  WHERE LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy)
    AND PRO_ID NOT IN (SELECT PRO_ID FROM SOUPRO WHERE SOU_ID = @NewSouID)

INSERT INTO SOUPRO (
  SOU_ID, 
  PRO_ID, 
  CLEMANU, 
  CLEDIST, 
  CLEPERS, 
  [DESC],
  QTEENS, 
  QTELOT, 
  QTEOTH, 
  CALCTIMSTP, 
  COUBRUTUNI, 
  COUUM, 
  QPP, 
  COUESC,
  PROMCOUNET, 
  TEMPUNI, 
  TEMPUM, 
  MULCOM, 
  CODEIMPR, 
  CODEFOUR, 
  CODECAT,
  DATECOUT, 
  QTECOM, 
  QTEACOM
)
SELECT
  @NewSouID, 
  PRO_ID, 
  CLEMANU, 
  CLEDIST, 
  CLEPERS, 
  [DESC],
  QTEENS, 
  QTELOT, 
  QTEOTH, 
  CALCTIMSTP, 
  COUBRUTUNI, 
  COUUM, 
  QPP, 
  COUESC,
  PROMCOUNET, 
  TEMPUNI, 
  TEMPUM, 
  MULCOM, 
  CODEIMPR, 
  CODEFOUR, 
  CODECAT,
  DATECOUT, 
  QTECOM, 
  QTEACOM
  FROM SOUPRO
  WHERE PRO_ID IN (SELECT PRO_ID FROM #ProductsToCopy)

DROP TABLE #AssembliesToCopy
DROP TABLE #LotsToCopy
DROP TABLE #ProductsToCopy
GO

   -- V2.#0003
   -- up_CopySouBlocDiv_FAC - Stored proc de copy de block / division dans facture
CREATE PROCEDURE [dbo].up_CopySouBlocDiv_FAC (
  @OldSouID     varchar(20), 
  @NewSouID     varchar(20),
  @OldBloc      varchar(3),  
  @NewBloc      varchar(3),
  @OldDivision  varchar(3),  
  @NewDivision  varchar(3)
) AS

  --Trouver le prochain ORDRE dans FACREL
DECLARE @LastSouRelOrdre varchar(6)
SELECT @LastSouRelOrdre = ISNULL(MAX(ORDRE), '000000') 
  FROM FACREL 
  WHERE SOU_ID = @NewSouID 
    AND TYPERELEVE = 'P' 
    AND BLO_ID = @NewBloc 
    AND DIV_ID = @NewDivision

DECLARE @UniqueId int
DECLARE CopySouRel CURSOR FOR
  
  SELECT UniqueId 
    FROM FACREL 
    WHERE SOU_ID = @OldSouID 
      AND TYPERELEVE = 'P' 
      AND BLO_ID = @OldBloc 
      AND DIV_ID = @OldDivision 
    ORDER BY ORDRE 

OPEN CopySouRel

FETCH NEXT FROM CopySouRel INTO @UniqueId

WHILE @@FETCH_STATUS = 0
BEGIN
    --Augmenter le prochain ORDRE
  SELECT @LastSouRelOrdre = RIGHT('000000' + CAST(CAST(@LastSouRelOrdre as int) + 1000 as varchar), 6)

  --Copier ce FACREL...
  INSERT INTO FACREL (
    SOU_ID, 
    BLO_ID, 
    DIV_ID, 
    TYPERELEVE, 
    ORDRE,
    TYPEITEM, 
    ITEM_ID, 
    DESCR, 
    QTE, 
    SECTION, 
    QTEUM,
    PROFIT, 
    TYPETAXE, 
    CODEIMPR, 
    COUTANBRUT,
    TEMPSUNIT, 
    TEMPSSEC, 
    TEMPSUM, 
    PROFITPLUS, 
    PROFITMOIN
  )
  SELECT
    @NewSouID, 
    @NewBloc, 
    @NewDivision, 
    TYPERELEVE, 
    @LastSouRelOrdre,
    TYPEITEM, 
    ITEM_ID, 
    DESCR, 
    QTE, 
    SECTION, 
    QTEUM,
    PROFIT, 
    TYPETAXE, 
    CODEIMPR, 
    COUTANBRUT,
    TEMPSUNIT, 
    TEMPSSEC, 
    TEMPSUM, 
    PROFITPLUS, 
    PROFITMOIN
    FROM FACREL
    WHERE UniqueId = @UniqueId

    -- This is executed as long as the previous fetch succeeds.
  FETCH NEXT FROM CopySouRel INTO @UniqueId
END

CLOSE CopySouRel
DEALLOCATE CopySouRel

  --Liste des ensembles à copier
IF OBJECT_ID('tempdb..#AssembliesToCopy') IS NOT NULL
  DROP TABLE #AssembliesToCopy

SELECT ITEM_ID AS ENS_ID
  INTO #AssembliesToCopy
  FROM FACREL
  WHERE TYPEITEM = 'A'
    AND SOU_ID = @OldSouID
    AND BLO_ID = @OldBloc
    AND DIV_ID = @OldDivision
    AND ITEM_ID NOT IN (SELECT ENS_ID FROM FACENS WHERE SOU_ID = @NewSouID)
  GROUP BY ITEM_ID

  --Copier les FACENS
INSERT INTO FACENS (
  SOU_ID, 
  ENS_ID, 
  [DESC],
  QTETOT, 
  QTETOTSECT, 
  CALCTIMSTP, 
  COUUM,
  TEMPUNI, 
  TEMPSEC, 
  TEMPUM,
  DATECREE, 
  OLDESTPROD, 
  CLEPERS, 
  PROFIT
)
SELECT DISTINCT
  @NewSouID, 
  ENS_ID, 
  [DESC],
  QTETOT, 
  QTETOTSECT, 
  CALCTIMSTP, 
  COUUM,
  TEMPUNI, 
  TEMPSEC, 
  TEMPUM,
  DATECREE, 
  OLDESTPROD, 
  CLEPERS, 
  PROFIT
  FROM FACENS
  WHERE ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy)

  --Copier les FACENSCO
INSERT INTO FACENSCO (
  SOU_ID, 
  ENS_ID, 
  PRO_ID,
  ORDRE, 
  QTE, 
  QTEUM,
  TYPRATIO, 
  DIV, 
  DIVUM
)
SELECT
  @NewSouID, 
  ENS_ID, 
  PRO_ID,
  ORDRE, 
  QTE, 
  QTEUM,
  TYPRATIO, 
  DIV, 
  DIVUM
  FROM FACENSCO
  WHERE ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy)

  --Liste des lots à copier
IF OBJECT_ID('tempdb..#LotsToCopy') IS NOT NULL
  DROP TABLE #LotsToCopy

SELECT ITEM_ID AS LOTS_ID
  INTO #LotsToCopy
  FROM FACREL
  WHERE TYPEITEM = 'L'
    AND SOU_ID = @OldSouID
    AND BLO_ID = @OldBloc
    AND DIV_ID = @OldDivision
    AND ITEM_ID NOT IN (SELECT LOTS_ID FROM FACLOTS WHERE SOU_ID = @NewSouID)
  GROUP BY ITEM_ID

  --Copier les FACLOTS
INSERT INTO FACLOTS (
  SOU_ID, 
  LOTS_ID, 
  [DESC],
  QTETOT, 
  QTETOTSECT, 
  CALCTIMSTP, 
  COUUM,
  TEMPUNI, 
  TEMPUM, 
  DATECREE, 
  OLDESTPROD,
  CLEPERS, 
  PROFIT, 
  COUTANTSEL,
  COUTANT1, 
  COUTANT2, 
  COUTANT3, 
  COUTANT4
)
SELECT DISTINCT
  @NewSouID, 
  LOTS_ID, 
  [DESC],
  QTETOT, 
  QTETOTSECT, 
  CALCTIMSTP, 
  COUUM,
  TEMPUNI, 
  TEMPUM, 
  DATECREE, 
  OLDESTPROD,
  CLEPERS, 
  PROFIT, 
  COUTANTSEL,
  COUTANT1, 
  COUTANT2, 
  COUTANT3, 
  COUTANT4
  FROM FACLOTS
  WHERE LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy)

  --Copier les FACLOTSCO
INSERT INTO FACLOTSCO (
  SOU_ID, 
  LOTS_ID, 
  PRO_ID, 
  ORDRE, 
  QTE, 
  QTEUM
)
SELECT
  @NewSouID, 
  LOTS_ID, 
  PRO_ID, 
  ORDRE, 
  QTE, 
  QTEUM
  FROM FACLOTSCO
  WHERE LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy)

  --Liste des produits à copier
IF OBJECT_ID('tempdb..#ProductsToCopy') IS NOT NULL
  DROP TABLE #ProductsToCopy

  --Produits à copier...
SELECT ITEM_ID AS PRO_ID
  INTO #ProductsToCopy
  FROM FACREL
  WHERE TYPEITEM NOT IN ('A', 'L', 'T')
    AND SOU_ID = @OldSouID
    AND BLO_ID = @OldBloc
    AND DIV_ID = @OldDivision
    AND ITEM_ID NOT IN (SELECT PRO_ID FROM FACPRO WHERE SOU_ID = @NewSouID)
  GROUP BY ITEM_ID

  --Produits à copier (ensembles)
INSERT INTO #ProductsToCopy (PRO_ID)
SELECT PRO_ID
  FROM FACENSCO
  WHERE ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy)
    AND PRO_ID NOT IN (SELECT PRO_ID FROM FACPRO WHERE SOU_ID = @NewSouID)

  --Produits à copier (lots)
INSERT INTO #ProductsToCopy (PRO_ID)
SELECT PRO_ID
  FROM FACLOTSCO
  WHERE LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy)
    AND PRO_ID NOT IN (SELECT PRO_ID FROM FACPRO WHERE SOU_ID = @NewSouID)

INSERT INTO FACPRO (
  SOU_ID, 
  PRO_ID, 
  CLEMANU, 
  CLEDIST, 
  CLEPERS, 
  [DESC],
  QTEENS, 
  QTELOT, 
  QTEOTH, 
  CALCTIMSTP, 
  COUBRUTUNI, 
  COUUM, 
  QPP, 
  COUESC,
  PROMCOUNET, 
  TEMPUNI, 
  TEMPUM, 
  MULCOM, 
  CODEIMPR, 
  CODEFOUR, 
  CODECAT,
  DATECOUT, 
  QTECOM, 
  QTEACOM
)
SELECT
  @NewSouID, 
  PRO_ID, 
  CLEMANU, 
  CLEDIST, 
  CLEPERS, 
  [DESC],
  QTEENS, 
  QTELOT, 
  QTEOTH, 
  CALCTIMSTP, 
  COUBRUTUNI, 
  COUUM, 
  QPP, 
  COUESC,
  PROMCOUNET, 
  TEMPUNI, 
  TEMPUM, 
  MULCOM, 
  CODEIMPR, 
  CODEFOUR, 
  CODECAT,
  DATECOUT, 
  QTECOM, 
  QTEACOM
  FROM FACPRO
  WHERE PRO_ID IN (SELECT PRO_ID FROM #ProductsToCopy)

DROP TABLE #AssembliesToCopy
DROP TABLE #LotsToCopy
DROP TABLE #ProductsToCopy
GO
