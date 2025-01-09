/* Assignment 1
* Juanette van Wyk
* vanwykj@oregonstate.edu
* OSU: CS 492
*/

package com.example.businesscard

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Email
import androidx.compose.material.icons.filled.Phone
import androidx.compose.material.icons.filled.Share
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.businesscard.ui.theme.BusinessCardTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            BusinessCardTheme {
                // A surface container using the 'background' color from the theme
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = Color(0xff14181d)
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(bottom = 40.dp)
                            .padding(vertical = 10.dp),
                    ) {
                        CardHeader(
                            name = "Juanette van Wyk",
                            occupation = "CS 492 Student Extraordinaire",
                            modifier = Modifier.align(Alignment.Center)
                        )
                        Column(
                            modifier = Modifier
                                .align(Alignment.BottomCenter),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ){
                            Info(
                                icon = Icons.Filled.Phone,
                                info = "+11 (123) 444 555 666"
                            )
                            Spacer(modifier = Modifier
                                .height(5.dp)
                            )
                            Info(
                                icon = Icons.Filled.Share,
                                info = "@Another.Dev"
                            )
                            Spacer(modifier = Modifier
                                .height(5.dp)
                            )
                            Info(
                                icon = Icons.Filled.Email,
                                info = "vanwykj@oregonstate.edu"
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun CardHeader(name: String, occupation: String, modifier: Modifier = Modifier){
    val image = painterResource(R.drawable.android_logo)

    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = modifier
            .padding(8.dp)
    ) {
        Image(
            painter = image,
            contentDescription = null,
            modifier = Modifier
                .height(130.dp)
        )
        Spacer(modifier = Modifier
            .height(5.dp)
        )
        Text(
            text = name,
            fontSize = 40.sp,
            fontWeight = FontWeight.Thin,
            color = Color(0xFFFFFFFF)
        )
        Spacer(modifier = Modifier
            .height(10.dp)
        )
        Text(
            text = occupation,
            fontSize = 15.sp,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF3ddc84)
        )
    }
}

@Composable
fun Info(icon: ImageVector, info: String, modifier: Modifier = Modifier){
    Row(
        modifier = modifier
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = Color(0xFF3ddc84)
        )
        Spacer(modifier = Modifier
            .width(20.dp)
        )
        Text(
            text = info,
            color = Color(0xFFFFFFFF)
        )
    }
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    BusinessCardTheme {
        // CardHeader(name = "Jo van Wyk", occupation = "CS 492 Student Extraordinaire")
        Info(icon = Icons.Filled.Phone, info = "+11 (123) 444 555 666")
    }
}