/* Assignment 4
* Juanette van Wyk
* vanwykj@oregonstate.edu
* OSU: CS 492
*/

package com.example.cityreccomendations.data

import com.example.cityreccomendations.R
import com.example.cityreccomendations.model.Category
import com.example.cityreccomendations.model.Recommendation

object Datasource {
    val categories = listOf(
        Category(
            name = "Coffee shops",
            recommendations = listOf(
                Recommendation(
                    "Lune Cafe",
                    "107 1st Ave S, Seattle, WA 98104",
                    "Welcome aboard! Buckle up for an exquisite time and prepare to glow with Lune in every city around the world. You heard that right! Here, you’ll satisfy those insatiable cravings with a taste of the adventure your heart desires. So what are you waiting for? Hop on!",
                    R.drawable.lune_cafe),
                Recommendation(
                    "Victrola Coffee Roasters",
                    "108 Pine St, Seattle, WA 98101",
                    "Victrola Coffee Roasters has been a Seattle staple since 2000, known for its meticulously roasted beans and cozy, vintage-inspired cafes.",
                    R.drawable.victrola),
                Recommendation(
                    "Monorail Espresso",
                    "510 Pike St, Seattle, WA 98101",
                    "Serving Seattle espresso since 1980, Monorail Espresso is a beloved walk-up window known for its rich, smooth coffee and friendly service.",
                    R.drawable.monorail),
                Recommendation(
                    "Storyville Coffee Pike Place",
                    "94 Pike Street Top floor Suite 34, Seattle, WA 98101",
                    "Located on the top floor of the Corner Market building, Storyville offers stunning views of Pike Place Market along with their exceptional coffee.",
                    R.drawable.storyville),
                Recommendation(
                    "Elm Coffee Roasters",
                    "240 2nd Ave S #103, Seattle, WA 98104",
                    "Elm Coffee Roasters is dedicated to bringing you the finest coffee, roasted fresh in Seattle. Their minimalist space and friendly baristas make it a must-visit.",
                    R.drawable.elm)
            ),
            imageResId = R.drawable.coffee_shop
        ),
        Category(
            name = "Restaurants",
            recommendations = listOf(
                Recommendation(
                    "Canlis",
                    "2576 Aurora Ave N, Seattle, WA 98109",
                    "Canlis is a landmark fine-dining restaurant in Seattle, offering a contemporary American menu with Pacific Northwest ingredients in an elegant, mid-century modern setting.",
                    R.drawable.canlins),
                Recommendation(
                    "The Pink Door",
                    "1919 Post Alley, Seattle, WA 98101",
                    "The Pink Door is an Italian-American restaurant with a whimsical atmosphere, known for its delicious food and nightly entertainment, including trapeze acts.",
                    R.drawable.the_pink_door_back_dining),
                Recommendation(
                    "Pike Place Chowder",
                    "1530 Post Alley, Seattle, WA 98101",
                    "Pike Place Chowder is famous for its award-winning New England Clam Chowder, served in a cozy, casual setting right in the heart of Pike Place Market.",
                    R.drawable.chowder),
                Recommendation(
                    "Toulouse Petit Kitchen & Lounge",
                    "601 Queen Anne Ave N, Seattle, WA 98109",
                    "Toulouse Petit offers a New Orleans-inspired menu with a Pacific Northwest twist, featuring an extensive brunch menu that draws crowds daily.",
                    R.drawable.toulous),
                Recommendation(
                    "Maneki",
                    "304 6th Ave S, Seattle, WA 98104",
                    "Maneki is a historic Japanese restaurant in Seattle's International District, serving traditional sushi and homestyle Japanese dishes since 1904.",
                    R.drawable.maneki_seattle_0)
            ),
            imageResId = R.drawable.restaurants
        ),
        Category(
            name = "Book Stores",
            recommendations = listOf(
                Recommendation(
                    "Elliott Bay Book Company",
                    "1521 10th Ave, Seattle, WA 98122",
                    "Elliott Bay Book Company is a large, independent bookstore with a wide selection of books and frequent author events, located in the vibrant Capitol Hill neighborhood.",
                    R.drawable.eliot),
                Recommendation(
                    "Third Place Books",
                    "17171 Bothell Way NE, Lake Forest Park, WA 98155",
                    "Third Place Books offers a huge selection of new and used books, along with a community space for events and a connected food court.",
                    R.drawable.third_place_books),
                Recommendation(
                    "Ada's Technical Books and Cafe",
                    "425 15th Ave E, Seattle, WA 98112",
                    "Ada's Technical Books is a unique bookstore and cafe focused on technical and scientific literature, providing a cozy space for Seattle's tech community.",
                    R.drawable.ada),
                Recommendation(
                    "Ophelia's Books",
                    "3504 Fremont Ave N, Seattle, WA 98103",
                    "Ophelia's Books is a charming used bookstore in the Fremont neighborhood, known for its friendly cat and well-curated selection of secondhand books.",
                    R.drawable.ophelia),
                Recommendation(
                    "Kinokuniya Seattle",
                    "525 S Weller St, Seattle, WA 98104",
                    "Kinokuniya Seattle is a Japanese bookstore offering a wide range of Japanese books, manga, and stationery, located within the Uwajimaya shopping complex.",
                    R.drawable.kinokuniya_san_francisco)
            ),
            imageResId = R.drawable.book_shop
        ),
        Category(
            name = "Parks",
            recommendations = listOf(
                Recommendation(
                    "Discovery Park",
                    "3801 Discovery Park Blvd, Seattle, WA 98199",
                    "Discovery Park is Seattle's largest green space, offering miles of trails, stunning views of Puget Sound, and a historic lighthouse.",
                    R.drawable.discovery),
                Recommendation(
                    "Gas Works Park",
                    "2101 N Northlake Way, Seattle, WA 98103",
                    "Gas Works Park features the remnants of a former gasification plant, now serving as a unique and popular spot for picnics and panoramic views of Lake Union.",
                    R.drawable.gas_works_park_max),
                Recommendation(
                    "Kerry Park",
                    "211 W Highland Dr, Seattle, WA 98119",
                    "Kerry Park offers some of the best views of the Seattle skyline, including the Space Needle and Mount Rainier on clear days.",
                    R.drawable.kerry_park_max),
                Recommendation(
                    "Volunteer Park",
                    "1247 15th Ave E, Seattle, WA 98112",
                    "Volunteer Park is home to the Volunteer Park Conservatory, a water tower with a view, and the Seattle Asian Art Museum, all amidst beautiful green lawns.",
                    R.drawable.volunteer_park_01_front),
                Recommendation(
                    "Washington Park Arboretum",
                    "2300 Arboretum Dr E, Seattle, WA 98112",
                    "The Washington Park Arboretum features a diverse collection of plants, with miles of trails and seasonal blooms that attract visitors year-round.",
                    R.drawable.washington_park_arboretum_gettyimages_635835982_jpg)
            ),
            imageResId = R.drawable.parks
        ),
        Category(
            name = "Shopping",
            recommendations = listOf(
                Recommendation(
                    "Pike Place Market",
                    "85 Pike St, Seattle, WA 98101",
                    "Pike Place Market is Seattle's iconic public market, offering fresh produce, unique crafts, and the famous fish-throwing fishmongers.",
                    R.drawable.pike_place_market_entrance_0_0_0),
                Recommendation(
                    "University Village",
                    "2623 NE University Village St, Seattle, WA 98105",
                    "University Village is an open-air shopping center with a mix of national retailers, local boutiques, and a variety of dining options.",
                    R.drawable.u_village),
                Recommendation(
                    "Pacific Place",
                    "600 Pine St, Seattle, WA 98101",
                    "Pacific Place is a premier downtown shopping mall with high-end retailers, a movie theater, and several dining options.",
                    R.drawable.pacificplace),
                Recommendation(
                    "Ballard Avenue",
                    "Ballard Ave NW, Seattle, WA 98107",
                    "Ballard Avenue offers a vibrant shopping experience with its mix of trendy boutiques, vintage shops, and popular restaurants in the historic Ballard neighborhood.",
                    R.drawable.ballard),
                Recommendation(
                    "Fremont Sunday Market",
                    "3401 Evanston Ave N, Seattle, WA 98103",
                    "The Fremont Sunday Market is a beloved local market featuring a variety of vendors selling antiques, crafts, and food in the quirky Fremont neighborhood.",
                    R.drawable.fremontmarket_150)
            ),
            imageResId = R.drawable.shopping
        )
    )
}
