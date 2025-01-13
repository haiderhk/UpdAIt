//
//  GenerateQuestionsButton.swift
//  UpdAIt
//
//  Created by Haider Khan on 06/01/2025.
//

import SwiftUI

struct GenerateQuestionsButton: View {
    @Binding var isGeneratingQuestions: Bool
    var generateAction: () -> Void
    
    @State private var dotOffset: CGFloat = -10
    @State private var isAnimating: Bool = false 
    
    var body: some View {
        Button {
            withAnimation(.spring(response: 0.3, dampingFraction: 0.6)) {
                isGeneratingQuestions = true
            }
            generateAction()
        } label: {
            HStack {
                if isGeneratingQuestions {
                    HStack(spacing: 4) {
                        ForEach(0..<3) { index in
                            Circle()
                                .fill(Color.white)
                                .frame(width: 6, height: 6)
                                .offset(y: isAnimating ? 0 : dotOffset) // Use animation state
                                .animation(
                                    Animation.easeInOut(duration: 0.5)
                                        .repeatForever()
                                        .delay(0.2 * Double(index)),
                                    value: isAnimating
                                )
                        }
                    }
                    .frame(width: 40)
                    
                    Text("Generating...")
                        .font(.headline)
                        .foregroundColor(.white)
                } else {
                    Image(systemName: "questionmark.circle.fill")
                        .font(.title2)
                        .foregroundColor(.blue)
                    Text("Generate Questions")
                        .font(.headline)
                        .foregroundColor(.blue)
                }
            }
            .padding()
            .frame(width: 300)
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(isGeneratingQuestions
                          ? Color(UIColor.systemGray4)
                          : Color(UIColor.systemGray6))
                    .shadow(color: Color.black.opacity(0.1), radius: 5, x: 0, y: 2)
            )
            .scaleEffect(isGeneratingQuestions ? 0.95 : 1.0)
        }
        .onAppear {
            if isGeneratingQuestions {
                startAnimation()
            }
        }
        .onChange(of: isGeneratingQuestions) { _, newValue in
            if newValue {
                startAnimation()
            } else {
                stopAnimation()
            }
        }
    }
    
    private func startAnimation() {
        isAnimating = true
    }
    
    private func stopAnimation() {
        isAnimating = false
    }
}

#Preview {
    GenerateQuestionsButton(isGeneratingQuestions: .constant(false)) {
        print("ACtion")
    }
}
