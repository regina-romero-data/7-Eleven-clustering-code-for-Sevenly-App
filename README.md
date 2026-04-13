# 7-Eleven-clustering-code-for-Sevenly-App
Customer segmentation using K-Means clustering on real 7-Eleven México transactional data to optimize mobile coupon strategy by behavioral profile.
# 7-Eleven Customer Segmentation — K-Means Clustering
### ICONN / Petro Seven · Academic Consulting Project · 2025

## Overview
End-to-end customer segmentation analysis on real transactional data from 
ICONN/7-Eleven México, aimed at identifying behavioral customer profiles 
to optimize the Petro Seven mobile coupon strategy.

## Business Problem
How can ICONN personalize coupon offerings based on customer behavior, 
product preferences, temperature patterns, and sports event correlation?

## What This Notebook Does
1. **Data Wrangling** — Loads transactional Excel data, normalizes column 
   names (removes accents, spaces), filters by geographic region 
   (Nuevo León) and year (2025), and excludes non-consumer products 
   (Magna, Premium, Diesel).

2. **Feature Engineering** — Combines numerical features (average 
   temperature) and categorical features (product, coupon type, match day) 
   into a unified representation for clustering.

3. **Preprocessing Pipeline** — Applies StandardScaler to numerical 
   features and OneHotEncoder to categorical features using a 
   Scikit-learn ColumnTransformer pipeline.

4. **K-Means Clustering (k=4)** — Segments customers into 4 distinct 
   behavioral profiles based on product preference, coupon sensitivity, 
   temperature patterns, and soccer match correlation.

5. **Cluster Analysis** — Summarizes each segment by unique customers, 
   most common product, coupon type, match-day behavior, and average 
   temperature — exported to Excel for business reporting.

## Customer Segments Identified
| Cluster | Profile | Key Characteristic |
|---|---|---|
| 0 | Hydration & Snacks | Cold drink + snack buyers |
| 1 | Summer Peak | High demand in hot weather |
| 2 | Winter Peak | Cold season snack consumers |
| 3 | Salty + Sweet | Mixed snack preference |

## Tech Stack
- Python · Pandas · NumPy
- Scikit-learn (KMeans, StandardScaler, OneHotEncoder, Pipeline)
- KPrototypes (kmodes)
- OpenPyXL

## Key Findings
- Temperature is a significant driver of product demand
- Soccer match days (Rayados/Tigres) correlate with specific product spikes
- 4 distinct customer segments with differentiated coupon sensitivity profiles
  

## Context
This project is part of a larger consulting engagement that also included 
ANOVA-based uplift modeling, promotional effectiveness analysis, and a 
proposed Next Best Offer (NBO) recommendation system for real-time 
personalized coupon delivery at point of sale.
