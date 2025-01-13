//
//  InfoPopup.swift
//  UpdAIt
//
//  Created by Haider Khan on 09/01/2025.
//

import SwiftUI

struct InfoPopup: View {
    var body: some View {
        ZStack {
            LinearGradient(
                colors: [Color.blue.opacity(0.1), Color.purple.opacity(0.1), Color.yellow.opacity(0.1)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            VStack(alignment: .leading, spacing: 16) {
                // Header
                VStack(alignment: .center, spacing: 8) {
                    Image(systemName: "sparkles")
                        .font(.system(size: 40))
                        .foregroundStyle(
                            LinearGradient(
                                colors: [.blue, .purple],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )
                    
                    Text("How the App Works")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .multilineTextAlignment(.center)
                        .foregroundColor(.primary)
                }
                .padding(.bottom, 16)
                
                // Explanation Section
                VStack(alignment: .leading, spacing: 12) {
                    InfoRow(
                        icon: "newspaper",
                        title: "Articles",
                        description: "Articles are retrieved from DeepLearning.AI and processed for AI use."
                    )
                    
                    InfoRow(
                        icon: "cube.transparent",
                        title: "Vector Database",
                        description: "Articles are intelligently chunked and stored in a Vector Database (ChromaDB) for efficient AI-based retrieval."
                    )
                    
                    InfoRow(
                        icon: "magnifyingglass",
                        title: "Ask Questions",
                        description: "Ask the AI any question. It retrieves relevant chunks and provides an accurate answer."
                    )
                    
                    InfoRow(
                        icon: "questionmark.circle",
                        title: "Generate Questions",
                        description: "Generate questions for any article to test your knowledge. Reveal answers when needed."
                    )
                }
                
                Spacer()
                
                // Visit Link
                Button(action: {
                    if let url = URL(string: "https://www.deeplearning.ai") {
                        UIApplication.shared.open(url)
                    }
                }) {
                    HStack {
                        Text("Visit DeepLearning.AI")
                            .fontWeight(.medium)
                        Image(systemName: "arrow.right.circle")
                    }
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(
                        LinearGradient(
                            colors: [.purple, .blue],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                        .cornerRadius(12)
                    )
                    .foregroundColor(.white)
                    .shadow(radius: 5)
                }
            }
            .padding()
        }
    }
}

struct InfoRow: View {
    let icon: String
    let title: String
    let description: String
    
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: icon)
                .font(.system(size: 28))
                .foregroundStyle(
                    LinearGradient(
                        colors: [.purple, .blue],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
                .frame(width: 40, height: 40)
                .background(
                    Circle()
                        .fill(Color.blue.opacity(0.2))
                )
            
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.headline)
                    .foregroundColor(.primary)
                Text(description)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 8)
    }
}
#Preview {
    InfoPopup()
}
