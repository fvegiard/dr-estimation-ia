  
IF OBJECT_ID(N'dbo.fn_UM_GetNatureUnite', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.fn_UM_GetNatureUnite ;
GO

CREATE FUNCTION [dbo].fn_UM_GetNatureUnite(@CodeUM VARCHAR(2))
RETURNS VARCHAR(1)
AS BEGIN
--- Patch : ATTENTION dans le futur il faudrait introduir un parametre @Lang ainsi :
--- si @Lang = 0 alors WHERE P.CodeEN = @CodeUM
--- si @Lang = 1 alors WHERE P.CodeFR = @CodeUM

  DECLARE @R VARCHAR(1)
  SET @R = '';


  SELECT @R = P.[Type] 
  FROM Sys_Units P 
  WHERE P.CodeEN = @CodeUM;
  
  IF (@R = '')
  BEGIN
	  SELECT @R = P.[Type] 
	  FROM Sys_Units P 
	  WHERE P.CodeFR = @CodeUM;
  END;
 
  RETURN @R

END
GO

