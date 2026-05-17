package com.nyayasarathi.app.data.local.db

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface TrackedCaseDao {
    @Query("SELECT * FROM tracked_cases ORDER BY next_hearing_date ASC")
    suspend fun getAllTrackedCases(): List<TrackedCaseEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(cases: List<TrackedCaseEntity>)

    @Query("DELETE FROM tracked_cases WHERE id = :caseId")
    suspend fun deleteById(caseId: String)

    @Query("DELETE FROM tracked_cases")
    suspend fun deleteAll()
}
