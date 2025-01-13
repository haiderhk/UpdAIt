//
//  Article.swift
//  UpdAIt
//
//  Created by Haider Khan on 05/01/2025.
//

import Foundation
import SwiftUI

struct Article: Identifiable, Codable {
    var id = UUID()
    let articleLink: String
    let articleTitle: String
    let articlePublicationDate: String
    let articleImageUrl: String
    
    enum CodingKeys: String, CodingKey {
        case articleLink = "article_link"
        case articleTitle = "article_title"
        case articlePublicationDate = "article_publication_date"
        case articleImageUrl = "article_image_url"
    }
}

struct ArticlesResponse: Codable {
    let articles: [Article]
}


var mockData = [
    Article(articleLink: "https://www.deeplearning.ai/the-batch/issue-282/", articleTitle: "Happy New Year! Hopes For 2025 With Mustafa Suleyman, Audrey Tang, Albert Gu, Hanno Basse, Joseph Gonzalez, David Ding", articlePublicationDate: "Jan 01, 2025", articleImageUrl: "https://dl-staging-website.ghost.io/content/images/2025/01/unnamed--35--1.png"),
]
