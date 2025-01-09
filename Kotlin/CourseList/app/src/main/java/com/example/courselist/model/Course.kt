package com.example.courselist.model

import androidx.annotation.StringRes

data class Course (
    @StringRes val stringResourceId: Int,
    val department: String,
    val number: Int,
    val capacity: Int
)