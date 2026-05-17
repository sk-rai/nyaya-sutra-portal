package com.nyayasarathi.app.data.local.db

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface CourtDao {
    @Query("SELECT * FROM courts ORDER BY type, state, name")
    suspend fun getAllCourts(): List<CourtEntity>

    @Query("SELECT * FROM courts WHERE type = :type")
    suspend fun getCourtsByType(type: String): List<CourtEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(courts: List<CourtEntity>)

    @Query("DELETE FROM courts")
    suspend fun deleteAll()
}
