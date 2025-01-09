/* Assignment 5
* Juanette van Wyk
* vanwykj@oregonstate.edu
* OSU: CS 492
*/

package com.example.treasurehunt.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.graphics.Color

private val DarkColorScheme = darkColorScheme(
    // Use the default colors for dark theme, or customize if needed
    primary = Purple80,
    secondary = PurpleGrey80,
    tertiary = Pink80
)

private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF598392),        // --primary: #598392
    onPrimary = Color(0xFFEDEDE9),      // --onPrimary: #EDEDE9
    secondary = Color(0xFF936059),      // --secondary: #936059
    onSecondary = Color(0xFFEDEDE9),    // --onSecondary: #EDEDE9
    background = Color(0xFFE3D5CA),     // --backgroundColor1: #E3D5CA
    surface = Color(0xFFF5EBE0),        // --backgroundColor2: #F5EBE0
    onBackground = Color(0xFFEFEBE6),   // --backgroundColor3: #EFEBE6
    // You can add other color overrides here if necessary
)

@Composable
fun TreasureHuntTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    // Dynamic color is available on Android 12+
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = LightColorScheme,
        typography = Typography,
        content = content
    )
}
