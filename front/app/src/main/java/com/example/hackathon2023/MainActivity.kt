package com.example.hackathon2023

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.DatePicker
import android.widget.TextView
import java.text.SimpleDateFormat
import java.util.*

class MainActivity : AppCompatActivity() {

    private lateinit var datePicker: DatePicker

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        datePicker = findViewById(R.id.datePicker)
    }

    fun onSendButtonClick(view: View) {
        val day = datePicker.dayOfMonth
        val month = datePicker.month
        val year = datePicker.year

        val calendar = Calendar.getInstance()
        calendar.set(year, month, day)

        val sdf = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault())
        val formattedDate = sdf.format(calendar.time)

        // Créer un intent pour lancer l'activité suivante
        val intent = Intent(this, SecondActivity::class.java)

        // Ajouter la date à l'intent en utilisant une clé
        intent.putExtra("selectedDate", formattedDate)

        // Démarrer l'activité suivante
        startActivity(intent)
    }
}