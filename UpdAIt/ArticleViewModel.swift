//
//  viewModel.swift
//  UpdAIt
//
//  Created by Haider Khan on 06/01/2025.
//

import Foundation
import SwiftUI


class ArticleViewModel: ObservableObject {
    
    @Published var articles: [Article] = []
    @Published var isLoading = false
    @Published var error: String?
    @Published var isShowingSafariView = false
    @Published var selectedArticleURL: URL?
    @Published var generatedQuestions: [Question] = []
    @Published var isGeneratingQuestions: Bool = false
    @Published var isGeneratedQuestions: Bool = false
    
    var baseURL = "https://71bb-39-43-151-52.ngrok-free.app"
    private let userDefaults = UserDefaults.standard
    private let cacheKey = "cached_articles"
    private let cacheTimeKey = "articles_cache_time"
    private let cacheValidityDuration: TimeInterval = 3600

    init() {
        loadArticles()
    }
    
    func fetchQuestions(for article: Article) {
        print("generating and fetching questions for the article")
        error = nil
        
        guard let url = URL(string: "\(baseURL)/generate-questions") else {
            self.error = "Invalid URL for Generating Questions"
            isGeneratingQuestions = false
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let payload = ["article_link": article.articleLink]
        
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: payload)
            print("Request sent with the following payload: \(payload)")
        } catch {
            self.error = "Failed to encode generate questions request data"
            isGeneratingQuestions = false
            return
        }
        
        URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
            DispatchQueue.main.async {
                self?.isGeneratingQuestions = false
                
                if let error = error {
                    self?.error = error.localizedDescription
                    return
                }
                
                guard let data = data else {
                    self?.error = "No data received in the generate questions function"
                    return
                }
                
                print("The Data received in URL Session: \(data)")
                do {
                    let response = try JSONDecoder().decode(QuestionsResponse.self, from: data)
                    print("The response has been decoded and is now: \(response)")
                    self?.generatedQuestions = response.questions
                    self?.isGeneratedQuestions = true
                    print("Generated Questions: \(response.questions.count)")
                } catch {
                    self?.error = "Failed to decode generate questions data: \(error.localizedDescription)"
                }
            }
        }.resume()
    }
    
    
    func loadArticles() {
        if let cachedArticles = loadFromCache() {
            self.articles = cachedArticles
            print("Loaded articles from cache: \(cachedArticles.count)")
        }
        
        if !isCacheValid() || articles.isEmpty {
            fetchArticles()
        }
    }
    
    private func fetchArticles() {
        guard !isLoading else { return }
        isLoading = true
        error = nil
        
        guard let url = URL(string: "\(baseURL)/fetch") else {
            self.error = "Invalid URL"
            isLoading = false
            return
        }
        
        print("Fetching Articles from: \(url.absoluteString)")
        
        URLSession.shared.dataTask(with: url) { [weak self] data, response, error in
            DispatchQueue.main.async {
                self?.isLoading = false
                
                if let error = error {
                    self?.error = error.localizedDescription
                    return
                }
                
                guard let data = data else {
                    self?.error = "No data received"
                    return
                }
                
                do {
                    let response = try JSONDecoder().decode(ArticlesResponse.self, from: data)
                    self?.articles = response.articles
                    self?.saveToCache(response.articles)
                    print("Successfully fetched and cached articles: \(response.articles.count)")
                } catch {
                    self?.error = "Failed to decode data: \(error.localizedDescription)"
                }
            }
        }.resume()
    }
    
    private func saveToCache(_ articles: [Article]) {
        do {
            let encoded = try JSONEncoder().encode(articles)
            userDefaults.set(encoded, forKey: cacheKey)
            userDefaults.set(Date().timeIntervalSince1970, forKey: cacheTimeKey)
            print("Articles Cached Successfully")
        } catch {
            print("Failed to cache articles: \(error.localizedDescription)")
        }
    }
    
    private func loadFromCache() -> [Article]? {
        guard let data = userDefaults.data(forKey: cacheKey) else {
            print("No cache data found.")
            return nil
        }
        
        do {
            let articles = try JSONDecoder().decode([Article].self, from: data)
            print("Loaded articles from cache: \(articles.count)")
            return articles
        } catch {
            print("Failed to decode cached data: \(error.localizedDescription)")
            return nil
        }
    }
    
    private func isCacheValid() -> Bool {
        let lastCacheTime = userDefaults.double(forKey: cacheTimeKey)
        let currentTime = Date().timeIntervalSince1970
        let isValid = (currentTime - lastCacheTime) < cacheValidityDuration
        print("Cache Validity: \(isValid)")
        return isValid
    }

    
    func visitArticle(articleLink: String) {
        print("Visiting article...")
        if let url = URL(string: articleLink) {
            selectedArticleURL = url
            isShowingSafariView = true
            
        }
    }
}



