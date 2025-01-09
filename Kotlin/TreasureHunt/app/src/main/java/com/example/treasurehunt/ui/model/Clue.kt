/* Assignment 5
* Juanette van Wyk
* vanwykj@oregonstate.edu
* OSU: CS 492
*/

package com.example.treasurehunt.ui.model

class Clue(
    val number: Int,
    val text: String,
    val hint: String,
    val correctLocation: List<Double>, // Latitude and Longitude
    val funFactId: Int,
    val imageRes: String
)