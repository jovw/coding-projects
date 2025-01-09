package com.example.courselist

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.asPaddingValues
import androidx.compose.foundation.layout.calculateEndPadding
import androidx.compose.foundation.layout.calculateStartPadding
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.res.integerResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.courselist.data.Datasource
import com.example.courselist.model.Course
import com.example.courselist.ui.theme.CourseListTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            CourseListTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                ) {
                    CourseListApp()
                }
            }
        }
    }
}

@Composable
fun CourseListApp() {
    val layoutDirection = LocalLayoutDirection.current
    Surface(
        modifier = Modifier
            .fillMaxSize()
            .statusBarsPadding()
            .padding(
                start = WindowInsets.safeDrawing
                    .asPaddingValues()
                    .calculateStartPadding(layoutDirection),
                end = WindowInsets.safeDrawing
                    .asPaddingValues()
                    .calculateEndPadding(layoutDirection),
            ),
    ) {
        CourseList(
            courseList = Datasource().loadCourses(),
        )
    }
}


@Composable
fun CourseListCard(
    course: Course,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
    ) {
        Column(
            modifier = Modifier
                .padding(8.dp)
        ) {
            Text(
                text = "${course.department} ${course.number}",
                fontWeight = FontWeight.Bold
            )
            Text(
                text = stringResource(course.stringResourceId)
            )
            Text(
                text = "Capacity: ${course.capacity}"
            )
        }
    }
}

@Composable
fun CourseList(
    courseList: List<Course>,
    modifier: Modifier = Modifier
) {
    LazyColumn(modifier = modifier) {
        items(courseList) { course ->
            CourseListCard(
                course = course,
                modifier = Modifier
                    .padding(8.dp)
            )
        }
    }
}

@Preview(showBackground = true)
@Composable
fun CourseListPreview() {
    CourseListCard(Course( R.string.course_161_title, "Cs", 150, 100 ))
}