/* Assignment 5
* Juanette van Wyk
* vanwykj@oregonstate.edu
* OSU: CS 492
*/

package com.example.treasurehunt.ui.viewmodel

import android.content.Context
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider

class TreasureHuntViewModelFactory(private val context: Context) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(TreasureHuntViewModel::class.java)) {
            return TreasureHuntViewModel(context) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
