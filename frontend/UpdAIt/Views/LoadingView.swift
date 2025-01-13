//
//  LoadingView.swift
//  UpdAIt
//
//  Created by Haider Khan on 09/01/2025.
//

import SwiftUI

struct LoadingView: View {
    @State private var rotation = 0.0
    @State private var scale = 1.0
    
    var body: some View {
        ZStack {
            Color.black.opacity(0.4)
                .ignoresSafeArea()
            
            VStack(spacing: 20) {
                ZStack {
                    Circle()
                        .stroke(LinearGradient(colors: [.blue, .purple], startPoint: .topLeading, endPoint: .bottomTrailing), lineWidth: 8)
                        .frame(width: 80, height: 80)
                        .rotationEffect(.degrees(rotation))
                        .animation(Animation.linear(duration: 1).repeatForever(autoreverses: false), value: rotation)
                    
                    Circle()
                        .fill(LinearGradient(colors: [.purple, .blue], startPoint: .leading, endPoint: .trailing))
                        .frame(width: 20, height: 20)
                        .scaleEffect(scale)
                        .animation(Animation.easeInOut(duration: 0.8).repeatForever(), value: scale)
                }
                .onAppear {
                    rotation = 360
                    scale = 1.5
                }
                
                Text("Thinking...")
                    .font(.headline)
                    .foregroundColor(.white)
            }
        }
    }
}

#Preview {
    LoadingView()
}
