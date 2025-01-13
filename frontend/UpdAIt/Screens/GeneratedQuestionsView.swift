//
//  GeneratedQuestionsView.swift
//  UpdAIt
//
//  Created by Haider Khan on 08/01/2025.
//

import SwiftUI

struct GeneratedQuestionsView: View {
    let questions: [Question]
    
    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                ForEach(questions) { question in
                    QuestionCardView(question: question)
                }
            }
            .padding()
        }
        .background(
            LinearGradient(
                colors: [Color.blue.opacity(0.1), Color.yellow.opacity(0.2), Color.purple.opacity(0.2)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        )
        .navigationTitle("Questions")
//        .navigationBarTitleDisplayMode(.inline)
    }
}



#Preview {
    GeneratedQuestionsView(questions: mockQuestions)
}

