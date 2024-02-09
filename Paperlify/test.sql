-- To rearrange the id serially
SET @counter = 0;
UPDATE auth_user SET id = @counter:=@counter+1 ORDER BY id;
ALTER TABLE auth_user AUTO_INCREMENT = 1;

-- To delete duplicate documents
DELETE FROM document
WHERE id NOT IN (
    SELECT MIN(id)
    FROM document
    GROUP BY doc_name
);
