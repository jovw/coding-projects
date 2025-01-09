/* Assignment 5
* Juanette van Wyk
* vanwykj@oregonstate.edu
* OSU: CS 492
*/

package com.example.treasurehunt.ui.screens

import android.content.Context
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import com.example.treasurehunt.ui.components.TimeComponent
import com.example.treasurehunt.R
import com.example.treasurehunt.ui.model.FunFact
import com.example.treasurehunt.ui.model.Rules
import com.example.treasurehunt.ui.viewmodel.TreasureHuntViewModel

@Composable
fun ClueSolvedScreen(
    funFactId: Int,
    onContinueClick: () -> Unit,
    viewModel: TreasureHuntViewModel,
    navController: NavHostController,
) {
    val funFacts by viewModel.funFacts.collectAsState()
    val funFact = funFacts.firstOrNull { it.id == funFactId }

    val context = LocalContext.current
    val imageResId = context.resources.getIdentifier(funFact?.imageRes, "drawable", context.packageName)

    val elapsedTime by viewModel.elapsedTime.collectAsState()

    Box(
        modifier = Modifier
            .fillMaxSize()
    ) {
        // Background content
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(10.dp),
            verticalArrangement = Arrangement.SpaceBetween,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Title
            Text(
                text = "More info about location",
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

            // Scrollable content (Image and Fun Facts)
            Column(
                modifier = Modifier
                    .weight(1f)
                    .verticalScroll(rememberScrollState())
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp)
            ) {
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

                Spacer(modifier = Modifier.height(8.dp))

                // Fun Facts
                Text(
                    text = "Fun Facts",
                    textAlign = TextAlign.Left,
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = funFact?.description ?: "No Fun Fact Available",
                    textAlign = TextAlign.Left,
                    fontSize = 16.sp
                )
            }

            // Continue button at the bottom
            Button(
                onClick = {
                    viewModel.moveToNextClue()
                    viewModel.startTimer()
                    navController.navigate("clue")
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 16.dp),
                shape = MaterialTheme.shapes.medium,
                contentPadding = PaddingValues(16.dp)
            ) {
                Text(
                    text = "Continue",
                    fontSize = 20.sp
                )
            }
        }
    }
}