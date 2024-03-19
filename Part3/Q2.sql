WITH TotalPayments AS (
    SELECT 
        p.client_id, 
        SUM(CASE WHEN YEAR(p.transaction_date) = 2018 THEN p.payment_amt ELSE 0 END) AS TotalPayment2018,
        SUM(p.payment_amt) AS TotalPaymentAllTime
    FROM 
        [Transaction].[dbo].[payments] p
    WHERE 
        p.payment_code <> 'DEFAULT'
    GROUP BY 
        p.client_id
),
RankedClients AS (
    SELECT 
        c.client_id, 
        c.entity_type, 
        tp.TotalPayment2018, 
        RANK() OVER (ORDER BY tp.TotalPaymentAllTime DESC) AS RankTotalPaymentAllTime
    FROM 
        [Transaction].[dbo].[clients] c
    INNER JOIN 
        TotalPayments tp ON c.client_id = tp.client_id
)
SELECT TOP 20 
    rc.client_id, 
    rc.entity_type, 
    ROUND(rc.TotalPayment2018,2) AS TotalPayment2018,
    rc.RankTotalPaymentAllTime
FROM 
    RankedClients rc
ORDER BY 
    rc.TotalPayment2018 DESC
