/* Assignment 5
* Juanette van Wyk
* vanwykj@oregonstate.edu
* OSU: CS 492
*/

package com.example.treasurehunt.ui.viewmodel

import android.annotation.SuppressLint
import android.content.Context
import android.location.Location
import android.os.CountDownTimer
import android.os.Handler
import android.os.Looper
import androidx.lifecycle.ViewModel
import com.example.treasurehunt.ui.data.Datasource
import com.example.treasurehunt.ui.model.Clue
import com.example.treasurehunt.ui.model.FunFact
import com.example.treasurehunt.ui.model.Rules
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationRequest
import com.google.android.gms.location.LocationServices
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class TreasureHuntViewModel(context: Context) : ViewModel() {
    // Timer related state
    private val _elapsedTime = MutableStateFlow(0L)
    val elapsedTime: StateFlow<Long> = _elapsedTime.asStateFlow()

    private val handler = Handler(Looper.getMainLooper())
    private var startTime: Long = 0L
    private var pausedTime: Long = 0L
    private var isPaused: Boolean = false

    private val runnable = object : Runnable {
        override fun run() {
            val currentTime = System.currentTimeMillis()
            _elapsedTime.value = (currentTime - startTime) / 1000
            handler.postDelayed(this, 1000)
        }
    }

    private val _rules = MutableStateFlow<List<Rules>>(emptyList())
    val rules: StateFlow<List<Rules>> = _rules

    private val _clues = MutableStateFlow<List<Clue>>(emptyList())
    val clues: StateFlow<List<Clue>> = _clues

    private val _funFacts = MutableStateFlow<List<FunFact>>(emptyList())
    val funFacts: StateFlow<List<FunFact>> = _funFacts

    private val _currentClueIndex = MutableStateFlow(0)
    val currentClueIndex: StateFlow<Int> = _currentClueIndex

    private val fusedLocationClient: FusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(context)
    private val _currentLocation = MutableStateFlow<Location?>(null)
    val currentLocation: StateFlow<Location?> = _currentLocation

    init {
        Datasource.loadData(context)
        loadRules()
        loadCluesAndFunFacts()
    }

    private fun loadRules() {
        _rules.value = Datasource.rules
    }

    private fun loadCluesAndFunFacts() {
        _clues.value = Datasource.clues
        _funFacts.value = Datasource.funFacts
    }

    fun moveToNextClue() {
        if (_currentClueIndex.value < _clues.value.size - 1) {
            _currentClueIndex.value += 1
        }
    }

    fun isLastClue(): Boolean {
        return _currentClueIndex.value == _clues.value.size - 1
    }

    fun resetClueIndex() {
        _currentClueIndex.value = 0
    }

    fun startTimer() {
        if (isPaused) {
            startTime = System.currentTimeMillis() - (pausedTime * 1000)
            isPaused = false
        } else {
            startTime = System.currentTimeMillis()
            pausedTime = 0L
        }
        handler.post(runnable)
    }

    fun pauseTimer() {
        if (!isPaused) {
            handler.removeCallbacks(runnable)
            pausedTime = _elapsedTime.value
            isPaused = true
        }
    }

    fun stopTimer() {
        handler.removeCallbacks(runnable)
        _elapsedTime.value = 0L
        pausedTime = 0L
        isPaused = false
    }

    fun haversine(lat1: Double, lon1: Double, lat2: Double, lon2: Double): Double {
        val R = 6371e3 // Earth radius in meters
        val phi1 = Math.toRadians(lat1)
        val phi2 = Math.toRadians(lat2)
        val deltaPhi = Math.toRadians(lat2 - lat1)
        val deltaLambda = Math.toRadians(lon2 - lon1)

        val a = Math.sin(deltaPhi / 2) * Math.sin(deltaPhi / 2) +
                Math.cos(phi1) * Math.cos(phi2) *
                Math.sin(deltaLambda / 2) * Math.sin(deltaLambda / 2)
        val c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))

        return R * c // distance in meters
    }

    @SuppressLint("MissingPermission")
    fun checkLocationForClue(
        correctLat: Double,
        correctLon: Double,
        onResult: (Boolean) -> Unit
    ) {
        println("checkLocationForClue called")
        fusedLocationClient.getCurrentLocation(
            LocationRequest.PRIORITY_HIGH_ACCURACY,
            null
        ).addOnSuccessListener { location: Location? ->
            if (location != null) {
                _currentLocation.value = location
                val distance = haversine(location.latitude, location.longitude, correctLat, correctLon)
                val isCorrectLocation = distance <= 50
                println("Fetched Location: ${location.latitude}, ${location.longitude}")
                println("Correct Location: $correctLat, $correctLon")
                println("Distance: $distance meters")
                println("Is the location correct? $isCorrectLocation")
                onResult(isCorrectLocation)
            } else {
                println("Failed to fetch location: Location is null")
                onResult(false)
            }
        }.addOnFailureListener {
            println("Failed to fetch location: ${it.message}")
            onResult(false)
        }
    }
}
