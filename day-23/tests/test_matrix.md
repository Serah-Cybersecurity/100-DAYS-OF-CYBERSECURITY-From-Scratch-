# Sigma Detection Rule Test Matrix

| Test ID | Event | Expected result | Actual result |
| :--- | :--- | :--- | :--- |
| T001 | EventID 4625 | Rule 1 matches | Matched Records 1 & 2 (script summary printed No match due to alphabetical glob order) |
| T002 | EventID 4740 | Rule 2 matches | Matched Record 4 (script summary printed No match due to alphabetical glob order) |
| T003 | EventID 4624 | Rule 3 matches | Matched Records 3 & 5 (script summary printed No match due to alphabetical glob order) |
| T004 | EventID 4740 | Rule 3 does not match | Rule 3 does not match (Record 4 only matched Rule 2) |
| T005 | Unrelated event ID | No match | No match (fixture contains only 4624, 4625, and 4740) |
