package com.example.hackathon2023

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.text.SimpleDateFormat
import java.util.Locale

object ApiClient {
    private const val BASE_URL = "http://10.0.2.2:8000"

    val retrofit: Retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .addConverterFactory(GsonConverterFactory.create())
        .build()
}

class SecondActivity : AppCompatActivity() {

    private fun fetchDataFromApi(formattedDate: String) {
        val apiService = ApiClient.retrofit.create(ApiService::class.java)
        val call = apiService.getTravelData(formattedDate)

        println(call.request().url())

        call.enqueue(object : Callback<TravelResponse> {
            override fun onResponse(call: Call<TravelResponse>, response: Response<TravelResponse>) {
                if (response.isSuccessful) {
                    val travelResponse = response.body()

                    // Process the data, update UI, etc.
                    travelResponse?.let {

                        println(it)
                        val cityList = mutableListOf<String>()

                        val cityNames = it.toString().split("TravelResponse(")[1].split(")")[0].split(", ")

                        for (cityName in cityNames) {
                            cityList.add(cityName.toString())
                        }

                        val cityNames2 = Regex("\\b(\\w+)=\\[")
                            .findAll(cityList.joinToString(separator = "\n"))
                            .map { it.groupValues[1] }
                            .toList()

                        println(cityNames2)

                        // Update the TextView with the list of cities
                        val cityListTextView: TextView = findViewById(R.id.cityListTextView)
                        cityListTextView.text = "Liste des communes à parcourir dans l'ordre : \n\n" + cityNames2.joinToString(separator = "\n")
                    }
                } else {
                    // Log the error message and response code
                    println("Error: ${response.code()}")
                    println("Error Body: ${response.errorBody()?.string()}")
                }
            }

            override fun onFailure(call: Call<TravelResponse>, t: Throwable) {
                // Log the failure reason
                println("Failure: ${t.message}")
            }
        })
    }


    // Helper function to build a string from the list of cities
    private fun buildCityListString(cityList: List<String>): String {
        return cityList.joinToString(separator = "\n")
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_second)

        // Récupérer l'intent qui a démarré cette activité
        val intent = intent

        // Vérifier si l'intent contient la clé "selectedDate"
        if (intent.hasExtra("selectedDate")) {
            // Extraire la date de l'intent
            val selectedDate = intent.getStringExtra("selectedDate")
            // Convertir la date dans le nouveau format "yyyy-MM-dd"
            val originalFormat = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault())
            val targetFormat = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
            val date = originalFormat.parse(selectedDate)
            val formattedDate = targetFormat.format(date)

            println(formattedDate)

            fetchDataFromApi(formattedDate)
        }



//        val dateTextView: TextView = findViewById(R.id.dateTextView)
//
//        // Récupérer la date passée par l'activité précédente
//        val selectedDate = intent.getStringExtra("selectedDate")
//
//        // Afficher la date dans le TextView de cette activité
//        dateTextView.text = "Date sélectionnée : $selectedDate"
    }

    private fun buildCityListString(travelResponse: TravelResponse): String {
        val cityList = mutableListOf<String>()

        // Extract city names from property names
        val properties = TravelResponse::class.java.declaredFields
        for (property in properties) {
            if (property.type == List::class.java && property.genericType == Double::class.java) {
                // Convert property name to a more readable city name
                val cityName = property.name.toLowerCase().replace("_", " ")
                cityList.add(cityName)
            }
        }

        return cityList.joinToString(separator = "\n")
    }

}
