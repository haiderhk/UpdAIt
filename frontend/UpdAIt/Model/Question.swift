//
//  Question.swift
//  UpdAIt
//
//  Created by Haider Khan on 08/01/2025.
//

import Foundation
import SwiftUI

struct Question: Identifiable, Codable {
    var id = UUID()
    let questionType: String
    let question: String
    let answer: String
    let reference: String
    
    enum CodingKeys: String, CodingKey {
        case questionType = "question_type"
        case question = "question"
        case answer = "answer"
        case reference = "reference"
    }
}

struct QuestionsResponse: Codable {
    let questions: [Question]
}


var mockQuestions: [Question] = [
    Question(questionType: "Factual", question: "What is the new buzzword in AI?", answer: "The new buzzword in AI is Agentic", reference: "There is also a new ... which people call --agentic-- AI.")
]
