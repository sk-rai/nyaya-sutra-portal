package com.nyayasarathi.app.data.local.db

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "tracked_cases")
data class TrackedCaseEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "case_number") val caseNumber: String,
    @ColumnInfo(name = "court_code") val courtCode: String,
    @ColumnInfo(name = "court_name") val courtName: String,
    val parties: String,
    val status: String,
    @ColumnInfo(name = "next_hearing_date") val nextHearingDate: String?,
    @ColumnInfo(name = "filing_date") val filingDate: String?,
    @ColumnInfo(name = "last_updated") val lastUpdated: Long
)
