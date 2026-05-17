package com.nyayasarathi.app.di

import com.nyayasarathi.app.data.remote.AuthInterceptor
import com.nyayasarathi.app.data.remote.api.AuthApiService
import com.nyayasarathi.app.data.remote.api.CaseApiService
import com.nyayasarathi.app.data.remote.api.CourtApiService
import com.nyayasarathi.app.data.remote.api.SubscriptionApiService
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    private const val BASE_URL = "https://nyaya-sutra-api.onrender.com/"
    private const val TIMEOUT_SECONDS = 30L

    @Provides
    @Singleton
    fun provideLoggingInterceptor(): HttpLoggingInterceptor {
        return HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        }
    }

    @Provides
    @Singleton
    fun provideOkHttpClient(
        authInterceptor: AuthInterceptor,
        loggingInterceptor: HttpLoggingInterceptor
    ): OkHttpClient {
        return OkHttpClient.Builder()
            .addInterceptor(authInterceptor)
            .addInterceptor(loggingInterceptor)
            .connectTimeout(TIMEOUT_SECONDS, TimeUnit.SECONDS)
            .readTimeout(TIMEOUT_SECONDS, TimeUnit.SECONDS)
            .writeTimeout(TIMEOUT_SECONDS, TimeUnit.SECONDS)
            .build()
    }

    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {
        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    @Provides
    @Singleton
    fun provideAuthApiService(retrofit: Retrofit): AuthApiService {
        return retrofit.create(AuthApiService::class.java)
    }

    @Provides
    @Singleton
    fun provideCaseApiService(retrofit: Retrofit): CaseApiService {
        return retrofit.create(CaseApiService::class.java)
    }

    @Provides
    @Singleton
    fun provideCourtApiService(retrofit: Retrofit): CourtApiService {
        return retrofit.create(CourtApiService::class.java)
    }

    @Provides
    @Singleton
    fun provideSubscriptionApiService(retrofit: Retrofit): SubscriptionApiService {
        return retrofit.create(SubscriptionApiService::class.java)
    }
}
