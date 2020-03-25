--Create Stored Procedure for Python script to exectue
--Parameters are laid out to match Table

CREATE PROCEDURE RefreshHarvestPython
	@sPeriod varchar(6),
	@sDate DATE,
	@sClient varchar(200),
	@ProjName varchar(200),
	@ProjCode varchar(50),
	@Task varchar(800),
	@Hours decimal(8,2),
	@Billable varchar(10),
	@Employee varchar(80),
	@Department varchar(40),
	@BillRate decimal(8,2),
	@BillAmt decimal(8,2),
	@CostRate decimal(8,2),
	@CostAmt decimal(8,2)

AS
	INSERT INTO HarvestData (
		Period, Date, Client, ProjName, ProjCode, Task, Hours, Billable, Employee, Department, BillRate, BillAmt, CostRate, CostAmt
	)

	VALUES (
		@sPeriod,
		@sDate,
		@sClient,
		@ProjName,
		@ProjCode,
		@Task,
		@Hours,
		@Billable,
		@Employee,
		@Department,
		@BillRate,
		@BillAmt,
		@CostRate,
		@CostAmt
	)