/*SQL SERVER*/
/**********QUESTION_1**************/

SELECT
	p.SUBCATEGORY,
	ROUND((SUM(o.SALES)),3) AS SALE,
	ROUND((SUM(o.SALES) / (SELECT SUM(SALES) FROM [Sales].[dbo].[orders])) * 100, 2) AS '%'
FROM
	[Sales].[dbo].[orders] o
INNER JOIN
	[Sales].[dbo].[product] p ON o.PRODUCT_ID = p.ID
GROUP BY
	p.SUBCATEGORY
ORDER BY
	SALE DESC;

/**********QUESTION_2**************/

SELECT
    p.SUBCATEGORY,
    ROUND((SUM(o.SALES) / (SELECT SUM(SALES) FROM [Sales].[dbo].[orders])) * 100, 2) AS '%',
	ROUND((SUM(o.SALES) / (SELECT SUM(SALES) FROM [Sales].[dbo].[orders])) * 2000, 0) AS Spread
FROM
    [Sales].[dbo].[orders] o
INNER JOIN
    [Sales].[dbo].[product] p ON o.PRODUCT_ID = p.ID
GROUP BY
    p.SUBCATEGORY
ORDER BY
	'%' DESC

/* Sau khi thực hiện lệnh trên, tính tổng toàn bộ Spread được 2001, cho nên ta cần giảm 1 spread của một loại Subscategory.
Khi thực hiện tính toán chênh lệnh giữa việc làm tròn và không làm tròn, nhận thấy phần Art có phần chênh lệch tăng lên lớn nhất (0.39).
Cho nên ta sẽ chọn Art để giảm Spread xuống 1 đơn vị.
*/


/**********QUESTION_3**************/

WITH PairedProducts AS (
    SELECT
        o1.PRODUCT_ID as PRODUCT_1,
        o2.PRODUCT_ID as PRODUCT_2
    FROM
        [Sales].[dbo].[orders] o1
    INNER JOIN 
        [Sales].[dbo].[orders] o2
    ON 
        o1.ORDER_ID = o2.ORDER_ID AND
        o1.PRODUCT_ID != o2.PRODUCT_ID
)
SELECT 
    p1.ID as PRODUCT_1,
    p2.ID as PRODUCT_2,
    COUNT(*) as COUNT
FROM 
    PairedProducts pp
INNER JOIN
    [Sales].[dbo].[product] p1 ON pp.PRODUCT_1 = p1.ID
INNER JOIN
    [Sales].[dbo].[product] p2 ON pp.PRODUCT_2 = p2.ID
GROUP BY
    p1.ID,
    p2.ID
ORDER BY
    COUNT(*) DESC;

