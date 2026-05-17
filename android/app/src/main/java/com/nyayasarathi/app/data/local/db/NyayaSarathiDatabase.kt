package com.nyayasarathi.app.data.local.db

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(
    entities = [CourtEntity::class, TrackedCaseEntity::class],
    version = 1,
    exportSchema = false
)
abstract class NyayaSarathiDatabase : RoomDatabase() {
    abstract fun courtDao(): CourtDao
    abstract fun trackedCaseDao(): TrackedCaseDao
}
