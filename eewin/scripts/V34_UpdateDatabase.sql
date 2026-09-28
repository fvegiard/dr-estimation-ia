IF OBJECT_ID(N'dbo.sp_SOU_GetAssemblyCompositionConcat', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.sp_SOU_GetAssemblyCompositionConcat ;
GO

 CREATE FUNCTION [dbo].sp_SOU_GetAssemblyCompositionConcat  
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

-- Drop de l'original au besoin. N'est plus référencé dans le code
IF OBJECT_ID(N'dbo.sp_GetAssemblyCompositionConcat', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.sp_GetAssemblyCompositionConcat ;
GO
