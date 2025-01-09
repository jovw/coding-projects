/* Assignment 4
* Juanette van Wyk
* vanwykj@oregonstate.edu
* OSU: CS 492
*/
package com.example.cityreccomendations

import android.os.Bundle
import android.view.View
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.NavHostController
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.clickable
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.Divider
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.getValue
import androidx.compose.runtime.livedata.observeAsState
import androidx.compose.ui.Alignment
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.cityreccomendations.data.Datasource
import com.example.cityreccomendations.model.Category
import com.example.cityreccomendations.model.Recommendation
import com.example.cityreccomendations.ui.theme.CityReccomendationsTheme
import com.example.cityreccomendations.ui.theme.CityViewModel


class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            CityReccomendationsTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                ) {
                    CityRecApp()
                }
            }
        }
    }
}

@Composable
fun CityRecApp() {
    val navController = rememberNavController()
    NavHost(navController, startDestination = "categories") {
        composable("categories") { CategoryListScreen(navController) }
        composable("recommendations/{categoryName}") { backStackEntry ->
            val categoryName = backStackEntry.arguments?.getString("categoryName")
            categoryName?.let { RecommendationsScreen(navController, it) }
        }
        composable("details/{recommendationName}") { backStackEntry ->
            val recommendationName = backStackEntry.arguments?.getString("recommendationName")
            recommendationName?.let { RecommendationDetailsScreen(it, navController = navController) }
        }
    }
}

@Composable
fun CustomAppBar(title: String, navController: NavHostController, showBackButton: Boolean = false) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(85.dp)
            .background(MaterialTheme.colorScheme.primary)
            .padding(horizontal = 16.dp)
            .padding(top = 40.dp),
        contentAlignment = Alignment.Center
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            if (showBackButton) {
                IconButton(onClick = { navController.navigateUp() }) {
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                        contentDescription = "Back",
                        tint = MaterialTheme.colorScheme.onPrimary
                    )
                }
            }
            Text(
                text = title,
                fontSize = 25.sp,
                color = MaterialTheme.colorScheme.onPrimary,
                modifier = Modifier.padding(start = if (showBackButton) 8.dp else 0.dp)
            )
        }
    }
}

@Composable
fun CategoryListScreen(navController: NavHostController, viewModel: CityViewModel = viewModel()) {
    val categories by viewModel.categories.observeAsState(emptyList())
    Scaffold(
        topBar = { CustomAppBar(title = "Seattle", navController = navController) }
    ) { innerPadding ->
        LazyColumn(
            contentPadding = innerPadding,
            modifier = Modifier
                .padding(top = 16.dp)
        ) {
            items(categories) { category ->
                Column {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 16.dp)
                            .clickable {
                                navController.navigate("recommendations/${category.name}")
                            }
                    ) {
                        Image(
                            painter = painterResource(id = category.imageResId),
                            contentDescription = null,
                            modifier = Modifier
                                .height(80.dp)
                                .width(140.dp)
                                .padding(end = 16.dp),
                            contentScale = ContentScale.Crop
                        )
                        Text(
                            text = category.name,
                            style = MaterialTheme.typography.titleMedium,
                            fontSize = 18.sp,
                            modifier = Modifier.align(Alignment.CenterVertically)
                        )
                    }
                    HorizontalDivider(
                        modifier = Modifier.padding(vertical = 8.dp),
                        thickness = 1.dp,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.08f)
                    )
                }
            }
        }
    }
}

@Composable
fun RecommendationsScreen(navController: NavHostController, categoryName: String, viewModel: CityViewModel = viewModel()) {
    val categories by viewModel.categories.observeAsState(emptyList())
    val category = categories.find { it.name == categoryName }
    Scaffold(
        topBar = { CustomAppBar(title = categoryName, navController = navController, showBackButton = true) }
    ) { innerPadding ->
        LazyColumn(
            contentPadding = innerPadding,
            modifier = Modifier
                .padding(top = 16.dp)
                .padding(horizontal = 16.dp)
        ) {
            category?.recommendations?.let { recommendations ->
                items(recommendations) { recommendation ->
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { navController.navigate("details/${recommendation.name}") }
                    ) {
                        Text(
                            text = recommendation.name,
                            style = MaterialTheme.typography.titleMedium,
                            fontSize = 18.sp,
                            modifier = Modifier.padding(vertical = 16.dp)
                        )
                        HorizontalDivider(
                            modifier = Modifier.padding(vertical = 8.dp),
                            thickness = 1.dp,
                            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.08f)
                        )
                    }
                }
            }
        }
    }
}




@Composable
fun RecommendationDetailsScreen(recommendationName: String, navController: NavHostController, viewModel: CityViewModel = viewModel()) {
    val categories by viewModel.categories.observeAsState(emptyList())
    val recommendation = categories.flatMap { it.recommendations }
        .find { it.name == recommendationName }

    recommendation?.let {
        Scaffold(
            topBar = { CustomAppBar(title = it.name, navController = navController, showBackButton = true) }
        ) { innerPadding ->
            Column(
                modifier = Modifier
                    .padding(innerPadding)
                    .padding(16.dp)
            ) {
                Image(
                    painter = painterResource(id = it.imageUrl),
                    contentDescription = null,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(400.dp),
                    contentScale = ContentScale.Crop
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Address",
                    fontSize = 14.sp,
                    color = Color.Gray
                )
                Text(it.address)
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "Description",
                    fontSize = 14.sp,
                    color = Color.Gray
                )
                Text(it.description)
            }
        }
    }
}