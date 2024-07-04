SELECT e.Year, c.Constituency, p1.Party, p2.Party, a.*
FROM constituencyresult a
    INNER JOIN election e on a.ElectionID = e.ID
INNER JOIN constituency c on a.ConstituencyID = c.ID
INNER JOIN party p1 on a.FirstPartyID = p1.ID
INNER JOIN party p2 on a.SecondPartyID = p2.ID
ORDER BY a.ID
;