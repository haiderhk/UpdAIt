//
//  Retrieval.swift
//  UpdAIt
//
//  Created by Haider Khan on 09/01/2025.
//

import Foundation
import SwiftUI


struct RAGResponse: Codable {
    let answer: String
    let metadata: [RAGMetadata]
}

struct RAGMetadata: Identifiable, Codable {
    var id: String { article_link }
    let article_link: String
    let article_title: String
    let chunk_heading: String
    let score: Double
}
