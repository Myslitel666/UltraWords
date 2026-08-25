-- Записи за конкретный час (например, с 19:00 до 19:59)
SELECT * 
FROM UltraWords 
WHERE DATE(DateTimeSaving) = '2026-08-25'
  AND strftime('%H', DateTimeSaving) = '19'; -- 19 час