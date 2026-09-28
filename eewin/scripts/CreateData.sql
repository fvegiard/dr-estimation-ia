INSERT INTO [dbo].[Sys_Units] (
  UnitId, CodeEN, CodeFR, Type, Package, ForQuantity, ForProducts, ForAssemblies, 
  BaseUnitCodeEN, BaseUnitRatio, CompatibilityGroup, DescriptionEN, DescriptionFR)
SELECT   0,  'U',  'U',  'U', 0, 1, 1, 1, 'U',  1,    'A', 'Unit',            'Unité'          UNION ALL
SELECT   1,  'C',  'C',  'U', 0, 0, 1, 0, 'U',  100,  'A', 'Hundred',         'Centaine'       UNION ALL
SELECT   2,  'K',  'K',  'U', 0, 0, 1, 0, 'U',  1000, 'A', 'Thousand',        'Millier'        UNION ALL
SELECT   3,  'M',  'M',  'L', 0, 1, 1, 1, 'M',  1,    'B', 'Meter',           'Mètre'          UNION ALL
SELECT   4,  'HM', 'HM', 'L', 0, 1, 1, 1, 'M',  100,  'B', 'Hectometer',      'Hectomètre'     UNION ALL
SELECT   5,  'KM', 'KM', 'L', 0, 1, 1, 1, 'M',  1000, 'B', 'Kilometer' ,      'Kilomètre'      UNION ALL
SELECT   6,  'F',  'P',  'L', 0, 1, 1, 1, 'F',  1,    'B', 'Foot',            'Pied'           UNION ALL
SELECT   7,  'CF', 'CP', 'L', 0, 1, 1, 1, 'F',  100,  'B', 'Hundred feet',    'Cent pieds'     UNION ALL
SELECT   8,  'KF', 'KP', 'L', 0, 1, 1, 1, 'F',  1000, 'B', 'Thousand feet',   'Mille pieds'    UNION ALL
SELECT   12, 'PR', 'PR', 'U', 0, 1, 1, 0, 'PR', 1,    'C', 'Pair',            'Paire'          UNION ALL
SELECT   13, 'BO', 'BO', 'U', 1, 1, 1, 0, 'BO', 1,    'D', 'Box',             'Boîte'          UNION ALL
SELECT   14, 'PG', 'PQ', 'U', 1, 1, 1, 0, 'PG', 1,    'E', 'Package',         'Paquet'         UNION ALL
SELECT   11, 'RL', 'RL', 'U', 0, 1, 1, 0, 'RL', 1,    'F', 'Roll',            'Rouleau'        UNION ALL
SELECT   9,  'L',  'L',  'U', 0, 1, 1, 0, 'L',  1,    'G', 'Length',          'Longueur'       UNION ALL
SELECT   10, 'CL', 'CL', 'U', 0, 0, 1, 0, 'L',  100,  'G', 'Hundred lengths', 'Cent longueurs' UNION ALL
SELECT   15, 'LB', 'LB', 'U', 0, 1, 1, 0, 'LB', 1,    'H', 'Pounds',          'Livres'         UNION ALL
SELECT   16, 'CB', 'CB', 'U', 0, 1, 1, 0, 'LB', 100,  'H', 'Hundred pounds',  'Cent livres'    UNION ALL
SELECT   17, 'KG', 'KG', 'U', 0, 1, 1, 0, 'KG', 1,    'I', 'Kilos',           'Kilos'          UNION ALL
SELECT   18, 'CK', 'CK', 'U', 0, 1, 1, 0, 'KG', 100,  'I', 'Hundred kilos',   'Cent kilos'     
GO

INSERT INTO [dbo].[Sys_UnitsConversion] (
  ConversionId, UnitFrom, UnitTo, Ratio, UnitToUnit, PackageToUnit, UnitToPackage)
-- Unit to same unit
SELECT 00, 'U',  'U',  1, 1, 0, 0      UNION ALL
SELECT 01, 'C',  'C',  1, 1, 0, 0      UNION ALL
SELECT 02, 'K',  'K',  1, 1, 0, 0      UNION ALL
SELECT 03, 'M',  'M',  1, 1, 0, 0      UNION ALL
SELECT 04, 'HM', 'HM', 1, 1, 0, 0      UNION ALL
SELECT 05, 'KM', 'KM', 1, 1, 0, 0      UNION ALL
SELECT 06, 'F',  'F',  1, 1, 0, 0      UNION ALL
SELECT 07, 'CF', 'CF', 1, 1, 0, 0      UNION ALL
SELECT 08, 'KF', 'KF', 1, 1, 0, 0      UNION ALL
SELECT 09, 'L',  'L',  1, 1, 0, 0      UNION ALL
SELECT 10, 'CL', 'CL', 1, 1, 0, 0      UNION ALL
SELECT 11, 'PR', 'PR', 1, 1, 0, 0      UNION ALL
SELECT 12, 'BO', 'BO', 1, 1, 0, 0      UNION ALL
SELECT 13, 'RL', 'RL', 1, 1, 0, 0      UNION ALL
SELECT 14, 'PG', 'PG', 1, 1, 0, 0      UNION ALL
SELECT 15, 'LB', 'LB', 1, 1, 0, 0      UNION ALL
SELECT 16, 'CB', 'CB', 1, 1, 0, 0      UNION ALL
SELECT 17, 'KG', 'KG', 1, 1, 0, 0      UNION ALL
SELECT 18, 'CK', 'CK', 1, 1, 0, 0      UNION ALL

-- Unit to other unit
SELECT 19, 'U',  'C',  0.01,      1, 0, 0 UNION ALL
SELECT 20, 'U',  'K',  0.001,     1, 0, 0 UNION ALL
SELECT 21, 'U',  'BO', 0,         0, 1, 0 UNION ALL
SELECT 22, 'U',  'PG', 0,         0, 1, 0 UNION ALL
SELECT 23, 'C',  'U',  100,       1, 0, 0 UNION ALL
SELECT 24, 'C',  'K',  0.1,       1, 0, 0 UNION ALL
SELECT 25, 'K',  'U',  1000,      1, 0, 0 UNION ALL
SELECT 26, 'K',  'C',  10,        1, 0, 0 UNION ALL
SELECT 27, 'M',  'HM', 0.01,      1, 0, 0 UNION ALL
SELECT 28, 'M',  'KM', 0.001,     1, 0, 0 UNION ALL
SELECT 29, 'M',  'F',  3.2808,    1, 0, 0 UNION ALL
SELECT 30, 'M',  'CF', 0.0328,    1, 0, 0 UNION ALL
SELECT 31, 'M',  'KF', 0.00328,   1, 0, 0 UNION ALL
SELECT 32, 'HM', 'M',  100,       1, 0, 0 UNION ALL
SELECT 33, 'HM', 'KM', 0.1,       1, 0, 0 UNION ALL
SELECT 34, 'HM', 'F',  328.08,    1, 0, 0 UNION ALL
SELECT 35, 'HM', 'CF', 3.28,      1, 0, 0 UNION ALL
SELECT 36, 'HM', 'KF', 0.328,     1, 0, 0 UNION ALL
SELECT 37, 'KM', 'M',  1000,      1, 0, 0 UNION ALL
SELECT 38, 'KM', 'F',  3280.8,    1, 0, 0 UNION ALL
SELECT 39, 'KM', 'CF', 328.08,    1, 0, 0 UNION ALL
SELECT 40, 'KM', 'HM', 100,       1, 0, 0 UNION ALL
SELECT 41, 'KM', 'KF', 3.2808,    1, 0, 0 UNION ALL
SELECT 42, 'F',  'M',  0.3048,    1, 0, 0 UNION ALL
SELECT 43, 'F',  'HM', 0.003048,  1, 0, 0 UNION ALL
SELECT 44, 'F',  'KM', 0.0003048, 1, 0, 0 UNION ALL
SELECT 45, 'F',  'CF', 0.01,      1, 0, 0 UNION ALL
SELECT 46, 'F',  'KF', 0.001,     1, 0, 0 UNION ALL
SELECT 47, 'CF', 'M',  30.48,     1, 0, 0 UNION ALL
SELECT 48, 'CF', 'HM', 0.3048,    1, 0, 0 UNION ALL
SELECT 49, 'CF', 'KM', 0.03048,   1, 0, 0 UNION ALL
SELECT 50, 'CF', 'F',  100,       1, 0, 0 UNION ALL
SELECT 51, 'CF', 'KF', 0.1,       1, 0, 0 UNION ALL
SELECT 52, 'KF', 'M',  304.8,     1, 0, 0 UNION ALL
SELECT 53, 'KF', 'HM', 3.048,     1, 0, 0 UNION ALL
SELECT 54, 'KF', 'KM', 0.3048,    1, 0, 0 UNION ALL
SELECT 55, 'KF', 'F',  1000,      1, 0, 0 UNION ALL
SELECT 56, 'KF', 'CF', 10,        1, 0, 0 UNION ALL
SELECT 57, 'L',  'CL', 0.01,      1, 0, 0 UNION ALL
SELECT 58, 'CL', 'L',  100,       1, 0, 0 UNION ALL
SELECT 59, 'BO', 'U',  -1,        0, 0, 1 UNION ALL
SELECT 60, 'PG', 'U',  -1,        0, 0, 1 UNION ALL
SELECT 61, 'LB', 'CB', 0.01,      1, 0, 0 UNION ALL
SELECT 62, 'CB', 'LB', 100,       1, 0, 0 UNION ALL
SELECT 63, 'KG', 'CK', 0.01,      1, 0, 0 UNION ALL
SELECT 64, 'CK', 'KG', 100,       1, 0, 0
GO
