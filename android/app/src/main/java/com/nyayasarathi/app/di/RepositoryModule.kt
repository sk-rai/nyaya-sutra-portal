package com.nyayasarathi.app.di

import com.nyayasarathi.app.data.repository.AuthRepositoryImpl
import com.nyayasarathi.app.data.repository.CaseRepositoryImpl
import com.nyayasarathi.app.data.repository.CourtRepositoryImpl
import com.nyayasarathi.app.data.repository.SubscriptionRepositoryImpl
import com.nyayasarathi.app.domain.repository.AuthRepository
import com.nyayasarathi.app.domain.repository.CaseRepository
import com.nyayasarathi.app.domain.repository.CourtRepository
import com.nyayasarathi.app.domain.repository.SubscriptionRepository
import dagger.Binds
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    abstract fun bindAuthRepository(impl: AuthRepositoryImpl): AuthRepository

    @Binds
    abstract fun bindCaseRepository(impl: CaseRepositoryImpl): CaseRepository

    @Binds
    abstract fun bindCourtRepository(impl: CourtRepositoryImpl): CourtRepository

    @Binds
    abstract fun bindSubscriptionRepository(impl: SubscriptionRepositoryImpl): SubscriptionRepository
}
