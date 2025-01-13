//
//  AnswerView.swift
//  UpdAIt
//
//  Created by Haider Khan on 09/01/2025.
//

import SwiftUI

struct AnswerView: View {
    
    let question: String
    let answer: String
    let metadata: [RAGMetadata]
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Question Section
                VStack(alignment: .leading, spacing: 10) {
                    
                    Text(question)
                        .font(.body)
                        .foregroundColor(.secondary)
                        .padding()
                        .background(
                            RoundedRectangle(cornerRadius: 10)
                                .fill(Color(UIColor.systemGray6))
                        )
                }
                
                // Answer Section
                VStack(alignment: .leading, spacing: 10) {
                    Text(answer)
                        .font(.body)
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                        .padding()
                        .background(
                            RoundedRectangle(cornerRadius: 10)
                                .fill(LinearGradient(colors: [.blue, .purple], startPoint: .leading, endPoint: .trailing))
                        )
                }

                
                Divider()
                
                // Metadata Section
                VStack(alignment: .leading, spacing: 20) {
                    Text("Relevant Articles:")
                        .font(.title2)
                        .bold()
                        .foregroundColor(.primary)
                    
                    ForEach(metadata.reversed(), id: \.article_link) { meta in
                        VStack(alignment: .leading, spacing: 5) {
                            Text(meta.article_title)
                                .font(.headline)
                                .foregroundColor(.primary)
                            
                                    Text("\(meta.chunk_heading)...")
                                        .font(.subheadline)
                                        .foregroundColor(.secondary)
                                    
                                    Text("Relevance Score: \(meta.score, specifier: "%.2f")")
                                        .font(.caption)
                                        .foregroundColor(.blue)
                            
                            Button(action: {
                                if let url = URL(string: meta.article_link) {
                                    UIApplication.shared.open(url)
                                }
                            }) {
                                HStack {
                                    Spacer()
                                    Text("Read Full Article")
                                        .font(.body)
                                        .fontWeight(.semibold)
                                        .foregroundColor(.white)
                                    Spacer()
                                }
                                .frame(height: 20)
                                .padding()
                                .background(
                                    RoundedRectangle(cornerRadius: 10)
                                        .fill(LinearGradient(colors: [Color(UIColor.blue), .blue, Color(UIColor.systemGray2)], startPoint: .leading, endPoint: .trailing))
                                )
                            }
                        }
                        .padding()
                        .background(
                            RoundedRectangle(cornerRadius: 10)
                                .fill(Color(UIColor.systemGray6))
                                .shadow(radius: 2)
                        )
                    }
                }
            }
            .padding()
        }
        .navigationTitle("Answer")
        .navigationBarTitleDisplayMode(.inline)
    }
}
#Preview {
    AnswerView(
        question: "This is the question that you asked I am trying to make a very very long long one so that it is visually chekced",
        answer: "This is the answer to your question with the relevant texte of answer",
        metadata: [
            RAGMetadata(article_link: "https://TheArticleLink",
                        article_title: "Llama Goes Multimodal, Pros Embrance Generative Video, Military AI Guidelines, LLMs That Read Spreadsheets",
                        chunk_heading: "The Chunk Heading", score: 0.999)
        ])
}
