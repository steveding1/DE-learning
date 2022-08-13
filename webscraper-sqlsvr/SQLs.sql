CREATE DATABASE ETL
GO

CREATE TABLE [Products](
[Id] INT NOT NULL IDENTITY PRIMARY KEY,
[Item] VARCHAR (100) NOT NULL,
[Price] smallmoney NOT NULL,
[Volumn] smallint NOT NULL,
[UnitPrice] smallmoney,
[Alcohol] float
)
GO

Grant select on Products to etl

SELECT TOP (1000) [Id]
      ,[Item]
      ,[Price]
      ,[Volumn]
      ,[UnitPrice]
      ,[Alcohol]
  FROM [ETL].[dbo].[Products]
