CREATE OR REPLACE TABLE employeee (
    id INT AUTOINCREMENT PRIMARY KEY,
    name VARCHAR(100) 
);
 
 
INSERT INTO employeee (name)
VALUES
    ('John Smith'), ('Jane Doe'), ('Michael Johnson'), ('Emily Davis'),
    ('Chris Brown'), ('Amanda Miller'), ('David Wilson'), ('Sophia Lee'),
    ('James White'), ('Olivia Martinez'),
    ('Robert Brown'), ('Emma Thompson'), ('William Davis'), ('Mia Johnson'),
    ('Alexander Smith'), ('Ella Wilson'), ('Daniel Lee'), ('Madison White'),
    ('Matthew Martinez'), ('Isabella Miller'),('jerry'),('jeri'),('india'),('dani'),
    ('allu'),('arjum'),('ram'),('paki'),('raina'),('dhoni'),('bravo'),('chakara'),('vijay'),('ajith'),
    ('robert'),('brown'), ('jane'),('jaswal'),('gill'),('ruturaj'),('amb'),('william'),('fdani'),
    ('ajau'),('ajay'),('dube'),('raheane'),('noor'),('chahar'),('daniel'),('brain'),('brain'),('ocean'),
    ('ahmed'),('murugan'),('ashwin'),('amir'),('sundar'),('jeri'),('jadeja'),('John Smith'), ('Jane Doe'), ('Michael Johnson'), ('Emily Davis'),
    ('Chris Brown'), ('Amanda Miller'), ('David Wilson'), ('Sophia Lee'),
    ('James White'), ('Olivia Martinez'),
    ('Robert Brown'), ('Emma Thompson'), ('William Davis'), ('Mia Johnson'),
    ('Alexander Smith'), ('Ella Wilson'), ('Daniel Lee'), ('Madison White'),
    ('Matthew Martinez'), ('Isabella Miller'),('jerry'),('jeri'),('india'),('dani'),
    ('allu'),('arjum'),('ram'),('paki'),('raina'),('dhoni'),('bravo'),('chakara'),('vijay'),('ajith'),
    ('robert'),('brown'), ('jane'),('jaswal'),('gill'),('ruturaj'),('amb'),('william'),('fdani'),
    ('ajau'),('ajay'),('dube'),('raheane'),('noor'),('chahar'),('daniel'),('brain'),('brain'),('ocean'),
    ('ahmed'),('murugan'),('ashwin'),('amir'),('sundar'),('jeri'),('jadeja'),('John Smith'), ('Jane Doe'), ('Michael Johnson'), ('Emily Davis'),
    ('Chris Brown'), ('Amanda Miller'), ('David Wilson'), ('Sophia Lee'),
    ('James White'), ('Olivia Martinez'),
    ('Robert Brown'), ('Emma Thompson'), ('William Davis'), ('Mia Johnson'),
    ('Alexander Smith'), ('Ella Wilson'), ('Daniel Lee'), ('Madison White'),
    ('Matthew Martinez'), ('Isabella Miller'),('jerry'),('jeri'),('india'),('dani'),
    ('allu'),('arjum'),('ram'),('paki'),('raina'),('dhoni'),('bravo'),('chakara'),('vijay'),('ajith'),
    ('robert'),('brown'), ('jane'),('jaswal'),('gill'),('ruturaj'),('amb'),('william'),('fdani'),
    ('ajau'),('ajay'),('dube'),('raheane'),('noor'),('chahar'),('daniel'),('brain'),('brain'),('ocean'),
    ('ahmed'),('murugan'),('ashwin'),('amir'),('sundar'),('jeri'),('jadeja');
 
 
 
   WITH NameSimilarities AS (
    SELECT
        e1.id AS id1,
        e1.name AS name1,
        e2.id AS id2,
        e2.name AS name2,
        JAROWINKLER_SIMILARITY(e1.name, e2.name) AS similarity
    FROM
        employeee e1
    JOIN
        employeee e2 ON e1.id <> e2.id
),
RankedSimilarities AS (
    SELECT
        id1,
        name1,
        name2,
        similarity,
        ROW_NUMBER() OVER (PARTITION BY id1 ORDER BY similarity DESC) AS rank
    FROM
        NameSimilarities
)
SELECT
    id1,
    name1,
    name2,
    similarity
FROM
    RankedSimilarities
WHERE
    rank <= 10
ORDER BY
    id1, similarity DESC;
 