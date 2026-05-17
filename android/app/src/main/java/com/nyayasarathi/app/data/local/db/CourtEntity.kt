package com.nyayasarathi.app.data.local.db

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "courts")
data class CourtEntity(
    @PrimaryKey val id: String,
    val name: String,
    @ColumnInfo(name = "court_code") val courtCode: String,
    val type: String,
    val state: String?,
    val district: String?,
    val address: String?,
    @ColumnInfo(name = "vc_link") val vcLink: String?,
    val email: String?,
    @ColumnInfo(name = "proceedings_url") val proceedingsUrl: String?,
    @ColumnInfo(name = "last_updated") val lastUpdated: Long
)
