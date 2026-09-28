IF OBJECT_ID(N'dbo.sp_CalculProductUsageInAssemblies', N'FN') IS NOT NULL 
  EXEC sp_rename 'sp_CalculProductUsageInAssemblies', 'sp_SOU_CalculProductUsageInAssemblies';
GO