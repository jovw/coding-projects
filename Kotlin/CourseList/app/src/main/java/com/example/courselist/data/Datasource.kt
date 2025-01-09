package com.example.courselist.data

import com.example.courselist.R
import com.example.courselist.model.Course

class Datasource {
    fun loadCourses(): List<Course> {
        return listOf(
            Course(R.string.assignment_3, "Assignment", 3, 1 ),
            Course(R.string.course_161_title, "CS", 161, 100),
            Course(R.string.course_162_title, "CS", 162, 100),
            Course(R.string.course_225_title, "CS", 225, 200),
            Course(R.string.course_261_title, "CS", 261, 200),
            Course(R.string.course_271_title, "CS", 271, 200),
            Course(R.string.course_290_title, "CS", 290, 200),
            Course(R.string.course_325_title, "CS", 325, 300),
            Course(R.string.course_340_title, "CS", 340, 300),
            Course(R.string.course_344_title, "CS", 344, 300),
            Course(R.string.course_361_title, "CS", 361, 300),
            Course(R.string.course_362_title, "CS", 362, 300),
            Course(R.string.course_467_title, "CS", 467, 400)
        )
    }
}
