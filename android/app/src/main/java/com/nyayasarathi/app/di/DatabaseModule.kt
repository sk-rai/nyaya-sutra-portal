package com.nyayasarathi.app.di

import android.content.Context
import androidx.room.Room
import com.nyayasarathi.app.data.local.db.NyayaSarathiDatabase
import com.nyayasarathi.app.data.local.db.CourtDao
import com.nyayasarathi.app.data.local.db.TrackedCaseDao
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): NyayaSarathiDatabase {
        return Room.databaseBuilder(
            context,
            NyayaSarathiDatabase::class.java,
            "nyaya_sarathi_db"
        ).build()
    }

    @Provides
    fun provideCourtDao(database: NyayaSarathiDatabase): CourtDao {
        return database.courtDao()
    }

    @Provides
    fun provideTrackedCaseDao(database: NyayaSarathiDatabase): TrackedCaseDao {
        return database.trackedCaseDao()
    }
}
