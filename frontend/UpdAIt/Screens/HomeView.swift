//
//  HomeView.swift
//  UpdAIt
//
//  Created by Haider Khan on 06/01/2025.
//

import SwiftUI

struct HomeView: View {
    
    @StateObject private var viewModel = ArticleViewModel()
    @State private var question = ""
    @State private var isAnimating = false
    @State private var currentArticleNumber = 0
    @State private var currentArticleDate = 0
    
    @State private var answer: String? = nil
    @State private var metadata: [RAGMetadata] = []
    @State private var showAnswerView = false
    @State private var isRetrieving = false

    
    @State private var isShowingAlert = false
    @State private var isShowingInfo = false
    
    
    @FocusState private var isTextFieldFocused: Bool
    
    var body: some View {
        NavigationStack {
            ZStack {
                LinearGradient(
                    colors: [Color.blue.opacity(0.1), Color.yellow.opacity(0.2), Color.purple.opacity(0.2)],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()
  
                
                VStack {
                    Spacer()
                    HStack {
                        ZStack {
                            // Outer Pulsating Ring
                            Circle()
                                .stroke(LinearGradient(colors: [.purple.opacity(0.5), .blue.opacity(0.5)], startPoint: .top, endPoint: .bottom), lineWidth: 3)
                                .frame(width: 40, height: 40)
                                .scaleEffect(isAnimating ? 1.2 : 1.0)
                                .opacity(isAnimating ? 0.7 : 0.2)
                                .animation(Animation.easeInOut(duration: 1.5).repeatForever(autoreverses: true), value: isAnimating)

                            // Middle Static Ring
                            Circle()
                                .stroke(LinearGradient(colors: [.blue, .purple], startPoint: .leading, endPoint: .trailing), lineWidth: 2)
                                .frame(width: 30, height: 30)

                            // Inner Rotating Circle
                            Circle()
                                .fill(LinearGradient(colors: [.white, .purple], startPoint: .topLeading, endPoint: .bottomTrailing))
                                .frame(width: 18, height: 18)
                                .rotationEffect(.degrees(isAnimating ? 360 : 0))
                                .animation(Animation.linear(duration: 2.0).repeatForever(autoreverses: false), value: isAnimating)
                        }
                        .onAppear {
                            isAnimating = true
                        }
                        TextField("Ask AI", text: $question) // Question for RAG
                            .padding(.horizontal)
                            .padding(.vertical, 5)
//                            .textFieldStyle(.roundedBorder)
//                            .background(
//                                LinearGradient(colors: [Color.blue.opacity(0.1), Color.purple.opacity(0.2)],
//                                               startPoint: .leading,
//                                               endPoint: .trailing)
//                                    .clipShape(RoundedRectangle(cornerRadius: 12))
//                            )
                            .overlay(
                                RoundedRectangle(cornerRadius: 5)
                                    .stroke(
                                        LinearGradient(colors: [Color.purple, Color.blue],
                                                       startPoint: .topLeading,
                                                       endPoint: .bottomTrailing),
                                        lineWidth: 2
                                    )
                            )
                            .padding(.horizontal, 4)
                            .focused($isTextFieldFocused)
                        
                        Button(action: {
                            isTextFieldFocused = false
                            isRetrieving = true
                            fetchAnswer(for: question)
                            
                        }) {
                            Image(systemName: "arrow.up.circle.fill")
                                .font(.title)
                                .foregroundStyle(.blue)
                        }
                    }
                    .padding()
                    .clipShape(RoundedRectangle(cornerRadius: 15.0))
//                    .shadow(radius: 1)
                    
                    ScrollView(.horizontal, showsIndicators: false) {
                        LazyHStack(spacing: 20) {
                            ForEach(Array(viewModel.articles.enumerated()), id: \.offset) { index, article in
                                ArticleCardView(article: article, index: index + 1, viewModel: viewModel)
                                    .containerRelativeFrame(.horizontal, count: 1, spacing: 16)
                                    .scrollTransition { content, phase in
                                        content
                                            .opacity(phase.isIdentity ? 1.0 : 0.0)
                                            .scaleEffect(x: phase.isIdentity ? 1.0 : 0.6, y: phase.isIdentity ? 1.0 : 0.6)
                                            .offset(y: phase.isIdentity ? 0 : 50)
                                    }
                            }
                        }
                        .scrollTargetLayout()
                    }
                    .scrollTargetBehavior(.viewAligned)
                    
                    Spacer()
                    
                }
                
                if isRetrieving {
                    LoadingView()
                        .transition(.opacity)
                }
                
            }
            .navigationTitle("AI News")
            .navigationBarTitleDisplayMode(.inline)

            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        isShowingInfo = true
                    }) {
                        Image(systemName: "info.circle")
                            .font(.title3)
                    }
                }
            }
            .sheet(isPresented: $isShowingInfo, content: {
                InfoPopup()
            })
            .sheet(isPresented: $viewModel.isShowingSafariView) {
                if let url = viewModel.selectedArticleURL {
                    SafariView(url: url)
                }
            }
            .navigationDestination(isPresented: $viewModel.isGeneratedQuestions) {
                GeneratedQuestionsView(questions: viewModel.generatedQuestions)
            }
            .navigationDestination(isPresented: $showAnswerView) {
                AnswerView(question: question, answer: answer ?? "No Answer", metadata: metadata)
            }
            .alert(isPresented: $isShowingAlert) {
                Alert(title: Text("Unable to Generate"), message: Text("Sorry, I couldn't generate an answer for that question, please try another one."), dismissButton: .default(Text("Ok")))
            }
        }
    }

    
    func fetchAnswer(for question: String) {
        guard !question.isEmpty else {
            self.isShowingAlert = true
            self.isRetrieving = false
            return
        }
        
        let url = URL(string: "\(viewModel.baseURL)/query")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        let payload = ["question": question]
        
        request.httpBody = try? JSONSerialization.data(withJSONObject: payload)
        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data, error == nil else {
                print("Error fetching answer: \(error?.localizedDescription ?? "Unknown error")")
                return
            }
            
            do {
                let ragResponse = try JSONDecoder().decode(RAGResponse.self, from: data)
                DispatchQueue.main.async {
                    
                    if ragResponse.answer.contains("I don't know") {
                        self.isShowingAlert = true
                        self.isRetrieving = false
                        self.showAnswerView = false
                    }
                    else {
                        self.answer = ragResponse.answer
                        self.metadata = ragResponse.metadata
                        self.isRetrieving = false
                        self.showAnswerView = true // Navigate to AnswerView
                    }
                }
            } catch {
                print("Failed to decode response: \(error.localizedDescription)")
            }
        }.resume()
    }
}


#Preview {
    HomeView()
}
