//
//  QuestionCardView.swift
//  UpdAIt
//
//  Created by Haider Khan on 13/01/2025.
//

import SwiftUI

struct QuestionCardView: View {
    let question: Question
    @State private var isAnswerVisible = false
    @State private var userAnswer: String = ""
    @State private var isReferenceVisible = false
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            // Question Title
            Text(question.question)
                .font(.headline)
                .foregroundColor(.black)
                .padding(.horizontal)
                .padding(.top, 10)

            
            TextField("What do you think?", text: $userAnswer)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding(.horizontal)
                .cornerRadius(10)
            
            // Reveal Answer Button
            Button {
                withAnimation(.spring(response: 0.4, dampingFraction: 0.7)) {
                    isAnswerVisible.toggle()
                }
            } label: {
                HStack {
                    Text(isAnswerVisible ? "Hide Answer" : "Reveal Answer")
                        .font(.subheadline)
                        .fontWeight(.medium)
                    Spacer()
                    Image(systemName: "chevron.down")
                        .rotationEffect(.degrees(isAnswerVisible ? 180 : 0))
                        .animation(.easeInOut(duration: 0.3), value: isAnswerVisible)
                }
                .foregroundColor(.black)
                .padding()
                .background(Color.questionYellow)
                .clipShape(RoundedRectangle(cornerRadius: 12))
                .padding()
            }
            
            // Answer Section
            if isAnswerVisible {
                VStack(alignment: .leading, spacing: 10) {
                    // AI Answer
                    Text("AI's Answer:")
                        .font(.subheadline)
                        .foregroundColor(.black)
                        .bold()
                        .padding(.horizontal)
                    Text(question.answer)
                        .font(.body)
                        .foregroundColor(.black)
                        .padding()
                    
                
                    // Reference Button
//                    Button(action: {
//                        print("Reference button pressed")
//                        // Logic for reference action will go here
//                    }) {
//                        HStack {
//                            Text("Open Reference")
//                                .fontWeight(.medium)
//                            Spacer()
//                            Image(systemName: "arrow.right.circle.fill")
//                        }
//                        .frame(height: 10)
//                        .foregroundColor(.white)
//                        .padding()
//                        .background(
//                            LinearGradient(colors: [.blue, .purple], startPoint: .leading, endPoint: .trailing)
//                                .cornerRadius(12)
//                                .shadow(radius: 5)
//                        )
//                        .padding(.horizontal)
//                    }
                }
                .transition(
                    .asymmetric(
                        insertion: .scale(scale: 0.3)
                            .combined(with: .offset(y: -50))
                            .combined(with: .opacity),
                        removal: .scale(scale: 0.3)
                            .combined(with: .offset(y: -100))
                            .combined(with: .opacity)
                    )
                )
                .padding(.bottom, 10)
            }
        }
        .background(
            RoundedRectangle(cornerRadius: 20)
                .fill(LinearGradient(colors: [.questionPink.opacity(0.8), .yellow.opacity(0.5)], startPoint: .top, endPoint: .bottom))
                .shadow(radius: 5)
        )
        .padding(.horizontal)
        .padding(.vertical, 10)
    }
}

#Preview {
    QuestionCardView(question: mockQuestions[0])
}
