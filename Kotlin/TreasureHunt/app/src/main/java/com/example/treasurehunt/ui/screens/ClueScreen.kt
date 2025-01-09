/* Assignment 5
* Juanette van Wyk
* vanwykj@oregonstate.edu
* OSU: CS 492
*/

package com.example.treasurehunt.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Info
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.treasurehunt.ui.components.TimeComponent
import com.example.treasurehunt.R
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.draw.blur
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.navigation.NavHostController
import com.example.treasurehunt.ui.viewmodel.TreasureHuntViewModel

@Composable
fun ClueScreen(
    funFactId: Int,
    onFoundItClick: (Int) -> Unit,
    onQuitClick: () -> Unit,
    onFinishClick: (Int) -> Unit,
    viewModel: TreasureHuntViewModel,
    navController: NavHostController
) {
    var isHintVisible by remember { mutableStateOf(false) }
    var isDialogVisible by remember { mutableStateOf(false) }
    var isCheckingLocation by remember { mutableStateOf(false) }

    val clues by viewModel.clues.collectAsState()
    val currentClueIndex by viewModel.currentClueIndex.collectAsState()
    val currentClue = clues.getOrNull(currentClueIndex)

    val context = LocalContext.current
    val imageResId = context.resources.getIdentifier(currentClue?.imageRes, "drawable", context.packageName)

    val elapsedTime by viewModel.elapsedTime.collectAsState()
    val currentLocation by viewModel.currentLocation.collectAsState()

    Box(
        modifier = Modifier
            .fillMaxSize()
    ) {
        // Background content
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(10.dp)
                .blur(
                    radius = if (isDialogVisible) 16.dp else 0.dp
                ),
            verticalArrangement = Arrangement.SpaceBetween,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Title
            Text(
                text = "Your Clue",
                fontSize = 32.sp,
                textAlign = TextAlign.Center,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 24.dp)
            )
            Spacer(
                modifier = Modifier
                    .height(5.dp)
            )

            // Timer at the top
            TimeComponent(elapsedTime = elapsedTime)

            // Image
            Image(
                painter = painterResource(id = imageResId),
                contentDescription = null,
                contentScale = ContentScale.Crop,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(300.dp)
                    .padding(vertical = 8.dp)
                    .clip(RoundedCornerShape(16.dp))
            )

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp)
            ) {
                Text(
                    text = "Clue",
                    textAlign = TextAlign.Left,
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = currentClue?.text ?: "No Clue Available",
                    textAlign = TextAlign.Left,
                    fontSize = 16.sp
                )

                // need a hint?
                if (!isHintVisible) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 16.dp)
                            .clickable { isHintVisible = true }
                    ) {
                        Icon(
                            imageVector = Icons.Rounded.Info,
                            contentDescription = "Hint Icon",
                            modifier = Modifier
                                .size(25.dp)
                        )
                        Spacer(modifier = Modifier.width(5.dp))

                        Text(
                            text = "Do you need a hint?",
                            textAlign = TextAlign.Left,
                            fontSize = 16.sp,
                            color = Color.Gray
                        )
                    }
                }

                // Show the hint if it's visible
                if (isHintVisible) {
                    Text(
                        text = "Hint",
                        textAlign = TextAlign.Left,
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier
                            .padding(top = 8.dp)
                    )
                    Text(
                        text = currentClue?.hint ?: "No Hint Available",
                        textAlign = TextAlign.Left,
                        fontSize = 16.sp
                    )
                }
            }

            // Spacer to push buttons to the bottom
            Spacer(modifier = Modifier.weight(1f))

            // Buttons at the bottom
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Button(
                    onClick = {
                        isCheckingLocation = true
                        currentClue?.let { clue ->
                            viewModel.checkLocationForClue(
                                correctLat = clue.correctLocation[0],
                                correctLon = clue.correctLocation[1]
                            ) { isCorrect ->
                                isCheckingLocation = false
                                if (isCorrect) {
                                    if (viewModel.isLastClue()) {
                                        viewModel.pauseTimer()
                                        onFinishClick(currentClue.funFactId)
                                    } else {
                                        viewModel.pauseTimer()
                                        onFoundItClick(currentClue.funFactId)
                                    }
                                } else {
                                    isDialogVisible = true
                                }
                            }
                        }
                    },
                    enabled = !isCheckingLocation,
                    modifier = Modifier
                        .weight(1f)
                        .padding(end = 8.dp),
                    shape = MaterialTheme.shapes.medium,
                    contentPadding = PaddingValues(16.dp)
                ) {
                    Text(
                        text = "Found It",
                        fontSize = 20.sp
                    )
                }
                Button(
                    onClick = {
                        viewModel.stopTimer()
                        viewModel.resetClueIndex()
                        onQuitClick()
                    },
                    modifier = Modifier
                        .weight(1f)
                        .padding(start = 8.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.secondary
                    ),
                    shape = MaterialTheme.shapes.medium,
                    contentPadding = PaddingValues(16.dp)
                ) {
                    Text(
                        text = "Quit",
                        fontSize = 20.sp
                    )
                }
            }
        }

        // Show dialog if the location is incorrect
        if (isDialogVisible) {
            AlertDialog(
                onDismissRequest = { isDialogVisible = false },
                title = {
                    Text(text = "Wrong Location")
                },
                text = {
                    Text("The location is incorrect. Please try again.")
                },
                confirmButton = {
                    Button(
                        onClick = { isDialogVisible = false },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = MaterialTheme.colorScheme.primary
                        ),
                    ) {
                        Text("Try Again")
                    }
                }
            )
        }
    }
}
