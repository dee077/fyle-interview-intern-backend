-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

-- Step 1: Identify the teacher who has graded the most assignments
WITH teacher_grades_count AS (
    SELECT 
        teacher_id, 
        COUNT(*) AS total_graded
    FROM 
        assignments
    WHERE 
        state = 'GRADED'
    GROUP BY 
        teacher_id
),

-- Step 2: Get the teacher_id of the teacher who graded the most assignments
most_grading_teacher AS (
    SELECT 
        teacher_id
    FROM 
        teacher_grades_count
    ORDER BY 
        total_graded DESC
    LIMIT 1
)

-- Step 3: Count the number of grade A's given by that teacher
SELECT 
    COUNT(*) AS grade_a_count
FROM 
    assignments
WHERE 
    teacher_id = (SELECT teacher_id FROM most_grading_teacher)
    AND grade = 'A';
