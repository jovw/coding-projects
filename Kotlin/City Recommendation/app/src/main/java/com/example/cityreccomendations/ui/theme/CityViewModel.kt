/* Assignment 4
* Juanette van Wyk
* vanwykj@oregonstate.edu
* OSU: CS 492
*/

package com.example.cityreccomendations.ui.theme

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.cityreccomendations.data.Datasource
import com.example.cityreccomendations.model.Category

class CityViewModel : ViewModel() {
    private val _categories = MutableLiveData<List<Category>>(Datasource.categories)
    val categories: LiveData<List<Category>> = _categories
}