CREATE OR REPLACE FUNCTION get_student_timetable(
    upi         TEXT, -- UPI
    set_id      TEXT, -- Set ID
    rb_bucket   TEXT, -- Roombookings Bucket
    tt_bucket   TEXT  -- Timetable bucket
)
-- RETURNS SETOF RECORD -- TEXT --SETOF RECORD
RETURNS TABLE (
    moduleid TEXT,
    modgrpcode TEXT,
    instcode TEXT,
    weekid BIGINT,
    lecturerid TEXT,
    deptid TEXT,
    siteid TEXT,
    roomid TEXT,
    slotid BIGINT,
    sitename VARCHAR,
    roomname VARCHAR,
    bookabletype VARCHAR,
    starttime VARCHAR,
    finishtime VARCHAR,
    duration BIGINT,
    startdatetime TIMESTAMPTZ,
    finishdatetime TIMESTAMPTZ,
    weeknumber DOUBLE PRECISION,
    condisplayname VARCHAR,
    title VARCHAR,
    descrip VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE

-- Bucket table names
    bt_rb_booking       TEXT;
    bt_tt_cminstances   TEXT;
    bt_tt_course        TEXT;
    bt_tt_modulegroups  TEXT;
    bt_tt_students      TEXT;
    bt_tt_stumodules    TEXT;
    bt_tt_timetable     TEXT;

-- General calculation variables
    student_id       TEXT;
    st_course_id     TEXT;
    st_course_year   INTEGER;
    -- co_course_id     TEXT;
    co_course_year   TEXT;
    overall_year     TEXT;
BEGIN
-- qtype2 (UPI Field) is stored all caps in the database
    upi := UPPER(upi);

-- We process bucket names in upper case
    rb_bucket := UPPER(rb_bucket);
    tt_bucket := UPPER(tt_bucket);

-- Generate Table Names

    -- This is all extremely ugly but there isn't really an alternative that
    -- can make this function any more generalised.
    -- It will work without matching buckets, however.

    IF rb_bucket = 'A' THEN
        bt_rb_booking       := 'roombookings_bookinga';
    ELSE
        bt_rb_booking       := 'roombookings_bookingb';
    END IF;

    IF tt_bucket = 'A' THEN
        bt_tt_cminstances   := 'timetable_cminstancesa';
        bt_tt_course        := 'timetable_coursea';
        bt_tt_modulegroups  := 'timetable_modulegroupsa';
        bt_tt_students      := 'timetable_studentsa';
        bt_tt_stumodules    := 'timetable_stumodulesa';
        bt_tt_timetable     := 'timetable_timetablea';
    ELSE
        bt_tt_cminstances   := 'timetable_cminstancesb';
        bt_tt_course        := 'timetable_courseb';
        bt_tt_modulegroups  := 'timetable_modulegroupsb';
        bt_tt_students      := 'timetable_studentsb';
        bt_tt_stumodules    := 'timetable_stumodulesb';
        bt_tt_timetable     := 'timetable_timetableb';
    END IF;

-- Drop any temporary tables that already exist
    DROP TABLE IF EXISTS tt_tmp_hasgroupnum;
    DROP TABLE IF EXISTS tt_tmp_taking;
    DROP TABLE IF EXISTS tt_tmp_events_slot_id;
    DROP TABLE IF EXISTS tt_tmp_timetable_events;

-- Get basic information about the student
    
    IF tt_bucket = 'A' THEN

        SELECT  s.studentid,
                s.courseid,
                s.courseyear,
                -- c.courseid,
                s.courseyear + CASE WHEN SUBSTR(s.courseid, 1, 1) = 'U' THEN 0 WHEN SUBSTR(s.courseid, 1, 1) = 'T' THEN 10 ELSE 20 END,
                CASE WHEN SUBSTR(s.courseid, 1, 1) = 'U' THEN 9 WHEN SUBSTR(s.courseid, 1, 1) = 'T' THEN 19 ELSE 29 END courseyear
        INTO   student_id,
            st_course_id,
            st_course_year,
            -- co_course_id,
            co_course_year,
            overall_year
        FROM   timetable_studentsa s
        -- LEFT OUTER JOIN timetable_coursea c
        --     ON (c.setid = s.setid AND c.linkcode = s.linkcode)
        WHERE  s.qtype2 = upi AND s.setid = set_id;

    ELSE

        SELECT  s.studentid,
                s.courseid,
                s.courseyear,
                -- c.courseid,
                s.courseyear + CASE WHEN SUBSTR(s.courseid, 1, 1) = 'U' THEN 0 WHEN SUBSTR(s.courseid, 1, 1) = 'T' THEN 10 ELSE 20 END,
                CASE WHEN SUBSTR(s.courseid, 1, 1) = 'U' THEN 9 WHEN SUBSTR(s.courseid, 1, 1) = 'T' THEN 19 ELSE 29 END courseyear
        INTO   student_id,
            st_course_id,
            st_course_year,
            -- co_course_id,
            co_course_year,
            overall_year
        FROM   timetable_studentsb s
        -- LEFT OUTER JOIN timetable_courseb c
        --     ON (c.setid = s.setid AND c.linkcode = s.linkcode)
        WHERE  s.qtype2 = upi AND s.setid = set_id;

    END IF;


-- Modules where the student is in a specific group
    EXECUTE '
    CREATE TEMP TABLE tt_tmp_hasgroupnum (
        groupnum,
        moduleid,
        instid,
        instcode
    )
    AS
    SELECT mg.groupnum, mg.moduleid, ci.instid, ci.instcode
    FROM ' || bt_tt_stumodules   || ' sm
    JOIN ' || bt_tt_modulegroups || ' mg
        ON (
            sm.moduleid = mg.moduleid
            AND sm.modgrpcode = mg.grpcode
        )
    LEFT OUTER JOIN ' || bt_tt_cminstances || ' ci
         ON sm.instid = ci.instid
        AND sm.setid = ''' || set_id || '''
        AND ci.setid = ''' || set_id || '''
    WHERE sm.studentid = ''' || student_id || '''
    AND sm.setid = mg.setid
    AND sm.setid = ''' || set_id || '''
    AND sm.modgrpcode IS NOT NULL;
    ';

-- Modules the student is taking
    EXECUTE '
    CREATE TEMP TABLE tt_tmp_taking (
        moduleid,
        grpcode,
        groupnum,
        stumodselstatus,
        unfitted,
        instid,
        instcode
    )
    AS
    SELECT smUnion.moduleid,
           smUnion.grpcode,
           smUnion.groupnum,
        --    usm.status_flag,
            ''Y'', -- Temporarily using this as the stumodselstatus
           smUnion.unfitted,
           smUnion.instid,
           smUnion.instcode
    FROM (
        SELECT sm.setid,
               sm.studentid,
               sm.moduleid,
               mg.grpcode,
               mg.groupnum,
               ''Y'' as unfitted,
               ci.instid,
               ci.instcode
        FROM ' || bt_tt_stumodules    || ' sm
        JOIN ' || bt_tt_modulegroups  || ' mg
            ON sm.moduleid = mg.moduleid
        LEFT OUTER JOIN ' || bt_tt_cminstances || ' ci
            ON sm.instid = ci.instid
           AND sm.setid = ci.setid
           AND ci.setid = ''' || set_id || '''
        WHERE NOT EXISTS (
            SELECT 1
            FROM tt_tmp_hasgroupnum hg
            WHERE hg.moduleid = mg.moduleid
              AND hg.instid = mg.instid
              AND hg.groupnum = mg.groupnum
        )
        AND sm.studentid = ''' || student_id || '''
        AND sm.modgrpcode IS NULL
        AND sm.setid = mg.setid
        AND sm.setid = ''' || set_id || '''
    UNION all
    SELECT sm2.setid,
           sm2.studentid,
           sm2.moduleid,
           sm2.modgrpcode,
           NULL,
           ''N'' as unfitted,
           ci.instid,
           ci.instcode
    FROM '            || bt_tt_stumodules  || ' sm2
    LEFT OUTER JOIN ' || bt_tt_cminstances || ' ci
        ON sm2.instid = ci.instid
       AND sm2.setid = ci.setid
       AND ci.setid = ''' || set_id || '''
    WHERE sm2.studentid = ''' || student_id || '''
      AND sm2.setid = ''' || set_id || '''
    ) smUnion
        LEFT OUTER JOIN ' || bt_tt_stumodules || ' usm
            ON (
                smUnion.setid = usm.setid
                AND smUnion.studentid = usm.studentid
                AND smUnion.moduleid = usm.moduleid
                AND smUnion.instid = usm.instid
            );
    '
    ;

    RAISE NOTICE '%s', bt_tt_timetable;
    RAISE NOTICE '%s', bt_tt_cminstances;
    RAISE NOTICE '%s', set_id;
    RAISE NOTICE '%s', student_id;
    RAISE NOTICE '%s', st_course_id;
    RAISE NOTICE '%s', st_course_year;
    -- RAISE NOTICE co_course_id;
    RAISE NOTICE '%s', co_course_year;
    RAISE NOTICE '%s', overall_year;

    EXECUTE '
    CREATE TEMP TABLE tt_tmp_events_slot_id (
        slotid,          -- tt.slotid     | tt.slotid
        moduleid,        -- NULL          | tt.moduleid
        modgrpcode,      -- NULL          | tt.modgrpcode
        setid,           -- tt.setid      | tt.setid
        stumodselstatus, -- NULL          | st.stumodselstatus
        unfitted,        -- N             | st.unfitted
        compos_crit,     -- NO_MOD        | MOD
        instid,          -- ci.instid     | ci.instid
        instcode         -- ci.instcode   | ci.instcode
    )
    AS
        SELECT tt.slotid :: BIGINT,
               NULL :: TEXT,
               NULL :: TEXT,
               tt.setid :: TEXT,
               NULL :: TEXT,
               ''N'' :: TEXT,
               ''NO_MOD'' :: TEXT,
               ci.instid :: TEXT,
               ci.instcode :: TEXT
        FROM ' || bt_tt_timetable || ' tt
        LEFT OUTER JOIN ' || bt_tt_cminstances || ' ci
             ON tt.instid = ci.instid
            AND tt.setid  = ci.setid
            AND ci.setid  = ''' || set_id || '''
        WHERE tt.setid = ''' || set_id || '''
          AND tt.weekday BETWEEN 1 and 7
          AND tt.starttime  IS NOT NULL
          AND tt.finishtime IS NOT NULL
          AND (
                --   (
                --     tt.courseid,
                --     tt.courseyear,
                --     tt.classgroupid,
                --     COALESCE(tt.clsgrpcode, ''[|X|]'')
                --   ) IN
                -- (
                --     SELECT courseid,
                --            courseyear,
                --            classgroupid,
                --            COALESCE(clsgrpcode, ''[|X|]'') clsgrpcode
                --     FROM timetable_stuclassesa
                --     WHERE setid = ''' || set_id || '''
                --     AND studentid = ''' || student_id || '''
                -- )
                -- OR (
                  (
                      tt.courseid = ''' || st_course_id || '''
                      AND tt.classgroupid IS NULL
                      AND tt.courseyear:: TEXT IN (''' || st_course_year || ''' :: TEXT, ''-1'', ''0'')
                  )
                  OR (
                      tt.courseid = ''' || st_course_id || ''' -- NB: this was co_course_id!
                      AND tt.classgroupid IS NULL
                      AND tt.courseyear :: TEXT IN (''' || co_course_year || ''' :: TEXT, ''-1'', ''0'', ''' || overall_year || ''' :: TEXT)
                  )
              )
    UNION
        SELECT tt.slotid :: BIGINT,
               tt.moduleid :: TEXT,
               tt.modgrpcode :: TEXT, 
               tt.setid :: TEXT,
               st.stumodselstatus :: TEXT,
               st.unfitted :: TEXT,
               ''MOD'' :: TEXT,
               ci.instid :: TEXT,
               ci.instcode :: TEXT
        FROM ' || bt_tt_timetable  || ' tt
        JOIN tt_tmp_taking st
            ON (
                    st.moduleid = tt.moduleid
                AND tt.setid    = ''' || set_id || '''
                AND (
                    st.grpcode  = tt.modgrpcode
                    OR (
                            st.grpcode    IS NULL
                        AND tt.modgrpcode IS NULL
                    )
                )
                AND st.instid = tt.instid
                -- THIS IS A HACK TO FIX THE DUPLICATION BUG
                -- TODO: Remove this when stuclasses is available
            )
        LEFT OUTER JOIN ' || bt_tt_cminstances || ' ci
            ON tt.instid = ci.instid
           AND tt.setid  = ci.setid
           AND ci.setid  = ''' || set_id || ''';
    ';


    EXECUTE '
    CREATE TEMP TABLE tt_tmp_timetable_events
    AS
    SELECT tes.moduleid as moduleid,
           tes.modgrpcode as modgrpcode,
           tes.instcode as instcode,
           tt.weekid as weekid,
           tt.lecturerid as lecturerid,
           tt.deptid as deptid,
           tt.siteid as siteid,
           tt.roomid as roomid,
           tes.slotid as slotid,
           rb.sitename as sitename,
           rb.roomname as roomname,
           rb.bookabletype as bookabletype,
           rb.starttime as starttime,
           rb.finishtime as finishtime,
           tt.duration as duration,
           rb.startdatetime as startdatetime,
           rb.finishdatetime as finishdatetime,
           rb.weeknumber as weeknumber,
           rb.condisplayname as condisplayname,
           rb.title as title,
           rb.descrip as descrip
    FROM ' || bt_tt_timetable || ' tt
    INNER JOIN tt_tmp_events_slot_id tes
        ON tt.slotid = tes.slotid
       AND tt.slotid = tes.slotid
    INNER JOIN ' || bt_rb_booking || ' rb
        ON tt.slotid = rb.slotid
       AND tt.setid  = rb.setid
    LEFT OUTER JOIN ' || bt_tt_cminstances || ' ci
        ON tt.instid = ci.instid
       AND tt.setid  = ci.setid 
    WHERE (
            (tt.weekday IS NOT NULL)
        AND (tt.weekday > 0)
        AND (tt.starttime IS NOT NULL)
        AND (tt.duration IS NOT NULL)
        AND (tt.instid = ci.instid)
        AND (ci.instid :: TEXT = tes.instid :: TEXT)
    )
    ORDER BY weeknumber,
             startdatetime,
             moduleid,
             title
    ';

-- Return the timetable we just built back to the calling application
    RETURN QUERY SELECT DISTINCT * FROM tt_tmp_timetable_events;

END
$$;
