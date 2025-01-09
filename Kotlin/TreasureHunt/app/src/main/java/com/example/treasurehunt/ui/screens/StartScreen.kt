/* Assignment 5
* Juanette van Wyk
* vanwykj@oregonstate.edu
* OSU: CS 492
*/

package com.example.treasurehunt.ui.screens

import android.content.Context
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.treasurehunt.ui.model.Rules
import com.example.treasurehunt.ui.viewmodel.TreasureHuntViewModel
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavHostController
import androidx.compose.ui.platform.LocalContext

@Composable
fun StartScreen(
    viewModel: TreasureHuntViewModel = viewModel(),
    onStartClick: () -> Unit
) {
    // Observing the rules from the ViewModel
    val rules by viewModel.rules.collectAsState(emptyList())

    val context = LocalContext.current

    // UI for Start Screen
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.SpaceBetween,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // Title
        Text(
            text = "Treasure Hunt",
            fontSize = 32.sp,
            fontWeight = FontWeight.Bold,
            textAlign = TextAlign.Center,
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 24.dp)
        )
        Spacer(
            modifier = Modifier
                .height(20.dp)
        )

        Text(
            text = "Game Rules:",
            fontSize = 20.sp,
            textAlign = TextAlign.Start,
            modifier = Modifier
                .fillMaxWidth()
                .padding(start = 0.dp)
        )

        // Rules LazyColumn
        LazyColumn(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth()
        ) {
            itemsIndexed(rules) { index, rule ->
                RuleItem(rule = rule, isEven = index % 2 == 0, context = context)
            }
        }

        // Start Button
        Button(
            onClick = {
                viewModel.startTimer()
                onStartClick()
            },
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 16.dp),
            shape = MaterialTheme.shapes.medium,
            colors = ButtonDefaults.buttonColors(
                containerColor = MaterialTheme.colorScheme.primary
            ),
            contentPadding = PaddingValues(16.dp),
        ) {
            Text(
                text = "Start",
                fontSize = 20.sp,
                color = MaterialTheme.colorScheme.onPrimary
            )
        }
    }
}

@Composable
fun RuleItem(rule: Rules, isEven: Boolean, context: Context) {
    val imageResId = context.resources.getIdentifier(rule.imageRes, "drawable", context.packageName)

    Surface(
        color = MaterialTheme.colorScheme.background,
        shape = RoundedCornerShape(8.dp),
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp)
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
//            horizontalArrangement = Arrangement.Start,
            modifier = Modifier.padding(16.dp)
        ) {
            if (isEven) {
                Image(
                    painter = painterResource(id = imageResId),
                    contentDescription = null,
                    modifier = Modifier.size(85.dp),
                    contentScale = ContentScale.Crop
                )
            }
            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(
                        start = if (isEven) 16.dp else 0.dp,
                        end = if (!isEven) 16.dp else 0.dp
                    )
            ) {
                Text(
                    text = rule.title,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.Black
                )
                Text(
                    text = rule.description,
                    fontSize = 16.sp,
                    color = Color.Black
                )
            }
            if (!isEven) {
                Image(
                    painter = painterResource(id = imageResId),
                    contentDescription = null,
                    modifier = Modifier.size(85.dp),
                    contentScale = ContentScale.Crop
                )
            }
        }
    }
}
