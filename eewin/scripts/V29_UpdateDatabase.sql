IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'FUNCTION' AND Specific_Name = 'FnGetColsFromString')
  DROP FUNCTION FnGetColsFromString
GO

CREATE FUNCTION [dbo].FnGetColsFromString(@String VARCHAR(MAX), @Delimiter CHAR(1))
RETURNS  @Tmp TABLE 
(
    -- colones de la table retourn?e
    ID INT ,
    Name nvarchar(255)	
)
AS
BEGIN

DECLARE @cnt INT
DECLARE @idx INT    
SET     @idx = 1     
SET     @cnt = 0;

 -- si la liste est vide on retourne la table vide
IF LEN(RTRIM(@String)) = 0 return

 -- ajouter une virgule a la fin s'il n y en a pas
IF RIGHT(RTRIM(@String), 1) != ',' SET  @String = RTRIM(@String) + ','
 
 -- Debut du traitement 
WHILE (@idx != 0)
BEGIN    
    SET @idx = CHARINDEX(@Delimiter,@String)     
    IF @idx!=0 
    BEGIN
	  SET @cnt = @cnt + 1;
      insert into @Tmp(ID, name) values(@cnt, LTRIM(RTRIM(LEFT(@String,@idx - 1))))	  
    END
    SET @String = RIGHT(@String,LEN(@String) - @idx)     
    IF LEN(@String) = 0 BREAK
END

return
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_GetAllFieldsBut_v2')
  DROP PROCEDURE up_GetAllFieldsBut_v2
GO

CREATE PROCEDURE [dbo].[up_GetAllFieldsBut_v2] (
	@TableName		varchar(64),			-- Nom de la table pour les champs
	@FieldsName		varchar(3000),			-- Liste des champs à ne pas inclure séparé par virgule
        @SelectString	        varchar(8000) output            -- Chaine qui contient la liste des champs sauf @FieldName
)
AS
BEGIN
	SET NOCOUNT ON;

	SELECT @SelectString = ''
	SELECT @SelectString = @SelectString + '[' + Name + '], ' FROM SysColumns s WHERE s.id = Object_Id(@TableName) 
	   AND s.Name not IN (select Name from FnGetColsFromString (@FieldsName, ','))
	SELECT @SelectString = SubString(@SelectString, 1, Len(@SelectString) - Len(', '))
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'sp_FAC_SOU_Copy')
  DROP PROCEDURE sp_FAC_SOU_Copy
GO

CREATE PROCEDURE [dbo].[sp_FAC_SOU_Copy] (@SrcTableName VARCHAR(20), @DestTableName VARCHAR(20), @SOUID VARCHAR(20), @FactID VARCHAR(20))
AS 
BEGIN
  DECLARE @SelectString  varchar(8000);

  exec up_GetAllFieldsBut_v2 @SrcTableName, 'SOU_ID, UniqueId, SysDate,', @SelectString output 

  SELECT @SelectString = 'INSERT INTO ' + @DestTableName + ' ('  + '[SOU_ID], [SYSDATE], ' 
                                        + @SelectString  +  ') ' + 
                             ' SELECT ' +  '''' + @FactID + '''' + ' as [SOU_ID], '                                
                                        +  'getdate()'           + ' as [SYSDATE], ' 
                                        + @SelectString          +
                               ' FROM ' + @SrcTableName          +
                              ' WHERE SOU_ID = ' + '''' + @SOUID + '''';

  exec (@SelectString)
 
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'sp_SOUPRO_Del_UnusedProd')
  DROP PROCEDURE sp_SOUPRO_Del_UnusedProd
GO

CREATE PROCEDURE [dbo].[sp_SOUPRO_Del_UnusedProd] (
  @SOUID    varchar(20)
) AS
    -- total produit avant suppression
  DECLARE @OldTotal INT

  SELECT @OldTotal = Count(*)
	FROM  SOUPRO
	WHERE SOU_ID = @SOUID

  DELETE FROM  SOUPRO 
  WHERE PRO_ID IN( 
       SELECT p.PRO_ID FROM SOUPRO P 
        WHERE  p.SOU_ID = @SOUID  
          and  P.PRO_ID not in (
              select b.PRO_ID 
                from SOUENS a , SOUENSCO  b
               where a.SOU_ID = b.SOU_ID
                 and a.ENS_ID = b.ENS_ID 
                 and a.SOU_ID = @SOUID  

              UNION

              select  b.PRO_ID AS AA
                from SOULOTS a , SOULOTSCO  b
               where a.LOTS_ID = b.LOTS_ID
                 and a.SOU_ID  = b.SOU_ID
                 and a.SOU_ID  =  @SOUID 

              UNION
              
              select  r.ITEM_ID
                from SOUREL r
               where r.SOU_ID = @SOUID 
              and (r.TYPERELEVE = 'P' or r.TYPERELEVE = 'U')
             )
	       )

    -- total produit apres suppression   
  DECLARE @NewTotal INT

  SELECT	@NewTotal = Count(*)
	FROM  SOUPRO
	WHERE SOU_ID = @SOUID    

	-- Retourne le nombre de produits supprimé de Dans SOUPRO
   RETURN  @OldTotal - @NewTotal; 
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'sp_FACPRO_Del_UnusedProd')
  DROP PROCEDURE sp_FACPRO_Del_UnusedProd
GO

CREATE PROCEDURE [dbo].[sp_FACPRO_Del_UnusedProd] (
  @SOUID	    varchar(20)
) AS
    -- total produit avant suppression
  DECLARE @OldTotal INT

  SELECT @OldTotal = Count(*)
	FROM  FACPRO
	WHERE SOU_ID = @SOUID

  DELETE FROM  FACPRO 
  WHERE PRO_ID IN( 
       SELECT p.PRO_ID FROM FACPRO P 
        WHERE  p.SOU_ID = @SOUID  
          and  P.PRO_ID not in (
              select b.PRO_ID 
                from FACENS a , FACENSCO  b
               where a.SOU_ID = b.SOU_ID
                 and a.ENS_ID = b.ENS_ID 
                 and a.SOU_ID = @SOUID  

              UNION

              select  b.PRO_ID AS AA
                from FACLOTS a , FACLOTSCO  b
               where a.LOTS_ID = b.LOTS_ID
                 and a.SOU_ID  = b.SOU_ID
                 and a.SOU_ID  =  @SOUID 

              UNION
            
              select  r.ITEM_ID
                from FACREL r
               where r.SOU_ID = @SOUID 
                 and (r.TYPERELEVE = 'P' or r.TYPERELEVE = 'U')
            )
	       )

    -- total produit apres suppression   
  DECLARE @NewTotal INT

  SELECT	@NewTotal = Count(*)
	FROM  FACPRO
	WHERE SOU_ID = @SOUID    

	-- Retourne le nombre de produits supprimé de Dans FACPRO
   RETURN  @OldTotal - @NewTotal; 
GO
