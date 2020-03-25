--Create Table to import HarvestData
--Will match with Stored Procedure layout

CREATE TABLE HarvestData(
	Period varchar(6) NOT NULL,
	Date DATE NOT NULL,
	Client varchar(200) NULL,
	ProjName varchar(200) NULL,
	ProjCode varchar(50) NULL,
	Task varchar(800) NULL,
	Hours decimal(8,2) NULL,
	Billable varchar(10) NULL,
	Employee varchar(80) NULL,
	Department varchar(40) NULL,
	BillRate decimal(8,2) NULL,
	BillAmt decimal(8,2) NULL,
	CostRate decimal(8,2) NULL,
	CostAmt decimal(8,2) NULL
)