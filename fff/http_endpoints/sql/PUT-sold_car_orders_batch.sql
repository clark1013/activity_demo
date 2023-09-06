USE sample_data;
UPDATE `sold_car_orders` SET `name` = IF(length(${name})>0,${name},`name`),
`year` = IF(length(${year})>0,${year},`year`),
`selling_price` = IF(length(${selling_price})>0,${selling_price},`selling_price`),
`km_driven` = IF(length(${km_driven})>0,${km_driven},`km_driven`),
`fuel` = IF(length(${fuel})>0,${fuel},`fuel`),
`seller_type` = IF(length(${seller_type})>0,${seller_type},`seller_type`),
`transmission` = IF(length(${transmission})>0,${transmission},`transmission`),
`owner` = IF(length(${owner})>0,${owner},`owner`) 
 WHERE 1=0 ;