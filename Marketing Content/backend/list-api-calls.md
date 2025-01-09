# API Routes Documentation

## Overview

This document details the API endpoints available for the 1st user scenario, including methods, URLs, headers, and expected responses for functionality related to users, products, companies, and audiences.

## Authentication

### Logout 1st User with Tokens

- **Endpoint:** `/auth/google/logout`
- **Method:** GET
- **Headers:**
  - `Cookie: access_token={{accessToken}}; id_token={{idToken}}; refresh_token={{refreshToken}};`
- **Purpose:** Logs out the first user by invalidating their session tokens.

## Users

### Get 1st User by SUB

- **Endpoint:** `/users/sub`
- **Method:** GET
- **Headers:**
  - `Cookie: access_token={{accessToken}}; id_token={{idToken}}; refresh_token={{refreshToken}};`

### Add Company to 1st User

- **Endpoint:** `/users/company`
- **Method:** POST
- **Headers:**
  - `Cookie: access_token={{accessToken}}; id_token={{idToken}}; refresh_token={{refreshToken}};`
- **Body:**
  ```json
  {
    "companyName": "Euphoriq",
    "companyDescription": "Euphoriq description."
  }
  ```

### Get 1st User's Company

- **Endpoint:** `/users/company`
- **Method:** GET
- **Headers:**
  - `Cookie: access_token={{accessToken}}; id_token={{idToken}}; refresh_token={{refreshToken}};`

## Products

### Add Product to 1st User

- **Endpoint:** `/users/products`
- **Method:** POST
- **Headers:**
  - `Cookie: access_token={{accessToken}}; id_token={{idToken}}; refresh_token={{refreshToken}};`
- **Body:**
  ```json
  {
    "productName": "Euphoriq SynthWave 3000",
    "productDescription": "The SynthWave 3000 is a versatile synthesizer designed for electronic music enthusiasts. Featuring an array of vintage analog sounds and modern digital effects, it provides endless possibilities for crafting unique soundscapes. With an intuitive interface and customizable presets, it's perfect for both beginners and seasoned musicians."
  }
  ```

### Delete 1st User's Product by Product ID

- **Endpoint:** `/users/products/{id}`
- **Method:** DELETE
- **Headers:**
  - `Content-Type: application/json`
  - `Cookie: access_token={{accessToken}}; id_token={{idToken}}; refresh_token={{refreshToken}};`
- **Purpose:** Deletes a specified product by its ID from the first user's list.

### Get 1st User's Products

- **Endpoint:** `/users/products`
- **Method:** GET
- **Headers:**
  - `Cookie: access_token={{accessToken}}; id_token={{idToken}}; refresh_token={{refreshToken}};`

### Get all 1st User's Products by ID

- **Endpoint:** `/users/products/{id}`
- **Method:** GET
- **Headers:**
  - `Cookie: access_token={{accessToken}}; id_token={{idToken}}; refresh_token={{refreshToken}};`

### Edit Product of 1st User by Product ID

- **Endpoint:** `/users/products/{id}`
- **Method:** POST
- **Headers:**
  - `Cookie: access_token={{accessToken}}; id_token={{idToken}}; refresh_token={{refreshToken}};`
- **Body:**
  ```json
  {
    "productName": "Euphoriq SynthWave 2024",
    "productDescription": "The SynthWave 2024 is a versatile synthesizer designed for electronic music enthusiasts. Featuring an array of vintage analog sounds and modern digital effects, it provides endless possibilities for crafting unique soundscapes. With an intuitive interface and customizable presets, it's perfect for both beginners and seasoned musicians."
  }
  ```

## Audiences

### Add Audience to 1st User

- **Endpoint:** `/users/audiences`
- **Method:** POST
- **Headers:**
  - `Cookie: access_token={{accessToken}}; id_token={{idToken}}; refresh_token={{refreshToken}};`
- **Body:**
  ```json
  {
    "audienceName": "Electronic Music Producers",
    "audienceDescription": "Creatives specializing in various electronic music genres, such as EDM, synth-pop, house, techno, and synthwave. They seek advanced synthesizers capable of generating unique and diverse soundscapes, rich basslines, and atmospheric pads to push the boundaries of electronic music."
  }
  ```

## Edit an Audience of 1st User by Audience ID

- **Endpoint:** `/users/audiences/{id}`
- **Method:** POST
- **Headers:**
  - `Cookie: access_token={{accessToken}}; id_token={{idToken}}; refresh_token={{refreshToken}};`
- **Body:**
  ```json
  {
    "audienceName": "Live Performers and Touring Artists",
    "audienceDescription": "Musicians and bands who perform live or on tour, requiring robust, portable synthesizers with intuitive controls and extensive sound customization options. They value reliability and versatility for dynamic performances across various venues."
  }
  ```

## Delete 1st User's Audience via Audience ID

- **Endpoint:** `/users/audiences/{id}`
- **Method:** DELETE
- **Headers:**
  - `Content-Type: application/json`
  - `Cookie: access_token={{accessToken}}; id_token={{idToken}}; refresh_token={{refreshToken}};`

## Get 1st User's Audience ID

- **Endpoint:** `/users/audiences`
- **Method:** GET
- **Headers:**
  - `Cookie: access_token={{accessToken}}; id_token={{idToken}}; refresh_token={{refreshToken}};`

## Content

## Send Request to Content Generate APIs(returns json)

- \*\*Endpoint: `/contents/disperse`
- **Method:** POST
- **Headers:**
  - `Cookie: access_token={{accessToken}}; id_token={{idToken}}; refresh_token={{refreshToken}};`
- **Body:**
  ```json
  {
    "productId": 1,
    "audienceIds": [1, 2, 3],
    "tone": ["vaporwave", "sad", "dark"],
    "platform": ["Facebook"]
  }
  ```

### Get All 1st User's Generated Contents

- **Endpoint:** `/users/contents`
- **Method:** GET
- **Headers:**
  - `Cookie: access_token={{accessToken}}; id_token={{idToken}}; refresh_token={{refreshToken}};`

### Get All Generated Contents by Product ID

- **Endpoint:** `/users/products/:productId/contents`
- **Method:** GET
- **Headers:**
  - `Cookie: access_token={{accessToken}}; id_token={{idToken}}; refresh_token={{refreshToken}};`
