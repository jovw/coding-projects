/* Assignment 5
* Juanette van Wyk
* vanwykj@oregonstate.edu
* OSU: CS 492
*/

package com.example.treasurehunt.ui.data

import android.content.Context
import com.example.treasurehunt.ui.model.Rules
import com.example.treasurehunt.R
import com.example.treasurehunt.ui.model.Clue
import com.example.treasurehunt.ui.model.FunFact
import java.io.InputStreamReader
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken

object Datasource {
    private lateinit var data: TreasureHuntData

    fun loadData(context: Context) {
        val inputStream = context.resources.openRawResource(R.raw.treasure_hunt_data)
        val reader = InputStreamReader(inputStream)
        data = Gson().fromJson(reader, TreasureHuntData::class.java)
        reader.close()
    }

    val rules: List<Rules>
        get() = data.rules

    val clues: List<Clue>
        get() = data.clues

    val funFacts: List<FunFact>
        get() = data.funFacts
}

data class TreasureHuntData(
    val rules: List<Rules>,
    val clues: List<Clue>,
    val funFacts: List<FunFact>
)
