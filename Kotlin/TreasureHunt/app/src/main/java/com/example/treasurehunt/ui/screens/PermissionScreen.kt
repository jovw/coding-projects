/* Assignment 5
* Juanette van Wyk
* vanwykj@oregonstate.edu
* OSU: CS 492
*/

package com.example.treasurehunt.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.treasurehunt.R
import com.example.treasurehunt.ui.viewmodel.TreasureHuntViewModel

@Composable
fun PermissionScreen(
    viewModel: TreasureHuntViewModel,
    onSetPermissionClick: () -> Unit
) {
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
                text = "Treasure hunt",
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
                text = "Some permissions are required to play this game",
                fontSize = 25.sp,
                textAlign = TextAlign.Center,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 16.dp)
            )

            // Spacer to push buttons to the bottom
            Spacer(modifier = Modifier.weight(1f))

            Button(
                onClick = {
                    onSetPermissionClick()
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 16.dp),
                shape = MaterialTheme.shapes.medium,
                contentPadding = PaddingValues(16.dp)
            ) {
                Text(
                    text = "Set up Permissions",
                    fontSize = 20.sp
                )
            }

        }
    }
}
