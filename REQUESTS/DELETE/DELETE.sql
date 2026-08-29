DELETE FROM Words 
WHERE Value IN (
    SELECT lower(Value)
    FROM UltraWords
);