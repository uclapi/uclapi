CREATE OR REPLACE FUNCTION get_student_timetable_{{ bucket_id | sqlsafe }} (
    upi         TEXT, -- UPI
    set_id      TEXT  -- Set ID
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
    sessiontypestr      VARCHAR,                -- 18
    condisplayname      TEXT,                   -- 19
    modgrpcode          TEXT,                   -- 20
    instcode            TEXT,                   -- 21
    siteid              TEXT,                   -- 22
    roomid              TEXT,                   -- 23
    sitename            TEXT,                   -- 24
    roomname            VARCHAR,                -- 25
    roomcapacity        DOUBLE PRECISION,       -- 26
    roomtype            VARCHAR,                -- 27
    roomclassification  VARCHAR,                -- 28
    siteaddr1           TEXT,                   -- 29
    siteaddr2           TEXT,                   -- 30
    siteaddr3           TEXT,                   -- 31
    siteaddr4           TEXT,                   -- 32
    starttime           VARCHAR,                -- 33
    finishtime          VARCHAR,                -- 34
    descrip             VARCHAR                 -- 35
)
LANGUAGE plpgsql
AS $$
DECLARE

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

-- Drop any stale temporary tables that already exist
    DROP TABLE IF EXISTS tt_tmp_hasgroupnum; -- Not necessary now!
    DROP TABLE IF EXISTS tt_tmp_taking;
    DROP TABLE IF EXISTS tt_tmp_events_slot_id;
    DROP TABLE IF EXISTS tt_tmp_timetable_events;

-- Get basic information about the student

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
    FROM   timetable_students{{ bucket_id | sqlsafe }} s
    -- LEFT OUTER JOIN timetable_course{{ bucket_id | sqlsafe }} c
    --     ON (c.setid = s.setid AND c.linkcode = s.linkcode)
    WHERE  s.qtype2 = upi AND s.setid = set_id;

-- List of all groups the person is in. At least one group per module.
-- There are multiple entries for each module. One for every way the whole class
-- of students taking the module can be split. There will be an entry for each
-- module group (can be 0) plus a NULL grpcode if everyone taking the module has
-- a timetabled event where they are all present (usually a lecture).
CREATE TEMP TABLE tt_tmp_taking (
    moduleid,
    grpcode,
    stumodselstatus,
    unfitted,
    instid,
    instcode
)
AS
-- Get entries where students are split into groups.
SELECT sm.moduleid, sm.modgrpcode, 'Y', sm.fixingrp, ci.instid, ci.instcode
FROM timetable_stumodules{{ bucket_id | sqlsafe }} sm
JOIN timetable_modulegroups{{ bucket_id | sqlsafe }} mg
    ON sm.moduleid = mg.moduleid
    AND sm.modgrpcode = mg.grpcode
    AND sm.instid = mg.instid
    AND sm.setid = mg.setid
    AND mg.setid = set_id
LEFT OUTER JOIN timetable_cminstances{{ bucket_id | sqlsafe }} ci
    ON sm.instid = ci.instid
    AND sm.setid = ci.setid
    AND ci.setid = set_id
WHERE sm.studentid = student_id
AND sm.setid = mg.setid
AND sm.setid = set_id
UNION
-- Get students where all students are present (i.e. modgrpode IS NULL)
SELECT sm.moduleid, sm.modgrpcode, 'Y', sm.fixingrp, ci.instid, ci.instcode
FROM timetable_stumodules{{ bucket_id | sqlsafe }} sm
LEFT OUTER JOIN timetable_cminstances{{ bucket_id | sqlsafe }} ci
    ON sm.instid = ci.instid
    AND sm.setid = ci.setid
    AND ci.setid = set_id
WHERE sm.studentid = student_id
AND sm.setid = set_id
AND sm.modgrpcode IS NULL;

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
    FROM timetable_timetable{{ bucket_id | sqlsafe }} tt
    -- Join to get instance info.
    LEFT OUTER JOIN timetable_cminstances{{ bucket_id | sqlsafe }} ci
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
                    FROM timetable_stuclasses{{ bucket_id | sqlsafe }}
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
    FROM timetable_timetable{{ bucket_id | sqlsafe }} tt
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
    LEFT OUTER JOIN timetable_cminstances{{ bucket_id | sqlsafe }} ci
        ON tt.instid = ci.instid
        AND tt.setid  = ci.setid
        AND ci.setid  = set_id;


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
           FROM timetable_depts{{ bucket_id | sqlsafe }} de
           WHERE de.deptid = lecturer.owner
       )                    as lecturerdeptname,
       lecturer.linkcode    as lecturereppn,
       rb.title             as title, 
       tt.moduletype        as sessiontypeid,
       classifications.name as sessiontypestr,
--     rb.condisplayname    as condisplayname,
       string_agg(DISTINCT rb.condisplayname, ' / ') as condisplayname,
       tes.modgrpcode       as modgrpcode,
       tes.instcode         as instcode,
       tt.siteid            as siteid,
       tt.roomid            as roomid,
       sites.sitename       as sitename,
       rooms.roomname       as roomname,
       rooms.capacity       as roomcapacity,
       rooms.bookabletype   as roomtype,
       rooms.roomclass      as roomclassification,
       sites.address1       as siteaddr1,
       sites.address2       as siteaddr2,
       sites.address3       as siteaddr3,
       sites.address4       as siteaddr4,
       rb.starttime         as starttime,
       rb.finishtime        as finishtime,
       rb.descrip           as descrip

FROM timetable_timetable{{ bucket_id | sqlsafe }} tt
INNER JOIN tt_tmp_events_slot_id tes
    ON tt.slotid = tes.slotid
    AND tt.slotid = tes.slotid
LEFT OUTER JOIN roombookings_booking{{ bucket_id | sqlsafe }} rb
    ON tt.slotid = rb.slotid
    AND tt.setid  = rb.setid
LEFT OUTER JOIN timetable_cminstances{{ bucket_id | sqlsafe }} ci
    ON tt.instid = ci.instid
    AND tt.setid  = ci.setid 
LEFT JOIN timetable_module{{ bucket_id | sqlsafe }} m
    ON m.moduleid = tes.moduleid
    AND m.setid    = tes.setid
LEFT OUTER JOIN timetable_depts{{ bucket_id | sqlsafe }} depts
    ON depts.deptid = tt.deptid
LEFT OUTER JOIN timetable_lecturer{{ bucket_id | sqlsafe }} lecturer
    ON lecturer.lecturerid = tt.lecturerid
    AND lecturer.setid      = tes.setid
LEFT OUTER JOIN timetable_sites{{ bucket_id | sqlsafe }} sites
    ON sites.siteid = tt.siteid
    AND sites.setid  = tes.setid
LEFT OUTER JOIN roombookings_room{{ bucket_id | sqlsafe }} rooms
    ON rooms.roomid = tt.roomid
    AND rooms.siteid = tt.siteid
    AND rooms.setid  = tes.setid
-- This provides a mapping between a session type and its human readable string.
-- e.g. LAB -> Labaratory Session; T -> Tutorial; L -> Lecture;
LEFT OUTER JOIN timetable_classifications{{ bucket_id | sqlsafe }} classifications
    ON tt.moduletype = classifications.classid
    AND tt.setid = classifications.setid
    AND classifications.type = 'MOD_TYPE'
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
            rooms.roomname,
            rooms.capacity,
            rooms.bookabletype,
            rooms.roomclass,
            sites.address1,
            sites.address2,
            sites.address3,
            sites.address4,
            rb.starttime,
            rb.finishtime,
            rb.descrip,
            classifications.name
ORDER BY startdatetime,
            moduleid,
            title,
            sitename,
            roomname;

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
