package com.example.hackathon2023

import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Path

interface ApiService {
    @GET("/travelling/{date}")
    fun getTravelData(@Path("date") date: String): Call<TravelResponse>
}
