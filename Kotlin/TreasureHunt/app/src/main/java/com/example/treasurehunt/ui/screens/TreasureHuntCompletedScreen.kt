/* Assignment 5
* Juanette van Wyk
* vanwykj@oregonstate.edu
* OSU: CS 492
*/

package com.example.treasurehunt.ui.screens

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
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.treasurehunt.ui.theme.TreasureHuntTheme
import com.example.treasurehunt.ui.components.TimeComponent
import com.example.treasurehunt.R
import com.example.treasurehunt.ui.viewmodel.TreasureHuntViewModel

@Composable
fun TreasureHuntCompleteScreen(
    funFactId: Int,
    viewModel: TreasureHuntViewModel,
    onHomeClick: () -> Unit
) {
    val funFacts by viewModel.funFacts.collectAsState()
    val funFact = funFacts.firstOrNull { it.id == funFactId }

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
                text = "You Won!",
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
                    painter = painterResource(id = R.drawable.you_won),
                    contentDescription = null,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(300.dp)
                        .padding(vertical = 8.dp)
                        .clip(RoundedCornerShape(16.dp))
                )

                Text(
                    text = "Congratulations! You've found the treasure at ${funFact?.locationName ?: "the final location"}!",
                    fontSize = 25.sp,
                    textAlign = TextAlign.Center,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 16.dp)
                )
                Spacer(
                    modifier = Modifier
                        .height(16.dp)
                )

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
                    onHomeClick()
                    viewModel.stopTimer()
                    viewModel.resetClueIndex()
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 16.dp),
                shape = MaterialTheme.shapes.medium,
                contentPadding = PaddingValues(16.dp)
            ) {
                Text(
                    text = "Home",
                    fontSize = 20.sp
                )
            }
        }
    }
}