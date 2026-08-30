INSERT OR IGNORE INTO UltraWordsCases (wordId, caseId, value, multiplicity, GenderId)
SELECT 
  uw.Id wordId,
  c.Id caseId,
  OLD_NAMES_TRANSF(uw.value, c.id,q.qid) as value, 
  Q.QID as multiplicity,
  1 as GenderId
FROM UltraWords uw
JOIN Cases c
  on c.id <> 0
JOIN (
  SELECT 1 QID
  UNION ALL
  SELECT 2 QID
) Q
WHERE uw.comment = 'Библия'
  --AND SUBSTR(uw.value, -1) not in ('а','я','ь', 'ё')
  AND uw.value NOT LIKE '% %'
  AND uw.TypeId = 5
  AND uw.PartOfSpeechId = 2
  --AND SUBSTR(uw.value, -2) <> 'ов'
ORDER BY uw.value, c.id
--)