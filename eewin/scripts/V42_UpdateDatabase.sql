  -- Correctif - Nettoyage des produits non utilisé dans les soumissions et factures

IF OBJECT_ID(N'dbo.sp_SOUPRO_Del_UnusedProd', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_SOUPRO_Del_UnusedProd;
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
  WHERE
      SOU_ID = @SOUID AND 
      PRO_ID IN( 
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

IF OBJECT_ID(N'dbo.sp_FACPRO_Del_UnusedProd', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_FACPRO_Del_UnusedProd;
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
  WHERE
       SOU_ID = @SOUID AND
       PRO_ID IN( 
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