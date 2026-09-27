/******************************************************************************/
/* Delete des stored procedures propre à la version standard de EE            */
/* Ces stored procs. doivents être en tout temps identique à ceux déclarés    */
/* dans le fichier DeleteScripts_Calgary.sql SAUF pour les scripts ayant des  */
/* champs exclusifs à la version interne. Utiliser Beyond Compare au besoin   */
/* pour s'assurer de l'exactitude des tables                                  */ 
/******************************************************************************/

DROP PROCEDURE [dbo].[up_BDEE_Update]
GO

DROP PROCEDURE [dbo].[up_BDEE_Delete]
GO

DROP PROCEDURE [dbo].[up_CLIENTS_Update]
GO

DROP PROCEDURE [dbo].[up_CLIENTS_Delete]
GO

DROP PROCEDURE [dbo].[up_CLITAUX_Update]
GO

DROP PROCEDURE [dbo].[up_CLITAUX_Delete]
GO

DROP PROCEDURE [dbo].[up_COMMANDE_Update]
GO

DROP PROCEDURE [dbo].[up_COMMANDE_Delete]
GO

DROP PROCEDURE [dbo].[up_COMMITEM_Update]
GO

DROP PROCEDURE [dbo].[up_COMMITEM_Delete]
GO

DROP PROCEDURE [dbo].[up_DEFBLO_Update]
GO

DROP PROCEDURE [dbo].[up_DEFBLO_Delete]
GO

DROP PROCEDURE [dbo].[up_DEFDIV_Update]
GO

DROP PROCEDURE [dbo].[up_DEFDIV_Delete]
GO

DROP PROCEDURE [dbo].[up_ENSCOMPO_Update]
GO

DROP PROCEDURE [dbo].[up_ENSCOMPO_Delete]
GO

DROP PROCEDURE [dbo].[up_ENSEMBLE_Update]
GO

DROP PROCEDURE [dbo].[up_ENSEMBLE_Delete]
GO

DROP PROCEDURE [dbo].[up_FACAMD_Update]
GO

DROP PROCEDURE [dbo].[up_FACAMD_Delete]
GO

DROP PROCEDURE [dbo].[up_FACBLO_Update]
GO

DROP PROCEDURE [dbo].[up_FACBLO_Delete]
GO

DROP PROCEDURE [dbo].[up_FACDIV_Update]
GO

DROP PROCEDURE [dbo].[up_FACDIV_Delete]
GO

DROP PROCEDURE [dbo].[up_FACENS_Update]
GO

DROP PROCEDURE [dbo].[up_FACENS_Delete]
GO

DROP PROCEDURE [dbo].[up_FACENSCO_Update]
GO

DROP PROCEDURE [dbo].[up_FACENSCO_Delete]
GO

DROP PROCEDURE [dbo].[up_FACLOTS_Update]
GO

DROP PROCEDURE [dbo].[up_FACLOTS_Delete]
GO

DROP PROCEDURE [dbo].[up_FACLOTSCO_Update]
GO

DROP PROCEDURE [dbo].[up_FACLOTSCO_Delete]
GO

DROP PROCEDURE [dbo].[up_FACPRO_Update]
GO

DROP PROCEDURE [dbo].[up_FACPRO_Delete]
GO

DROP PROCEDURE [dbo].[up_FACREL_Update]
GO

DROP PROCEDURE [dbo].[up_FACREL_Delete]
GO

DROP PROCEDURE [dbo].[up_FACTURES_Update]
GO

DROP PROCEDURE [dbo].[up_FACTURES_Delete]
GO

DROP PROCEDURE [dbo].[up_FACWEBLOG_Update]
GO

DROP PROCEDURE [dbo].[up_FACWEBLOG_Delete]
GO

DROP PROCEDURE [dbo].[up_FRAIS_Update]
GO

DROP PROCEDURE [dbo].[up_FRAIS_Delete]
GO

DROP PROCEDURE [dbo].[up_IMPRIMER_Update]
GO

DROP PROCEDURE [dbo].[up_IMPRIMER_Delete]
GO

DROP PROCEDURE [dbo].[up_NOTES_Update]
GO

DROP PROCEDURE [dbo].[up_NOTES_Delete]
GO

DROP PROCEDURE [dbo].[up_PROCAT_Update]
GO

DROP PROCEDURE [dbo].[up_PROCAT_Delete]
GO

DROP PROCEDURE [dbo].[up_PRODUITS_Update]
GO

DROP PROCEDURE [dbo].[up_PRODUITS_Delete]
GO

DROP PROCEDURE [dbo].[up_PROFGRID_Update]
GO

DROP PROCEDURE [dbo].[up_PROFGRID_Delete]
GO

DROP PROCEDURE [dbo].[up_PROGLOSS_Update]
GO

DROP PROCEDURE [dbo].[up_PROGLOSS_Delete]
GO

DROP PROCEDURE [dbo].[up_SOUAMD_Update]
GO

DROP PROCEDURE [dbo].[up_SOUAMD_Delete]
GO

DROP PROCEDURE [dbo].[up_SOUBLO_Update]
GO

DROP PROCEDURE [dbo].[up_SOUBLO_Delete]
GO

DROP PROCEDURE [dbo].[up_SOUDIV_Update]
GO

DROP PROCEDURE [dbo].[up_SOUDIV_Delete]
GO

DROP PROCEDURE [dbo].[up_SOUENS_Update]
GO

DROP PROCEDURE [dbo].[up_SOUENS_Delete]
GO

DROP PROCEDURE [dbo].[up_SOUENSCO_Update]
GO

DROP PROCEDURE [dbo].[up_SOUENSCO_Delete]
GO

DROP PROCEDURE [dbo].[up_SOULOTS_Update]
GO

DROP PROCEDURE [dbo].[up_SOULOTS_Delete]
GO

DROP PROCEDURE [dbo].[up_SOULOTSCO_Update]
GO

DROP PROCEDURE [dbo].[up_SOULOTSCO_Delete]
GO

DROP PROCEDURE [dbo].[up_SOUMIS_Update]
GO

DROP PROCEDURE [dbo].[up_SOUMIS_Delete]
GO

DROP PROCEDURE [dbo].[up_SOUPRO_Update]
GO

DROP PROCEDURE [dbo].[up_SOUPRO_Delete]
GO

DROP PROCEDURE [dbo].[up_SOUREL_Update]
GO

DROP PROCEDURE [dbo].[up_SOUREL_Delete]
GO

DROP PROCEDURE [dbo].[up_SOUWEBLOG_Update]
GO

DROP PROCEDURE [dbo].[up_SOUWEBLOG_Delete]
GO

DROP PROCEDURE [dbo].[up_TAUX_Update]
GO

DROP PROCEDURE [dbo].[up_TAUX_Delete]
GO

DROP PROCEDURE [dbo].[up_TAXDEF_Update]
GO

DROP PROCEDURE [dbo].[up_TAXDEF_Delete]
GO

DROP PROCEDURE [dbo].[up_PriceUpdate_ClearProducts]
GO

DROP PROCEDURE [dbo].[up_PriceUpdate_SaveProduct]
GO

DROP PROCEDURE [dbo].[up_PriceUpdate_UpdateProducts]
GO

DROP PROCEDURE [dbo].[up_PriceUpdate_DiscontinueProducts]
GO

DROP PROCEDURE [dbo].[up_PriceUpdate_ClearGlossary]
GO

DROP PROCEDURE [dbo].[up_PriceUpdate_InsertGlossary]
GO

  -- V2.#0002
DROP PROCEDURE [dbo].[up_CopySouBlocDiv]
GO

  -- V2.#0003
DROP PROCEDURE [dbo].[up_CopySouBlocDiv_FAC]
GO

