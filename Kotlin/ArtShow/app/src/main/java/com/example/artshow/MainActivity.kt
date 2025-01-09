/* Assignment 2
* Juanette van Wyk
* vanwykj@oregonstate.edu
* OSU: CS 492
*/

package com.example.artshow

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.artshow.ui.theme.ArtShowTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            ArtShowTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                ) {
                    ArtShowLayout()
                }
            }
        }
    }
}

@Composable
fun ArtShowLayout() {
    var count by remember { mutableStateOf(3) }

    Column(
        modifier = Modifier
            .fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ){
        // Image
        ArtImage()
        // Title
        TextBox(count)
        //Buttons
        ArtButtons(
            onPreviousClick = {
                count = if (count == 1) 5 else count - 1
            },
            onNextClick = {
                count = if (count == 5) 1 else count + 1
            }
        )
    }
}

@Composable
fun ArtImage() {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
            .shadow(8.dp, RoundedCornerShape(8.dp))
            .background(Color.White, RoundedCornerShape(8.dp))
            .padding(20.dp)
    ) {
        Image(
            painter = painterResource(R.drawable.nature),
            contentDescription = "Drawing of a flower vase with books and a candle",
            modifier = Modifier
                .fillMaxWidth()
                .height(530.dp)
        )
    }
}

@Composable
fun TextBox(count: Int){
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
            .background(Color.LightGray)
            .padding(14.dp),
        verticalArrangement = Arrangement.Center,
    ) {
        Text(
            text = "Current count: $count",
            fontWeight = FontWeight.Light
        )
        Row(){
            Text(
                text = "Juanette van Wyk",
                fontSize = 11.sp,
                fontWeight = FontWeight.Bold
            )
            Text(
                text = "(CS 492)",
                fontSize = 11.sp,
                fontWeight = FontWeight.Normal
            )
        }
    }
}

@Composable
fun ArtButtons(
    onPreviousClick: () -> Unit,
    onNextClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(14.dp),
        horizontalArrangement = Arrangement.SpaceBetween
    ){
        Button(onClick = onPreviousClick) {
            Text(text = stringResource(R.string.previous))
        }
        Button(onClick = onNextClick) {
            Text(text = stringResource(R.string.next))
        }
    }
}

@Preview(showBackground = true)
@Composable
fun ArtShowPreview(
    modifier: Modifier = Modifier.fillMaxSize()
) {
    ArtShowTheme {
        ArtShowLayout()
    }
}