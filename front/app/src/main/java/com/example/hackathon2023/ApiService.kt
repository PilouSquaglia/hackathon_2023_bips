package com.example.hackathon2023

import retrofit2.Call
import retrofit2.http.GET

interface ApiService {
    @GET("/travelling")
    fun getTravelData(): Call<TravelResponse>
}
