-- =========================
-- 1. UPSERT (insert/update)
-- =========================
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM contacts WHERE name = p_name
    ) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


-- =========================
-- 2. DELETE (by name or phone)
-- =========================
CREATE OR REPLACE PROCEDURE delete_contact(
    p_value TEXT
)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts
    WHERE name = p_value
       OR phone = p_value;
END;
$$;


-- =========================
-- 3. BULK INSERT + VALIDATION
-- =========================
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    names TEXT[],
    phones TEXT[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
    invalid_data TEXT[] := ARRAY[]::TEXT[];
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP

        -- проверка телефона: только цифры, длина 10-15
        IF phones[i] ~ '^[0-9]{10,15}$' THEN

            -- upsert логика
            IF EXISTS (
                SELECT 1 FROM contacts WHERE name = names[i]
            ) THEN
                UPDATE contacts
                SET phone = phones[i]
                WHERE name = names[i];
            ELSE
                INSERT INTO contacts(name, phone)
                VALUES (names[i], phones[i]);
            END IF;

        ELSE
            -- сохраняем некорректные данные
            invalid_data := array_append(
                invalid_data,
                names[i] || ':' || phones[i]
            );
        END IF;

    END LOOP;

    -- вывод ошибок
    RAISE NOTICE 'Invalid data: %', invalid_data;

END;
$$;