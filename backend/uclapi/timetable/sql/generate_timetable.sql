CREATE OR REPLACE FUNCTION get_student_timetable_a(
    TEXT, -- UPI
    TEXT  -- Set ID
)
RETURNS SETOF RECORD -- TEXT --SETOF RECORD
LANGUAGE plpgsql
AS $$
DECLARE
  upi ALIAS FOR $1;
  set_id ALIAS FOR $2;

  student_id       TEXT;
  st_course_id     TEXT;
  st_course_year   INTEGER;
  co_course_id     TEXT;
  co_course_year   TEXT;
  overall_year     TEXT;
BEGIN
-- qtype2 (UPI Field) is stored all caps in the database
    upi := UPPER(upi);

-- Drop any temporary tables
    DROP TABLE IF EXISTS tt_tmp_hasgroupnum;
    DROP TABLE IF EXISTS tt_tmp_taking;
    DROP TABLE IF EXISTS tt_tmp_events_slot_id;
    DROP TABLE IF EXISTS tt_tmp_cmis_events;

-- Get basic information about the student
    SELECT  s.studentid,
            s.courseid,
            s.courseyear,
            c.courseid,
            s.courseyear + CASE WHEN SUBSTR(s.courseid, 1, 1) = 'U' THEN 0 WHEN SUBSTR(s.courseid, 1, 1) = 'T' THEN 10 ELSE 20 END,
            CASE WHEN SUBSTR(s.courseid, 1, 1) = 'U' THEN 9 WHEN SUBSTR(s.courseid, 1, 1) = 'T' THEN 19 ELSE 29 END courseyear
    INTO   student_id,
           st_course_id,
           st_course_year,
           co_course_id,
           co_course_year,
           overall_year
    FROM   timetable_studentsa s
    LEFT OUTER JOIN timetable_coursea c
        ON (c.setid = s.setid AND c.linkcode = s.linkcode)
    WHERE  s.qtype2 = upi AND s.setid = set_id;

-- Modules where the student is in a specific group
    CREATE TEMP TABLE tt_tmp_hasgroupnum (
        groupnum,
        moduleid,
        instid,
        instcode
    )
    AS
    SELECT mg.groupnum, mg.moduleid, ci.instid, ci.instcode
    FROM timetable_stumodulesa sm
    JOIN timetable_modulegroupsa mg
        ON (
            sm.moduleid = mg.moduleid
            AND sm.modgrpcode = mg.grpcode
        )
    LEFT OUTER JOIN timetable_cminstancesa ci
         ON sm.instid = ci.instid
        AND sm.setid = set_id
        AND ci.setid = set_id
    WHERE sm.studentid = student_id
    AND sm.setid = mg.setid
    AND sm.setid = set_id
    AND sm.modgrpcode IS NOT NULL;

-- Modules the student is taking
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
            'Y', -- Temporarily using this as the stumodselstatus
           smUnion.unfitted,
           smUnion.instid,
           smUnion.instcode
    FROM (
        SELECT sm.setid,
               sm.studentid,
               sm.moduleid,
               mg.grpcode,
               mg.groupnum,
               'Y' as unfitted,
               ci.instid,
               ci.instcode
        FROM timetable_stumodulesa sm
        JOIN timetable_modulegroupsa mg
            ON sm.moduleid = mg.moduleid
        LEFT OUTER JOIN timetable_cminstancesa ci
            ON sm.instid = ci.instid
           AND sm.setid = ci.setid
           AND ci.setid = set_id
        WHERE NOT EXISTS (
            SELECT 1
            FROM tt_tmp_hasgroupnum hg
            WHERE hg.moduleid = mg.moduleid
              AND hg.instid = mg.instid
              AND hg.groupnum = mg.groupnum
        )
        AND sm.studentid = student_id
        AND sm.modgrpcode IS NULL
        AND sm.setid = mg.setid
        AND sm.setid = set_id
    UNION all
    SELECT sm2.setid,
           sm2.studentid,
           sm2.moduleid,
           sm2.modgrpcode,
           NULL,
           'N' as unfitted,
           ci.instid,
           ci.instcode
    FROM timetable_stumodulesa sm2
    LEFT OUTER JOIN timetable_cminstancesa ci
        ON sm2.instid = ci.instid
       AND sm2.setid = ci.setid
       AND ci.setid = set_id
    WHERE sm2.studentid = student_id
      AND sm2.setid = set_id
    ) smUnion
        LEFT OUTER JOIN timetable_stumodulesa usm
            ON (
                smUnion.setid = usm.setid
                AND smUnion.studentid = usm.studentid
                AND smUnion.moduleid = usm.moduleid
                AND smUnion.instid = usm.instid
            )
    ;

    CREATE TEMP TABLE tt_tmp_events_slot_id (
        slotid,          -- tt.slotid   | tt.slotid
        moduleid,        -- NULL        | tt.moduleid
        modgrpcode,      -- NULL        | tt.modgrpcode
        setid,           -- tt.setid    | tt.setid
        stumodselstatus, -- NULL        | st.stumodselstatus
        unfitted,        -- 'N'         | st.unfitted
        compos_crit,     -- 'NO_MOD'    | 'MOD'
        instid,          -- ci.instid   | ci.instid
        instcode         -- ci.instcode | ci.instcode
    )
    AS
        SELECT tt.slotid :: BIGINT,
               NULL :: TEXT,
               NULL :: TEXT,
               tt.setid :: TEXT,
               NULL :: TEXT,
               'N' :: TEXT,
               'NO_MOD' :: TEXT,
               ci.instid :: TEXT,
               ci.instcode :: TEXT
        FROM timetable_timetablea tt
        LEFT OUTER JOIN timetable_cminstancesa ci
             ON tt.instid = ci.instid
            AND tt.setid  = ci.setid
            AND ci.setid  = set_id
        WHERE tt.setid = set_id
          AND tt.weekday BETWEEN 1 and 7
          AND tt.starttime  IS NOT NULL
          AND tt.finishtime IS NOT NULL
          AND (
                --   (
                --     tt.courseid,
                --     tt.courseyear,
                --     tt.classgroupid,
                --     COALESCE(tt.clsgrpcode, '[|X|]')
                --   ) IN
                -- (
                --     SELECT courseid,
                --            courseyear,
                --            classgroupid,
                --            COALESCE(clsgrpcode, '[|X|]') clsgrpcode
                --     FROM timetable_stuclassesa
                --     WHERE setid = set_id
                --     AND studentid = student_id
                -- )
                -- OR (
                  (
                      tt.courseid = st_course_id
                      AND tt.classgroupid IS NULL
                      AND tt.courseyear:: TEXT IN (st_course_year :: TEXT, '-1', '0')
                  )
                  OR (
                      tt.courseid = co_course_id
                      AND tt.classgroupid IS NULL
                      AND tt.courseyear :: TEXT IN (co_course_year :: TEXT, '-1', '0', overall_year :: TEXT)
                  )
              )
    UNION
        SELECT tt.slotid :: BIGINT,
               tt.moduleid :: TEXT,
               tt.modgrpcode :: TEXT, 
               tt.setid :: TEXT,
               st.stumodselstatus :: TEXT,
               st.unfitted :: TEXT,
               'MOD' :: TEXT,
               ci.instid :: TEXT,
               ci.instcode :: TEXT
        FROM timetable_timetablea tt
        JOIN tt_tmp_taking st
            ON (
                    st.moduleid = tt.moduleid
                AND tt.setid    = set_id
                AND (
                    st.grpcode  = tt.modgrpcode
                    OR (
                            st.grpcode    IS NULL
                        AND tt.modgrpcode IS NULL
                    )
                )
            )
        LEFT OUTER JOIN timetable_cminstancesa ci
            ON tt.instid = ci.instid
           AND tt.setid  = ci.setid
           AND ci.setid  = set_id
    ;


-- Get all the CMIS events associated with the slots occupied by
-- the modules the student is taking

    CREATE TEMP TABLE tt_tmp_cmis_events
    AS
    SELECT * FROM tt_tmp_events_slot_id -- TODO: figure out how this relates to cmis_g_tt_stu_events
    WHERE (
            (weekday is not null)
        AND (weekday > 0)
        AND (starttime is not null)
        AND (duration is not null)
    )
    ORDER BY weekday,
             starttime,
             weekmap DESC,
             moduleid,
             modgrpcode,
             duration,
             slotid,
             compos_crit;

-- Return the timetable we just built back to the calling application
    RETURN QUERY SELECT * FROM tt_tmp_cmis_events;

END
$$;