/* Assignment 5
* Juanette van Wyk
* vanwykj@oregonstate.edu
* OSU: CS 492
*/

package com.example.treasurehunt

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext
import androidx.core.content.ContextCompat
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.treasurehunt.ui.screens.ClueScreen
import com.example.treasurehunt.ui.screens.ClueSolvedScreen
import com.example.treasurehunt.ui.screens.PermissionScreen
import com.example.treasurehunt.ui.screens.StartScreen
import com.example.treasurehunt.ui.screens.TreasureHuntCompleteScreen
import com.example.treasurehunt.ui.theme.TreasureHuntTheme
import com.example.treasurehunt.ui.viewmodel.TreasureHuntViewModel
import com.example.treasurehunt.ui.viewmodel.TreasureHuntViewModelFactory
import java.lang.reflect.Modifier
import androidx.compose.foundation.layout.fillMaxSize

class MainActivity : ComponentActivity() {

    private val viewModel: TreasureHuntViewModel by viewModels {
        TreasureHuntViewModelFactory(applicationContext)
    }

    private var navController: NavHostController? = null

    // permission request callback
    private val requestPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { permissions ->
            val fineLocationGranted = permissions[Manifest.permission.ACCESS_FINE_LOCATION] ?: false
            val coarseLocationGranted = permissions[Manifest.permission.ACCESS_COARSE_LOCATION] ?: false

            if (fineLocationGranted || coarseLocationGranted) {
                // Use navController safely
                navController?.let {
                    navigateToStartScreen(it)
                }
            } else {
                // Handle permission denied case
            }
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            navController = rememberNavController()

            TreasureHuntTheme {
                TreasureHuntApp(
                    navController = navController!!,
                    viewModel = viewModel,
                    requestPermission = {
                        checkAndRequestPermissions(navController!!)
                    }
                )
            }
        }
    }

    private fun checkAndRequestPermissions(navController: NavHostController) {
        when {
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) == PackageManager.PERMISSION_GRANTED -> {
                println("Location permission granted")
                navigateToStartScreen(navController)
            }
            else -> {
                println("Requesting location permission")
                requestPermissionLauncher.launch(
                    arrayOf(
                        Manifest.permission.ACCESS_FINE_LOCATION,
                        Manifest.permission.ACCESS_COARSE_LOCATION
                    )
                )
            }
        }
    }

    // Function to navigate to the StartScreen
    private fun navigateToStartScreen(navController: NavHostController) {
        navController.navigate("start") {
            popUpTo("permission") { inclusive = true } // Clear back stack so user can't go back to PermissionScreen
        }
    }
}


@Composable
fun TreasureHuntApp(
    navController: NavHostController,
    viewModel: TreasureHuntViewModel,
    requestPermission: () -> Unit
) {
    // Surface to set the background color for all screens
    Surface(
//        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.surface
    ) {
        // Check if location permissions are granted
        val startDestination = if (ContextCompat.checkSelfPermission(
                LocalContext.current,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) == PackageManager.PERMISSION_GRANTED
        ) {
            "start"
        } else {
            "permission"
        }

        NavHost(navController = navController, startDestination = startDestination) {
            composable("permission") {
                PermissionScreen(
                    viewModel = viewModel,
                    onSetPermissionClick = requestPermission
                )
            }

            composable("start") {
                StartScreen(
                    viewModel = viewModel,
                    onStartClick = {
                        navController.navigate("clue")
                    }
                )
            }

            composable("clue") { backStackEntry ->
                val funFactId = backStackEntry.arguments?.getString("funFactId")?.toInt() ?: -1
                ClueScreen(
                    onFoundItClick = { funFactId ->
                        navController.navigate("clueSolved/$funFactId")
                    },
                    onQuitClick = {
                        navController.navigate("start")
                    },
                    onFinishClick = { funFactId ->
                        navController.navigate("treasureHuntCompleted/$funFactId")
                    },
                    viewModel = viewModel,
                    funFactId = funFactId,
                    navController = navController
                )
            }

            composable("clueSolved/{funFactId}") { backStackEntry ->
                val funFactId = backStackEntry.arguments?.getString("funFactId")?.toInt() ?: -1
                ClueSolvedScreen(
                    funFactId = funFactId,
                    onContinueClick = { /* Handle continue click */ },
                    viewModel = viewModel,
                    navController = navController
                )
            }

            composable("treasureHuntCompleted/{funFactId}") { backStackEntry ->
                val funFactId = backStackEntry.arguments?.getString("funFactId")?.toInt() ?: -1
                TreasureHuntCompleteScreen(
                    funFactId = funFactId,
                    viewModel = viewModel,
                    onHomeClick = { navController.navigate("start") }
                )
            }
        }
    }
}
