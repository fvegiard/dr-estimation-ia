IF OBJECT_ID(N'dbo.fn_UM_GetRatioDeConversion ', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.fn_UM_GetRatioDeConversion  ;
GO

CREATE FUNCTION [dbo].fn_UM_GetRatioDeConversion  (@UMDE_ID VARCHAR(2), @UMA_ID VARCHAR(2), @QPP INT)
RETURNS FLOAT 
AS BEGIN

    IF (( @UMDE_ID = 'PG') OR (@UMDE_ID = 'BO')) AND (@UMA_ID = 'U') RETURN 0;

    DECLARE @UNITTOUNIT    BIT
    DECLARE @UNITTOPACKAGE BIT
    DECLARE @PACKAGETOUNIT BIT    
    DECLARE @RATIO         FLOAT
    DECLARE @R             FLOAT    
    
    SELECT @UNITTOUNIT    = P.UNITTOUNIT, 
           @UNITTOPACKAGE = P.UNITTOPACKAGE, 
           @PACKAGETOUNIT = P.PACKAGETOUNIT,
           @RATIO         = P.RATIO
    FROM   SYS_UNITSCONVERSION P
    WHERE  P.UNITFROM = @UMDE_ID
    AND    P.UNITTO   = @UMA_ID;

    SET @R = CASE WHEN @PACKAGETOUNIT = 1 THEN
                     CASE WHEN @QPP = 0 THEN 0 
                          ELSE  (CAST(1 AS float) / CAST(@QPP AS float)) 
                     END 

                  WHEN @UNITTOUNIT    = 1 THEN @RATIO
                  ELSE 0
             END;
    RETURN @R

END
GO


IF OBJECT_ID(N'dbo.fn_DateTime_GetTimeStampStr', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.fn_DateTime_GetTimeStampStr ;
GO


CREATE FUNCTION [dbo].fn_DateTime_GetTimeStampStr()
RETURNS VARCHAR(14)
AS BEGIN
  DECLARE @R VARCHAR(14)

  SELECT @R = CAST(DATEPART(YEAR,  GETDATE()) AS varchar)   + 
              CAST(DATEPART(MONTH, GETDATE()) AS varchar)   + 
              CAST(DATEPART(DAY,   GETDATE()) AS varchar)   + 
              CAST(DATEPART(HH,    GETDATE()) AS varchar)   + 
              CAST(DATEPART(MM,    GETDATE()) AS varchar)   + 
              CAST(DATEPART(SS,    GETDATE()) AS varchar)   + 
              CAST(DATEPART(MS,    GETDATE()) AS varchar)   
  RETURN @R

END
GO


IF OBJECT_ID(N'dbo.fn_UM_GetNatureUnite', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.fn_UM_GetNatureUnite ;
GO


CREATE FUNCTION [dbo].fn_UM_GetNatureUnite(@CodeEN VARCHAR(1))
RETURNS VARCHAR(1)
AS BEGIN
  DECLARE @R VARCHAR(1)

  SELECT @R = P.[Type] 
  FROM Sys_Units P 
  WHERE P.CodeEN = @CodeEN

  RETURN @R

END
GO


IF OBJECT_ID(N'dbo.fn_UM_GetUniteDeBase', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.fn_UM_GetUniteDeBase ;
GO


CREATE FUNCTION [dbo].fn_UM_GetUniteDeBase(@CodeEN VARCHAR(2))
RETURNS VARCHAR(2)
AS BEGIN
  DECLARE @R VARCHAR(2)

  SELECT @R = P.BaseUnitCodeEN
  FROM Sys_Units P 
  WHERE P.CodeEN = @CodeEN

  RETURN @R

END
GO


IF OBJECT_ID(N'dbo.sp_UpdateQteTotalOth', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_UpdateQteTotalOth ;
GO

CREATE PROCEDURE [dbo].sp_UpdateQteTotalOth (@SOU_ID VARCHAR(20), @ITEM_ID VARCHAR(20), @CALCTIMSTP VARCHAR(14), @UID VARCHAR(14), @QTE_TOTAL FLOAT)
AS BEGIN
   IF @CALCTIMSTP = @UID 
   BEGIN
     UPDATE SOUPRO
     SET   QTEOTH   = QTEOTH + @QTE_TOTAL
     WHERE   SOU_ID = @SOU_ID
     AND     PRO_ID = @ITEM_ID 
   END ELSE
   BEGIN
     UPDATE SOUPRO
     SET QTEOTH     = @QTE_TOTAL,
         CALCTIMSTP = @UID
     WHERE   SOU_ID = @SOU_ID
     AND     PRO_ID = @ITEM_ID     
   END
END
GO

IF OBJECT_ID(N'dbo.sp_UpdateQteTotalEns', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_UpdateQteTotalEns ;
GO

CREATE PROCEDURE [dbo].sp_UpdateQteTotalEns (@SOU_ID VARCHAR(20), @ITEM_ID VARCHAR(20), @CALCTIMSTP VARCHAR(14), @UID VARCHAR(14), @QTE_TOTAL FLOAT)
AS BEGIN
   IF @CALCTIMSTP = @UID 
   BEGIN
     UPDATE SOUPRO
     SET   QTEENS   = QTEENS + @QTE_TOTAL
     WHERE   SOU_ID = @SOU_ID
     AND     PRO_ID = @ITEM_ID 
   END ELSE
   BEGIN
     UPDATE SOUPRO
     SET QTEENS     = @QTE_TOTAL,
         CALCTIMSTP = @UID
     WHERE   SOU_ID = @SOU_ID
     AND     PRO_ID = @ITEM_ID     
   END
END
GO

IF OBJECT_ID(N'dbo.sp_UpdateQteTotalLots', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_UpdateQteTotalLots ;
GO

CREATE PROCEDURE [dbo].sp_UpdateQteTotalLots (@SOU_ID VARCHAR(20), @ITEM_ID VARCHAR(20), @CALCTIMSTP VARCHAR(14), @UID VARCHAR(14), @QTE_TOTAL FLOAT)
AS BEGIN
   IF @CALCTIMSTP = @UID 
   BEGIN
     UPDATE SOUPRO
     SET   QTELOT   = QTELOT + @QTE_TOTAL
     WHERE   SOU_ID = @SOU_ID
     AND     PRO_ID = @ITEM_ID 
   END ELSE
   BEGIN
     UPDATE SOUPRO
     SET QTELOT     = @QTE_TOTAL,
         CALCTIMSTP = @UID
     WHERE   SOU_ID = @SOU_ID
     AND     PRO_ID = @ITEM_ID     
   END
END
GO


IF OBJECT_ID(N'dbo.sp_CalculQteTotalItem', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_CalculQteTotalItem ;
GO

CREATE PROCEDURE [dbo].sp_CalculQteTotalItem (@SOU_ID VARCHAR(20), @ITEM_ID VARCHAR(20), @TYPEITEM VARCHAR(1), @BLO_ID_REL VARCHAR(3), @QTE FLOAT, @QTEUM VARCHAR(2) , @UID VARCHAR(14))
AS BEGIN
  DECLARE @COUUM_SOUPRO   VARCHAR(2)
  DECLARE @QPP_SOUPRO     INT
  DECLARE @MULT_BLOC      INT
  DECLARE @QTE_TOTAL      FLOAT
  DECLARE @CALCTIMSTP     VARCHAR(14)
       
  SET @QTE_TOTAL = 0;


  SELECT @COUUM_SOUPRO = P.COUUM,  @QPP_SOUPRO = P.QPP , @CALCTIMSTP = P.CALCTIMSTP
    FROM SOUPRO P
   WHERE P.SOU_ID = @SOU_ID
     AND P.PRO_ID = @ITEM_ID

  SET @QTE_TOTAL = @QTE * DBO.fn_UM_GetRatioDeConversion  (@QTEUM, DBO.fn_UM_GetUniteDeBase(@COUUM_SOUPRO),  @QPP_SOUPRO)
     
  SELECT @MULT_BLOC = B.MULT
    FROM SOUBLO B
   WHERE B.BLO_ID = @BLO_ID_REL
     AND B.SOU_ID = @SOU_ID

  IF @MULT_BLOC IS NOT NULL 
  BEGIN
    SET @QTE_TOTAL = @QTE_TOTAL * @MULT_BLOC
  END


  IF @CALCTIMSTP <> @UID 
  BEGIN
    UPDATE SOUPRO
      SET   QTEOTH = 0, 
            QTEENS = 0,
            QTELOT = 0
    WHERE   SOU_ID = @SOU_ID
    AND     PRO_ID = @ITEM_ID 
  END

  IF ((@TYPEITEM = 'P') OR (@TYPEITEM = 'N'))
    EXEC dbo.sp_UpdateQteTotalOth @SOU_ID, @ITEM_ID, @CALCTIMSTP, @UID , @QTE_TOTAL  
  ELSE IF @TYPEITEM = 'A'
    EXEC dbo.sp_UpdateQteTotalEns @SOU_ID, @ITEM_ID, @CALCTIMSTP, @UID , @QTE_TOTAL  
  ELSE IF @TYPEITEM = 'L'
    EXEC dbo.sp_UpdateQteTotalLots @SOU_ID, @ITEM_ID, @CALCTIMSTP, @UID , @QTE_TOTAL  

END 
GO

  -- New field - SOUPRO.INASSEMBLIE
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUPRO'
    AND [COLUMN_NAME] = 'INASSEMBLIE' )
BEGIN
  ALTER TABLE
    SOUPRO
  ADD
    INASSEMBLIE  VARCHAR(2000);--NVARCHAR(MAX)
END
GO

IF OBJECT_ID(N'dbo.sp_GetAssemblyCompositionConcat', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.sp_GetAssemblyCompositionConcat ;
GO

 CREATE FUNCTION [dbo].sp_GetAssemblyCompositionConcat  
( @SOU_ID VARCHAR(20),
  @PRO_ID VARCHAR(20))
RETURNS VARCHAR(2000)
AS 
BEGIN
  DECLARE @s VARCHAR(2000);  
  SELECT @s = COALESCE(@s , N'') + 
              E.[DESC] + CHAR(13) +  CHAR(10) +  '> ' + LTRIM(STR(C.QTE, 10, 2)) + ' ' + C.QTEUM + ' / 1.00 '+ E.COUUM + 
              CHAR(13) + CHAR(10) 
    FROM SOUENS E, SOUENSCO C , SOUREL L
   WHERE E.ENS_ID = C.ENS_ID
     AND E.SOU_ID = C.SOU_ID
     AND L.SOU_ID = E.SOU_ID
     AND L.ITEM_ID = E.ENS_ID
     AND C.SOU_ID = @SOU_ID
     AND C.PRO_ID = @PRO_ID;

  RETURN (@s);
END
GO

IF OBJECT_ID(N'dbo.sp_CalculProductUsageInAssemblies', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_CalculProductUsageInAssemblies ;
GO

CREATE PROCEDURE [dbo].sp_CalculProductUsageInAssemblies (@SOU_ID VARCHAR(20), @LANG INT)
AS BEGIN
  DECLARE  @TITLE  VARCHAR(60);
  DECLARE  @DESCR  VARCHAR(2000);  
  DECLARE  @SOUID  VARCHAR(20);
  DECLARE  @PRO_ID VARCHAR(20);



  IF @LANG = 1 
    SET @TITLE = 'Dans les ensembles'
  ELSE
    SET @TITLE = 'In assemblies '

  SET @TITLE =    @TITLE + CHAR(13) + CHAR(10) + REPLICATE('-', LEN(@TITLE))

  DECLARE CUR_1 CURSOR FOR 
   
   SELECT E.SOU_ID, C.PRO_ID , DESCR = @TITLE +  CHAR(13) + CHAR(10) + dbo.sp_GetAssemblyCompositionConcat(E.SOU_ID, C.PRO_ID)    
   FROM SOUENS E, SOUENSCO C , SOUREL L
      WHERE E.ENS_ID = C.ENS_ID
        AND E.SOU_ID = C.SOU_ID
        AND L.SOU_ID = E.SOU_ID
        AND L.ITEM_ID = E.ENS_ID
        AND C.SOU_ID = @SOU_ID    
  GROUP BY  E.SOU_ID, C.PRO_ID

  OPEN CUR_1
  FETCH NEXT FROM CUR_1
  INTO @SOUID, @PRO_ID, @DESCR

  WHILE @@FETCH_STATUS = 0
   BEGIN
     UPDATE SOUPRO
        SET INASSEMBLIE = @DESCR
      WHERE PRO_ID = @PRO_ID 
        AND SOU_ID = @SOUID 

     FETCH NEXT FROM CUR_1
     INTO @SOUID, @PRO_ID, @DESCR
   END
  CLOSE CUR_1;
  DEALLOCATE CUR_1;

END
GO

--- Fonctions pour les filtres

IF OBJECT_ID(N'dbo.[fn_Str_RemoveAllRepeatingChars]', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.[fn_Str_RemoveAllRepeatingChars] ;
GO

create function [dbo].[fn_Str_RemoveAllRepeatingChars](
@input_string varchar(2000))

returns varchar(2000)
as 
begin
 
declare @output_string varchar(2000)
declare @index int
declare @current_char char(1)
declare @previous_chars varchar(2000)
 
set @output_string = ''
set @current_char  = 0
set @previous_chars  = ''
set @output_string = ''
set @index = 1
 
--traverse input string
while @index <= len(@input_string) 
begin
          
    --get current character in string
    set @current_char = substring(@input_string, @index, 1)
 
    if charindex(@current_char, @previous_chars) = 0
    begin   
        set @output_string = @output_string + substring(@input_string, @index, 1)                          
    end
    
    -- store all the characters for comparison
    set @previous_chars = @previous_chars + substring(@input_string, @index, 1)
    
    set @index = @index + 1
    
end

return @output_string

end
GO

IF OBJECT_ID(N'dbo.fn_STR_Alphaorder', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.fn_STR_Alphaorder ;
GO


CREATE FUNCTION [dbo].fn_STR_Alphaorder (@str VARCHAR(50))
returns VARCHAR(50)
  BEGIN
      DECLARE @len    INT,
              @cnt    INT,
              @str1   VARCHAR(50),
              @output VARCHAR(50)
      set @cnt    = 1
      set @str1   =''
      set @output =''

      SELECT @len = Len(@str)
      WHILE @cnt <= @len
        BEGIN
            SELECT @str1 = @str1 + Substring(@str, @cnt, 1) + ','

            SET @cnt = @cnt + 1
        END

      SELECT @str1 = LEFT(@str1, Len(@str1) - 1)

      SELECT @output = @output + Sp_data
      FROM  (SELECT Split.a.value('.', 'VARCHAR(100)') Sp_data
             FROM   (SELECT Cast ('<M>' + Replace(@str1, ',', '</M><M>') + '</M>' AS XML) AS Data) AS A
                    CROSS APPLY Data.nodes ('/M') AS Split(a)) A
      ORDER  BY Sp_data

      RETURN @output
  END
GO


IF OBJECT_ID(N'dbo.fn_STR_AddAndSortChars', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.fn_STR_AddAndSortChars ;
GO


CREATE FUNCTION [dbo].fn_STR_AddAndSortChars (@aStr VARCHAR(200), @aNewStr VARCHAR(200))
RETURNS VARCHAR(40) 
AS BEGIN
    DECLARE @R VARCHAR(400) 

    SELECT  @R = dbo.fn_STR_Alphaorder ([dbo].[fn_Str_RemoveAllRepeatingChars](@aStr + @aNewStr)) ;
    RETURN  @R

END
GO

IF OBJECT_ID(N'dbo.sp_CalculCodeImpr', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_CalculCodeImpr ;
GO

CREATE PROCEDURE [dbo].sp_CalculCodeImpr(@SOU_ID VARCHAR(20), @PRO_ID  VARCHAR(20), @value  VARCHAR(36))
AS BEGIN
   if ( @value is not null ) AND (@value <> '')
   BEGIN
    UPDATE SOUPRO
      SET CODEIMPR = dbo.fn_STR_AddAndSortChars(CODEIMPR, @value) 
    WHERE   SOU_ID = @SOU_ID
    AND     PRO_ID = @PRO_ID 
   END
END
GO

-- procedure de calcule des quantités


IF OBJECT_ID(N'dbo.up_SOUPRO_Quantity', N'P') IS NOT NULL
    DROP PROCEDURE dbo.up_SOUPRO_Quantity ;
GO


CREATE PROCEDURE [dbo].up_SOUPRO_Quantity (@SOU_ID VARCHAR(20), @REPLACE_FILTER INT)
AS BEGIN

   DECLARE @UID            VARCHAR(14)
   DECLARE @QTE            FLOAT    
   DECLARE @QTEUM          VARCHAR(2)
    --
   DECLARE @TYPERELEVE_REL CHAR
   DECLARE @TYPEITEM_REL   CHAR
   DECLARE @QTE_REL        FLOAT 
   DECLARE @QTEUM_REL      VARCHAR(2)
   DECLARE @ITEM_ID_REL    VARCHAR(20)
   DECLARE @BLO_ID_REL     VARCHAR(3)
   DECLARE @SECTION_REL    FLOAT 
   DECLARE @CODEIMPR_REL   VARCHAR(36)
    --
   DECLARE @QPP_SOUPRO     INT
    --
   DECLARE @COUUM_ENS      VARCHAR(2)
   DECLARE @QTEUM_ENSCO    VARCHAR(2)
   DECLARE @TYPRATIO_ENSCO VARCHAR(1)
   DECLARE @QTE_ENSCO      FLOAT 
   DECLARE @ENS_ID_ENS     VARCHAR(20)
   DECLARE @PRO_ID_ENSCO   VARCHAR(20)
    --
   DECLARE @COUUM_LOT      VARCHAR(2)
   DECLARE @QTE_LOTCO      FLOAT
   DECLARE @QTEUM_LOTCO    VARCHAR(2)
   DECLARE @PRO_ID_LOTCO   VARCHAR(20)
    --
   DECLARE CUR_SOUREL CURSOR FOR 
      SELECT S.ITEM_ID , S.TYPERELEVE, S.TYPEITEM, S.QTE, S.QTEUM, S.BLO_ID, S.SECTION, S.CODEIMPR
   FROM SOUREL S
   WHERE S.SOU_ID = @SOU_ID
  
   SELECT @UID = DBO.fn_DateTime_GetTimeStampStr()

   ----------------------------------
   ---- Pour les codes d'impression : 0 Pour Ne pas traiter , 1 Pour Ajouter, 2 pour remplacer
   ----------------------------------

   IF @REPLACE_FILTER = 2 
   BEGIN
     UPDATE   SOUPRO
        SET CODEIMPR = ''
        WHERE   SOU_ID = @SOU_ID
   END
 
   -----------------------------------

   OPEN CUR_SOUREL
   FETCH NEXT FROM CUR_SOUREL
   INTO @ITEM_ID_REL, @TYPERELEVE_REL, @TYPEITEM_REL, @QTE_REL, @QTEUM_REL, @BLO_ID_REL, @SECTION_REL, @CODEIMPR_REL


   UPDATE SOUMIS 
      SET CALCTIMSTP = @UID
    WHERE SOU_ID = @SOU_ID 


   UPDATE SOUPRO 
      SET QTEOTH = 0,  
          QTEENS = 0, 
          QTELOT = 0  
    WHERE SOU_ID = @SOU_ID 


   WHILE @@FETCH_STATUS = 0
   BEGIN
     IF ((@TYPERELEVE_REL = 'P') AND (@TYPEITEM_REL <> 'T'))
     BEGIN
       --------------------------------------
       ---- Produits-------------------------
       --------------------------------------
       IF ((@TYPEITEM_REL = 'P') OR (@TYPEITEM_REL = 'N'))
       BEGIN

         SET @QTE   = @QTE_REL
         SET @QTEUM = @QTEUM_REL

         EXEC dbo.sp_CalculQteTotalItem @SOU_ID, 
                                     @ITEM_ID_REL, 
                                     @TYPEITEM_REL,
                                     @BLO_ID_REL, 
                                     @QTE, 
                                     @QTEUM, 
                                     @UID

         IF @REPLACE_FILTER > 0
         BEGIN
          EXEC dbo.sp_CalculCodeImpr @SOU_ID, @ITEM_ID_REL, @CODEIMPR_REL
         END

       END ELSE
       --------------------------------------
       ---- Ensembles------------------------
       --------------------------------------
       IF (@TYPEITEM_REL = 'A')
       BEGIN

         DECLARE CUR_PRODUITSENS CURSOR FOR
            SELECT E.COUUM, C.QTEUM, C.TYPRATIO,
                    CASE 
                      WHEN (C.TYPRATIO = 'L') AND (E.COUUM <> '') AND (DBO.fn_UM_GetNatureUnite(E.COUUM) = 'L') THEN 
                        CASE 
                          WHEN (C.DIV <> '')  THEN (C.QTE / C.DIV) * DBO.fn_UM_GetRatioDeConversion  (E.COUUM, C.DIVUM,  0)   
                          ELSE 0
                        END
                      ELSE C.QTE          
                    END AS QTE_ENSCO , E.ENS_ID, C.PRO_ID

            FROM SOUENS E, SOUENSCO C
            WHERE E.SOU_ID = C.SOU_ID
            AND   E.ENS_ID = C.ENS_ID
            AND   E.SOU_ID = @SOU_ID
            AND   E.ENS_ID = @ITEM_ID_REL               
        ----------------------------------


         OPEN CUR_PRODUITSENS

         FETCH NEXT FROM CUR_PRODUITSENS
         INTO @COUUM_ENS, @QTEUM_ENSCO, @TYPRATIO_ENSCO, @QTE_ENSCO, @ENS_ID_ENS, @PRO_ID_ENSCO

         WHILE @@FETCH_STATUS = 0
         BEGIN
           SET @QTE = 0;

           IF @TYPRATIO_ENSCO = 'L'
             SET @QTE = (@QTE_ENSCO * @QTE_REL * DBO.fn_UM_GetRatioDeConversion  (@QTEUM_REL, @COUUM_ENS,  0))
           ELSE
             SET @QTE = (@QTE_ENSCO * @SECTION_REL)

           SET @QTEUM = @QTEUM_ENSCO

           EXEC dbo.sp_CalculQteTotalItem @SOU_ID, 
                                       @PRO_ID_ENSCO, 
                                       @TYPEITEM_REL,
                                       @BLO_ID_REL, 
                                       @QTE, 
                                       @QTEUM, 
                                       @UID

           IF @REPLACE_FILTER > 0
           BEGIN
             EXEC dbo.sp_CalculCodeImpr @SOU_ID, @PRO_ID_ENSCO, @CODEIMPR_REL
           END

           FETCH NEXT FROM CUR_PRODUITSENS
           INTO @COUUM_ENS, @QTEUM_ENSCO, @TYPRATIO_ENSCO, @QTE_ENSCO, @ENS_ID_ENS, @PRO_ID_ENSCO
         END

         CLOSE CUR_PRODUITSENS;
         DEALLOCATE CUR_PRODUITSENS;
       END ELSE
       --------------------------------------
       ---- Lots-----------------------------
       --------------------------------------
       IF (@TYPEITEM_REL = 'L')
       BEGIN

       ----------------------------------

         DECLARE CUR_PRODUITSLOTS CURSOR FOR
            SELECT L.COUUM, C.QTE, C.QTEUM, C.PRO_ID
            FROM SOULOTS L, SOULOTSCO C
            WHERE L.LOTS_ID = C.LOTS_ID
            AND   L.SOU_ID = @SOU_ID

         OPEN CUR_PRODUITSLOTS

         FETCH NEXT FROM CUR_PRODUITSLOTS
         INTO @COUUM_LOT, @QTE_LOTCO, @QTEUM_LOTCO, @PRO_ID_LOTCO

         WHILE @@FETCH_STATUS = 0
         BEGIN

           SELECT @QPP_SOUPRO = P.QPP
            FROM SOUPRO P
           WHERE P.SOU_ID = @SOU_ID
             AND P.PRO_ID = @ITEM_ID_REL

           SET @QTE = (@QTE_LOTCO * @QTE_REL * DBO.fn_UM_GetRatioDeConversion  (@QTEUM_REL, @COUUM_LOT,  @QPP_SOUPRO))

           SET @QTEUM = @QTEUM_LOTCO

           EXEC dbo.sp_CalculQteTotalItem @SOU_ID, 
                                       @PRO_ID_LOTCO, 
                                       @TYPEITEM_REL,
                                       @BLO_ID_REL, 
                                       @QTE, 
                                       @QTEUM, 
                                       @UID

           IF @REPLACE_FILTER > 0
           BEGIN
             EXEC dbo.sp_CalculCodeImpr @SOU_ID, @PRO_ID_LOTCO, @CODEIMPR_REL
           END

           FETCH NEXT FROM CUR_PRODUITSLOTS
           INTO @COUUM_LOT, @QTE_LOTCO, @QTEUM_LOTCO, @PRO_ID_LOTCO 

         END

         CLOSE CUR_PRODUITSLOTS;
         DEALLOCATE CUR_PRODUITSLOTS;
       END
       --------------------------------------
     END
     FETCH NEXT FROM CUR_SOUREL
     INTO @ITEM_ID_REL, @TYPERELEVE_REL, @TYPEITEM_REL, @QTE_REL, @QTEUM_REL, @BLO_ID_REL, @SECTION_REL, @CODEIMPR_REL

   END
   CLOSE CUR_SOUREL;
   DEALLOCATE CUR_SOUREL;

END
GO

