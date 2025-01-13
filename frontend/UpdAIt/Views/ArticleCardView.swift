//
//  ArticleCardView.swift
//  UpdAIt
//
//  Created by Haider Khan on 06/01/2025.
//

import Kingfisher
import SwiftUI

struct ArticleCardView: View {
    
    let article: Article
    let index: Int
    @ObservedObject var viewModel: ArticleViewModel
    
    var body: some View {
        VStack {
            KFImage(URL(string: article.articleImageUrl))
                .placeholder {
                    ProgressView()
                }
                .resizable()
                .scaledToFill()
                .frame(width: 330, height: 300)
            
            HStack {
                Text(article.articleTitle)
                    .font(.system(size: 18))
                    .fontWeight(.bold)
                    .lineLimit(3)
                
                Spacer()
            }
            .padding()
            
            Spacer()
            
            GenerateQuestionsButton(isGeneratingQuestions: $viewModel.isGeneratingQuestions) {
                viewModel.fetchQuestions(for: article)
            }
            
            Spacer()
            
            HStack {
                
                Text("\(article.articlePublicationDate)")
                    .font(.system(size: 12))
                    .foregroundStyle(.secondary)
                
                Spacer()
                
                Text(String(format: "%02d / %02d", index, viewModel.articles.count)) // Zero-padded index
                    .font(.system(size: 12))
                    .foregroundColor(.secondary)
            }
            .padding()
            
        }
        .frame(width: 330, height: 550)
        .background(        LinearGradient(
            colors: [.yellow.opacity(0.15), .blue.opacity(0.15), .red.opacity(0.1)],
            startPoint: .top,
            endPoint: .bottom
        ))
        .clipShape(RoundedRectangle(cornerRadius: 16))
        .shadow(color: Color.black.opacity(0.08), radius: 15, y: 2)
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(Color.gray.opacity(0.1), lineWidth: 1)
        )
        .onTapGesture {
            viewModel.visitArticle(articleLink: article.articleLink)
        }
        .disabled(viewModel.isGeneratingQuestions)
    }
}


#Preview {
    ArticleCardView(article: mockData[0], index: 1, viewModel: ArticleViewModel())
}
