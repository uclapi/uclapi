CREATE OR REPLACE FUNCTION get_student_timetable(
    upi         TEXT, -- UPI
    set_id      TEXT, -- Set ID
    bucket      TEXT  -- Cache bucket (a or b)
)
RETURNS TABLE (
    startdatetime       TIMESTAMPTZ,            -- 01
    finishdatetime      TIMESTAMPTZ,            -- 02
    duration            BIGINT,                 -- 03
    slotid              BIGINT,                 -- 04
    weekid              BIGINT,                 -- 05
    weeknumber          DOUBLE PRECISION,       -- 06
    moduleid            TEXT,                   -- 07
    modulename          TEXT,                   -- 08
    deptid              TEXT,                   -- 09
    deptname            TEXT,                   -- 10
    lecturerid          TEXT,                   -- 11
    lecturername        TEXT,                   -- 12
    lecturerdeptid      TEXT,                   -- 13
    lecturerdeptname    TEXT,                   -- 14
    lecturereppn        TEXT,                   -- 15
    title               VARCHAR,                -- 16
    sessiontypeid       TEXT,                   -- 17
    condisplayname      TEXT,                   -- 18
    modgrpcode          TEXT,                   -- 19
    instcode            TEXT,                   -- 20
    siteid              TEXT,                   -- 21
    roomid              TEXT,                   -- 22
    sitename            TEXT,                   -- 23
    roomname            TEXT,                   -- 24
    roomcapacity        BIGINT,                 -- 25
    roomtype            TEXT,                   -- 26
    roomclassification  TEXT,                   -- 27
    siteaddr1           TEXT,                   -- 28
    siteaddr2           TEXT,                   -- 29
    siteaddr3           TEXT,                   -- 30
    siteaddr4           TEXT,                   -- 31
    bookabletype        TEXT,                   -- 32
    starttime           VARCHAR,                -- 33
    finishtime          VARCHAR,                -- 34
    descrip             VARCHAR                 -- 35
)
LANGUAGE plpgsql
AS $$
DECLARE

-- Bucket table names
    bt_rb_booking       TEXT;
    bt_tt_cminstances   TEXT;
    bt_tt_course        TEXT;
    bt_tt_depts         TEXT;
    bt_tt_lecturer      TEXT;
    bt_tt_module        TEXT;
    bt_tt_modulegroups  TEXT;
    bt_rb_room         TEXT;
    bt_tt_sites         TEXT;
    bt_tt_stuclasses    TEXT;
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

-- Check the bucket ID in lower case
    bucket := LOWER(bucket)

-- Generate Table Names

    -- This is all extremely ugly but there isn't really an alternative that
    -- can make this function any more generalised.
    -- It will work without matching buckets, however.

    bt_rb_booking       := 'roombookings_booking'   || bucket;
    bt_rb_room          := 'roombookings_room'      || bucket;

    bt_tt_cminstances   := 'timetable_cminstances'  || bucket;
    bt_tt_course        := 'timetable_course'       || bucket;
    bt_tt_depts         := 'timetable_depts'        || bucket;
    bt_tt_lecturer      := 'timetable_lecturer'     || bucket;
    bt_tt_module        := 'timetable_module'       || bucket;
    bt_tt_modulegroups  := 'timetable_modulegroups' || bucket;
    bt_tt_sites         := 'timetable_sites'        || bucket;
    bt_tt_stuclasses    := 'timetable_stuclasses'   || bucket;
    bt_tt_students      := 'timetable_students'     || bucket;
    bt_tt_stumodules    := 'timetable_stumodules'   || bucket;
    bt_tt_timetable     := 'timetable_timetable'    || bucket;

-- Drop any stale temporary tables that already exist
    DROP TABLE IF EXISTS tt_tmp_hasgroupnum;
    DROP TABLE IF EXISTS tt_tmp_taking;
    DROP TABLE IF EXISTS tt_tmp_events_slot_id;
    DROP TABLE IF EXISTS tt_tmp_timetable_events;

-- Get basic information about the student
    
    IF tt_bucket = 'a' THEN

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

IF tt_bucket = 'a' THEN
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

ELSE

    CREATE TEMP TABLE tt_tmp_hasgroupnum (
        groupnum,
        moduleid,
        instid,
        instcode
    )
    AS
    SELECT mg.groupnum, mg.moduleid, ci.instid, ci.instcode
    FROM timetable_stumodulesb sm
    JOIN timetable_modulegroupsb mg
        ON (
            sm.moduleid = mg.moduleid
            AND sm.modgrpcode = mg.grpcode
        )
    LEFT OUTER JOIN timetable_cminstancesb ci
         ON sm.instid = ci.instid
        AND sm.setid = set_id
        AND ci.setid = set_id
    WHERE sm.studentid = student_id
    AND sm.setid = mg.setid
    AND sm.setid = set_id
    AND sm.modgrpcode IS NOT NULL;

END IF;

-- Modules the student is taking
IF tt_bucket = 'a' THEN

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
            );

ELSE

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
        FROM timetable_stumodulesb sm
        JOIN timetable_modulegroupsb mg
            ON sm.moduleid = mg.moduleid
        LEFT OUTER JOIN timetable_cminstancesb ci
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
    FROM timetable_stumodulesb sm2
    LEFT OUTER JOIN timetable_cminstancesb ci
        ON sm2.instid = ci.instid
       AND sm2.setid = ci.setid
       AND ci.setid = set_id
    WHERE sm2.studentid = student_id
      AND sm2.setid = set_id
    ) smUnion
        LEFT OUTER JOIN timetable_stumodulesb usm
            ON (
                smUnion.setid = usm.setid
                AND smUnion.studentid = usm.studentid
                AND smUnion.moduleid = usm.moduleid
                AND smUnion.instid = usm.instid
            );

END IF;

IF tt_bucket = 'a' THEN

    CREATE TEMP TABLE tt_tmp_events_slot_id (
        slotid,          -- tt.slotid     | tt.slotid
        moduleid,        -- NULL          | tt.moduleid
        modgrpcode,      -- NULL          | tt.modgrpcode
        setid,           -- tt.setid      | tt.setid
        stumodselstatus, -- NULL          | st.stumodselstatus
        unfitted,        -- N             | st.unfitted
        compos_crit,     -- NO_MOD        | MOD
        instid,          -- ci.instid     | ci.instid
        instcode,        -- ci.instcode   | ci.instcode
        siteid,          -- tt.siteid     | tt.siteid
        roomid           -- tt.roomid     | tt.roomid
    )
    AS
        SELECT tt.slotid   :: BIGINT,
               NULL        :: TEXT,
               NULL        :: TEXT,
               tt.setid    :: TEXT,
               NULL        :: TEXT,
               'N'         :: TEXT,
               'NO_MOD'    :: TEXT,
               ci.instid   :: TEXT,
               ci.instcode :: TEXT,
               tt.siteid   :: TEXT,
               tt.roomid   :: TEXT
        FROM timetable_timetablea tt
        LEFT OUTER JOIN timetable_cminstancesa ci
             ON tt.instid = ci.instid
            AND tt.setid  = ci.setid
            AND ci.setid  = set_id
        WHERE tt.setid = set_id
            AND tt.weekday BETWEEN 1 and 7
            AND tt.starttime  IS NOT NULL
            AND tt.finishtime IS NOT NULL
            AND
            (
                (
                    (
                        tt.courseid,
                        tt.courseyear,
                        tt.classgroupid,
                        COALESCE(tt.clsgrpcode, '[|X|]')
                    )
                    IN
                    (
                        SELECT courseid,
                            courseyear,
                            classgroupid,
                            COALESCE(clsgrpcode, '[|X|]') clsgrpcode
                        FROM timetable_stuclassesa
                        WHERE setid = set_id
                        AND studentid = student_id
                    )
                )
                OR
                (
                    tt.courseid = st_course_id
                    AND tt.classgroupid IS NULL
                    AND tt.courseyear:: TEXT IN (st_course_year :: TEXT, '-1', '0')
                )
                OR
                (
                    tt.courseid = st_course_id -- NB: this was co_course_id!
                    AND tt.classgroupid IS NULL
                    AND tt.courseyear :: TEXT IN (co_course_year :: TEXT, '-1', '0', overall_year :: TEXT)
                )
            )
    UNION
        SELECT tt.slotid            :: BIGINT,
               tt.moduleid          :: TEXT,
               tt.modgrpcode        :: TEXT, 
               tt.setid             :: TEXT,
               st.stumodselstatus   :: TEXT,
               st.unfitted          :: TEXT,
               'MOD'                :: TEXT,
               ci.instid            :: TEXT,
               ci.instcode          :: TEXT,
               tt.siteid            :: TEXT,
               tt.roomid            :: TEXT
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
                AND st.instid = tt.instid
                -- THIS IS A HACK TO FIX THE DUPLICATION BUG
                -- TODO: confirm that this is the correct solution
            )
        LEFT OUTER JOIN timetable_cminstancesa ci
            ON tt.instid = ci.instid
           AND tt.setid  = ci.setid
           AND ci.setid  = set_id;

ELSE

    CREATE TEMP TABLE tt_tmp_events_slot_id (
        slotid,          -- tt.slotid     | tt.slotid
        moduleid,        -- NULL          | tt.moduleid
        modgrpcode,      -- NULL          | tt.modgrpcode
        setid,           -- tt.setid      | tt.setid
        stumodselstatus, -- NULL          | st.stumodselstatus
        unfitted,        -- N             | st.unfitted
        compos_crit,     -- NO_MOD        | MOD
        instid,          -- ci.instid     | ci.instid
        instcode,        -- ci.instcode   | ci.instcode
        siteid,          -- tt.siteid     | tt.siteid
        roomid           -- tt.roomid     | tt.roomid
    )
    AS
        SELECT tt.slotid   :: BIGINT,
               NULL        :: TEXT,
               NULL        :: TEXT,
               tt.setid    :: TEXT,
               NULL        :: TEXT,
               'N'         :: TEXT,
               'NO_MOD'    :: TEXT,
               ci.instid   :: TEXT,
               ci.instcode :: TEXT,
               tt.siteid   :: TEXT,
               tt.roomid   :: TEXT
        FROM timetable_timetableb tt
        LEFT OUTER JOIN timetable_cminstancesb ci
             ON tt.instid = ci.instid
            AND tt.setid  = ci.setid
            AND ci.setid  = set_id
        WHERE tt.setid = set_id
            AND tt.weekday BETWEEN 1 and 7
            AND tt.starttime  IS NOT NULL
            AND tt.finishtime IS NOT NULL
            AND
            (
                (
                    (
                        tt.courseid,
                        tt.courseyear,
                        tt.classgroupid,
                        COALESCE(tt.clsgrpcode, '[|X|]')
                    )
                    IN
                    (
                        SELECT courseid,
                            courseyear,
                            classgroupid,
                            COALESCE(clsgrpcode, '[|X|]') clsgrpcode
                        FROM timetable_stuclassesb
                        WHERE setid = set_id
                        AND studentid = student_id
                    )
                )
                OR
                (
                    tt.courseid = st_course_id
                    AND tt.classgroupid IS NULL
                    AND tt.courseyear:: TEXT IN (st_course_year :: TEXT, '-1', '0')
                )
                OR
                (
                    tt.courseid = st_course_id -- NB: this was co_course_id!
                    AND tt.classgroupid IS NULL
                    AND tt.courseyear :: TEXT IN (co_course_year :: TEXT, '-1', '0', overall_year :: TEXT)
                )
            )
    UNION
        SELECT tt.slotid            :: BIGINT,
               tt.moduleid          :: TEXT,
               tt.modgrpcode        :: TEXT, 
               tt.setid             :: TEXT,
               st.stumodselstatus   :: TEXT,
               st.unfitted          :: TEXT,
               'MOD'                :: TEXT,
               ci.instid            :: TEXT,
               ci.instcode          :: TEXT,
               tt.siteid            :: TEXT,
               tt.roomid            :: TEXT
        FROM timetable_timetableb tt
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
                AND st.instid = tt.instid
                -- THIS IS A HACK TO FIX THE DUPLICATION BUG
                -- TODO: confirm that this is the correct solution
            )
        LEFT OUTER JOIN timetable_cminstancesb ci
            ON tt.instid = ci.instid
           AND tt.setid  = ci.setid
           AND ci.setid  = set_id;

END IF;

IF tt_bucket = 'a' THEN

    CREATE TEMP TABLE tt_tmp_timetable_events
    AS
    SELECT rb.startdatetime     as startdatetime,
           rb.finishdatetime    as finishdatetime,
           tt.duration          as duration,
           tes.slotid           as slotid,
           tt.weekid            as weekid,
           rb.weeknumber        as weeknumber,
           tes.moduleid         as moduleid,
           m.name               as modulename,
           tt.deptid            as deptid,
           depts.name           as deptname,
           tt.lecturerid        as lecturerid,
           lecturer.name        as lecturername,
           lecturer.owner       as lecturerdeptid,
           (
               SELECT name
               FROM timetable_deptsa
               WHERE deptid = lecturer.owner
           )                    as lecturerdeptname,
           lecturer.linkcode    as lecturereppn,
           rb.title             as title, 
           tt.moduletype        as sessiontypeid,
    --     rb.condisplayname    as condisplayname,
           string_agg(DISTINCT rb.condisplayname, ' / ') as condisplayname,
           tes.modgrpcode       as modgrpcode,
           tes.instcode         as instcode,
           tt.siteid            as siteid,
           tt.roomid            as roomid,
           sites.sitename       as sitename,
           rooms.name           as roomname,
           rooms.capacity       as roomcapacity,
           rooms.type           as roomtype,
           rooms.classification as roomclassification,
           sites.address1       as siteaddr1,
           sites.address2       as siteaddr2,
           sites.address3       as siteaddr3,
           sites.address4       as siteaddr4,
           rooms.type           as bookabletype,
           rb.starttime         as starttime,
           rb.finishtime        as finishtime,
           rb.descrip           as descrip

    FROM timetable_timetablea tt
    INNER JOIN tt_tmp_events_slot_id tes
        ON tt.slotid = tes.slotid
       AND tt.slotid = tes.slotid
    LEFT OUTER JOIN roombookings_bookinga rb
        ON tt.slotid = rb.slotid
       AND tt.setid  = rb.setid
    LEFT OUTER JOIN timetable_cminstancesa ci
        ON tt.instid = ci.instid
       AND tt.setid  = ci.setid 
    LEFT JOIN timetable_modulea m
        ON m.moduleid = tes.moduleid
       AND m.setid    = tes.setid
    LEFT OUTER JOIN timetable_deptsa depts
        ON depts.deptid = tt.deptid
    LEFT OUTER JOIN timetable_lecturera lecturer
        ON lecturer.lecturerid = tt.lecturerid
       AND lecturer.setid      = tes.setid
    LEFT OUTER JOIN timetable_sitesa sites
        ON sites.siteid = tt.siteid
       AND sites.setid  = tes.setid
    LEFT OUTER JOIN roombookings_rooma rooms
        ON rooms.roomid = tt.roomid
       AND rooms.siteid = tt.siteid
       AND rooms.setid  = tes.setid
    WHERE (
            (tt.weekday IS NOT NULL)
        AND (tt.weekday > 0)
        AND (tt.starttime IS NOT NULL)
        AND (tt.duration IS NOT NULL)
        AND (tt.instid = ci.instid)
        AND (ci.instid :: TEXT = tes.instid :: TEXT)
    )
    GROUP BY rb.startdatetime,
             rb.finishdatetime,
             tt.duration,
             tes.slotid,
             tt.weekid,
             rb.weeknumber,
             tes.moduleid,
             m.name,
             tt.deptid,
             depts.name,
             tt.lecturerid,
             lecturer.name,
             lecturer.owner,
             lecturerdeptname,
             lecturer.linkcode,
             rb.title, 
             tt.moduletype,
             tes.modgrpcode,
             tes.instcode,
             tt.siteid,
             tt.roomid,
             sites.sitename,
             rooms.name,
             rooms.capacity,
             rooms.type,
             rooms.classification,
             sites.address1,
             sites.address2,
             sites.address3,
             sites.address4,
             rooms.type,
             rb.starttime,
             rb.finishtime,
             rb.descrip
    ORDER BY startdatetime,
             moduleid,
             title,
             sitename,
             roomname;

ELSE
    CREATE TEMP TABLE tt_tmp_timetable_events
    AS
    SELECT rb.startdatetime     as startdatetime,
           rb.finishdatetime    as finishdatetime,
           tt.duration          as duration,
           tes.slotid           as slotid,
           tt.weekid            as weekid,
           rb.weeknumber        as weeknumber,
           tes.moduleid         as moduleid,
           m.name               as modulename,
           tt.deptid            as deptid,
           depts.name           as deptname,
           tt.lecturerid        as lecturerid,
           lecturer.name        as lecturername,
           lecturer.owner       as lecturerdeptid,
           (
               SELECT name
               FROM timetable_deptsb
               WHERE deptid = lecturer.owner
           )                    as lecturerdeptname,
           lecturer.linkcode    as lecturereppn,
           rb.title             as title, 
           tt.moduletype        as sessiontypeid,
    --     rb.condisplayname    as condisplayname,
           string_agg(DISTINCT rb.condisplayname, ' / ') as condisplayname,
           tes.modgrpcode       as modgrpcode,
           tes.instcode         as instcode,
           tt.siteid            as siteid,
           tt.roomid            as roomid,
           sites.sitename       as sitename,
           rooms.name           as roomname,
           rooms.capacity       as roomcapacity,
           rooms.type           as roomtype,
           rooms.classification as roomclassification,
           sites.address1       as siteaddr1,
           sites.address2       as siteaddr2,
           sites.address3       as siteaddr3,
           sites.address4       as siteaddr4,
           rooms.type           as bookabletype,
           rb.starttime         as starttime,
           rb.finishtime        as finishtime,
           rb.descrip           as descrip

    FROM timetable_timetableb tt
    INNER JOIN tt_tmp_events_slot_id tes
        ON tt.slotid = tes.slotid
       AND tt.slotid = tes.slotid
    LEFT OUTER JOIN roombookings_bookingb rb
        ON tt.slotid = rb.slotid
       AND tt.setid  = rb.setid
    LEFT OUTER JOIN timetable_cminstancesb ci
        ON tt.instid = ci.instid
       AND tt.setid  = ci.setid 
    LEFT JOIN timetable_moduleb m
        ON m.moduleid = tes.moduleid
       AND m.setid    = tes.setid
    LEFT OUTER JOIN timetable_deptsb depts
        ON depts.deptid = tt.deptid
    LEFT OUTER JOIN timetable_lecturerb lecturer
        ON lecturer.lecturerid = tt.lecturerid
       AND lecturer.setid      = tes.setid
    LEFT OUTER JOIN timetable_sitesb sites
        ON sites.siteid = tt.siteid
       AND sites.setid  = tes.setid
    LEFT OUTER JOIN roombookings_roomb rooms
        ON rooms.roomid = tt.roomid
       AND rooms.siteid = tt.siteid
       AND rooms.setid  = tes.setid
    WHERE (
            (tt.weekday IS NOT NULL)
        AND (tt.weekday > 0)
        AND (tt.starttime IS NOT NULL)
        AND (tt.duration IS NOT NULL)
        AND (tt.instid = ci.instid)
        AND (ci.instid :: TEXT = tes.instid :: TEXT)
    )
    GROUP BY rb.startdatetime,
             rb.finishdatetime,
             tt.duration,
             tes.slotid,
             tt.weekid,
             rb.weeknumber,
             tes.moduleid,
             m.name,
             tt.deptid,
             depts.name,
             tt.lecturerid,
             lecturer.name,
             lecturer.owner,
             lecturerdeptname,
             lecturer.linkcode,
             rb.title, 
             tt.moduletype,
             tes.modgrpcode,
             tes.instcode,
             tt.siteid,
             tt.roomid,
             sites.sitename,
             rooms.name,
             rooms.capacity,
             rooms.type,
             rooms.classification,
             sites.address1,
             sites.address2,
             sites.address3,
             sites.address4,
             rooms.type,
             rb.starttime,
             rb.finishtime,
             rb.descrip
    ORDER BY startdatetime,
             moduleid,
             title,
             sitename,
             roomname;

END IF;

-- Return the timetable we just built back to the calling application
    RETURN QUERY SELECT
    DISTINCT ON
    (
        startdatetime,
        finishdatetime,
        slotid,
        weeknumber,
        moduleid,
        modgrpcode
    ) *
    FROM tt_tmp_timetable_events te
    WHERE te.startdatetime IS NOT NULL;

END
$$;
